from openai import OpenAI
import streamlit as st
import re
import base64
import io
import prompts

################################################################################
##                           INITIALIZE APPLICATION                           ##
################################################################################
# Initialize OpenAI Assistant API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': prompts.get_instructions()}]

################################################################################
##                                 FUNCTIONS                                  ##
################################################################################
# Process the messsage and display it in the chat message container and also append message to chat history
def displayMessage(role, content):
    st.text(content)
    with st.chat_message(role):
        for item in content:
            if item['type'] == 'image_url':
                st.text(item['image_url'])
                #st.image(io.BytesIO(base64.b64decode(item['image_url'])))
            elif item['type'] == 'text':
                string_pos = 0
                for match in re.finditer('```dot[^}]*}\n```|digraph.*{[^}]*}', item['text']):
                    st.write(item['text'][string_pos: match.start() - 1])
                    st.text('------------')
                    st.text(match.group())
                    st.text('------------')
                    #st.graphviz_chart(match.group())
                    string_pos = match.end() + 1
                st.write(item['text'][string_pos:])
    st.write('')

def getCompletion():
    with st.spinner('Thinking ...'):
        try:
            response = client.chat.completions.create(
                model = 'gpt-4-vision-preview',
                max_tokens = 1024,
                messages = st.session_state.messages
            )
            content = [
                {
                    'type': 'text',
                    'text': response.choices[0].message.content
                }
            ]
            st.text(response.choices)
            displayMessage('assistant', content)
            st.session_state.messages.append({'role': 'assistant', 'content': content})
        except Exception as e:
            st.error(f'Error: {e}')

################################################################################
##                                  LAYOUTS                                   ##
################################################################################
# Create title and subheader for the Streamlit page
st.title('CS 3186 Student Assistant Chatbot')
st.subheader('Using OpenAI Completions API')

# Display chat messages
for message in st.session_state.messages[1:]:
    displayMessage(message['role'], message['content'])

with st.sidebar:
    st.write('Features')
    
if st.sidebar.button('Convert NFA to DFA'):
    content = [
        {
            'type': 'text',
            'text': 'I would like to convert NFA to DFA'
        }
    ]
    displayMessage('user', content)
    st.session_state.messages.append({'role': 'user', 'content': content})
    getCompletion()
    
if st.sidebar.button('Generate a DFA diagram'):
    content = [
        {
            'type': 'text',
            'text': 'I would like to generate a DFA from regular expression or langage'
        }
    ]
    displayMessage('user', content)
    st.session_state.messages.append({'role': 'user', 'content': content})
    getCompletion()

# File uploader
uploaded_image = st.sidebar.file_uploader('Upload an image', type=['png', 'jpg', 'jpeg', 'gif'])

# Chat input
if prompt := st.chat_input('Ask me anything about CS 3186'):
    content = []

    # If there are files uploaded
    if uploaded_image is not None:
        content.append({
            'type': 'image_url',
            'image_url': {
                'url': f'data:{uploaded_image.type};base64,{base64.b64encode(uploaded_image.getvalue()).decode("utf-8")}'
            }
        })

    # Display user message in chat message container and add to chat history
    content.append({
        'type': 'text',
        'text': prompt
    })
    displayMessage('user', content)
    st.session_state.messages.append({'role': 'user', 'content': content})
    getCompletion()