# chatbot_app.py
import openai
import streamlit as st

# Initialize OpenAI once an API key is entered
def initialize_openai(api_key):
    openai.api_key = api_key

# Fetch response from GPT model
def get_openai_response(prompt_text, directive):
    prompt = directive + " " + prompt_text
    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt,
      max_tokens=150
    )
    return response.choices[0].text.strip()

st.title("OpenAI Chatbot")

# API Key Input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
if api_key:
    initialize_openai(api_key)

# Directive Input
directive = st.text_area("Enter your custom directive:")

# User Input
user_input = st.text_input("Ask the chatbot:")

if user_input and directive and api_key:
    # Fetch the chatbot's answer
    chatbot_response = get_openai_response(user_input, directive)
    st.write("Chatbot:", chatbot_response)

# Slider
st.sidebar.slider('Set a custom value:', 0, 100, 50)

st.sidebar.markdown("""
### Instructions
1. Enter your OpenAI API Key.
2. Add a custom directive.
3. Ask your question!
""")

