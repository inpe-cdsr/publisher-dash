from functools import wraps
from time import sleep

from pandas import read_sql
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.pool import NullPool

from modules.environment import PD_LOGGING_LEVEL, PGUSER, PGPASSWORD, \
                                PGHOST, PGPORT, PGDATABASE
from modules.logger import create_logger


# create logger object
logger = create_logger(__name__, level=PD_LOGGING_LEVEL)


class PostgreSQLConnection:

    def _init_attributes(self):
        self.PGUSER = PGUSER
        self.PGPASSWORD = PGPASSWORD
        self.PGHOST = PGHOST
        self.PGPORT = PGPORT
        self.PGDATABASE = PGDATABASE

    def _create_engine(self):
        engine_connection = (f'postgresql+psycopg2://{self.PGUSER}:{self.PGPASSWORD}'
                             f'@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}')

        # logger.info(f'PostgreSQLConnection._create_engine() - engine_connection: {engine_connection}')

        try:
            # `NullPool prevents the Engine from using any connection more than once`
            self.engine = create_engine(engine_connection, poolclass=NullPool)

        except SQLAlchemyError as error:
            logger.error('PostgreSQLConnection._create_engine() - An error occurred during engine creation.')
            logger.error(f'PostgreSQLConnection._create_engine() - error.code: {error.code} - error.args: {error.args}')
            logger.error(f'PostgreSQLConnection._create_engine() - error: {error}\n')

            raise SQLAlchemyError(error)

    def __handle_db_exceptions(func):
        '''This decorator handles multiple database exceptions.'''

        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 1

            while True:
                try:
                    return func(*args, **kwargs)
                except OperationalError:
                    logger.warning('PostgreSQLConnection - Could not connect to database, trying to '
                                  f'connect again... [attempts: `{attempts}`]')
                    attempts += 1
                    sleep(2)
                except SQLAlchemyError as error:
                    logger.error(f'PostgreSQLConnection - An error occurred during query execution.')
                    logger.error(f'PostgreSQLConnection - error.code: {error.code} - error.args: {error.args}')
                    logger.error(f'PostgreSQLConnection - error: {error}\n')

                    raise SQLAlchemyError(error)

        return wrapper

    @__handle_db_exceptions
    def execute(self, query: str, params: dict=None, is_transaction: bool=False):
        # logger.debug('PostgreSQLConnection.execute()')
        # logger.debug(f'PostgreSQLConnection.execute() - is_transaction: {is_transaction}')
        # logger.debug(f'PostgreSQLConnection.execute() - query: {query}')
        # logger.debug(f'PostgreSQLConnection.execute() - params: {params}')

        # SELECT (return dataframe)
        if not is_transaction:
            return read_sql(query, con=self.engine)

        # SELECT (return ResultProxy)
        # with self.engine.connect() as connection:
        #     # convert rows from ResultProxy to list and return the object
        #     return list(connection.execute(query))

        # INSERT, UPDATE and DELETE
        with self.engine.begin() as connection:  # runs a transaction
            connection.execute(query, params)


class CDSRCatalogConnection(PostgreSQLConnection):
    '''Main database.'''

    def __init__(self):
        self._init_attributes()
        self._create_engine()

    def select_from_collections(self):
        return self.execute('SELECT * FROM bdc.collections ORDER BY name;')

    def select_count_all_from_collections(self):
        return self.execute('SELECT COUNT(*) FROM bdc.collections;')

    def select_from_items(self):
        result = self.execute('SELECT name, collection_id, start_date::timestamp, '
                              'end_date::timestamp, assets, metadata, geom, min_convex_hull '
                              'FROM bdc.items ORDER BY name;')

        result['assets'] = result['assets'].astype('str')
        result['metadata'] = result['metadata'].astype('str')

        return result

    def select_count_all_from_items(self):
        return self.execute('SELECT COUNT(*) FROM bdc.items;')


class CDSROperationConnection(PostgreSQLConnection):
    '''Operation database.'''

    def __init__(self):
        self._init_attributes()
        self.PGDATABASE = 'cdsr_publisher'  # set the correct database
        self._create_engine()

    def select_from_task_error(self):
        return self.execute('SELECT * FROM task_error ORDER BY message;')

    def select_count_all_from_task_error(self):
        return self.execute('SELECT COUNT(*) FROM task_error;')
