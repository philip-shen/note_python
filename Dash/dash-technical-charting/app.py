# In[]:
# Import required libraries
import os, sys
import datetime as dt
import pickle
import yfinance as yf

import quantmod as qm
import pandas_datareader.data as web

import flask
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from flask_caching import Cache

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")
dirnamedata= os.path.join(strdirname,"data")
# In[]:
# Setup the app
server = flask.Flask(__name__)
app = dash.Dash(__name__)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-finance-1.28.0.min.js'

class Asset:
    """Class to initialize the stock, given a ticker, period and interval"""
    def __init__(self, ticker, period='1y', interval='1d'):
        self.ticker = ticker.upper()
        self.period = period
        self.interval = interval

    def __repr__(self):
        return f"Ticker: {self.ticker}, Period: {self.period}, Interval: {self.interval}"

    def get_info(self):
        """Uses yfinance to get information about the ticker
        returns a dictionary filled with at-point information about the ticker"""
        ticker_info = yf.Ticker(self.ticker).info
        return ticker_info

    def get_data(self):
        """Uses yfinance to get data, returns a Pandas DataFrame object
        Index: Date
        Columns: Open, High, Low, Close, Adj Close, Volume
        """
        try:
            self.data = yf.download(
                tickers=self.ticker,
                period=self.period,
                interval=self.interval)
            return self.data
        except Exception as e:
            return e

# In[]:
# Put your Dash code here

# Add caching
cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})
timeout = 60 * 60  # 1 hour

