import streamlit as st
from streamlit_option_menu import option_menu
from components.data_collection import data_collection
from components.question_data import questions

def tabs():
  options = ["Collection", "Question", "Answer", "Knowledge"]
  icons = ['cloud-upload-fill','clipboard-data-fill', 'gear-fill', 'person-fill', 'person-fill'] 

  login_menu = option_menu(None, options, 
    icons=icons, 
    menu_icon="cast", 
    key='nav_menu',
    default_index=0, 
    orientation="horizontal"
  )

  login_menu

  if st.session_state["nav_menu"] == "Collection" or st.session_state["nav_menu"] == None:
    data_collection()
  elif st.session_state["nav_menu"] == "Question":
    questions()
  elif st.session_state["nav_menu"] == "Answer":
    st.write("3")
  elif st.session_state["nav_menu"] == "Knowledge":
    st.write("4")
  elif st.session_state["nav_menu"] == "Account":
    st.write("5")