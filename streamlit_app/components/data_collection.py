import streamlit as st
import requests
import json
import re

def data_collection():
    ''' data collection menu page'''
    tab1, tab2 = st.tabs(["View Topics", "Load New Topic"])
    
    with tab1:
      st.subheader("A tab with a chart")
    
    with tab2:
      st.subheader("A tab with the data")