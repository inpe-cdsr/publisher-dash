from datetime import date, timedelta

import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable
from pandas import DataFrame

# from apps.publisher.service import default_csc
from apps.service import get_table_styles
from modules.environment import PD_LOGGING_LEVEL
from modules.logger import create_logger
from modules.utils import colors


# create logger object
logger = create_logger(__name__, level=PD_LOGGING_LEVEL)

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
        # satellite
        dcc.Dropdown(
            id='publisher-table-satellite',
            options=[
                {'label': s['satellite'], 'value': s['satellite']} \
                    for s in satellites
            ],
            value='CBERS4A',
            clearable=False
        ),
        # sensor
        dcc.Dropdown(
            id='publisher-table-sensor',
            # options=[],  # this key is updated by callback
            value='ALL',
            clearable=False
        ),
        # date range
        dcc.DatePickerRange(
            id='publisher-table-date-picker-range',
            min_date_allowed=date(1975, 1, 1),
            max_date_allowed=date.today() + timedelta(days=1),
            initial_visible_month=date.today(),
            start_date=date.today() - timedelta(weeks=4),
            end_date=date.today(),
            display_format='DD/MM/YYYY'
        ),
        # path/row
        dcc.Input(id='publisher-table-path', placeholder='Path', type='number', value='', min=1, max=999),
        dcc.Input(id='publisher-table-row', placeholder='Row', type='number', value='', min=1, max=999),
        # geo processing
        dcc.RadioItems(
            id='publisher-table-geo_processing',
            options=[
                {'label': 'All', 'value': 'ALL'},
                {'label': '2', 'value': '2'},
                {'label': '2B', 'value': '2B'},
                {'label': '3', 'value': '3'},
                {'label': '4', 'value': '4'}
            ],
            value='ALL',
            labelStyle={'display': 'inline-block'}
        ),
        # radio processing
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
        # action
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
    # html.H3(children='Operation analysis', style={'textAlign': 'center', 'color': colors['text']}),
    # tables
    html.Div([
        # left tables
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
        # right tables
        html.Div([
            # title
            html.P(children='Information', style={'textAlign': 'center', 'color': colors['text']}),
            # table information
            DataTable(
                id='publisher-table-information',
                columns=[{"name": i, "id": i} for i in ['information', 'value']],
                data=[],
                fixed_rows={'headers': True, 'data': 0},
                **get_table_styles()
            ),
            # title
            html.P(children='Items', style={'textAlign': 'center', 'color': colors['text'], 'paddingTop': '10px'}),
            # table items
            DataTable(
                id='publisher-table-items',
                columns=[{"name": i, "id": i} for i in (
                    'name', 'collection_id', 'start_date', 'end_date', 'metadata', 'assets'
                )],
                data=[],
                fixed_rows={ 'headers': True, 'data': 0 },
                **get_table_styles(),
                sort_action='native',
                sort_mode='multi',
                filter_action='native',
                page_size=10,
            ),
            # title
            html.P(children='Task error', style={'textAlign': 'center', 'color': colors['text'], 'paddingTop': '30px'}),
            # table task error
            DataTable(
                id='publisher-table-task-error',
                columns=[{"name": i, "id": i} for i in ('id', 'message', 'metadata')],
                data=[],
                fixed_rows={ 'headers': True, 'data': 0 },
                **get_table_styles(),
                sort_action='native',
                sort_mode='multi',
                filter_action='native',
                page_size=10,
            ),
            dcc.Interval(
                id='publisher-interval-update-tables',
                interval=3000, # each 3 secs the table is updated
                n_intervals=0
            )
        ], style={'maxWidth': '350px'}),
    ], style={'width': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
])
