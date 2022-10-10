'''
https://www.cnblogs.com/feffery/p/14641943.html
'''
import dash
#import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table

import seaborn as sns

df = sns.load_dataset('tips')
df.insert(0, '#', df.index)

app = dash.Dash(__name__)

app.layout = dbc.Container(
    [
        dash_table.DataTable(
            id='dash-table',
            data=df.to_dict('records'),
            virtualization=True,
            style_as_list_view=False,#True
                
            columns=[
                {'name': column, 'id': column}
                for column in df.columns
            ],
            page_size=15,  # 设置单页显示15行记录行数
            style_header={
                'font-family': 'Times New Roman',
                'font-weight': 'bold',
                'text-align': 'center'
            },
            style_data={
                'font-family': 'Times New Roman',
                'text-align': 'center'
            }
        )
    ],
    style={
        'margin-top': '50px'
    }
)

if __name__ == '__main__':
    app.run_server(port=8000, debug=True)