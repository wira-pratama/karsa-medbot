import streamlit as st
from privateGPT import privateGPT

st.set_page_config(
    page_title="Chat",
    page_icon="👋",
)

st.sidebar.info("Setup you Karsa Bot here.")

st.title("Karsa Chat")
st.write("Hospital first, private, customer centric, medical administration chatbot")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.status("Running..."):
            full_response = privateGPT(st.session_state.messages[0]["content"])
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
