import streamlit as st
import requests

# Configure Streamlit page
st.set_page_config(
    page_title="Brutus AI Chat",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for UI Enhancements
st.markdown("""
    <style>
        .stApp {
            background-color: #1e1e1e;
        }
        .chat-header {
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            color: white;
            margin-bottom: 5px;
        }
        .chat-subtitle {
            text-align: center;
            font-size: 1rem;
            color: #bbbbbb;
            margin-bottom: 20px;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding: 15px;
            background-color: transparent;
            border-radius: 10px;
            overflow-y: auto;
            max-height: 60vh;
        }
        .user-message {
            text-align: right;
            background-color: #007bff;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            width: fit-content;
            max-width: 75%;
            align-self: flex-end;
        }
        .bot-message {
            text-align: left;
            background-color: #2c2c2c;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            width: fit-content;
            max-width: 75%;
            align-self: flex-start;
        }
        .footer {
            text-align: center;
            font-size: 0.85rem;
            color: #bbbbbb;
            margin-top: 5px;
        }
        .footer a {
            color: #ff4757;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        .input-container {
            display: flex;
            justify-content: center;
            position: fixed;
            bottom: 10px;
            left: 0;
            width: 100%;
            padding: 10px;
            background: #1e1e1e;
        }
        .stTextInput > div > div > input {
            width: 50% !important;  /* Makes the text box smaller */
            text-align: left;       /* Keeps user input left-aligned */
            padding: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Store last message to prevent re-triggering on rerun
if "last_message" not in st.session_state:
    st.session_state.last_message = ""

# **Display Title & Subtitle**
st.markdown('<div class="chat-header">🤖 Brutus AI</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle">Hi, I\'m Brutus, your AI assistant. Let\'s chat!</div>', unsafe_allow_html=True)

# Chat messages container
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role_class = "user-message" if msg["sender"] == "User" else "bot-message"
        st.markdown(f'<div class="{role_class}">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# **User Input Field (Centered Box, Left-Aligned Text)**
with st.container():
    user_input = st.text_input(
        "Type your message and press Enter",
        key="user_message_input",  # Using a different key to prevent modification error
        placeholder="Enter your message...",
        label_visibility="collapsed"
    )

# Handle user input (Prevents duplicate message submission)
if user_input and user_input != st.session_state.last_message:
    st.session_state.last_message = user_input  # Store last user input to prevent loop

    # Append user message to history
    st.session_state.messages.append({"sender": "User", "content": user_input})

    # Fetch AI response
    with st.spinner("Brutus is thinking..."):
        try:
            response = requests.post("http://127.0.0.1:5000/chat", json={"message": user_input})
            if response.status_code == 200:
                ai_response = response.json().get("response", "No response from server.")
            else:
                ai_response = f"Server error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            ai_response = f"Error connecting to server: {str(e)}"

    # Append AI response to history
    st.session_state.messages.append({"sender": "Bot", "content": ai_response})

    # **Force UI to refresh**
    st.rerun()

# **Footer**
st.markdown(
    '<div class="footer">Brutus can make mistakes. <a href="https://example.com" target="_blank">Check important info.</a></div>',
    unsafe_allow_html=True
)
