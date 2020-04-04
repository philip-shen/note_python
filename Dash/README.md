# Purpose  
Take note of Dash  

# Table of Contents  
[Plotly](#plotly)  
[Cufflinks](#cufflinks)  

[plotnine, altair, seaborn, pixiedust](#plotnine-altair-seaborn-pixiedust)  

[Data Visualization-Dash Tutorial](#data-visualization-dash-tutorial)  

[Data Visualization-Dash Python Libray](#data-visualization-dash-python-libray)  

[Data Visualization- Dash](#data-visualization-dash)  
[Html Elements](#html-elements)  
[Graphs](#graphs)  
[Table](#table)  
[Callback](#callback)  
[UIパーツをが必要不可欠]()  
[Outputは1つだけの法則]()  
[ButtonのCallback]()  

[]()  

# Plotly  
[[Python] Plotlyでぐりぐり動かせるグラフを作る Mar 16, 2019](https://qiita.com/inoory/items/12028af62018bf367722)  

## Cufflinks  
[[Python] CufflinksでPandasのデータフレームをPlotlyに一発描画 Mar 23, 2019](https://qiita.com/inoory/items/7c8ca9fd5e1aca3e2e72)  
[santosjorge /cufflinks](https://github.com/santosjorge/cufflinks) 
```
This library binds the power of plotly with the flexibility of pandas for easy plotting.

This library is available on https://github.com/santosjorge/cufflinks

This tutorial assumes that the plotly user credentials have already been 
configured as stated on the getting started guide.
```

# plotnine, altair, seaborn, pixiedust  
[Python でデータ分析するのに適したグラフツール3選 Jan 22, 2019](https://qiita.com/s_katagiri/items/26763fd39f3dd9756809)  

## plotnine  
[plotnine](https://qiita.com/s_katagiri/items/26763fd39f3dd9756809#plotnine)  

## altair  
[altair](https://qiita.com/s_katagiri/items/26763fd39f3dd9756809#altair)  

## seaborn  
[seaborn](https://qiita.com/s_katagiri/items/26763fd39f3dd9756809#seaborn)  

## pixiedust  
[補足: pixiedust について](https://qiita.com/s_katagiri/items/26763fd39f3dd9756809#%E8%A3%9C%E8%B6%B3-pixiedust-%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)  


# Data Visualization-Dash Tutorial  
[可視化ツールDashのチュートリアル - Part1: インストール～描画 - May 11, 2018](https://qiita.com/shimopino/items/ddc46adcbd6332511b92)  
[可視化ツールDashのチュートリアル - Part 2: 対話形式 - May 14, 2018](https://qiita.com/shimopino/items/8f524916eeac8c445cf0)  
[可視化ツールDashのチュートリアル - Part 3: State - May 14, 2018]()  

# Data Visualization-Dash Python Libray   
[Pythonの可視化ライブラリDashを使う　1 Mar 12, 2019](https://qiita.com/OgawaHideyuki/items/6df65fbbc688f52eb82c)  
[Pythonの可視化ライブラリDashを使う　2　Callbackをみる Mar 12, 2019](https://qiita.com/OgawaHideyuki/items/1eea435b3f7c90375848)  
[Pythonの可視化ライブラリDashを使う　3　マウスホバーを活用する Mar 13, 2019](https://qiita.com/OgawaHideyuki/items/b4e0c4f134c94037fd4f)  
[Pythonの可視化ライブラリDashを使う　4　herokuに7行であげてウェブでみられるようにする Mar 15, 2019](https://qiita.com/OgawaHideyuki/items/e2a046bf80bdae5ca61a)  

[COVID-19のデータでネットワーク図を作成した。Mar 13, 2020](https://qiita.com/OgawaHideyuki/items/204a2bcff6a3022ffc50)
[アプリリンク](https://chomoku.herokuapp.com/covid-19)

# Data Visualization-Dash  
[python製データ可視化ツール Dashを触ってみた所感 Dec 16, 2019](https://qiita.com/T_2/items/aa29dd8f8402d426ff83)  

## Html Elements  
[Html Elements](https://qiita.com/T_2/items/aa29dd8f8402d426ff83#html-elements)  
```
app.layout = html.Div(children=[
  html.H1(id='elm1', className='hoge' children=[]),
  #略
  html.Div(id='elm2', className='hoge' children=[]),]

```

```
import dash_core_components as dcc

dcc.Markdown('''

# 見出し
## 見出し2
本文
''')  
```
[Markdown](https://dash.plot.ly/dash-core-components/markdown)

## Graphs  
[Graphs](https://qiita.com/T_2/items/aa29dd8f8402d426ff83#graphs)  
```
dcc.Graph(
    figure={
        'data': [
             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
             {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
        ],
```

## Table   
[表](https://qiita.com/T_2/items/aa29dd8f8402d426ff83#%E8%A1%A8)  
```
import pandas as pd

dataframe = pd.read_csv('url')

dash_table.DataTable(
    id='table',
    columns=[ {"name": i, "id": i} for i in dataframe.columns],
    hidden_columns=[],
    row_selectable="single",
    data=dataframe.to_dict('records'),
),
```

## Callback  
[Callback](https://qiita.com/T_2/items/aa29dd8f8402d426ff83#callback)  
```
@app.callback(
    Output('table', 'data'),
    [Input('region-dropdown', 'value')])
def update_table(value):
    return df.query('市区町村名 == @value').to_dict('records')
```

## UIパーツをが必要不可欠  
[UIパーツをが必要不可欠](https://qiita.com/T_2/items/aa29dd8f8402d426ff83#ui%E3%83%91%E3%83%BC%E3%83%84%E3%82%92%E3%81%8C%E5%BF%85%E8%A6%81%E4%B8%8D%E5%8F%AF%E6%AC%A0)  
```
#app.layout
dcc.Location(id='location', refresh=False),
　　　

@app.callback(
    [Output('hoge', 'value1'),
    Input('location', 'pathname')])
def pass_change(value1, pathname):
```

## Outputは1つだけの法則  
[Outputは1つだけの法則](https://qiita.com/T_2/items/aa29dd8f8402d426ff83#output%E3%81%AF1%E3%81%A4%E3%81%A0%E3%81%91%E3%81%AE%E6%B3%95%E5%89%87)  
```
@app.callback(
    Output('hoge', 'children'),
    Input('fuga', 'value2'))
def func(value2):

@app.callback(
    Output('hoge', 'children'),
    [Input('fuga', 'value'),
     Input('hoyo', 'value')
   ])
def func(value1, value2):
```
上記のように、hogeをoutputとするcallbackが重複していた場合、  
```
DuplicateCallbackOutput
You have already assigned a callback to the output
An output can only havea single callback function.
```

```
@app.callback(
    [Output('hoge', 'children'),
     Output('hoge', 'children'),
     Output('hoge', 'children'),
     Output('hoge', 'children'),
     Output('hoge', 'children'),
     ],
    [Input('fuga1', 'value'),
     Input('fuga2', 'value'),
     Input('fuga3', 'value'),
     Input('fuga4', 'value'),
     Input('fuga5', 'value'),
   ])

```
多数のInputに対して多数のOutputが集まった巨大なCallbackになってしまうので注意が必要  

## ButtonのCallback  
[ButtonのCallback](https://qiita.com/T_2/items/aa29dd8f8402d426ff83#button%E3%81%AEcallback)  
```
@app.callback(
    Output('hoge', 'children'),
    Input('close-button', 'n_clicks_timestamp')])
def click(n_clicks_timestamp):
    if n_clicks_timestamp != None:
        if (time.time() * 1000 - n_clicks_timestamp) < 1000:
            return something
```



#  
[使用 Dash 所開發的互動式 Python框架範例專案 ](https://softnshare.com/%e4%bd%bf%e7%94%a8dash-%e6%89%80%e9%96%8b%e7%99%bc%e7%9a%84%e4%ba%92%e5%8b%95%e5%bc%8f-python%e6%a1%86%e6%9e%b6%e7%af%84%e4%be%8b%e5%b0%88%e6%a1%88/?fbclid=IwAR1gpdXGcBXC2V76b5ZEPVePIiiryUmgnYwK__w5zK9lEOgJCP6T9GL07E4)  
[plotly /dash-sample-apps ](https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-web-trader)   


# Troubleshooting


# Reference
[Awesome Dash](https://github.com/ucg8j/awesome-dash)  
[Tutorials](https://github.com/ucg8j/awesome-dash#tutorials)  
[App Examples](https://github.com/ucg8j/awesome-dash#app-examples)  



* []()
![alt tag]()

# h1 size

## h2 size

### h3 size

#### h4 size

##### h5 size

*strong*strong  
**strong**strong  

> quote  
> quote

- [ ] checklist1
- [x] checklist2

* 1
* 2
* 3

- 1
- 2
- 3
