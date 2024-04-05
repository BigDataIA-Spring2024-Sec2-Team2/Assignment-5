import streamlit as st
from streamlit_option_menu import option_menu

def tabs():
  options = ["Data Collection", "Question Generation", "Context Answer", "Knowledge Answer", "Account"]
  icons = ['cloud-upload-fill','clipboard-data-fill', 'gear-fill', 'person-fill', 'person-fill', 'person-fill'] 


  login_menu = option_menu(None, options, 
    icons=icons, 
    menu_icon="cast", 
    key='nav_menu',
    default_index=0, 
    orientation="horizontal"
  )

  login_menu

  if st.session_state["nav_menu"] == "Data Collection" or st.session_state["nav_menu"] == None:
    st.write("1")
  elif st.session_state["nav_menu"] == "Question Generation":
    st.write("2")
  elif st.session_state["nav_menu"] == "Context Answer":
    st.write("3")
  elif st.session_state["nav_menu"] == "Knowledge Answer":
    st.write("4")
  elif st.session_state["nav_menu"] == "Account":
    st.write("5")