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
    API_BASE_PATH = os.environ.get("API_BASE_PATH")
    print(f"API_BASE_PATH={API_BASE_PATH}", flush=True)
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
    
    col1, col2, col3 = st.columns([1,1,1])

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
    
    with col2:
        upload = st.button('Upload', type="primary")
        
    if upload:
        response = requests.post(f'{API_BASE_PATH}/esgreports/upload', headers=headers, files=files, auth=("stanleyjobson", "swordfish"))
        # uploaded_files = []
        print(response.json())
        if len(uploaded_files) != 0 :
            alert = st.toast("Successfully Uploaded!", icon='✔️') # Display the alert
            time.sleep(3) # Wait for 3 seconds
            alert.empty() # Clear the alert
            # st.success("Successfully Uploaded")
    
        
    myObj = {
            "year": option,
        }
    
    with col2:
        upStatus = st.button('Upload Status')
    
    if upStatus:
        uploaded_files = []
        response = requests.post('http://localhost:8000/esgreports/retrieve', headers=headers, json=myObj, auth=("stanleyjobson", "swordfish"))
        st.write(response.json())
        print(response.json())
        
        
        
    # url = ''

    # x = requests.post(url, data = uploaded_files)

    # print(x.text)

        
    # st.write(len(uploaded_files))

    print(uploaded_files)
        
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
    


