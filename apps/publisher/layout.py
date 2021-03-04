from dash_core_components import Input as dcc_Input
from dash_html_components import Div, H1, H3, P
from dash_table import DataTable
from pandas import DataFrame

# from apps.publisher.service import default_csc
from apps.service import get_table_styles
from modules.environment import PD_LOGGING_LEVEL
from modules.logger import create_logger
from modules.model import CDSRCatalogConnection, CDSROperationConnection
from modules.utils import colors


# create logger object
logger = create_logger(__name__, level=PD_LOGGING_LEVEL)


##################################################
# get the dataframes from database
##################################################
# database connection
db_catalog = CDSRCatalogConnection()
db_operation = CDSROperationConnection()


count_items = db_catalog.select_count_all_from_items()
count_task_error = db_operation.select_count_all_from_task_error()

logger.info(f'publisher.layout - count_items.head(): \n{count_items.head()}\n')
logger.info(f'publisher.layout - count_task_error.head(): \n{count_task_error.head()}\n')


information_data = [
    ['Number of items', count_items['count']],
    ['Number of task errors', count_task_error['count']]
]
df_information = DataFrame(information_data, columns=['information', 'value'])


layout = Div([
    # title
    H1(
        children='publisher-dash',
        style={'textAlign': 'center', 'color': colors['text']}
    ),
    # subtitle
    H3(
        children='Operation analysis',
        style={'textAlign': 'center', 'color': colors['text']}
    ),

    # information table
    Div([
        # table information, date picker range and limit
        Div([
            # table information
            Div([
                # title
                P(
                    children='Table: Information',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                # table information
                DataTable(
                    id='publisher--table--information',
                    columns=[{"name": i, "id": i} for i in df_information.columns],
                    data=df_information.to_dict('records'),
                    fixed_rows={'headers': True, 'data': 0},
                    **get_table_styles()
                ),
            ], style={'max-width': '500px'}),
            # limit
            Div([
                # limit
                P(
                    children='Limit (max. 1000):',
                    style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        'margin-top': '20px'
                    }
                ),
                # date picker range
                dcc_Input(
                    id="publisher--input--limit",
                    type="number",
                    placeholder="Limit (max. 1000)",
                    value=100,
                    min=1,
                    max=1000
                )
            ], style={'padding': '10px'}),
        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    ], style={'padding': '10px'})
])
