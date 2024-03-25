import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with AI!",
    page_icon=" :speech_balloon:",  # Favicon emoji
    layout="wide",  # Page layout option
    initial_sidebar_state="collapsed"  # Collapse sidebar initially
)

# Set dark theme as default
dark_theme = """
<style>
:root {
  --primary-color: #000000;
  --secondary-color: #1c1c1c;
  --text-color: #ffffff;
}

[data-testid="stAppViewContainer"] {
  background-color: var(--primary-color);
  color: var(--text-color);
}

[data-testid="stMarkdownContainer"] {
  background-color: var(--secondary-color);
  padding: 1rem;
  border-radius: 0.5rem;
}

[data-testid="stChatMessageElement"] {
  background-color: var(--secondary-color);
  padding: 1rem;
  border-radius: 0.5rem;
}
</style>
"""
st.markdown(dark_theme, unsafe_allow_html=True)

# Set background image
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://images.unsplash.com/photo-1542831371-29b0f74f9713?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80");
background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Header
st.markdown("""
<div style='background-color: var(--secondary-color); padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
    <h1 style='text-align: center; color: var(--text-color);'>💬 Large Language Model <br> ChatBot <br> ~ Aarav Nigam</h1>
</div>
""", unsafe_allow_html=True)

# Container for chat history
chat_container = st.container()

# Display the chat history
for message in st.session_state.chat_session.history:
    with chat_container.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("What's in your mind....?", key="input")
if user_prompt:
    # Add user's message to chat and display it
    with chat_container.chat_message("user"):
        st.markdown(user_prompt)

    # Show a loading spinner while waiting for the response
    with st.spinner("Let me think....."):
        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with chat_container.chat_message("assistant"):
        st.markdown(gemini_response.text)


