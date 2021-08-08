import streamlit as st

st.title("Streamlit")
st.text_input("ねるねるねるねる", "は")
st.text("ねれば")
st.checkbox("ねるほど")
st.selectbox("色が", ("変わって",))
smile = st.slider("",  min_value=1, max_value=10, value=3)
if smile != -1:
    st.error("ひっ" * smile)
st.text_area("こうやって", value="つ\nけ\nて")
st.radio("うまい！", ("うまい！", "うまい！", "うまい！"))