from dash.dependencies import Input, Output

from app import app
from modules.environment import PD_LOGGING_LEVEL
from modules.logger import create_logger

from apps.publisher.layout import layout, satellites


# create logger object
logger = create_logger(__name__, level=PD_LOGGING_LEVEL)


@app.callback(
    Output('publisher-table-sensor', 'options'),
    [Input('publisher-table-satellite', 'value')]
)
def publisher__update_sensor_dropdown(satellite):
    logger.info('publisher__update_sensor_dropdown()')
    logger.info(f'publisher__update_sensor_dropdown - satellite: {satellite}')

    satellite_info = list(filter(lambda s: s['satellite'] == satellite, satellites))

    if not satellite_info:
        return []

    satellite_info = satellite_info[0]
    logger.info(f'publisher__update_sensor_dropdown - satellite_info: {satellite_info}')

    return [{'label': 'All', 'value': 'ALL'}] + \
        [{'label': s, 'value': s} for s in satellite_info['sensors']]
