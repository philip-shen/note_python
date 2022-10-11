'''
https://www.cnblogs.com/feffery/p/14641943.html
'''
import dash
#import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
from dash.dependencies import Input, Output

import sys
from pymongo import MongoClient
import pandas as pd
import json

from logger_setup import *
import lib_mongo_atlas

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
opt_verbose='ON'

json_file= 'secret.json'
    
with open(json_file, encoding="utf-8") as f:
    json_data = json.load(f)  

db, collection= lib_mongo_atlas.mongodb_conn(json_data, opt_verbose)

dict_filter = {"jobContent": {"$regex": "(audio|Audio|image|Image|5G|O-RAN|QA)"}}
list_targets, dict_targets= lib_mongo_atlas.mongodb_search(db, collection, dict_filter, opt_verbose)

df= pd.DataFrame(list_targets, columns = ['jobLocation', 'jobTitles', 'jobCompanyName','jobContent'])    
df.insert(0, '#', df.index)

app = dash.Dash(__name__)

app.layout = dbc.Container(
    [
        dbc.Spinner(
            dash_table.DataTable(
                virtualization=True,
                style_as_list_view=False,#True
                
                id='dash-table',
                columns=[
                    {'name': column, 'id': column}
                    for column in df.columns
                ],
                page_size=15,  # 设置单页显示15行记录行数
                page_action='custom',
                page_current=0,
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
        )
    ],
    style={
        'margin-top': '50px'
    }
)


@app.callback(
    [Output('dash-table', 'data'),
     Output('dash-table', 'page_count')],
    [Input('dash-table', 'page_current'),
     Input('dash-table', 'page_size')]
)
def refresh_page_data(page_current, page_size):
    return df.iloc[page_current * page_size:(page_current + 1) * page_size].to_dict('records'), 1 + df.shape[
        0] // page_size


if __name__ == '__main__':
    app.run_server(port=8000, debug=True)