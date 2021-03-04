from dash_core_components import Link
from dash_html_components import Br, Div, H1, H3

from app import url_base_pathname
from modules.utils import colors


layout = Div([
    # title
    H1(
        children='publisher-dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    # subtitle
    H3(
        children='Index',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    # Link('Scene', href=f'{url_base_pathname}/scene'),
    Br(),
    Link('Publisher', href=f'{url_base_pathname}/publisher')
])
