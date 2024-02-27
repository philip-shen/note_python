
# Dash Application
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State

# Data Viz
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Data Source
import yfinance as yf
#import pickle5 as pickle 
import pickle
import pandas as pd

# Global Variable: Ticker List
#with open("data/tickers.pickle", "rb") as f:
with open("data/twse_otc_id.pickle", "rb") as f:
#with open("data/steady_growth.pickle", "rb") as f:
#with open("data/ETF.pickle", "rb") as f:    
    TICKER_LIST = pickle.load(f)


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


class Indicator:
    """Class that takes in a pandas dataframe object and adds trading indicators"""

    def __init__(self, data):
        self.data = data

    def BollingerBands(self, width=1.96, window=21):
        """Default period set at 21 days"""
        self.data['BB Middle'] = self.data['Close'].rolling(window=window).mean()
        self.data['BB Upper'] = self.data['BB Middle'] + width * self.data['Close'].rolling(window=window).std()
        self.data['BB Lower'] = self.data['BB Middle'] - width * self.data['Close'].rolling(window=window).std()

        return self.data

    def MovingAverage(self, period=50):
        """Default is set to 50 days simple moving average"""
        self.ma_period = period
        self.data[f'MA{period}'] = self.data['Close'].rolling(period).mean()

        return self.data

    def MACD(self, period1=12, period2=26, period3=9):
        """Default is set to 12 and 26 exponential moving average for macd
        9 period units for signal"""
        # ewm = exponential weighted mean from pandas
        ema1 = self.data['Close'].ewm(span=period1, adjust=False).mean()   
        ema2 = self.data['Close'].ewm(span=period2, adjust=False).mean()
        macd_line = ema1 - ema2
        macd_signal = self.data['Close'].ewm(span=period3, adjust=False).mean()

        self.data['MACD'] = macd_line
        self.data['MACD Signal'] = macd_signal
        self.data['MACD Histogram'] = macd_line - macd_signal

        return self.data

    def RSI(self, period=14):
        """Relative Strength Index (RSI) is an oscillator that measures the rate of change in price
        0 <= RSI <= 100 | if RSI > 70, overbought | if RSI < 30, oversold"""
        # difference in price from previous step
        delta = self.data['Adj Close'].diff()        
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        _gain = up.ewm(com=(period - 1), min_periods=period).mean()
        _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
        RS = _gain / _loss

        self.data['RSI'] = (100 - (100 / (1 + RS)))
        return self.data

"""
Custom Candlestick Colors
https://plotly.com/python/candlestick-charts/
"""
"""
設定顏色
https://waynestalk.com/python-candlesticks/
"""

class Plotter:
    """Plotter class that takes in a Pandas dataframe object
    returns a Plotly graphic object compatible with Dash apps"""

    def __init__(self, data):
        self.data = data

    def plotCandlestick(self):
        chart = go.Candlestick(
            x=list(self.data.index), open=list(self.data['Open']),
            high=list(self.data['High']), low=list(self.data['Low']),
            close=list(self.data['Close']), name="Candlestick",
            increasing_line_color= 'red', decreasing_line_color= 'green',
            visible=True)
        return chart

    def plotRSI(self):
        chart = go.Scatter(
            x=list(self.data.index), y=list(self.data['RSI']),
            line=dict(color='pink', width=1.5), name="RSI")
        return chart

    def plotSMA(self, period=50):
        chart = go.Scatter(
            x=list(self.data.index), y=list(self.data[f'MA{period}']),
            line=dict(color='orange', width=1.3), name=f'SMA{period}')
        return chart

    def plotBBUpper(self):
        chart = go.Scatter(
            x=list(self.data.index), y=list(self.data['BB Upper']),
            line=dict(color='white', width=1.0), name="Bollinger Upper Band")
        return chart

    def plotBBLower(self):
        chart = go.Scatter(
            x=list(self.data.index), y=list(self.data['BB Lower']),
            line=dict(color='white', width=1.0), name="Bollinger Lower Band")
        return chart

    def plotVolume(self):
        chart = go.Bar(
            x=list(self.data.index), y=list(self.data['Volume']),
            marker_color='lightgrey', name="Volume")
        return chart


