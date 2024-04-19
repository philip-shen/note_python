import fta
import vectorbt as vbt

yf_data = vbt.YFData.download(
    "TSLA",
    start='2024-03-01 09:30:00 -0400',
    end='2024-04-19 09:35:00 -0400',
    interval='5m'
)
price = yf_data.get()
ta = fta.TA_Features()
ta.get_all_indicators(price)