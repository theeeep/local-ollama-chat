import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage


def app_session_state_init():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            AIMessage("Hello! How can I help you today?")
        ]

    chat_history = st.session_state["chat_history"]

    for history in chat_history:
        if isinstance(history, AIMessage):
            st.chat_message("assistant").write(history.content)
        else:
            st.chat_message("user").write(history.content)


def app():
    st.set_page_config(
        page_title="AI Chatbot",
        page_icon=":blue[robot]",
        layout="centered",
    )
    st.image("https://ollama.com/public/ollama.png", width=100)
    st.header(":blue[Chat] with :blue[Ollama] :dolphin:")
    llm = ChatOllama(model="llama3.2:latest", temperature=0.7)

    app_session_state_init()

    user_input = st.chat_input("You: ")

    if user_input:
        st.chat_message("user").write(user_input)
        st.session_state["chat_history"] += [HumanMessage(content=user_input)]
        response = llm.stream(user_input)

        with st.chat_message("assistant"):
            ai_message = st.write_stream(response)

        st.session_state["chat_history"] += [AIMessage(content=ai_message)]


if __name__ == "__main__":
    app()
