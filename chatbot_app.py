import openai
import streamlit as st

# Initialize OpenAI once an API key is entered
def initialize_openai(api_key):
    openai.api_key = api_key

# Fetch a response from GPT-3.5 Turbo model using the chat endpoint
def get_openai_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        return response['choices'][0]['message']['content']
    except Exception as e:
        return str(e)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.markdown("[View the source code](https://github.com/YourGitHub/YourRepoName)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://YourGitHubCodespaceLink)")

st.title("💬 PW Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a helpful assistant."}]

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    if role == "assistant":
        st.container().write("PW Chatbot: " + content)
    elif role == "user":
        st.container().write("You: " + content)

if openai_api_key:
    initialize_openai(openai_api_key)
    user_message = st.text_input("Enter your message:")
    
    if user_message:
        st.session_state.messages.append({"role": "user", "content": user_message})
        bot_response = get_openai_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
else:
    st.info("Please add your OpenAI API key in the sidebar.")
