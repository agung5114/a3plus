import streamlit as st
import pandas as pd
import numpy as np
# import plotly_express as px
from PIL import Image
import streamlit.components.v1 as components
# import matplotlib.pyplot as plt
from tensorflow import keras
import joblib
import operator
import sys

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.applications.mobilenet import decode_predictions

from PIL import Image
sys.modules['Image'] = Image 
# [theme]
base="light"
primaryColor="purple"

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

model = keras.models.load_model('model/grabcv.h5')
food = ['beefburger','beefcurry','friedchicken','lambskewer','panacota','springsalad']

def getPrediction(data,model):
    img = Image.open(data)
    newsize = (224, 224)
    image = img.resize(newsize)
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    yhat = model.predict(image)
    label = yhat[0]
    prob = []
    for i in range(len(label)):
        # prob.append(i)
        prob.append(np.round(label[i]*100,2))
    data = {'Food': food, 'Prob': prob}
    # return data
    dfhasil = pd.DataFrame.from_dict(data)

    dfhasil['Probability'] = dfhasil.apply(lambda x: f"{x['Prob']}%", axis=1)
    top3 = dfhasil.nlargest(3, 'Prob')
    # top = dict(zip(food, prob))
    # top3 = dict(sorted(top.items(), key=operator.itemgetter(1), reverse=True)[:3])
    return top3

# st.set_page_config(layout='wide')

def main():
    st.subheader("Heal - Food Analyzer")
    with st.expander('Open Camera'):
        data1 = st.camera_input('')
    with st.expander('Upload A Photo'):
        data2 = st.file_uploader('')

    if data1 != None:
        data = data1
    elif data2 != None:
        data = data2
    else:
        data = None

    if data == None:
        st.write('Please Upload Photo of Food')
    else:
        img = Image.open(data)
        newsize = (280, 230)
        image = img.resize(newsize)
        st.image(image)

#     if st.button('Jalankan Prediksi'):
        hasil = getPrediction(data,model)
        hasil = hasil[['Food','Probability']]
        hasil.set_index('Food', inplace=True)
        st.table(hasil)
        # st.write(f'prediction: {hasil}')
        st.write(hasil.index[0].upper())



        

if __name__=='__main__':
    main()
