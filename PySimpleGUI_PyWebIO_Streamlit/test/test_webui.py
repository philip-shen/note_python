# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np

def render_gup():
    """GuP のアプリケーションを処理する関数"""
    character_and_quotes = {
        'Miho Nishizumi': 'パンツァーフォー',
        'Saori Takebe': 'やだもー',
        'Hana Isuzu': '私この試合絶対勝ちたいです',
        'Yukari Akiyama': '最高だぜ！',
        'Mako Reizen': '以上だ',
    }
    selected_items = st.multiselect('What are your favorite characters?',
                                    list(character_and_quotes.keys()))
    for selected_item in selected_items:
        st.write(character_and_quotes[selected_item])


def render_aim_for_the_top():
    """トップ！のアプリケーションを処理する関数"""
    selected_item = st.selectbox('Which do you like more in the series?',
                                 [1, 2])
    if selected_item == 1:
        st.write('me too!')
    else:
        st.write('2 mo ii yo ne =)')

def main():
    placeholder = st.empty()
    # プレースホルダにコンテナを追加する
    container = placeholder.container()
    # コンテナにカラムを追加する
    col1, col2 = container.columns(2)
    # それぞれのカラムに書き込む
    with col1:
        st.write('Hello, World')
    with col2:
        st.write('Konnichiwa, Sekai')

    

    # アプリケーション名と対応する関数のマッピング
    apps = {
        '-': None,
        'GIRLS und PANZER': render_gup,
        'Aim for the Top! GunBuster': render_aim_for_the_top,
    }
    selected_app_name = st.sidebar.selectbox(label='apps',
                                             options=list(apps.keys()))

    if selected_app_name == '-':
        st.info('Please select the app')
        st.stop()

    # 選択されたアプリケーションを処理する関数を呼び出す
    render_func = apps[selected_app_name]
    render_func()

    # サイドバーにリロードボタンをつける
    st.sidebar.button('Reload')
    # サイドバーにデータフレームを書き込む
    data = np.random.randn(20, 3)
    df = pd.DataFrame(data, columns=['x', 'y', 'z'])
    st.sidebar.dataframe(df)
    
if __name__ == '__main__':
    main()