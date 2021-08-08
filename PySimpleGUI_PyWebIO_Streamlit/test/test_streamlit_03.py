import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.title("Streamlit")
st.text("サインいっこいれる")
fig = plt.figure()
xs = np.linspace(0, np.pi*4, 500)
plt.plot(xs, np.sin(xs))
st.pyplot(fig)