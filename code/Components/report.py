import streamlit as st

import pandas as pd
import numpy as np
import os
import time
from io import BytesIO, BufferedReader

import requests
import json

taskid = ''

def show():

    API_BASE_PATH = os.environ.get("API_BASE_PATH")
    st.title('Report Generation')
    option = st.selectbox(
    'Year',
    ('2019', '2020', '2021', '2022', '2023'))



    # st.warning('This is a warning', icon="⚠️")
    
    # col1, col2 = st.columns([1,1])
    files = ()
    
    uploaded_file = st.file_uploader("Choose a PDF file", type = "pdf", accept_multiple_files=False)
    # bytes_data = uploaded_file.read()
    if uploaded_file:
        bytes_data = uploaded_file.read()
        f_handle = BytesIO()
        f_handle.write(bytes_data)
        f_handle.seek(0)
        br = BufferedReader(f_handle)
        data = (uploaded_file.name, br, 'application/pdf')
        files = ("documentName", (uploaded_file.name, br, 'application/pdf'))
        
        st.write("filename:", uploaded_file.name)
    # st.write(bytes_data)
        
    # if uploaded_file:
    #     alert = st.toast("Successfully Uploaded!", icon='✔️') # Display the alert
    #     time.sleep(3) # Wait for 3 seconds
    #     alert.empty() # Clear the alert
    #     # st.success("Successfully Uploaded")
        
    col1, col2, col3 = st.columns([1,1,1])
    
    headers = {
        'accept': 'application/json',
        # 'Content-Type': 'multipart/form-data',
    }
    
    myObj = {
            "generateReportForYear": option,
            "userId": "Stanleyjobson"
            }
    download_disable = True
    with col2:
        if st.button("Generate", type="primary"):
            response = requests.post(f'{API_BASE_PATH}/questionnaire/generatefirstdraft/pdf',
                                     headers=headers,
                                     files={
                                    'SurveyQuestionnaireDocumentName': data,
                                    'documentType': (None, 'PDF'),
                                    'metadata': (None, json.dumps(myObj))},
                                     auth=("stanleyjobson", "swordfish"))
            uploaded_files = []
            print(response.text)
            taskid = response.json().get('taskid', '')
            if "task_id" not in st.session_state:
                st.session_state.task_id = taskid
            else:
                st.session_state.task_id = taskid
            st.write(taskid)
            if taskid != '':
                download_disable = False
            if len(uploaded_files) != 0 :
                alert = st.toast("Successfully Uploaded!", icon='✔️') # Display the alert
                time.sleep(3) # Wait for 3 seconds
                alert.empty() # Clear the alert
                # st.success("Successfully Uploaded")
        
    

    text_contents = '''This is some text'''
    with col2:
        if st.button('Download'):
            taskid = st.session_state.task_id
            url_path = f'{API_BASE_PATH}/questionnaire/generatefirstdraft/pdf/{option}/{taskid}/status'
            st.write(url_path)
            response = requests.get(url_path,
                            headers={'accept': 'application/json',},
                            auth=("stanleyjobson", "swordfish"))

            try:
                out = response.json()
                st.write(out)
                if out.get('status') == "DONE":
                    response = requests.get(f'{API_BASE_PATH}/firstdraftreport/download/result/{option}',
                                headers={'accept': 'application/json',},
                                auth=("stanleyjobson", "swordfish"))
                    print(response.json())
                    st.write(response.json().get("documents")[0].get("metadata").get("referenceLink"))
                else:
                    st.write("File Not yet ready")
                    download_disable=False
            except Exception:
                print("exception")
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
        
    


