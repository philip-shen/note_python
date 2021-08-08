import json
from datetime import datetime
import os

import streamlit as st
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly, add_changepoints_to_plot


def load_data(data_path):
    """
    データを読み込む
    """
    with open(data_path, 'r') as f:
        covid19_data = json.load(f)

    df = pd.DataFrame.from_records(covid19_data['patients_summary']['data'])

    # 日付の変換
    TIME_FORMAT_FROM = '%Y-%m-%dT%H:%M:%S.000Z'
    TIME_FORMAT_TO = '%Y-%m-%d'
    df['日付'] = df['日付'].map(lambda x: datetime.strftime(datetime.strptime(x, TIME_FORMAT_FROM), TIME_FORMAT_TO))

    df['感染者総数'] = df['小計'].cumsum()

    return df


@st.cache(allow_output_mutation=True)
def fit_and_forecast(df: 'pd.DataFrame', periods:int = 14):
    """
    与えられたDataFrameに対して、prophetのmodelと予測結果を返す
    """
    model = Prophet(growth='logistic')
    model.fit(df)
    future = model.make_future_dataframe(periods=periods)
    future['cap'] = df.iloc[0].cap
    forecast = model.predict(future)
    return model, forecast


def main():
    st.title('東京都COVID-19感染者数をprophetする')

    df = load_data('data/data.json')

    st.write('### 直近の感染者数')
    st.write(df.tail())

    prophet_df = df[['日付', '感染者総数']].rename(columns={'日付':'ds', '感染者総数':'y'})
    prophet_df['cap'] = prophet_df.iloc[-1].y*1.5

    model, forecast = fit_and_forecast(prophet_df)

    st.write('### モデルの予測結果と実測値')

    fig = plot_plotly(model, forecast)
    st.plotly_chart(fig, use_container_width=True)

    st.write('予測値テーブル')
    forecast['diff_yhat'] = forecast['yhat'].diff()
    prophet_df['diff_y'] = prophet_df.y.diff()
    df_view = pd.concat((forecast, prophet_df[['y', 'diff_y']]), axis=1)[['ds','y','diff_y','yhat','diff_yhat']]
    st.write(
        df_view.rename(columns={'ds':'日付', 'y': '感染者総数', 'diff_y': '小計', 'yhat': '感染者総数予測値', 'diff_yhat': '小計予測値'}).tail(17)
    )

    st.write('### トレンドと季節変動')
    fig = plot_components_plotly(model, forecast)
    st.plotly_chart(fig, use_container_width=True)

    st.write('### 変化点')
    fig = model.plot(forecast)
    add_changepoints_to_plot(fig.gca(), model, forecast)
    st.pyplot(fig)


if __name__ == '__main__':
    main()
