from dash.dependencies import Input, Output

from app import app
from modules.environment import PD_LOGGING_LEVEL
from modules.logger import create_logger

from apps.publisher.layout import *


# create logger object
# logger = create_logger(__name__, level=PD_LOGGING_LEVEL)


# @app.callback(
#     Output('table--information', 'data'),
#     [Input('publisher--date-picker-range', 'start_date'),
#     Input('publisher--date-picker-range', 'end_date')])
# def publisher_callback(start_date, end_date):
#     logger.info('publisher_callback()')

#     return None
