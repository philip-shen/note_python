'''
https://www.cnblogs.com/feffery/p/14674642.html
'''
import dash
#import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
from dash.dependencies import Input, Output


import seaborn as sns

df = sns.load_dataset('iris')

app = dash.Dash(__name__)

app.layout = dbc.Container(
    [
        dash_table.DataTable(
            data=df.to_dict('records'),
            virtualization=True,
            style_as_list_view=False,#True
                
            columns=[
                {'name': column, 'id': column}
                for column in df.columns
            ],
            style_table={
                'height': '500px',
                'overflow-y': 'auto'
            },
            sort_action='native'
        )
    ],
    style={
        'margin-top': '50px'
    }
)

if __name__ == '__main__':
    app.run_server(port=8000, debug=True)