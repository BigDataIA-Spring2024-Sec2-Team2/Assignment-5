import streamlit as st
from components.login_signup import menu_login
from components.navigation import tabs


if "auth_status" not in st.session_state:
  st.session_state.auth_status = False

if not st.session_state["auth_status"]:
  st.set_page_config(page_title='Streamlit App', page_icon='🤧')
  menu_login()
else:
  st.set_page_config(page_title='Streamlit App', page_icon='🤧', layout="wide")
  tabs()
