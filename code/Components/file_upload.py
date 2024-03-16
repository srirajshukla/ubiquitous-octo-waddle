import streamlit as st

import pandas as pd
import numpy as np
import os
import time

import requests


def show():


    st.title('ESG Survey')
    option = st.selectbox(
    'Year',
    ('2019', '2020', '2021', '2022', '2023'))

    # st.warning('This is a warning', icon="⚠️")

    uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        # bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        # st.write(bytes_data)
        
    if len(uploaded_files) != 0 :
        alert = st.toast("Successfully Uploaded!", icon='✔️') # Display the alert
        time.sleep(3) # Wait for 3 seconds
        alert.empty() # Clear the alert
        # st.success("Successfully Uploaded")
        
        
    # url = ''

    # x = requests.post(url, data = uploaded_files)

    # print(x.text)

        
    # st.write(len(uploaded_files))

    print(uploaded_files)
        
    # st.write(uploaded_files)
    


