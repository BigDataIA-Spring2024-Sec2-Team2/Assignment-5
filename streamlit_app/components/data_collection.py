import streamlit as st
import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('./configuration.properties')
base_url = config['APIs']['base_url_service']

def data_collection():
  ''' data collection menu page '''
  tab1, tab2 = st.tabs(["View Topics", "Load New Topic"])
  
  with tab1:
    show_data()
  with tab2:
    st.subheader("A tab with the data")
      
def show_data():
  url = base_url + '/collection/topics'
  access_token = st.session_state["access_token"]
  token_type = st.session_state["token_type"]
  # Making the POST request
  headers = {
    "Authorization": "{} {}".format(token_type, access_token),
    'Content-Type': 'application/json',
  }
  response = requests.get(url, headers=headers)
  topic = tuple([""])
  if response.status_code == 200:
    topic += tuple(response.json()["topics"])
  else: 
    st.error("Invalid Credential")
    
  if topic == (""):
    st.write("No Topics found")
  else:
    option = st.selectbox(
      'Select A Topic',
      topic
    )
    if option:
      get_markdown(option)


def get_markdown(topic):
  url = base_url + '/collection/markdown'
  access_token = st.session_state["access_token"]
  token_type = st.session_state["token_type"]
  # Making the POST request
  headers = {
    "Authorization": "{} {}".format(token_type, access_token),
    'Content-Type': 'application/json',
  }
  body = {
    "topic": topic
  }
  response = requests.get(url, headers=headers, json=body)
  learnings = tuple([""])
  learnings_map = {}
  if response.status_code == 200:
    learnings_map = response.json()["markdown"]
    learnings += tuple(response.json()["markdown"].keys())
  else: 
    st.error("Invalid Credential")
  if learnings == (""):
    st.write("No Topics found")
  else:
    learning = st.selectbox(
      'Select A LOS',
      learnings
    )
    bt_2 = st.button("Load Summary")
    if bt_2:
      st.markdown(learnings_map[learning])