import openai
import streamlit as st
import time

# Set the icon and title of the chatbot
icon_url = "https://drive.google.com/uc?export=view&id=1qaSJMQRCQxCTlL-obX0T2YsP64rZq5sq"
st.set_page_config(page_title="PW Chatbot", page_icon=icon_url)

# Introduce a typewriter effect to the chat
def typewriter_effect(text):
    container = st.empty()
    output_text = ""
    for char in text:
        time.sleep(0.05)
        output_text += char
        container.text(output_text)

# Sidebar
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    directive = st.text_input("Directive for Chatbot")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")

st.title("PW Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    if role == "assistant":
        typewriter_effect(content)
    else:
        st.chat_message(role).write(content)

if prompt := st.chat_input():
    if not openai_api_key:
        st.warning("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    if directive:  
        prompt = f"{directive}: {prompt}"
    response = openai.Completion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)  # fixed method name
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    typewriter_effect(msg["content"])
# ... [previous code]

if prompt := st.chat_input():
    if not openai_api_key:
        st.warning("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    if directive:  
        prompt = f"{directive}: {prompt}"
    
    try:
        response = openai.Completion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message
        st.session_state.messages.append(msg)
        typewriter_effect(msg["content"])
    except openai.error.AuthenticationError:
        st.error("There was an error authenticating with OpenAI. Please check your API key.")
    except openai.error.InvalidRequestError:
        st.error("There was an error with the API request. Please try again or check the request format.")
