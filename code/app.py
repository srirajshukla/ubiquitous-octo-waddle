import streamlit as st
from Components import file_upload, report, chatbot
# from streamlit.state.session_state import SessionState
from streamlit_option_menu import option_menu

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
            options = ["File Upload", "Report", "ChatBot"],
            icons=['file-earmark-arrow-up', 'file-arrow-down', "chat-left-dots"], 
            menu_icon="cast",
            default_index = 0
            # orientation = "horizontal"
        )

    if comp == "File Upload":
        file_upload.show()
    elif comp == "Report":
        report.show()
    elif comp == "ChatBot":
        chatbot.show()

if __name__ == "__main__":
    main()
