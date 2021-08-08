from PIL import Image
import json
import os

import streamlit as st
import pandas as pd
import numpy as np

from keras.preprocessing import image
from keras.applications.xception import Xception, preprocess_input, decode_predictions

st.set_option('deprecation.showfileUploaderEncoding', False)


@st.cache(allow_output_mutation=True)
def load_model():
    """
    Xceptionモデルをloadする。
    """

    model = Xception(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000)

    return model


def preprocessing_image(image_pil_array: 'PIL.Image'):
    """
    予測するためにPIL.Imageで読み込んだarrayを加工する。
    299×299にして、pixelを正規化

    cf: https://keras.io/ja/applications/#xception
    """

    image_pil_array = image_pil_array.convert('RGB')
    x = image.img_to_array(image_pil_array)
    x = np.expand_dims(x, axis=0)
    print(x.shape)
    x = preprocess_input(x)
    print(x.shape)

    return x


def main():
    model = load_model()

    st.title('画像分類器')

    st.write("pretrained modelを使って、アップロードした画像を分類します。")

    uploaded_file = st.file_uploader('Choose a image file to predict')

    if uploaded_file is not None:
        image_pil_array = Image.open(uploaded_file)
        st.image(
            image_pil_array, caption='uploaded image',
            use_column_width=True
        )

        x = preprocessing_image(image_pil_array)
        result = model.predict(x)

        predict_rank = decode_predictions(result, top=5)[0]
        st.write('機械学習モデルは画像を', predict_rank[0][1], 'と予測しました。')

        st.write('#### 予測確率@p5')
        df = pd.DataFrame(predict_rank, columns=['index', 'name', 'predict_proba'])
        st.write(df)
        df_chart = df[['name', 'predict_proba']].set_index('name')
        st.bar_chart(df_chart)


if __name__ == '__main__':
    main()
