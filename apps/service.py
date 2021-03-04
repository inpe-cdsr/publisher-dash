# from pandas import set_option


# display a larger dataframe on the console
# set_option('display.max_rows', 500)
# set_option('display.max_columns', 500)
# set_option('display.width', 1000)


##################################################
# layout services
##################################################

def get_table_styles():
    return {
        'style_as_list_view': True,
        'style_table': {
            'maxHeight': '390px',
            'overflowY': 'scroll'
        },
        'style_data_conditional': [
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'gray'
            }
        ],
        'style_filter': {
            'backgroundColor': 'white'
        },
        'style_header': {
            'backgroundColor': 'black',
            'fontWeight': 'bold'
        },
        'style_cell': {
            'textAlign': 'left',
            'minWidth': '100px',
            'backgroundColor': '#404040',
            'color': 'white'
        }
    }

##################################################
# callback services
##################################################
