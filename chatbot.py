import prompts
import json
import streamlit as st
import graphviz
from openai import OpenAI

def createDiagram(dot_script):
   # st.markdown(dot_script)
    st.graphviz_chart(dot_script)

# Functions for OpenAI's function calling method
def call_function(function):
    if function.name == 'createDiagram':
        try:
            parsed_args = json.loads(function.arguments)
            createDiagram(parsed_args['dot_script'])
            st.session_state.messages.append(
                {
                    'role': 'assistant',
                    'content': parsed_args['dot_script']
                }   
            )
        except Exception as e:
            st.write(e)
    else:  
        st.session_state.messages.append(
            {
                'role': 'assistant',
                'content': 'N/A'
            }
        )
    ## Add if statemnt to check function name before
    ## Will need to save the content as the parsed_args for function role 
    

st.title('CS 3186 Student Assistant Chatbot')

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
#client = OpenAI(api_key="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")

# Set a default model
if 'openai_model' not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': prompts.get_instructions()}]

# Display chat messages from history on app rerun (Skipping 1st element - system message)
for message in st.session_state.messages[1:]:
    with st.chat_message(message['role']):
        st.markdown(message['content'][:7])
        st.write(message['content'])
        # if(message['content'] == 'function'):
        #     st.graphviz_chart(message['content'])
        # else:
        #     st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('Ask me anything about CS 3186'):
    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # Display assistant response in chat message container
    with st.spinner('Hold on,..'):
        with st.chat_message('assistant'):
            response = client.chat.completions.create(
                model = st.session_state['openai_model'],
                messages = [
                    {'role': m['role'], 'content': m['content']}
                    for m in st.session_state.messages
                ],
                tools = prompts.get_tools(),
            )
            response = response.choices[0]
            if response.finish_reason == 'tool_calls':
                call_function(response.message.tool_calls[0].function)
            else:
                st.write(response.message.content)
                st.session_state.messages.append({'role': 'assistant', 'content': response.message.content})