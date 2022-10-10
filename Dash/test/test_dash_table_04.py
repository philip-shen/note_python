'''
https://www.cnblogs.com/feffery/p/14616652.html
'''
import dash
#import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table

import seaborn as sns

app = dash.Dash(__name__)

# 载入演示数据集
df = sns.load_dataset('iris')
# 创建行下标列
df.insert(loc=0, column='#', value=df.index)

app.layout = html.Div(
    dbc.Container(
        [
            dash_table.DataTable(
                columns=[{'name': column, 'id': column} for column in df.columns],
                data=df.to_dict('records'),
                virtualization=True,
                style_as_list_view=False,#True
                style_table={
                    'height': '500px'
                },
                style_cell={
                    'font-family': 'Times New Roman',
                    'text-align': 'center'
                },
                style_header_conditional=[
                    {
                        'if': {
                            # 选定列id为#的列
                            'column_id': '#'
                        },
                        'font-weight': 'bold',
                        'font-size': '24px'
                    }
                ],
                style_data_conditional=[
                    {
                        'if': {
                            # 选中行下标为奇数的行
                            'row_index': 'odd'
                        },
                        'background-color': '#cfd8dc'
                    }
                ]
            )
        ],
        style={
            'margin-top': '100px'
        }
    )
)

if __name__ == '__main__':
    app.run_server(port=8000, debug=True)