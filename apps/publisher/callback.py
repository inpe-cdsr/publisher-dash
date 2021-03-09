from urllib.parse import urlencode

from dash.dependencies import Input, Output, State
import dash_html_components as html
from requests import get

from app import app
from modules.environment import PD_LOGGING_LEVEL, PD_PUBLISHER_SERVICE
from modules.logger import create_logger
from modules.model import CDSRCatalogConnection, CDSROperationConnection

from apps.publisher.layout import layout, satellites


# create logger object
logger = create_logger(__name__, level=PD_LOGGING_LEVEL)

# database connection
db_catalog = CDSRCatalogConnection()
db_operation = CDSROperationConnection()


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
    [Output('publisher-table-label-request', 'children'),
     Output('publisher-table-label-response', 'children')],
    [Input('publisher-table-button-submit', 'n_clicks')],
    [State('publisher-table-satellite', 'value'),
     State('publisher-table-sensor', 'value'),
     State('publisher-table-date-picker-range', 'start_date'),
     State('publisher-table-date-picker-range', 'end_date'),
     State('publisher-table-path', 'value'),
     State('publisher-table-row', 'value'),
     State('publisher-table-geo_processing', 'value'),
     State('publisher-table-radio_processing', 'value'),
     State('publisher-table-action', 'value')]
)
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
        'end_date': end_date
    }

    if sensor != 'ALL':
        query['sensor'] = sensor

    if geo_processing != 'ALL':
        query['geo_processing'] = geo_processing

    if radio_processing != 'ALL':
        query['radio_processing'] = radio_processing

    if path != '':
        query['path'] = path

    if row != '':
        query['row'] = row

    url = PD_PUBLISHER_SERVICE
    if action == '/publish':
        url += '/publish'

    logger.info(f'publisher__button_was_clicked - url: {url}')
    logger.info(f'publisher__button_was_clicked - query: {query}')

    # it calls publisher service
    result = get(url, params=query)

    request_label = url + '?' + urlencode(query)
    response_label = [
        html.Label(f'status_code: {result.status_code}'),
        html.Label(f'text: {result.text}')
    ]

    logger.info(f'publisher__button_was_clicked - request_label: {request_label}')
    logger.info(f'publisher__button_was_clicked - response_label: {response_label}')

    return request_label, response_label


@app.callback(
    [Output('publisher-table-information', 'data'),
    Output('publisher-table-items', 'data'),
    Output('publisher-table-task-error', 'data')],
    [Input('publisher-interval-update-tables', 'n_intervals')]
)
def publisher__update_tables(n_intervals):
    # get information from the databases
    items = db_catalog.select_from_items()
    task_errors = db_operation.select_from_task_error()

    table_information = [
        {'information': 'Number of items', 'value': len(items.index)},
        {'information': 'Number of task errors', 'value': len(task_errors.index)}
    ]

    return table_information, items.to_dict('records'), task_errors.to_dict('records')