class Layout:
    """Handles the layout and front-facing app of Dash application"""

    @classmethod
    def dash_layout(self):
        layout = html.Div(
            children=[
                html.Div(
                    className='row',
                    children=[
                        # Left Tab: Inputs
                        html.Div(
                            className='three columns div-user-controls',
                            children=[

                                # Title
                                html.H1(
                                    'STOCK CHART ANALYZER',
                                    style={'text-align': 'center', 'font-size': '25px'}),
                                html.Br(),
                                html.P('Select Asset:',
                                       style={'font-size': '17px'}),

                                # Dropdown Input
                                dcc.Dropdown(
                                    id="ticker",
                                    options=[
                                        {
                                            "label": str(TICKER_LIST[i]),
                                            "value": str(TICKER_LIST[i]),
                                        }
                                        for i in range(len(TICKER_LIST))
                                    ],
                                    searchable=True,
                                    value="TSLA",
                                    placeholder="Enter Stock Ticker",
                                    style={'color': '#FFFFFF'}
                                ),
                                html.Br(),

                                # Plot Button
                                html.Button(
                                    'PLOT',
                                    style={'color': '#FDFDFD'},
                                    id='plot_button',
                                    n_clicks=1
                                ),
                                html.Br(), #html.Br(),

                                # Table info
                                html.P('Summary Statistics:',
                                       style={'font-size': '17px'}),
                                dt.DataTable(
                                    id='info',
                                    data=[],
                                    columns=[{'id': c, 'name': c}
                                             for c in ['Metric', 'Value']],
                                    style_cell={
                                        'textAlign': 'left',
                                        'color': 'black',
                                        'font-size': '15px'},
                                ),

                                # Credits
                                html.Br(), html.Br(), html.Br(), html.Br(),
                                html.Br(), html.Br(), html.Br(), html.Br(),
                                html.P('Frok from Jericho Villareal',
                                       style={'font-size': '17px'}
                                       ),
                                html.P('MIDS W200: '),
                                html.P('~ to the moon! ~',
                                       style={'font-size': '12px'}),
                                html.P('#HODL #DiamondHands #StonksOnlyGoUp',
                                       style={'font-size': '12px'})
                            ]
                        ),
                        # Right Tab: Graphs
                        html.Div(
                            className='nine columns div-for-charts bg-grey',
                            children=[
                                dcc.Graph(
                                    id='graph',
                                    config={'displayModeBar': False},
                                    animate=True
                                )
                            ]
                        )
                    ]
                )
            ]
        )
        return layout


class App:
    """Instantiates a Dash app that is already layouted using the Layout class"""

    @classmethod
    def init_app(cls):

        # Initialize Dash Application
        app = dash.Dash(__name__)
        app.config.suppress_callback_exceptions = True

        # Set up Dash Layout
        layout = Layout().dash_layout()
        app.layout = layout

        return app

