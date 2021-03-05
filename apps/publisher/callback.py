from urllib.parse import urlencode

from dash.dependencies import Input, Output, State
# from requests import get

from app import app
from modules.environment import PD_LOGGING_LEVEL, PD_PUBLISHER_SERVICE
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


@app.callback(
    [
        Output('publisher-table-label-request', 'children'),
        Output('publisher-table-label-response', 'children'),
    ],
    [Input('publisher-table-button-submit', 'n_clicks')],
    [
        State('publisher-table-satellite', 'value'),
        State('publisher-table-sensor', 'value'),
        State('publisher-table-date-picker-range', 'start_date'),
        State('publisher-table-date-picker-range', 'end_date'),
        State('publisher-table-path', 'value'),
        State('publisher-table-row', 'value'),
        State('publisher-table-geo_processing', 'value'),
        State('publisher-table-radio_processing', 'value'),
        State('publisher-table-action', 'value')
    ])
def publisher__button_was_clicked(n_clicks, satellite, sensor, start_date, end_date,
                                  path, row, geo_processing, radio_processing, action):

    if n_clicks == 0:
        return '', ''

    logger.info('publisher__button_was_clicked()')
    logger.info(f'publisher__button_was_clicked - satellite: {satellite}')
    logger.info(f'publisher__button_was_clicked - sensor: {sensor}')
    logger.info(f'publisher__button_was_clicked - start_date: {start_date}')
    logger.info(f'publisher__button_was_clicked - end_date: {end_date}')
    logger.info(f'publisher__button_was_clicked - path: {path}')
    logger.info(f'publisher__button_was_clicked - row: {row}')
    logger.info(f'publisher__button_was_clicked - geo_processing: {geo_processing}')
    logger.info(f'publisher__button_was_clicked - radio_processing: {radio_processing}')
    logger.info(f'publisher__button_was_clicked - action: {action}')

    query = {
        'satellite': satellite,
        'start_date': start_date,
        'end_date': end_date,
        'path': path,
        'row': row
    }

    if sensor != 'ALL':
        query['sensor'] = sensor

    if geo_processing != 'ALL':
        query['geo_processing'] = geo_processing

    if radio_processing != 'ALL':
        query['radio_processing'] = radio_processing

    url = PD_PUBLISHER_SERVICE
    if action == '/publish':
        url += '/publish'

    logger.info(f'publisher__button_was_clicked - url: {url}')
    logger.info(f'publisher__button_was_clicked - query: {query}')

    # result = get(url, params=query)

    # logger.info(f'publisher__button_was_clicked - result: {result}')
    # logger.info(f'publisher__button_was_clicked - result.text: {result.text}')

    # construct query string and add it to the url
    url += '?' + urlencode(query)

    return url, f'n_clicks: {n_clicks}'

