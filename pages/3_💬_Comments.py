import streamlit as st
import pickle
import os

st.set_page_config(
    layout="wide",
    page_title="RubenXI",
    page_icon="logo.png"
)

data_file = "chat_history.pkl"

def load_chat_history():
    if os.path.exists(data_file):
        with open(data_file, "rb") as f:
            return pickle.load(f)
    return []


def save_chat_history(messages):
    with open(data_file, "wb") as f:
        pickle.dump(messages, f)


def main():
    st.sidebar.title("💬 Leave a comment!")
    st.sidebar.text("You can write as many comments as you want, it's anonymous!")

    if "messages" not in st.session_state:
        st.session_state["messages"] = load_chat_history()

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your comment...")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        save_chat_history(st.session_state["messages"])

        with st.chat_message("user"):
            st.markdown(user_input)

        save_chat_history(st.session_state["messages"])

if __name__ == "__main__":
    main()
