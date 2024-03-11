import streamlit as st
from openai import OpenAI

st.title('CS 3186 Student Assistant Chatbot')

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if 'openai_model' not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('Ask me anything about CS 3186'):
    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    response = f'Echo: {prompt}'

    # Display assistant response in chat message container
    with st.chat_message('assistant'):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({'role': 'assistant', 'content': response})


