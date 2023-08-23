import databutton as db
import streamlit as st
import openai
import os
import time
from embedchain import App

# This is the yellow title
st.markdown(
    """
    <h1 style="color: #FDE443; text-align: center; font-size: 40px; font-weight: bold; text-shadow: 2px 2px 4px #000000;">EvolutioGPT</h1>
    """,
    unsafe_allow_html=True,
)

# Initiating OpenAI API Key
openai.api_key = db.secrets.get("OPENAI_API_KEY")
if not openai.api_key:  # Ask for key if we don't have one
    with st.chat_message("assistant"):
        st.write(
            """
        Hi there. You haven't provided me with an OpenAI API key that I can use. 
        Please provide a key in the box below so we can start chatting:
        """
        )
        api_key = st.text_input("Please type in your API key", type="password")
        if api_key:
            db.secrets.put("OPENAI_API_KEY", api_key)
            st.experimental_rerun()
        st.stop()


# Initiating the Embedchain Bot
@st.cache_resource
def botadd(URL):
    databutton_bot = App()
    databutton_bot.add("web_page", URL)
    return databutton_bot

if "btn_state" not in st.session_state:
    st.session_state.btn_state = False

URL_TO_EMBED = st.text_input("Enter a URL")

btn = st.button("Initialize Bot")

if btn or st.session_state.btn_state:
    st.session_state.btn_state = True
    databutton_bot = botadd(URL_TO_EMBED)
    st.success("Bot Initiated!")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = databutton_bot.query(prompt)
    
    # Simulate stream of response with milliseconds delay
    for chunk in assistant_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "... ")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
else:
    st.info("Initiate a bot first!")
