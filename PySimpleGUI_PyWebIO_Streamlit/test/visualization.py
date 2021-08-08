import streamlit as st
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

@st.cache
def load_time_series_data():
    """
    ランダムに時系列データを生成する。
    """
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c']
    )
    return chart_data


@st.cache
def load_iris_data():
    """
    データ読み込み, cacheにして最適化を行う
    """
    iris_data = load_iris()
    df = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
    labels = iris_data.target_names[iris_data.target]
    return df, labels


def show_heatmap(df: 'pd.DataFrame'):
    """
    各特徴の相関ヒートマップをみる
    """
    fig, ax = plt.subplots(figsize=(10,10))
    sns.heatmap(df.corr(), annot=True, ax=ax)
    st.pyplot(fig)


def show_distplot(df: 'pd.DataFrame', labels: 'np.ndarray'):
    """
    それぞれの特徴について、各ラベルごとの分布を見る
    """
    for column in df.columns:
        st.write(f'- {column}')
        series = df[column]
        target_names = list(set(labels))
        hist_data = [series[labels == name] for name in target_names]
        fig = ff.create_distplot(
            hist_data, target_names, bin_size=[.1, .25, .5])
        st.plotly_chart(fig, use_container_width=True)


@st.cache(allow_output_mutation=True)
def fit_transform_pca(df: 'pd.DataFrame'):
    """
    主成分分析した結果の第二主成分ベクトルを可視化した結果を得る
    """
    pca = PCA(n_components=2)
    X = pca.fit_transform(df)
    return X

def show_scatter2d(X: 'np.ndarray', labels: 'np.ndarray'):
    fig, ax = plt.subplots(figsize=(10,10))
    target_names = list(set(labels))
    for i, target in enumerate(target_names):
        X_ = X[labels == target]
        x = X_[:, 0]
        y = X_[:, 1]
        ax.scatter(x, y, cmap=[i]*len(X_), label=target)

    ax.legend()
    st.pyplot(fig)


def main():
    st.title('Visualization app')

    st.write('時系列データをline plot')
    chart_data = load_time_series_data()
    st.line_chart(chart_data)

    st.write('### アイリスデータを見ていく')
    df, labels = load_iris_data()

    st.write('DataFrameの表示')
    st.write(df)

    st.write('特徴ごとの相関のHeatMap表示')
    show_heatmap(df)

    st.write('ラベルごとの特徴の分布をみる')
    show_distplot(df, labels)

    st.write('主成分分析をして、2次元にマッピングする')
    df_pca = fit_transform_pca(df)
    show_scatter2d(df_pca, labels)


if __name__ == '__main__':
    main()
