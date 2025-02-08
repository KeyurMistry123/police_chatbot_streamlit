import os
import json

import streamlit as st
from groq import Groq


# Updated streamlit page configuration for public safety theme with new colors
st.set_page_config(
    page_title="Public Safety Chatbot",
    page_icon="🚔",
    layout="centered"
)

# Custom CSS to improve the aesthetics and ensure visibility
st.markdown("""
<style>
    body {
        background-color: #1e1e2f;  /* Dark background for better contrast */
        color: #ffffff;  /* White text for readability */
    }
    .stApp {
        background-color: #1e1e2f;
        color: #ffffff;
    }
    .chat-message {
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        background-color: #2a2a40;  /* Slightly lighter than the background for visibility */
        border: 2px solid #4a69bd;  /* Blue border for aesthetic */
    }
    .chat-message.user {
        background-color: #4a69bd;  /* Blue background for user messages */
        color: #ffffff;  /* White text for readability */
    }
    .chat-message.assistant {
        background-color: #6a89cc;  /* Lighter blue for assistant messages */
        color: #ffffff;  /* White text for readability */
    }
    button {
        background-color: #4a69bd;  /* Blue buttons */
        color: #ffffff;  /* White text for readability */
    }
</style>
""", unsafe_allow_html=True)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

# save the api key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# initialize the chat history as streamlit session state of not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Updated streamlit page title for public safety
st.title("🚔 Public Safety Chatbot")

# Icon button for going back to home
if st.button("🏠", key="back_home"):
    st.experimental_rerun()  # Placeholder for redirection, update with actual navigation logic

# New description section for chatbot features
st.markdown("""
#### Welcome to the Public Safety Chatbot
This chatbot is designed to provide you with important safety and awareness information. It is a multilingual platform, so feel free to ask questions in your preferred language. Here are some questions you might ask:
- "List some safety tips."
- "List new police initiatives that I need to be aware of."
Feel free to explore and ask other questions related to public safety!
""")

# Hardcoded safety and awareness tips
st.markdown("""
### Safety and Awareness Tips
- **Tip 1:** Always be aware of your surroundings.
- **Tip 2:** Do not share personal information with strangers.
- **Tip 3:** Report any suspicious activity to the police immediately.
- **Tip 4:** Keep emergency numbers saved in your phone.
- **Tip 5:** Follow the local laws and regulations for your safety.
""")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message:
user_prompt = st.chat_input("Ask for safety tips...")

if user_prompt:

    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # sens user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)