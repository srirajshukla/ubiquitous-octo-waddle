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
    from io import BytesIO, BufferedReader
    files = []
    urls = []
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        f_handle = BytesIO()
        f_handle.write(bytes_data)
        f_handle.seek(0)
        br = BufferedReader(f_handle)
        files.append(('documentName', (uploaded_file.name, br, 'application/pdf')))
        urls.append(uploaded_file.name)
        st.write("filename:", uploaded_file.name)
        # st.write(bytes_data)

    import requests

    headers = {
        'accept': 'application/json',
        # 'Content-Type': 'multipart/form-data',
    }

    files.append(('DocumentURL', (None, ','.join(urls))))
    files.append(('year', (None, option)))

    # files = {
    #     'documentName': ('Survey-Questionnire-Part1.pdf', open('Survey-Questionnire-Part1.pdf', 'rb'), 'application/pdf'),
    #     'DocumentURL': (None, 'ok'),
    #     'year': (None, '2023'),
    # }

    response = requests.post('http://localhost:8000/esgreports/upload', headers=headers, files=files, auth=("stanleyjobson", "swordfish"))
    print(response.json())
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
    


