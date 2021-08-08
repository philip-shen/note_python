import streamlit as st

#セッションの属性を読み書き
def show_page(voice):
    if "call_of_beauty" not in st.session_state:
        st.session_state.call_of_beauty = ""
    call = st.session_state.call_of_beauty
    call += voice
    st.session_state.call_of_beauty = call
    st.text(call)

#ページ遷移のようなもの
page = st.sidebar.radio("選択", ["ねこ", "いぬ", "てがみ"]) 
if page == "ねこ":
    show_page("にゃー")
elif page == "いぬ":
    show_page("わん")
elif page == "てがみ":
    show_page("！")