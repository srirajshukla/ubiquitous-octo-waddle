import streamlit as st
import file_upload, report, chatbot
# from streamlit.state.session_state import SessionState
from streamlit_option_menu import option_menu
import requests

from streamlit_local_storage import LocalStorage

# Main function
def main():
    
    
    # st.set_page_config(initial_sidebar_state="collapsed")
    
    # st.markdown(
    #         """
    #     <style>
    #         [data-testid="collapsedControl"] {
    #             display: none
    #         }
    #     </style>
    #     """,
    #         unsafe_allow_html=True,
    #     )

    with st.sidebar:
        comp = option_menu(
            menu_title = "Navigation",
            options = ["Home", "File Upload", "Report", "ChatBot"],
            icons=['house-check', 'file-earmark-arrow-up', 'file-arrow-down', "chat-left-dots"], 
            menu_icon="cast",
            default_index = 0
            # orientation = "horizontal"
        )
        
    logged_in = False
        
    print(comp)
    # print(st.sidebar())
        
    myobj = {}
    localS = LocalStorage()

    
    # def show():
    #     st.title("Login")
    #     user= st.text_input(
    #                             "UserName",
    #                             # "Enter Username",
    #                             key="placeholder",
    #                         )
    #     passwd = st.text_input("Password", type="password")
        
    #     creds = user + "," + passwd
        
        
    #     if st.button('Login'):
    #         # st.write('Why hello there')
    #         # url = 'http://localhost:8000/login'
        
    #         # res = requests.post(url, data = myobj)
    #         # print(res)
    #         localS.setItem("credential", creds)
            
        
    #     myobj = {
    #         'username': user,
    #         'password': passwd
    #     }
        
        
    ret_cred = localS.getItem("credential")
    if ret_cred :
        print(ret_cred['credential'])
        cred_data = ret_cred['credential'].split(',')
        # username = "so"
        # password = "as"
        # print(cred_data[0], cred_data[1])
        username = cred_data[0]
        password = cred_data[1]
        if 'username' not in st.session_state:
            st.session_state.username = username
        if 'password' not in st.session_state:
            st.session_state.password = password
        print("final",username, password)
        # password = localS.getItem('password')
    else:
        username = ''
        password = ''
    
    username = ''
    password = ''
    if 'username' in st.session_state:
        username = st.session_state.username
    if 'password' in st.session_state:
        password = st.session_state.password

    if comp == "Home" :
        if username == "Stanleyjobson" and password == "swordfish":
            home.show(username)
        else:
            # comp = "Home"
            ret_cred = ""
            login.show()
        
    elif comp == "File Upload":
        if username == "Stanleyjobson" and password == "swordfish":
            file_upload.show()
        else:
            # comp = "Home"
            ret_cred = ""
            login.show()
    elif comp == "Report":
        if username == "Stanleyjobson" and password == "swordfish":
            report.show()
        else:
            # comp = "Home"
            ret_cred = ""
            login.show()
    elif comp == "ChatBot":
        if username == "Stanleyjobson" and password == "swordfish":
            chatbot.show()
        else:
            # comp = "Home"
            ret_cred = ""
            login.show()
    else:
        show()
        

if __name__ == "__main__":
    main()
