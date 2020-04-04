# 4/4/2020 Initial
# 
########################################################
import pandas as pd
import plotly
import os,sys,time

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from logger import logger

if __name__ == "__main__":
    t0 = time.time()

    # read raw data from CSV file    
    csv_birth = os.path.join(dirnamelog,"birth.csv")
    raw = pd.read_csv(csv_birth)

    # initial
    #plotly.offline.init_notebook_mode(connected=False)
    #plotly.offline.init_notebook_mode(connected=True)

    # プロットするデータの指定  
    data = [
        plotly.graph_objs.Bar(x=raw["year"], y=raw["births"], name="Births"),
        plotly.graph_objs.Scatter(x=raw["year"], y=raw["birth rate"], name="Birth Rate", yaxis="y2")
    ]

    # graphic layout
    layout = plotly.graph_objs.Layout(
        width=1000, height=800,
        font={"family":"Yu Gothic Bold, sans-selif", "size":22},

        title="Births and Birth Rate in Japan",
        legend={"x":0.8, "y":0.1},
        xaxis={"title":"Year"},
        #xaxis={"title":"Year", "range": [2010, 2016]}, #from year 2010 to 2016
        
        #yaxis={"title":"Births"},
        yaxis={"title":"Births", "rangemode":"tozero"}, #starts from zero
        yaxis2={"title":"Birth Rate", "overlaying":"y", "side":"right"}
    )

    ''' 
    Jupyter内で表示したい場合には、iplotを呼んで、グラフを作成します。
    
    Jupyter外部で表示する場合や、HTMLを作成したい場合には、plotを呼びます。
    オプションでファイル名を指定しない場合には、同一フォルダにtemp-plot.htmlが作成されます。
    '''
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    #plotly.offline.iplot(fig, show_link=False)
    plotly.offline.plot(fig, show_link=False)

    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))     