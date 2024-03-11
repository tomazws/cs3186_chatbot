import streamlit as st
import openai
import time

openai.api_key = st.secrets['OPENAI_API_KEY']

prompt = st.chat_input('Ask me anything about CS 3186')
if prompt:
    st.write(f'/user has sent the following prompt: {prompt}')