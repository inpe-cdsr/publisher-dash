from datetime import date

import dash_core_components as dcc
import dash_html_components as html
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


data_table = {
    'Key' : [
        'Satellite',
        'Sensor',
        'Date',
        'Path',
        'Row',
        'Geo. Processing',
        'Radio. Processing',
        'Action',
        '',
    ],
    'Value' : [
        dcc.Dropdown(
            id='satellite',
            options=[
                {'label': 'AMAZONIA1', 'value': 'AMAZONIA1'},
                {'label': 'CBERS2B', 'value': 'CBERS2B'},
                {'label': 'CBERS4', 'value': 'CBERS4'},
                {'label': 'CBERS4A', 'value': 'CBERS4A'},
                {'label': 'LANDSAT1', 'value': 'LANDSAT1'},
                {'label': 'LANDSAT2', 'value': 'LANDSAT2'},
                {'label': 'LANDSAT3', 'value': 'LANDSAT3'},
                {'label': 'LANDSAT5', 'value': 'LANDSAT5'},
                {'label': 'LANDSAT7', 'value': 'LANDSAT7'},
            ],
            value='CBERS2B',
            clearable=False
        ),
        dcc.Dropdown(
            id='sensor',
            options=[
                {'label': 'All', 'value': 'All'},
                {'label': 'WFI', 'value': 'WFI'},
                {'label': 'MUX', 'value': 'MUX'}
            ],
            value='All',
            clearable=False
        ),
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=date(2020, 6, 1),
            max_date_allowed=date(2020, 6, 30),
            initial_visible_month=date(2020, 6, 1),
            start_date=date(2020, 6, 5),
            end_date=date(2020, 6, 14)
        ),
        dcc.Input(id='path', placeholder='Path', type='number', value=1, min=1, max=999),
        dcc.Input(id='row', placeholder='Row', type='number', value=1, min=1, max=999),
        dcc.RadioItems(
            id='geo_processing',
            options=[
                {'label': 'All', 'value': 'ALL'},
                {'label': '2', 'value': '2'},
                {'label': '4', 'value': '4'}
            ],
            value='ALL',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.RadioItems(
            id='radio_processing',
            options=[
                {'label': 'All', 'value': 'ALL'},
                {'label': 'DN', 'value': 'DN'},
                {'label': 'SR', 'value': 'SR'},
            ],
            value='ALL',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='action',
            options=[
                {'label': '/publish', 'value': 'publish'},
            ],
            value='publish',
            clearable=False
        ),
        html.Button('Submit', id='submit_button')
    ]
}


def generate_table(df, max_rows=26):
    return html.Table(
        # Header
        # [ Tr([Th(col) for col in df.columns]) ] +
        # Body
        [
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))
        ],
        style={'color': colors['text']}
    )


layout = html.Div([
    # title
    html.H1(
        children='publisher-dash',
        style={'textAlign': 'center', 'color': colors['text']}
    ),
    # subtitle
    html.H3(
        children='Operation analysis',
        style={'textAlign': 'center', 'color': colors['text']}
    ),

    html.Div([
        html.Div([
            generate_table(DataFrame(data_table)),
        ], style={'padding-right': '50px'}),
        html.Div([
            # title
            html.P(
                children='Table: Information',
                style={'textAlign': 'center', 'color': colors['text']}
            ),
            # table information
            DataTable(
                id='publisher--table--information',
                columns=[{"name": i, "id": i} for i in df_information.columns],
                data=df_information.to_dict('records'),
                fixed_rows={'headers': True, 'data': 0},
                **get_table_styles()
            )
        ]),
    ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
])
