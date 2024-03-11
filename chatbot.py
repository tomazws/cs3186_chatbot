import streamlit as st
import openai
import time

with st.chat_message('user'):
    st.write('Hello!')

openai.api_key = st.secrets['OPENAI_API_KEY']