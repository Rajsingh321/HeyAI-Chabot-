import os
import streamlit as st
from google import genai
import webbrowser
import time  # Added for delay during thinking stage

# ————— Session State Initialization —————
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'clear_input' not in st.session_state:
    st.session_state.clear_input = False
if 'is_thinking' not in st.session_state:
    st.session_state.is_thinking = False  # New flag to manage thinking state


# ————— AI Reply and Command Functions —————
def aireply(command):
    """Generate a response from the AI model."""
    client = genai.Client(api_key="AIzaSyDRIj0sAHmZdQIw2bipPxCfdmeNbfsaJdA")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=command)
        if response and response.text:
            reply = response.text.strip()
            if len(reply) > 50000:
                reply = reply[:50000] + "..."
            return reply
        else:
            return "Sorry, I got no response from the model."
    except Exception as e:
        return f"Error: {e}\nSorry, I couldn't process your request."

def introduce():
    """Return the AI's introduction."""
    return "I'm HeyAI, created by Raj and the Shree.ai team to assist and provide helpful answers."

def open_google():
    """Open Google in a new Chrome tab."""
    webbrowser.register(
        'chrome', None,
        webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe")
    )
    webbrowser.get('chrome').open_new_tab('https://www.google.com')
    return "Opening Google..."

def search(query):
    """Search Google for the given query."""
    webbrowser.register(
        'chrome', None,
        webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe")
    )
    webbrowser.get('chrome').open_new_tab(f'https://www.google.com/search?q={query}')
    return f"Searching Google for \"{query}\"..."

def open_youtube():
    """Open YouTube in a new Chrome tab."""
    webbrowser.register(
        'chrome', None,
        webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe")
    )
    webbrowser.get('chrome').open_new_tab('https://www.youtube.com')
    return "Opening YouTube..."

def open_gmail():
    """Open Gmail in a new Chrome tab."""
    webbrowser.register(
        'chrome', None,
        webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe")
    )
    webbrowser.get('chrome').open_new_tab('https://mail.google.com')
    return "Opening Gmail..."

def open_webside(url):
    """Open a specified URL in a new Chrome tab."""
    webbrowser.register(
        'chrome', None,
        webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe")
    )
    webbrowser.get('chrome').open_new_tab(url)
    return f"Opening {url}..."

def process_command(command):
    """Process user commands and return appropriate responses."""
    cmd = command.lower()
    if "open google" in cmd:
        return open_google()
    elif "your name" in cmd or "who are you" in cmd:
        return introduce()
    elif "raj" in cmd:
        return "Raj is my creator — a student of Data Science and an AI developer. 🧠💻"
    elif "search" in cmd:
        return search(command.replace("search", "").strip())
    elif "open youtube" in cmd:
        return open_youtube()
    elif "open gmail" in cmd:
        return open_gmail()
    elif cmd.startswith("open "):
        return open_webside(command.replace("open", "").strip())
    else:
        return aireply(command.strip())

# ————— Helper Functions for Chat —————
def add_message(role, text):
    """Add a message to the chat history."""
    st.session_state.chat_history.append({"role": role, "text": text})

# ————— Initial Greeting Message —————
if len(st.session_state.chat_history) == 0:
    add_message("assistant", "Hello! 👋 How can I help you today?")


# ————— Page Header —————
st.markdown("<h1 style='text-align: center;'>HeyAI! 👋</h1>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; color:#444; font-size:30px; font-weight:1000;'>Chat with your AI assistant</div>",
    unsafe_allow_html=True
)
# ————— Render Chat History —————
for msg in st.session_state.chat_history:
    bubble_color = "#f0f2f6" if msg["role"] == "user" else "#d1e7dd"
    justify = "flex-end" if msg["role"] == "user" else "flex-start"
    text_align = "right" if msg["role"] == "user" else "left"
    st.markdown(
        f"""
        <div style="display:flex; justify-content:{justify}; margin:10px 0;">
          <div style="
            background-color: {bubble_color};
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 60%;
            text-align: {text_align};
          ">
            {msg["text"]}
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ————— Fixed Footer Input Styling —————
st.markdown("""
    <style>
      .stTextInput {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
      }
      .stButton {
        position: fixed;
        bottom: 20px;
        left: 82%;
        transform: translateX(-50%);
        width: 100px;
      }
    </style>
""", unsafe_allow_html=True)

# ————— Clear Input Logic —————
if st.session_state.clear_input:
    st.session_state.input_text = ""
    st.session_state.clear_input = False

# ————— Input and Button Layout —————
col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_input("Enter prompt", key="input_text")
with col2:
    send = st.button("Send", disabled=st.session_state.is_thinking)  # Disable if thinking

# ————— Process Input on Send —————
if send and user_input.strip():
    add_message("user", user_input)
    st.session_state.is_thinking = True  # Start thinking

    # Add "thinking..." temporary response
    add_message("assistant", "🤔 Thinking...")

    # Rerun to display "thinking..." first
    st.rerun()

# ————— Replace "thinking..." with actual response —————
if (
    len(st.session_state.chat_history) >= 2 and
    st.session_state.chat_history[-1]["role"] == "assistant" and
    st.session_state.chat_history[-1]["text"] == "🤔 Thinking..."
):
    time.sleep(1)  # Optional delay to simulate thinking
    last_user_input = st.session_state.chat_history[-2]["text"]
    response = process_command(last_user_input)
    st.session_state.chat_history[-1] = {"role": "assistant", "text": response}
    st.session_state.clear_input = True
    st.session_state.is_thinking = False  # Done thinking
    st.rerun()
