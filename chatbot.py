import prompts
import json
import streamlit as st
import graphviz
from openai import OpenAI

def createDiagram(dot_script):
    st.graphviz_chart('''
        digraph {
            run -> intr
            intr -> runbl
            runbl -> run
            run -> kernel
            kernel -> zombie
            kernel -> sleep
            kernel -> runmem
            sleep -> swap
            swap -> runswap
            runswap -> new
            runswap -> runmem
            new -> runmem
            sleep -> runmem
        }
    ''')

# Functions for OpenAI's function calling method
def call_function(function):
    if function.name == 'createDiagram':
        try:
            parsed_args = json.loads(function.arguments)
            st.write(parsed_args)
            createDiagram(parsed_args.dot_script)
        except Exception as e:
            st.write(e)
            return f'Function execution failed: {e}'
    return ''

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
        stream = client.chat.completions.create(
            model = st.session_state['openai_model'],
            messages = [
                {'role': m['role'], 'content': m['content']}
                for m in st.session_state.messages
            ],
            tools = prompts.get_tools(),
            stream = True
        )
        st.write(stream)
        #response = st.write_stream(stream)
    #st.session_state.messages.append({'role': 'assistant', 'content': response})




    # with st.chat_message('assistant'):
    #     response = client.chat.completions.create(
    #         model = st.session_state['openai_model'],
    #         messages = [
    #             {'role': m['role'], 'content': m['content']}
    #             for m in st.session_state.messages
    #         ],
    #         tools = prompts.get_tools(),
    #     )
    #     response = response.choices[0]
    #     if response.finish_reason == 'tool_calls':
    #         response = call_function(response.message.tool_calls[0].function)
    #     else:
    #         st.write(response.message.content)
    # st.session_state.messages.append({'role': 'assistant', 'content': response})


##### REGULAR RESPONSE
# Choice(
#     finish_reason='stop',
#     index=0,
#     logprobs=None,
#     message=ChatCompletionMessage(
#         content='Model's response',
#         role='assistant',
#         function_call=None,
#         tool_calls=None)
#     )

##### FUNCTION CALLING RESPONSE
# Choice(
#     finish_reason='tool_calls',
#     index=0,
#     logprobs=None,
#     message=ChatCompletionMessage(
#         content=None,
#         role='assistant',
#         function_call=None,
#         tool_calls=[
#             ChatCompletionMessageToolCall(
#                 id='call_FmckOxTq0rCsTGCEYWdrevLW',
#                 function=Function(
#                     arguments='asdfdsf',
#                     name='createDiagram'
#                 ),
#                 type='function'
#             )
#         ]
#     )
# )






