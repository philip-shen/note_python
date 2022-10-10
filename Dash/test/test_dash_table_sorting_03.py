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
df.insert(0, '#', df.index)

app = dash.Dash(__name__)

app.layout = dbc.Container(
    [
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[
                {'name': column, 'id': column}
                for column in df.columns
            ],
            # 自定义条件筛选单元格样式
            style_filter={
                'font-family': 'Times New Roman',
                'background-color': '#e3f2fd'
            },
            style_table={
                'height': '500px',
                'overflow-y': 'auto'
            },
            style_header={
                'font-family': 'Times New Roman',
                'font-weight': 'bold',
                'text-align': 'center'
            },
            style_data={
                'font-family': 'Times New Roman',
                'text-align': 'center'
            },
            fixed_rows={
                'headers': True
            },
            filter_action="native"
        )
    ],
    
    style={
        'margin-top': '50px'
    }
)


if __name__ == '__main__':
    app.run_server(port=8000, debug=True)