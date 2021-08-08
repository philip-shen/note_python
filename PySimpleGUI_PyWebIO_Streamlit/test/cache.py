import time

import streamlit as st


@st.cache
def progress_cache(i):
    time.sleep(0.05)


def progress_no_cache(i):
    time.sleep(0.05)


def view_bar(func):
    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        func(i)


st.title('Cache example')
st.write('Starting a long computation with cache...')
view_bar(progress_cache)

st.write('Starting a long computation without cache...')
view_bar(progress_no_cache)

st.write('...and now we\'re done!')
