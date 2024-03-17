import streamlit as st
from Components import home, file_upload, report, chatbot
# from streamlit.server.server import Server
# from streamlit.state.session_state import SessionState
from streamlit_option_menu import option_menu
import requests

from streamlit_local_storage import LocalStorage

localSt = LocalStorage()


def show():
    # st.rerun()
    # Server.get_current()._reloader.reload()
    st.title("Login")
    user= st.text_input(
                                "UserName",
                                # "Enter Username",
                                key="placeholder",
                            )
    passwd = st.text_input("Password", type="password")
        
    creds = user + "," + passwd
        
        
    if st.button('Login'):
            # st.write('Why hello there')
            # url = 'http://localhost:8000/login'
        
            # res = requests.post(url, data = myobj)
            # print(res)
        localSt.setItem("credential", creds)
        if 'username' not in st.session_state:
            st.session_state.username = user
        if 'password' not in st.session_state:
            st.session_state.password = passwd
        
            
        
    myobj = {
            'username': user,
            'password': passwd
        }