class Engine:
    """Engine superclass that calls on: 
    - App: initiates a dash application with a Layout object
    - Asset: calls on particular stock ticker from TICKER_LIST
        - get_info(): summary statistics about the stock
        - get_data(): historical price/volume data 
    - Indicator: adds various signals and indicator to the stock
        - Bollinger Bands, RSI, MACD
    - Plotter: plots various indicators using Plotly  

    This class is responsible for callbacks which enable the app to update lower-level objects 
    """

    @classmethod
    def run(cls):
        app = App().init_app()  # important to initialize main Dash app layout
        
        # Update charts
        @app.callback(
            # Output
            Output("graph", "figure"),
            # Input
            [Input("plot_button", "n_clicks")],
            # State
            [State("ticker", "value")]
        )
        def update_graph(n_clicks, ticker):

            if ticker not in TICKER_LIST:
                print(f'ticker: {ticker}')
                #raise Exception("Invalid Ticker!")
            else:
                pass

            if n_clicks >= 1:
                
                # initialize Asset object 
                asset = Asset(ticker, period='1y', interval='1d')
                asset_info = asset.get_info()  # Information about the Company
                asset_df = asset.get_data()    # Historical price data

                # Check in terminal for n_clicks and status
                print(f'\nTicker: {ticker} | Clicks: {n_clicks}\n')
                print("Program is running...")

                # add Indicator objects
                asset_df = Indicator(asset_df).BollingerBands()
                asset_df = Indicator(asset_df).MovingAverage()
                asset_df = Indicator(asset_df).RSI()
                asset_df = Indicator(asset_df).MACD()
                
                # initialize Plotter trace objects
                candlestick = Plotter(asset_df).plotCandlestick()
                sma = Plotter(asset_df).plotSMA()
                bb_upper = Plotter(asset_df).plotBBUpper()
                bb_lower = Plotter(asset_df).plotBBLower()
                rsi = Plotter(asset_df).plotRSI()
                volume = Plotter(asset_df).plotVolume()

                # initialize Dash plot layout, 
                figure = make_subplots(
                    shared_xaxes=True, vertical_spacing=0.1,
                    rows=4, cols=1,                 # Partition layout in 4, row-wise
                    specs=[[{"rowspan": 2}],        # first chart will take up rows 1 and 2
                        [None],
                        [{}],                       # second chart will take up row 3
                        [{}]],                      # third chart will take up row 4
                    print_grid=False)
                
                figure.append_trace(candlestick, 1, 1)    # Plots in rows 1 and 2
                figure.append_trace(sma, 1, 1)
                figure.append_trace(bb_upper, 1, 1)
                figure.append_trace(bb_lower, 1, 1)
                figure.append_trace(rsi, 3, 1)            # Plot in row 2
                figure.append_trace(volume, 4, 1)         # Plot in row 3

                figure.update_xaxes(rangeslider_visible=False)
                #figure.update_yaxes(title_text="Price (USD)", row=1, col=1)
                figure.update_yaxes(title_text="Price (NTD)", row=1, col=1)
                figure.update_yaxes(title_text="RSI", row=3, col=1)
                figure.update_yaxes(title_text="Volume", row=4, col=1)

                figure['layout'].update(
                    height=950, autosize=True, template='plotly_dark',
                    title={

                        'text': f'{asset_info["longName"]} | Last Price: ${asset_df.iloc[-1]["Close"]:.2f}',
                        'font': {'color': 'white', 'size': 30}
                    }
                )

            return figure
        
        # Update Table
        @app.callback(
            # Output
            [Output("info", "columns"), Output("info", "data")],
            # Input
            [Input("plot_button", "n_clicks")],
            # State
            [State("ticker", "value")]
        )
        def update_table(n_clicks,  ticker):
            """Updates the metrics found on asset info"""

            if ticker not in TICKER_LIST:
                print(f'ticker: {ticker}')
                #raise Exception("Invalid Ticker!")
            else:
                pass

            metric_ls = ["longName", "sector", "industry",
                        "marketCap", "previousClose", "dayHigh", "dayLow"]
            if n_clicks >= 1:
                asset = Asset(ticker, period='1y', interval='1d')
                asset_info = asset.get_info() 
                print(f'asset_info: {asset_info}')
                #print(f'asset_info.items: {asset_info.items()}')

                data = [{'Metric': i, 'Value': j}
                        for i, j in asset_info.items() if i in metric_ls]
                data = pd.DataFrame.from_dict(data)
                data = data.reindex([6, 1, 0, 3, 2, 5, 4])
                data = data.to_dict('records')
                columns = [{'id': c, 'name': c} for c in ['Metric', 'Value']]

            return columns, data

        return app


if __name__ == '__main__':
    app = Engine().run()
    app.run_server(debug=True, port=8000, use_reloader=True)
    print("End of Program")
