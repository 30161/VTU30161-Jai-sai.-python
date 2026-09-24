```python
import streamlit as st
from openai import OpenAI

# 1. Setup the Page Layout and Title
st.set_page_config(
    page_title="Advanced AI Assistant",
    page_icon="🚀",
    layout="wide"
)

# 2. Sidebar Configuration Controls
st.sidebar.title("⚙️ Configuration")

# Securely handle the API Key
openai_api_key = st.sidebar.text_input(
    "Enter OpenAI API Key",
    type="password"
)

# Model Selection Dropdown
selected_model = st.sidebar.selectbox(
    "Choose AI Model",
    ["gpt-4o-mini", "gpt-4o"],
    index=0,
    help="gpt-4o-mini is faster and cheaper. gpt-4o is more capable for complex tasks."
)

# Temperature Slider
temperature = st.sidebar.slider(
    "Creativity (Temperature)",
    min_value=0.0,
    max_value=1.5,
    value=0.7,
    step=0.1,
    help="Lower values are more focused. Higher values are more creative."
)

# 3. App Title
st.title("🚀 Advanced Personal AI Assistant")

col1, col2 = st.columns([6, 1])

with col1:
    st.caption(
        "An upgraded AI chatbot featuring context settings, "
        "conversation exports, and history resets."
    )

# Initialize the OpenAI Client
client = None

if openai_api_key:
    client = OpenAI(api_key=openai_api_key)

# 4. Initialize Conversation History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful, clever, and friendly AI chat assistant."
            )
        }
    ]

# Clear Chat History
with col2:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful, clever, and friendly AI chat assistant."
                )
            }
        ]
        st.rerun()

# 5. Display Existing Chat Messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Stop if API key is missing
if not openai_api_key:
    st.info(
        "Please add your OpenAI API key in the sidebar to get started.",
        icon="🗝️"
    )
    st.stop()

# 6. Handle New User Input
if user_query := st.chat_input("Ask me anything..."):

    # Add user message to history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)

    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model=selected_model,
                messages=[
                    {
                        "role": m["role"],
                        "content": m["content"]
                    }
                    for m in st.session_state.messages
                ],
                temperature=temperature,
                stream=True,
            )

            for chunk in stream:
                if (
                    chunk.choices
                    and chunk.choices[0].delta.content
                ):
                    content = chunk.choices[0].delta.content
                    full_response += content

                    message_placeholder.markdown(
                        full_response + "▌"
                    )

            message_placeholder.markdown(full_response)

            # Save assistant response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response
```
