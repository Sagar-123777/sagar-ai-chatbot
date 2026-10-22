import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Sagar AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 Sagar AI Chatbot")
st.caption("Your personal AI assistant")

# Keep your API key private in Streamlit Secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    client = None

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    if client is None:
        st.error("API key not configured yet. Please set GROQ_API_KEY in Streamlit Secrets.")
    else:
        try:
            with st.chat_message("assistant"):
                with st.spinner("AI is thinking..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=st.session_state.messages
                    )
                    answer = response.choices[0].message.content
                    st.write(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
        except Exception as e:
            st.error(f"AI request failed: {e}")