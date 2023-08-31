import openai
import streamlit as st

# Initialize OpenAI with the provided API key
def initialize_openai(api_key):
    openai.api_key = api_key

# Fetch a response from GPT-3.5 Turbo model using the chat endpoint
def get_openai_response(messages, directive=""):
    try:
        initial_message = {
            "role": "system",
            "content": directive
        } if directive else {
            "role": "user",
            "content": "You are a helpful assistant."
        }

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[initial_message, {"role": "user", "content": messages[-1]['content']}]
        )
        
        return response['choices'][0]['message']['content']
    except Exception as e:
        return str(e)

st.title("PW Chatbots")

# Sidebar for settings
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")
directive = st.sidebar.text_area("Enter Directive:")

# Initialize OpenAI if API key is present
if api_key:
    initialize_openai(api_key)

# Message management
messages = []

# Capture user input
user_input = st.text_input("You:")

if user_input:
    if api_key:  # Ensure API key is present
        messages.append({"role": "user", "content": user_input})
        bot_response = get_openai_response(messages, directive)
        messages.append({"role": "assistant", "content": bot_response})
        
        # Clear the user input box
        st.text_input("You:", value="", key="user_input")

# Display chat history
for message in messages:
    role = message["role"].capitalize()
    content = message["content"]
    st.write(f"{role}: {content}")

# Explanation in sidebar
st.sidebar.markdown("""
### How to use:
1. Enter your OpenAI API key in the sidebar.
2. (Optional) Provide a directive.
3. Type your message and hit enter to chat.
""")
