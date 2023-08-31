from pathlib import Path
from random import randrange
import time
import openai
import streamlit as st
from utils.styles.menu_styles import FOOTER_STYLES, HEADER_STYLES
from utils.conversation import get_user_input, show_chat_buttons, show_conversation
from utils.footer import show_donates, show_info
from utils.helpers import get_files_in_dir, get_random_img
from utils.lang import en, ru
from streamlit_option_menu import option_menu

# --- PATH SETTINGS ---
current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
assets_dir: Path = current_dir / "assets"
icons_dir: Path = assets_dir / "icons"
img_dir: Path = assets_dir / "img"
tg_svg: Path = icons_dir / "tg.svg"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "AI Talks"
PAGE_ICON: str = "🤖"
LANG_EN: str = "En"
LANG_RU: str = "Ru"
AI_MODEL_OPTIONS: list[str] = ["gpt-3.5-turbo"]

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# Storing The Context
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

openai.api_key = st.sidebar.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

def typewriter_effect(message):
    for char in message:
        st.write(char, end='', use_container_width=True)
        st.markdown("", unsafe_allow_html=True)  # Force a rerun and display the character
        time.sleep(0.05)

def main():
    if openai.api_key:
        user_input = st.text_input("You: ")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            # AI Response
            response = openai.Completion.create(
                model="gpt-3.5-turbo",
                prompt=f"You: {user_input}\nPW Chatbot:",
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7
            )
            chatbot_response = response.choices[0].text.strip()
            st.session_state.messages.append({"role": "assistant", "content": chatbot_response})

            # Display the chat history
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.write(f"You: {msg['content']}")
                else:
                    st.write(f"PW Chatbot: {msg['content']}")

    else:
        st.warning("Please provide your OpenAI API Key to interact with PW Chatbot.")

if __name__ == "__main__":
    main()
