Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Plotly](#plotly)
   * [Cufflinks](#cufflinks)
   * [plotnine, altair, seaborn, pixiedust](#plotnine-altair-seaborn-pixiedust)
      * [plotnine](#plotnine)
      * [altair](#altair)
      * [seaborn](#seaborn)
      * [pixiedust](#pixiedust)
   * [Data Visualization-Dash Tutorial](#data-visualization-dash-tutorial)
   * [Data Visualization-Dash Python Libray](#data-visualization-dash-python-libray)
   * [Data Visualization-Dash](#data-visualization-dash)
      * [Html Elements](#html-elements)
      * [Graphs](#graphs)
      * [Table](#table)
      * [Callback](#callback)
      * [UIパーツをが必要不可欠](#uiパーツをが必要不可欠)
      * [Outputは1つだけの法則](#outputは1つだけの法則)
      * [ButtonのCallback](#buttonのcallback)
   * [auto_report_using_dash_python](#auto_report_using_dash_python)
   * [Stock Analysis Dashboard](#stock-analysis-dashboard)
      * [Stock Charter](#stock-charter)
   * [Stock Price Predictor](#stock-price-predictor)
   * [Dash Technical Charting App](#dash-technical-charting-app)
   * [Dash Collection](#dash-collection)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)
# Purpose  
Take note of Dash  


# Plotly  
[[Python] Plotlyでぐりぐり動かせるグラフを作る Mar 16, 2019](https://qiita.com/inoory/items/12028af62018bf367722)  

# Cufflinks  
[[Python] CufflinksでPandasのデータフレームをPlotlyに一発描画 Mar 23, 2019](https://qiita.com/inoory/items/7c8ca9fd5e1aca3e2e72)  
[santosjorge /cufflinks](https://github.com/santosjorge/cufflinks) 
```
This library binds the power of plotly with the flexibility of pandas for easy plotting.

This library is available on https://github.com/santosjorge/cufflinks

This tutorial assumes that the plotly user credentials have already been 
configured as stated on the getting started guide.
```

[jupyter notebook上で金融データの描画・取得・操作 Dec 23, 2017](https://qiita.com/u1and0/items/6bc0dbeed0e20dd89eda)  
```
この記事はplotlyとpandasを結びつけるライブラリ"cufflinks"の紹介、およびそれを利用した金融関連のデータ描画、
pandas_datareaderや自作モジュールによる金融データの取得、自作モジュールによる金融データの操作を行います。
```
![alt tag](https://i.imgur.com/OJgp2Z2.jpg)

[Python金融分析（一）：Cufflinks与数据可视化| 北远山村 Mar 8, 2019](https://beiyuan.me/python4finance-1/)  
示例2：金融数据可视化  
```
raw = pd.read_csv('./source/fxcm_eur_usd_eod_data.csv', index_col=0, parse_dates=True)
raw.info()
```

```
<class 'pandas.core.frame.DataFrame'>
DatetimeIndex: 1547 entries, 2013-01-01 22:00:00 to 2017-12-31 22:00:00
Data columns (total 8 columns):
BidOpen     1547 non-null float64
BidHigh     1547 non-null float64
BidLow      1547 non-null float64
BidClose    1547 non-null float64
AskOpen     1547 non-null float64
AskHigh     1547 non-null float64
AskLow      1547 non-null float64
AskClose    1547 non-null float64
dtypes: float64(8)
memory usage: 108.8 KB
```

```
quotes = raw[['AskOpen', 'AskHigh', 'AskLow', 'AskClose']]
quotes=quotes.iloc[-60:]
```
```
qf = cf.QuantFig(
    quotes,
    title='EUR/USD Exchange Rate',
    legend='top',
    name='EUR/USD'
)
py_offline.iplot(qf.iplot(asFigure=True))
```

![alt tag](https://cloud.tsinghua.edu.cn/seafhttp/files/a6b2e842-7757-40cf-9a05-378f1c8d8111/output_23_0.png)


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


# auto_report_using_dash_python 
[Python Dash 實踐（上）——草圖設計與CSS｜教學 已更新：2021年12月29日](https://www.bianalyst-gt.com/post/python-dash-%E5%AF%A6%E8%B8%90%EF%BC%88%E4%B8%8A%EF%BC%89-%E8%8D%89%E5%9C%96%E8%A8%AD%E8%A8%88%E8%88%87css-%E6%95%99%E5%AD%B8)

[python-dash-實踐（下）-callback與實際案例-教學](https://www.bianalyst-gt.com/post/python-dash-%E5%AF%A6%E8%B8%90%EF%BC%88%E4%B8%8A%EF%BC%89-%E8%8D%89%E5%9C%96%E8%A8%AD%E8%A8%88%E8%88%87css-%E6%95%99%E5%AD%B8)

[ChunTingChang /auto_report_using_dash_python](https://github.com/ChunTingChang/auto_report_using_dash_python)


#  Stock Analysis Dashboard 
[Create a Stock Analysis Dashboard With Python May 20](https://medium.com/python-in-plain-english/stock-analysis-dashboard-with-python-366d431c8721)

```
The project's code can be divided into four major sections, which are in order:

1. Data Collection & Cleaning
2. Data Importing & Default Charts
3. Application’s Layout
4. Interactivity
```

## Stock Charter  
[stock_charter.py](stock-analyzer/stock_charter.py)  
<img src="images/2330.TW.jpg" width="800" height="400">  

[felipesveiga/Stock-Analysis-Dashboard](https://github.com/felipesveiga/Stock-Analysis-Dashboard)

>  Dash ImportError: cannot import name 'get_current_traceback' from 'werkzeug.debug.tbtools'
[cannot import name 'get_current_traceback' from 'werkzeug.debug.tbtools'](https://stackoverflow.com/questions/71654590/dash-importerror-cannot-import-name-get-current-traceback-from-werkzeug-debu)

<img src="https://i.stack.imgur.com/OFM7a.png" width="400" height="100">  

```
I've been in the same problem.

Uninstall the wrong version with:
pip uninstall werkzeug

Install the right one with:
pip install -v https://github.com/pallets/werkzeug/archive/refs/tags/2.0.1.tar.gz
```

# Stock Price Predictor

[stock-price-predictor](https://github.com/felipesveiga/stock-price-predictor)


#  
[使用 Dash 所開發的互動式 Python框架範例專案 ](https://softnshare.com/%e4%bd%bf%e7%94%a8dash-%e6%89%80%e9%96%8b%e7%99%bc%e7%9a%84%e4%ba%92%e5%8b%95%e5%bc%8f-python%e6%a1%86%e6%9e%b6%e7%af%84%e4%be%8b%e5%b0%88%e6%a1%88/?fbclid=IwAR1gpdXGcBXC2V76b5ZEPVePIiiryUmgnYwK__w5zK9lEOgJCP6T9GL07E4)  
[plotly /dash-sample-apps ](https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-web-trader)   


# Dash Technical Charting App
[plotly / dash-technical-charting](https://github.com/plotly/dash-technical-charting/tree/master/quantmod)


# Dash Collection
[6月 20, 2022 Dash 第62回（DashCanvas 画像の切り抜き）](https://ailog.site/2022/06/20/2022/0620/)

[6月 19, 2022 Dash 第61回（DashCanvas 選択情報をテーブル表示）](https://ailog.site/2022/06/19/2022/0619/)

[6月 18, 2022 Dash 第60回（DashCanvas 画像表示）](https://ailog.site/2022/06/18/2022/0618/)

[6月 17, 2022 Dash 第59回（DashCanvasクラスの属性）](https://ailog.site/2022/06/17/2022/0617/)

[6月 16, 2022 Dash 第58回（DashCanvas アノテーション表示）](https://ailog.site/2022/06/16/2022/0616/)

[6月 15, 2022 Dash 第57回（DashCanvas）](https://ailog.site/2022/06/15/2022/0615/)

[6月 14, 2022 Dash 第56回（テーブルデータを地図に表示）](https://ailog.site/2022/06/14/2022/0614/)

[6月 13, 2022 Dash 第55回（テーブルのソートとエクスポート）](https://ailog.site/2022/06/13/2022/0613/)

[6月 12, 2022 Dash 第54回（テーブルの行削除と行選択）](https://ailog.site/2022/06/12/2022/0612/)

[6月 11, 2022 Dash 第53回（テーブルの編集とフィルター）](https://ailog.site/2022/06/11/2022/0611/)

[6月 10, 2022 Dash 第52回（テーブルの表示幅変更とヘッダー固定表示）](https://ailog.site/2022/06/10/2022/0610/)

[6月 09, 2022 Dash 第51回（CSVファイルをテーブル表示）](https://ailog.site/2022/06/09/2022/0609/)

[6月 08, 2022 Dash㊿（DataTableコンポーネント　要素ごとにスタイル設定）](https://ailog.site/2022/06/08/2022/0608/)

[6月 07, 2022 Dash㊾（DataTableコンポーネント　スタイル設定）](https://ailog.site/2022/06/07/2022/0607/)

[6月 06, 2022 Dash㊽（DataTableコンポーネント　オプション設定その２）](https://ailog.site/2022/06/06/2022/0606/)

[6月 05, 2022 Dash㊼（DataTableコンポーネント　オプション設定その１）](https://ailog.site/2022/06/05/2022/0605/)

[6月 04, 2022 Dash㊻（DataTableコンポーネント）](https://ailog.site/2022/06/04/2022/0604/)

[6月 03, 2022 Dash㊺（Tabコンポーネント）](https://ailog.site/2022/06/03/2022/0603/)

[6月 02, 2022 Dash㊹（Uploadコンポーネント その３）](https://ailog.site/2022/06/02/2022/0602/)

[6月 01, 2022 Dash㊸（Uploadコンポーネント その２）](https://ailog.site/2022/06/01/2022/0601/)

[5月 31, 2022 Dash㊷（Uploadコンポーネント）](https://ailog.site/2022/05/31/2022/0531/)

[5月 30, 2022 Dash㊶（Intervalコンポーネント）](https://ailog.site/2022/05/30/2022/0530/)

[5月 29, 2022 Dash㊵（Locationコンポーネント）](https://ailog.site/2022/05/29/2022/05229/)

[5月 28, 2022 Dash㊴（Linkコンポーネント）](https://ailog.site/2022/05/28/2022/05228/)

[5月 27, 2022 Dash㊳（Sliderコンポーネント）](https://ailog.site/2022/05/27/2022/05227/)

[5月 26, 2022 Dash㊲（Loadingコンポーネント）](https://ailog.site/2022/05/26/2022/05226/)

[5月 25, 2022 Dash㊱（Checklistコンポーネント）](https://ailog.site/2022/05/25/2022/05225/)

[5月 24, 2022 Dash㉟（Dropdownコンポーネント／複数選択）](https://ailog.site/2022/05/24/2022/05224/)

[5月 23, 2022 Dash㉞（Dropdownコンポーネント）](https://ailog.site/2022/05/23/2022/05223/)

[5月 22, 2022 Dash㉝（標準コンポーネント／ボタン）](https://ailog.site/2022/05/22/2022/05222/)

[5月 21, 2022 Dash㉜（標準コンポーネント／文字列）](https://ailog.site/2022/05/21/2022/05221/)

[5月 20, 2022 Dash㉛（連鎖コールバック）](https://ailog.site/2022/05/20/2022/05220/)

[5月 19, 2022 Dash㉚（コールバック停止／部分）](https://ailog.site/2022/05/19/2022/0519/)

[5月 18, 2022 Dash㉙（コールバック停止／全体）](https://ailog.site/2022/05/18/2022/0518/)

[5月 17, 2022 Dash㉘（マウス動作　ドラッグ操作）](https://ailog.site/2022/05/17/2022/0517/)

[5月 16, 2022 Dash㉗（マウス動作　複数選択）](https://ailog.site/2022/05/16/2022/0516/)

[5月 15, 2022 Dash㉖（グラフ上のマウス動作）](https://ailog.site/2022/05/15/2022/0515/)

[5月 14, 2022 Dash㉕（レイアウトごとのコールバック　テーブル編）](https://ailog.site/2022/05/14/2022/0514/)

[5月 13, 2022 Dash㉔（レイアウトごとのコールバック　グラフ編）](https://ailog.site/2022/05/13/2022/0513/)

[5月 12, 2022 Dash㉓（画面遷移）](https://ailog.site/2022/05/12/2022/0512/)

[5月 11, 2022 Dash㉒（パターンマッチング・コールバック／ALLSMALLERセレクタ その２）](https://ailog.site/2022/05/11/2022/0511/)

[5月 10, 2022 Dash㉑（パターンマッチング・コールバック／ALLSMALLERセレクタ）](https://ailog.site/2022/05/10/2022/0510/)

[5月 09, 2022 Dash⑳（パターンマッチング・コールバック／MATCHセレクタ その２）](https://ailog.site/2022/05/09/2022/0509/)

[5月 08, 2022 Dash⑲（パターンマッチング・コールバック／MATCHセレクタ）](https://ailog.site/2022/05/08/2022/0508/)

[5月 07, 2022 Dash⑱（パターンマッチング・コールバック／ALLセレクタ その２）](https://ailog.site/2022/05/07/2022/0507/)

[5月 06, 2022 Dash⑰（パターンマッチング・コールバック／ALLセレクタ）](https://ailog.site/2022/05/06/2022/0506/)

[5月 05, 2022 Dash⑯（コールバック／複数入力）](https://ailog.site/2022/05/05/2022/0505/)

[5月 04, 2022 Dash⑮（コールバック／スライダー）](https://ailog.site/2022/05/04/2022/0504/)

[5月 03, 2022 Dash⑭（コールバック／ボタン）](https://ailog.site/2022/05/03/2022/0503/)

[5月 02, 2022 Dash⑬（複数のコンポーネントを組み合わせた配置）](https://ailog.site/2022/05/02/2022/0502/)

[5月 01, 2022 Dash⑫（複数コンポーネントの配置／スタイルシートをカスタマイズ）](https://ailog.site/2022/05/01/2022/0501/)

[4月 30, 2022 Dash⑪（複数コンポーネントの配置／外部css）](https://ailog.site/2022/04/30/2022/0430/)

[4月 29, 2022 Dash⑩（複数コンポーネントの配置／引数 style）](https://ailog.site/2022/04/29/2022/0429/)

[4月 28, 2022 Dash⑨（複数コンポーネントの配置／引数 style）](https://ailog.site/2022/04/28/2022/0428/)

[4月 27, 2022 Dash⑧（グラフの配置／plotly.py）](https://ailog.site/2022/04/27/2022/0427/)

[4月 26, 2022 Dash⑧（グラフの配置／Plotly Express）](https://ailog.site/2022/04/26/2022/0426/)

[4月 25, 2022 Dash⑦（コンポーネントの属性）](https://ailog.site/2022/04/25/2022/0425/)

[4月 24, 2022 Dash⑥（コールバック）](https://ailog.site/2022/04/24/2022/0424/)

[4月 23, 2022 Dash⑤（レイアウト）](https://ailog.site/2022/04/23/2022/0423/)

[4月 22, 2022 Dash④（グラフ作成）](https://ailog.site/2022/04/22/2022/0422/)

[4月 21, 2022 Dash③（スタイル設定）](https://ailog.site/2022/04/21/2022/0421/)

[4月 20, 2022 Dash②（最小アプリケーション）](https://ailog.site/2022/04/20/2022/0420/)

[4月 19, 2022 Dash①（概要とインストール）](https://ailog.site/2022/04/19/2022/0419/)


# Troubleshooting


# Reference
[Awesome Dash](https://github.com/ucg8j/awesome-dash)  
[Tutorials](https://github.com/ucg8j/awesome-dash#tutorials)  
[App Examples](https://github.com/ucg8j/awesome-dash#app-examples)  



* []()  
![alt tag]()
<img src="" width="400" height="500">  

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