# Controls
sp500 = ['2330.TW','AAPL', 'ABT', 'ABBV', 'ACN', 'ACE', 'ADBE', 'ADT', 'AAP', 'AES',
         'AET', 'AFL', 'AMG', 'A', 'GAS', 'ARE', 'APD', 'AKAM', 'AA', 'AGN',
         'ALXN', 'ALLE', 'ADS', 'ALL', 'ALTR', 'MO', 'AMZN', 'AEE', 'AAL',
         'AEP', 'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC',
         'ADI', 'AON', 'APA', 'AIV', 'AMAT', 'ADM', 'AIZ', 'T', 'ADSK', 'ADP',
         'AN', 'AZO', 'AVGO', 'AVB', 'AVY', 'BHI', 'BLL', 'BAC', 'BK', 'BCR',
         'BXLT', 'BAX', 'BBT', 'BDX', 'BBBY', 'BRK.B', 'BBY', 'BLX', 'HRB',
         'BA', 'BWA', 'BXP', 'BSX', 'BMY', 'BRCM', 'BF.B', 'CHRW', 'CA',
         'CVC', 'COG', 'CAM', 'CPB', 'COF', 'CAH', 'HSIC', 'KMX', 'CCL',
         'CAT', 'CBG', 'CBS', 'CELG', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW',
         'CHK', 'CVX', 'CMG', 'CB', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C',
         'CTXS', 'CLX', 'CME', 'CMS', 'COH', 'KO', 'CCE', 'CTSH', 'CL',
         'CMCSA', 'CMA', 'CSC', 'CAG', 'COP', 'CNX', 'ED', 'STZ', 'GLW',
         'COST', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA',
         'DE', 'DLPH', 'DAL', 'XRAY', 'DVN', 'DO', 'DTV', 'DFS', 'DISCA',
         'DISCK', 'DG', 'DLTR', 'D', 'DOV', 'DOW', 'DPS', 'DTE', 'DD', 'DUK',
         'DNB', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA',
         'EMC', 'EMR', 'ENDP', 'ESV', 'ETR', 'EOG', 'EQT', 'EFX', 'EQIX',
         'EQR', 'ESS', 'EL', 'ES', 'EXC', 'EXPE', 'EXPD', 'ESRX', 'XOM',
         'FFIV', 'FB', 'FAST', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FISV',
         'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'F', 'FOSL', 'BEN', 'FCX',
         'FTR', 'GME', 'GPS', 'GRMN', 'GD', 'GE', 'GGP', 'GIS', 'GM',
         'GPC', 'GNW', 'GILD', 'GS', 'GT', 'GOOGL', 'GOOG', 'GWW', 'HAL',
         'HBI', 'HOG', 'HAR', 'HRS', 'HIG', 'HAS', 'HCA', 'HCP', 'HCN',
         'HP', 'HES', 'HPQ', 'HD', 'HON', 'HRL', 'HSP', 'HST', 'HCBK',
         'HUM', 'HBAN', 'ITW', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG',
         'IFF', 'INTU', 'ISRG', 'IVZ', 'IRM', 'JEC', 'JBHT', 'JNJ',
         'JCI', 'JOY', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'GMCR', 'KMB',
         'KIM', 'KMI', 'KLAC', 'KSS', 'KRFT', 'KR', 'LB', 'LLL', 'LH',
         'LRCX', 'LM', 'LEG', 'LEN', 'LVLT', 'LUK', 'LLY', 'LNC', 'LLTC',
         'LMT', 'L', 'LOW', 'LYB', 'MTB', 'MAC', 'M', 'MNK', 'MRO', 'MPC',
         'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK',
         'MJN', 'MMV', 'MDT', 'MRK', 'MET', 'KORS', 'MCHP', 'MU', 'MSFT',
         'MHK', 'TAP', 'MDLZ', 'MON', 'MNST', 'MCO', 'MS', 'MOS', 'MSI',
         'MUR', 'MYL', 'NDAQ', 'NOV', 'NAVI', 'NTAP', 'NFLX', 'NWL',
         'NFX', 'NEM', 'NWSA', 'NEE', 'NLSN', 'NKE', 'NI', 'NE', 'NBL',
         'JWN', 'NSC', 'NTRS', 'NOC', 'NRG', 'NUE', 'NVDA', 'ORLY',
         'OXY', 'OMC', 'OKE', 'ORCL', 'OI', 'PCAR', 'PLL', 'PH', 'PDCO',
         'PAYX', 'PNR', 'PBCT', 'POM', 'PEP', 'PKI', 'PRGO', 'PFE',
         'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PBI', 'PCL', 'PNC', 'RL',
         'PPG', 'PPL', 'PX', 'PCP', 'PCLN', 'PFG', 'PG', 'PGR', 'PLD',
         'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM',
         'DGX', 'RRC', 'RTN', 'O', 'RHT', 'REGN', 'RF', 'RSG', 'RAI',
         'RHI', 'ROK', 'COL', 'ROP', 'ROST', 'RLD', 'R', 'CRM', 'SNDK',
         'SCG', 'SLB', 'SNI', 'STX', 'SEE', 'SRE', 'SHW', 'SPG', 'SWKS',
         'SLG', 'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SE', 'STJ', 'SWK',
         'SPLS', 'SBUX', 'HOT', 'STT', 'SRCL', 'SYK', 'STI', 'SYMC', 'SYY',
         'TROW', 'TGT', 'TEL', 'TE', 'TGNA', 'THC', 'TDC', 'TSO', 'TXN',
         'TXT', 'HSY', 'TRV', 'TMO', 'TIF', 'TWX', 'TWC', 'TJX', 'TMK',
         'TSS', 'TSCO', 'RIG', 'TRIP', 'FOXA', 'TSN', 'TYC', 'UA',
         'UNP', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'URBN', 'VFC',
         'VLO', 'VAR', 'VTR', 'VRSN', 'VZ', 'VRTX', 'VIAB', 'V', 'VNO',
         'VMC', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'ANTM', 'WFC', 'WDC',
         'WU', 'WY', 'WHR', 'WFM', 'WMB', 'WEC', 'WYN', 'WYNN', 'XEL',
         'XRX', 'XLNX', 'XL', 'XYL', 'YHOO', 'YUM', 'ZBH', 'ZION', 'ZTS']

etf = ['SPY', 'XLF', 'GDX', 'EEM', 'VXX', 'IWM', 'UVXY', 'UXO', 'GDXJ', 'QQQ']
#tickers = sp500 + etf

tickers= []
path_pickle_band_op= os.path.join(dirnamedata, 'band_op_202210.pickle')
path_pickle_business_cycle= os.path.join(dirnamedata, 'business_cycle.pickle')
path_pickle_steady_growth= os.path.join(dirnamedata, 'steady_growth_202210.pickle')

with open(path_pickle_band_op, "rb") as f:
    list_band_op = pickle.load(f)
