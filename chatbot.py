import streamlit as st
import openai
import time
assistant_id = "asst_XxWDDUodJclsJxmd4iOqBe5O"
client = openai

##############INIT################
st.title('Annual weather Chatbot')
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

######################

openai.api_key = "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"

#starts the api chat
thread = client.beta.threads.create()
st.session_state.thread_id = thread.id

#prints messages
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
           st.markdown(message['message'])

#
if prompt := st.chat_input("Type in your question"):
    #st.chat_message("User").markdown(prompt)
    with st.chat_message("user"):
            st.markdown(prompt)
    st.session_state.chat_history.append({"role":"user","message":prompt})

    client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )
    
    with st.spinner('Generating your response...'):  
            run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            )

            while run.status != 'completed':
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id
                )

        # Retrieve messages added by the assistant
            response = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )  

            messages = response.data
            answer = messages[0].content[0].text.value
    with st.chat_message("ai"):
            st.markdown(answer)
    st.session_state.chat_history.append({"role":"ai","message":answer})