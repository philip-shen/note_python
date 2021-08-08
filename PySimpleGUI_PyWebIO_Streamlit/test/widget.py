from PIL import Image
import io 

import streamlit as st
import numpy as np

def main():
    st.title('My first app')

    # checkbox
    checkbox_state = st.checkbox('Show text')

    if checkbox_state:
        st.write('checkbox enable')

    # button
    button_state = st.button('Say hello')
    if button_state:
        st.write('Why hello there')
    else:
        st.write('Goodbye')

    # selectbox
    option = st.selectbox(
        'select box:',
        [1, 2, 3]
    )

    st.write('You selected: ', option)

    # inputbox
    title = st.text_input('inputbox', 'おはよう')
    st.write('inputbox:', title)

    # slider
    age = st.slider('How old are you?', 0, 130, 25)
    st.write("I'm ", age, 'years old')

    # file upload
    uploaded_file = st.file_uploader('Choose a image file')

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        st.image(
            image, caption='upload images',
            use_column_width=True
        )


if __name__ == '__main__':
    main()