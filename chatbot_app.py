import openai
import streamlit as st
import time

# Initialize OpenAI once an API key is entered
def initialize_openai(api_key):
    openai.api_key = api_key

# Fetch response from GPT-3.5 Turbo model
def get_openai_response(prompt_text, directive=""):
    prompt = directive + " " + prompt_text
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use GPT-3.5 Turbo model
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# Typewriter effect
def typewriter(text):
    for char in text:
        st.write(char, end='', key='chat_output')
        time.sleep(0.05)

st.title("PW Chatbots")

# Sidebar
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")
directive = st.sidebar.text_area("Enter Directive:")

# Initialize OpenAI if API key is present
if api_key:
    initialize_openai(api_key)

# Chat UI
user_input = st.text_input("You:")

if user_input:
    if api_key:  # Ensure API key is present
        # Fetch chatbot response
        chatbot_response = get_openai_response(user_input, directive)
        # Display using typewriter effect
        typewriter("Chatbot: " + chatbot_response)
    else:
        st.write("Please enter OpenAI API key in the sidebar.")

# Explanation in sidebar
st.sidebar.markdown("""
### How to use:
1. Enter your OpenAI API key in the sidebar.
2. (Optional) Provide a directive.
3. Type your message and hit enter to chat.
""")
