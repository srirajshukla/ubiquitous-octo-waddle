import streamlit as st
from Components import file_upload, report, chatbot
# from streamlit.state.session_state import SessionState
from streamlit_option_menu import option_menu
import requests
from Components import login

from streamlit_local_storage import LocalStorage
import app


def show(username):
    localS = LocalStorage()
              
    ttl = st.title(f'Welcome {username} !!')
    # logout = st.button("Logout", type="primary")
    # if logout:
    #     localS.deleteAll()
    #     # st.rerun()
        
    #     login.show()
    #     # st.rerun()
        
        

