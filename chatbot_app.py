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
            engine="gpt-3.5-turbo",  
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

st.title("PW Chatbots")

# Sidebar for settings
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")
directive = st.sidebar.text_area("Enter Directive:")

# Initialize OpenAI if API key is present
if api_key:
    initialize_openai(api_key)

# Manage user and bot messages
user_messages = []
bot_messages = []

# Capture user input
user_input = st.text_input("You:")

if user_input:
    if api_key:  # Ensure API key is present
        # Save user message and get bot response
        user_messages.append(user_input)
        bot_response = get_openai_response(user_input, directive)
        bot_messages.append(bot_response)
        
        # Clear the user input box
        st.text_input("You:", value="", key="user_input")

# Display chat history
for user_msg, bot_msg in zip(user_messages, bot_messages):
    st.write(f"You: {user_msg}")
    st.write(f"Chatbot: {bot_msg}")

# Explanation in sidebar
st.sidebar.markdown("""
### How to use:
1. Enter your OpenAI API key in the sidebar.
2. (Optional) Provide a directive.
3. Type your message and hit enter to chat.
""")
