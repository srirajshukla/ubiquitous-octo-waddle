import streamlit as st

import pandas as pd
import numpy as np
import os
import time

import requests


def show():


    st.title('Report Generation')
    option = st.selectbox(
    'Year',
    ('2019', '2020', '2021', '2022', '2023'))

    # st.warning('This is a warning', icon="⚠️")
    
    # col1, col2 = st.columns([1,1])
    
    uploaded_file = st.file_uploader("Choose a PDF file", accept_multiple_files=False)
    # bytes_data = uploaded_file.read()
    if uploaded_file:
        st.write("filename:", uploaded_file.name)
    # st.write(bytes_data)
        
    if uploaded_file:
        alert = st.toast("Successfully Uploaded!", icon='✔️') # Display the alert
        time.sleep(3) # Wait for 3 seconds
        alert.empty() # Clear the alert
        # st.success("Successfully Uploaded")
        
    col1, col2, col3 = st.columns([1,1,1])
    
    with col2:
        st.button("Generate", type="primary")
        
    

    text_contents = '''This is some text'''
    
    with col2:
        st.download_button('Download', text_contents)
        
        
    # url = ''

    # x = requests.post(url, data = uploaded_files)

    # print(x.text)

        


    print(uploaded_file)
        
    # st.write(uploaded_files)
    
    
    
    css = '''
    <style>
        # [data-testid='stFileUploader'] {
        #     width: max-content;
        # }
        # [data-testid='stFileUploader'] section {
        #     padding: 0;
        #     float: left;
        # }
        # [data-testid='stFileUploader'] section > input + div {
        #     display: none;
        # }
        # [data-testid='stFileUploader'] section + div {
        #     float: right;
        #     padding-top: 0;
        # }
        [data-testid='stButton'] {
            justify-content: center;
            align-item: center;
            display: flex;
        }
        [data-testid='stDownloadButton'] {
            justify-content: center;
            align-item: center;
            display: flex;
        }
    </style>
    '''

    st.markdown(css, unsafe_allow_html=True)
        
    


