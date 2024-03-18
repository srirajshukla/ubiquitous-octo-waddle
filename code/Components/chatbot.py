import streamlit as st
import random
import time
import requests
import os


# Streamed response emulator
def response_generator(result):
    response = result
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
        
def metadata_generator(result):
    metadata = result
    yield metadata 
            

def show():
    API_BASE_PATH = os.environ.get("API_BASE_PATH")
    # st.title("Simple chat")
    option = st.selectbox(
    'Year',
    ('2019', '2020', '2021', '2022', '2023'))

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    
    
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            
        headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}
        
        myObj = {
            "reportYear": option,
            "inputQuestion": prompt,
        }
        
        res = requests.post(f'{API_BASE_PATH}/questionnaire/generatefirstdraft/generateAnswer', headers=headers, json = myObj, auth=("stanleyjobson", "swordfish"))
        #print(res.json())
        try:
            result = res.json()['questionnaireSummary']['response']['result']
            
            metadata = res.json()['questionnaireSummary']['response']['source_documents']
            for meta in metadata:
                print(meta['metadata'])
        except:
            result = "No data available for this year"
            metadata = ""

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(result))
            for meta in metadata:
                metadata = st.write_stream(metadata_generator(meta['metadata']))
                
        # chat_history = response + '\n' + metadata
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        if metadata:
            st.session_state.messages.append({"role": "assistant", "content": metadata})
        
        
