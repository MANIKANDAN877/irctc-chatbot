import streamlit as st
from google import genai

st.set_page_config(page_title="IRCTC Assistant", page_icon="🚆")
st.title("🚆 IRCTC Customer Service")

with open("irctc_document.txt.txt", "r", encoding="utf-8") as f:
    kb = f.read()

prompt = f"""
You are an IRCTC Customer Service Executive.
Answer user queries accurately and politely using ONLY the information
from the knowledge base below.
If the answer is not found in the knowledge base,
respond that the information is unavailable.
Knowledge Base:
{kb}
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("Ask your IRCTC question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    try:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": prompt}
        )
        response = chat.send_message(user_input)
        reply = response.text
    except Exception as e:
        reply = f"Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
