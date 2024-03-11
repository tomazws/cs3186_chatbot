import prompts
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
    st.session_state.messages = [{'role': 'system', 'content': prompts.get_instructions()}]

# Display chat messages from history on app rerun (Skipping 1st element - system message)
for message in st.session_state.messages[1:]:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('Ask me anything about CS 3186'):
    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # Display assistant response in chat message container
    with st.chat_message('assistant'):
        response = client.chat.completions.create(
            model = st.session_state['openai_model'],
            messages = [
                {'role': m['role'], 'content': m['content']}
                for m in st.session_state.messages
            ],
            tools = prompts.get_tools(),
            #stream = True,
        )
        if response[0].finish_reason == 'tool_calls':
            st.write(response[0])
            #st.write(call_function(messages, response[0]))
        else:
            st.write(response[0]['content'])
    #st.session_state.messages.append({'role': 'assistant', 'content': response})

# Functions for OpenAI's function calling method
def createDiagram(dot_script):
    return 'Yes yes yall'





'''
    with st.chat_message('assistant'):
        stream = client.chat.completions.create(
            model = st.session_state['openai_model'],
            messages = [
                {'role': m['role'], 'content': m['content']}
                for m in st.session_state.messages
            ],
            tools = prompts.get_tools(),
            #stream = True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
'''