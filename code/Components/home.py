import streamlit as st
import file_upload, report, chatbot
# from streamlit.state.session_state import SessionState
from streamlit_option_menu import option_menu
import requests
import login

from streamlit_local_storage import LocalStorage
import app
import time


def show(username):
    localS = LocalStorage()
              
    ttl = st.title(f'Welcome {username} !!')
    # logout = st.button("Logout", type="primary")
    # if logout:
    #     localS.deleteAll()
    #     time.sleep(3)
    #     css = '''
    # <style>
        # [data-testid='stButton'] {
            
        #     display: none;
        # }
        # [data-testid='login'] {
        #     display: none;
        # }
    # </style>
    # '''

    #     st.markdown(css, unsafe_allow_html=True)
    #     login.show()
    #     # st.rerun()
        
        