with open(path_pickle_business_cycle, "rb") as f:
    list_business_cycle = pickle.load(f)
with open(path_pickle_steady_growth, "rb") as f:
    list_steady_growth = pickle.load(f)
tickers= list_band_op + list_steady_growth + list_business_cycle

tickers = [dict(label=str(ticker), value=str(ticker))
           for ticker in tickers]

# Dynamic binding
functions = dir(qm.ta)[9:-4]
functions = [dict(label=str(function[4:]), value=str(function))
             for function in functions]

# Layout
app.layout = html.Div(
    [
        html.Div([
            html.H2(
                'Dash Finance',
                style={'padding-top': '20', 'text-align': 'center'}
            ),
            html.Div(
                [
                    html.Label('Select ticker:'),
                    dcc.Dropdown(
                        id='dropdown',
                        options=tickers,
                        value='SPY',
                    ),
                ],
                style={
                    'width': '910', 'display': 'inline-block',
                    'padding-left': '40', 'margin-bottom': '20'}
            ),
            html.Div(
                [
                    html.Label('Select technical indicators:'),
                    dcc.Dropdown(
                        id='multi',
                        options=functions,
                        multi=True,
                        value=['add_BBANDS', 'add_RSI', 'add_MACD'],
                    ),
                ],
                style={
                    'width': '510', 'display': 'inline-block',
                    'padding-right': '40', 'margin-bottom': '20'}
            ),
        ]),
        html.Div(
            [
                html.Label('Specify parameters of technical indicators:'),
                html.P('Use , to separate arguments and ; to separate indicators. () and spaces are ignored'),  # noqa: E501
                dcc.Input(
                    id='arglist',
                    style={'height': '32', 'width': '1020'}
                )
            ],
            id='arg-controls',
            style={'display': 'none'}
        ),
        dcc.Graph(id='output')
    ],
    style={
        'width': '1100',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'font-family': 'overpass',
        'background-color': '#F3F3F3'
    }
)

@app.callback(Output('arg-controls', 'style'), [Input('multi', 'value')])
def display_control(multi):
    if not multi:
        return {'display': 'none'}
    else:
        return {'margin-bottom': '20', 'padding-left': '40'}


@cache.memoize(timeout=timeout)
@app.callback(Output('output', 'figure'), [Input('dropdown', 'value'),
                                           Input('multi', 'value'),
                                           Input('arglist', 'value')])
def update_graph_from_dropdown(dropdown, multi, arglist):

    # Get Quantmod Chart
    try:
        df = web.DataReader(dropdown, 'yahoo', dt.datetime(2016, 1, 1), dt.datetime.now())
        
        print('ticker: {}'.format(dropdown))

        metric_ls = ["longName", "sector", "industry",
                        "marketCap", "previousClose", "dayHigh", "dayLow"]

        asset = Asset(dropdown, period='1y', interval='1d')
        asset_info = asset.get_info() 

        list_data = [{'Metric': i, 'Value': j}
                    for i, j in asset_info.items() if i in metric_ls]
        for data in list_data:
            print('{}: {}'.format(data['Metric'], data['Value']))

        ch = qm.Chart(df)
    except:
        pass

    # Get functions and arglist for technical indicators
    if arglist:
        arglist = arglist.replace('(', '').replace(')', '').split(';')
        arglist = [args.strip() for args in arglist]
        for function, args in zip(multi, arglist):
            if args:
                args = args.split(',')
                newargs = []
                for arg in args:
                    try:
                        arg = int(arg)
                    except:
                        try:
                            arg = float(arg)
                        except:
                            pass
                    newargs.append(arg)
                print(newargs)
                # Dynamic calling
                getattr(qm, function)(ch, *newargs)
            else:
                getattr(qm, function)(ch)
    else:
        for function in multi:
            # Dynamic calling
            getattr(qm, function)(ch)

    # Return plot as figure
    fig = ch.to_figure(width=1100)
    return fig


# In[]:
# External css

external_css = ["https://fonts.googleapis.com/css?family=Overpass:400,400i,700,700i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/c6a126a684eaaa94a708d41d6ceb32b28ac78583/dash-technical-charting.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })


# In[]:
# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, port=8000)