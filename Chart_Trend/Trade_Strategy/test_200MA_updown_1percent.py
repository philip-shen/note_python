import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 載入資料
data = pd.read_csv('00631L.csv', parse_dates=['Date'])
data.set_index('Date', inplace=True)
# 假設資料中包含以下欄位：大盤指數 (Index)、00631L 收盤價 (Close)
data['Index_200MA'] = data['Index'].rolling(window=200).mean() # 計算200日均線
data['Index_200MA_diff'] = (data['Index'] - data['Index_200MA']) / data['Index_200MA'] * 100
# 定義買賣訊號
data['Signal'] = 0 # 初始化訊號
data.loc[data['Index_200MA_diff'] > 1, 'Signal'] = 1 # 當均線高於1%時買進
data.loc[data['Index_200MA_diff'] < -1, 'Signal'] = -1 # 當均線低於-1%時賣出
# 計算持倉
data['Position'] = data['Signal'].replace(to_replace=0, method='ffill') # 持倉狀態
data['Position'] = data['Position'].fillna(0) # 預防初始時的空值
# 計算日報酬
data['Daily_Return'] = data['Close'].pct_change()
data['Strategy_Return'] = data['Position'].shift(1) * data['Daily_Return']
# 計算累積報酬
data['Cumulative_Market_Return'] = (1 + data['Daily_Return']).cumprod()
data['Cumulative_Strategy_Return'] = (1 + data['Strategy_Return']).cumprod()
# 計算最大回撤 (MDD)
def calculate_mdd(cumulative_return):
    peak = cumulative_return.cummax()
    drawdown = (cumulative_return - peak) / peak
    mdd = drawdown.min()
    return mdd
market_mdd = calculate_mdd(data['Cumulative_Market_Return'])
strategy_mdd = calculate_mdd(data['Cumulative_Strategy_Return'])

# 繪圖
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Cumulative_Market_Return'], label='Market Return')
plt.plot(data.index, data['Cumulative_Strategy_Return'], label='Strategy Return')
plt.title('Backtest Results')
plt.legend()
plt.show()

# 輸出結果
final_return = data[['Cumulative_Market_Return', 'Cumulative_Strategy_Return']].iloc[-1]
print(f"Market Return: {final_return['Cumulative_Market_Return']:.2f}")
print(f"Strategy Return: {final_return['Cumulative_Strategy_Return']:.2f}")
print(f"Market MDD: {market_mdd:.2%}")
print(f"Strategy MDD: {strategy_mdd:.2%}")