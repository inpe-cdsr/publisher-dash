from os import getenv

from modules.logger import AVAILABLE_LEVELS, INFO


def str2bool(value):
    '''Convert string to boolean.'''
    # Source: https://stackoverflow.com/a/715468
    return str(value).lower() in ('true', 't', '1', 'yes', 'y')


# Publisher Dash environment variables
PD_DEBUG_MODE = str2bool(getenv('PD_DEBUG_MODE', 'False'))
PD_LOGGING_LEVEL = getenv('PD_LOGGING_LEVEL', 'INFO')
PD_PUBLISHER_SERVICE = getenv('PD_PUBLISHER_HOST', 'http://inpe_cdsr_publisher:5000')


# if the inserted logger level already exists, then select it,
if PD_LOGGING_LEVEL in AVAILABLE_LEVELS:
    PD_LOGGING_LEVEL = AVAILABLE_LEVELS[PD_LOGGING_LEVEL]
else:
    # else, insert a default logger level
    PD_LOGGING_LEVEL = INFO


# PostgreSQL connection
PGUSER = getenv('PGUSER', 'postgres')
PGPASSWORD = getenv('PGPASSWORD', 'postgres')
PGHOST = getenv('PGHOST', 'inpe_cdsr_postgis')
PGPORT = int(getenv('PGPORT', 5432))
PGDATABASE = getenv('PGDATABASE', 'cdsr_catalog_test')
