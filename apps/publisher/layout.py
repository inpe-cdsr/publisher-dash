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


satellites = [
    {
        'satellite': 'AMAZONIA1',
        'sensors': ['WFI']
    },
    {
        'satellite': 'CBERS4A',
        'sensors': ['MUX', 'WFI', 'WPM']
    },
    {
        'satellite': 'CBERS4',
        'sensors': ['MUX', 'AWFI', 'PAN5M', 'PAN10M']
    },
    {
        'satellite': 'CBERS2B',
        'sensors': ['CCD', 'WFI', 'HRC']
    },
    {
        'satellite': 'LANDSAT1',
        'sensors': ['MSS']
    },
    {
        'satellite': 'LANDSAT2',
        'sensors': ['MSS']
    },
    {
        'satellite': 'LANDSAT3',
        'sensors': ['MSS']
    },
    {
        'satellite': 'LANDSAT5',
        'sensors': ['TM']
    },
    {
        'satellite': 'LANDSAT7',
        'sensors': ['ETM']
    }
]


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
        ''
    ],
    'Value' : [
        dcc.Dropdown(
            id='publisher-table-satellite',
            options=[
                {'label': s['satellite'], 'value': s['satellite']} \
                    for s in satellites
            ],
            value='CBERS4A',
            clearable=False
        ),
        dcc.Dropdown(
            id='publisher-table-sensor',
            # options=[],  # this key is updated by callback
            value='ALL',
            clearable=False
        ),
        dcc.DatePickerRange(
            id='publisher-table-date-picker-range',
            min_date_allowed=date(2020, 6, 1),
            max_date_allowed=date(2020, 6, 30),
            initial_visible_month=date(2020, 6, 1),
            start_date=date(2020, 6, 5),
            end_date=date(2020, 6, 14),
            display_format='DD/MM/YYYY'
        ),
        dcc.Input(id='publisher-table-path', placeholder='Path', type='number', value=1, min=1, max=999),
        dcc.Input(id='publisher-table-row', placeholder='Row', type='number', value=1, min=1, max=999),
        dcc.RadioItems(
            id='publisher-table-geo_processing',
            options=[
                {'label': 'All', 'value': 'ALL'},
                {'label': '2', 'value': '2'},
                {'label': '4', 'value': '4'}
            ],
            value='ALL',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.RadioItems(
            id='publisher-table-radio_processing',
            options=[
                {'label': 'All', 'value': 'ALL'},
                {'label': 'DN', 'value': 'DN'},
                {'label': 'SR', 'value': 'SR'},
            ],
            value='ALL',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='publisher-table-action',
            options=[
                {'label': '/publish', 'value': '/publish'},
            ],
            value='/publish',
            clearable=False
        ),
        html.Button('Submit', id='publisher-table-button-submit', n_clicks=0)
    ]
}


def generate_table(df, max_rows=26):
    return html.Table(
        [
            # Header
            # html.Thead([ html.Tr([html.Th(col) for col in df.columns]) ]),
            # Body
            html.Tbody([
                html.Tr([
                    html.Td(df.iloc[i][col]) for col in df.columns
                ]) for i in range(min(len(df), max_rows))
            ])
        ],
        style={'color': colors['text']}
    )


layout = html.Div([
    # title
    html.H1(children='publisher-dash', style={'textAlign': 'center', 'color': colors['text']}),
    # subtitle
    html.H3(children='Operation analysis', style={'textAlign': 'center', 'color': colors['text']}),
    # tables
    html.Div([
        html.Div([
            # form
            html.Div([
                html.P(children='Form', style={'textAlign': 'center', 'color': colors['text']}),
                generate_table(DataFrame(data_table)),
            ], style={'paddingBottom': '20px'}),
            # table request
            html.Div([
                html.P(children='Result', style={'textAlign': 'center', 'color': colors['text']}),
                html.Table(
                    html.Tbody([
                        html.Tr([
                            html.Td('Request'), html.Td(id='publisher-table-label-request')
                        ]),
                        html.Tr([
                            html.Td('Response'), html.Td(id='publisher-table-label-response')
                        ])
                    ]),
                    style={'width': '100%', 'color': colors['text']}
                )
            ])
        ], style={'maxWidth': '450px', 'paddingRight': '50px'}),
        html.Div([
            # title
            html.P(children='Information', style={'textAlign': 'center', 'color': colors['text']}),
            # table information
            DataTable(
                id='publisher--table--information',
                columns=[{"name": i, "id": i} for i in df_information.columns],
                data=df_information.to_dict('records'),
                fixed_rows={'headers': True, 'data': 0},
                **get_table_styles()
            )
        ], style={'maxWidth': '400px'}),
    ], style={'width': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
])
