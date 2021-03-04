#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dash_core_components import Location
from dash.dependencies import Input, Output
from dash_html_components import Div

from app import app, url_base_pathname
import apps
from modules.environment import PD_DEBUG_MODE, PD_LOGGING_LEVEL
from modules.logger import create_logger


# create logger object
logger = create_logger(__name__, level=PD_LOGGING_LEVEL)


app.layout = Div([
    Location(id='url', refresh=False),
    Div(id='page-content')
])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == f'{url_base_pathname}/':
        return apps.layout_index
    if pathname == f'{url_base_pathname}/publisher':
        return apps.layout_publisher
    else:
        return apps.layout_error_404


if __name__ == '__main__':
    logger.info(f'main.py - PD_DEBUG_MODE: {PD_DEBUG_MODE}')
    app.run_server(debug=PD_DEBUG_MODE, host='0.0.0.0', port=8050)
