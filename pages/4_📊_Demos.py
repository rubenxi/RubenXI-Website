import streamlit as st
import pickle
import os
import streamlit.components.v1 as components
from utils import show_options
from utils import get_coords
from utils import get_news
import pandas as pd
import re
from huggingface_hub import InferenceClient
from utils import save_n
from utils import save_date
from utils import load_n
from utils import load_date
from datetime import datetime

st.set_page_config(
    layout="wide",
    page_title="RubenXI",
    page_icon="logo.png"
)

def tries():
    st.session_state.tries = st.session_state.tries+1

def main():
    daily_questions = 10
    session_limit = 5
    date_file_demos = "date_file_demos.pkl"
    n_file_demos = "n_file_demos.pkl"
    st.sidebar.title("📊 Demo projects")
    st.sidebar.text("Here there are demos of some of my projects separated by tabs. You can click each tab to see the app and use it")
    news_tab, deepseek_tab = st.tabs(["**News**", "**DeepSeek**"])
    options_name_link = show_options()
    names = []
    for element in options_name_link:
        names.append(element[1])
    with news_tab:
        if names is not None:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.header("Latest World News")
            with col2:
                @st.dialog("Python News")
                def show_info():
                    st.markdown("""\
                            **This project consists of a Python script that, using web scraping, accesses the Liveuamap website to collect the most recent news from the site. To do this, it first gathers all the available country or open conflict options on the website. By combining the links to these pages with certain parameters, it obtains the link to the news page for that specific topic. After that, it collects all the news articles one by one, along with their publication time and description, as well as a link to each article for further information. I created this Python script to learn how to use web scraping and to become more familiar with Python.**

                            ---

                            🚀 This project and many others can be found on my GitHub.           
                                        """)

                if st.button("❓ About this project  "):
                    show_info()
            with col3:
                st.link_button("🚀 View on GitHub", "https://github.com/rubenxi/newsPython", type="primary")
            option = st.selectbox("**Choose a country or conflict**", names)
            if option is None:
                option = names[0]
            code = names.index(option)
            with st.spinner("Retrieving information...", show_time=True):
                news = get_news(code, options_name_link)
            if news is not None:
                for j in range(len(news)):
                        cols = st.columns(3)
                        for i in range(len(cols)):
                            col = cols[i]
                            with col:
                                if j * 3 + i < len(news):
                                    with st.container(border=True):
                                        st.link_button("**" + news[j * 3 + i][0] + "**\n\n" + news[j * 3 + i][1], news[j * 3 + i][2])
                                        if st.button("🗺️ See in map", key="map_"+news[j * 3 + i][2], type="tertiary"):
                                            @st.dialog(option + " Map")
                                            def show_map():
                                                lat, lon = get_coords(news[j * 3 + i][2])
                                                data = pd.DataFrame({
                                                    'latitude': [lat],
                                                    'longitude': [lon]
                                                })
                                                st.map(data, zoom=6, size=8000)

                                            with st.spinner("Loading map...", show_time=True):
                                                show_map()
                                else:
                                    break
    with deepseek_tab:

        api_key = st.secrets["api_key_d"]

        model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B" #Models: https://huggingface.co/playground
        template_server = """
        
        System: Answer the user.

        """
        col4, col5, col6 = st.columns(3)
        with col4:
            st.header("DeepSeek Chat")
        with col5:
            @st.dialog("DeepSeek Chat")
            def show_info():
                st.markdown("""\
                        **This project is a chat written in Python that communicates with a HuggingFace model of DeepSeek (or some other ones) in the cloud. It uses the HuggingFace API to send the content of the message to the model online, getting then a response in stream format to output it to the chat.** 
                        
                        **You can choose a model with the menu "Model to use". The model will change and the new one will be used.**  
                        
                        **You can write a context for the AI that will be treated like the setup of the conversation, if you want to roleplay with a character this is where you write the description for it.**
                        
                        **The memory toggle will change between 2 processing modes:**   
                        - **Memory on: The AI will remember the conversation all along. It gets slower with time since parsing more context takes more resources. In this mode old messages will appear.**  
                        - **Memory off: The AI will answer every question like if it was the first message that was sent. In this mode the old messages disappear every time a new one is sent.**

                        ---

                        🚀 This project and many others can be found on my GitHub.           
                                    """)

            if st.button("❓ About this project  ", key="deep"):
                show_info()
        with col6:
            st.link_button("🚀 View on GitHub", "https://github.com/rubenxi/deepseek-web-chat", type="primary")

        question = st.chat_input("Write a message...", max_chars=100)
        col_m, col_c = st.columns(2)
        with col_m:
            col_m1, col_m2 = st.columns(2)
            with col_m2:
                memory = st.toggle("Memory", value=True)
            with col_m1:
                if memory:
                    st.markdown("**Note: New messages appear on top**")
                else:
                    st.markdown("") 
            model = st.selectbox(
                "Model to use",
                ("deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", "Qwen/Qwen2.5-72B-Instruct", "Qwen/Qwen2.5-Coder-32B-Instruct"), key = "model"
            )
        with col_c:
            context = st.text_area("Context for the conversation", max_chars=200)
            api_key_user = st.sidebar.text_input("🔑 Api key", placeholder="hf_...",
                                                 help="Set your own HuggingFace api key. You can get one here: https://huggingface.co/settings/tokens/new?tokenType=read")
        if "messages" not in st.session_state or not memory:
            st.session_state.messages = []

        def answer_question_server_simple(question):
            client = InferenceClient(api_key=api_key)

            with st.chat_message("assistant"):
                messages_stream = [{"role": "user", "content": template_server + " context: " + context + " user: " + question}]
                if memory:
                    if len(context) >= 1:
                        messages_stream = [
                                              {"role": "user", "content": template_server}
                                          ] + [
                                              {"role": "user", "content": "context: " + context}
                                          ] + [
                                              {"role": m["role"], "content": m["content"]} for m in
                                              reversed(st.session_state.messages)
                                          ]
                    else:
                        messages_stream = [
                                              {"role": "user", "content": template_server}
                                          ] + [
                                              {"role": m["role"], "content": m["content"]} for m in
                                              reversed(st.session_state.messages)
                                          ]

                stream = client.chat.completions.create(
                    model=model,
                    messages=messages_stream,
                    temperature=0.5,
                    max_tokens=2048,
                    top_p=0.7,
                    stream=True
                )
                ended_thinking = False
                thinking = ""
                for chunk in stream:
                    if ended_thinking or model != "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B":
                        yield chunk.choices[0].delta.content
                    else:
                        thinking += chunk.choices[0].delta.content
                    if "</think" in chunk.choices[0].delta.content:
                        ended_thinking = True
                if len(thinking) >= 1:
                    with st.expander("See thinking"):
                        st.markdown(thinking.replace('</think>', ''))

        if question:
            current_date = datetime.today().strftime('%Y-%m-%d')
            last_date = load_date(date_file_demos)
            if current_date != last_date:
                save_date(current_date, date_file_demos)
                save_n(0, n_file_demos)
            if api_key_user:
                api_key = api_key_user
            elif load_n(n_file_demos) <= daily_questions:
                api_key = st.secrets["api_key_d"]
            else:
                st.chat_message("assistant").write("""**⚠️ Rate Limit ⚠️**

My website uses an api key that is free, so it may hit a limit at some point

Try again tomorrow or use your own api key...
                                            """)
            if api_key_user or (not api_key_user and load_n(n_file_demos) <= daily_questions):
                if "tries" not in st.session_state:
                    st.session_state.tries = 1
                if len(question) > 300 or len(context) > 400:
                    st.chat_message("assistant", avatar="logo.png").write("⚠️ The question is too long ⚠️")
                elif st.session_state.tries >= session_limit:
                    st.chat_message("assistant", avatar="logo.png").write("⚠️ Too many messages, try again later ⚠️")
                else:
                    tries()
                    if memory:
                        st.session_state.messages.insert(0, {"role": "user", "content": question})
                    else:
                        st.chat_message("user").write(question)
                    try:
                        with st.spinner("Thinking...", show_time=True):
                            response = st.write_stream(answer_question_server_simple(question))
                            save_n(load_n(n_file_demos) + 1, n_file_demos)
                        for message in st.session_state.messages:
                            with st.chat_message(message["role"]):
                                st.markdown(message["content"])
                        if memory:
                            st.session_state.messages.insert(0, {"role": "assistant", "content": response})
                    except Exception as e:
                        if api_key_user:
                            st.write("""**⚠️ Rate Limit ⚠️**

Your api key has been rate limited or you set an incorrect api key
                                                                        """)
                        else:
                            print("----api: "+api_key+" | error: "+ str(e))

                            st.write("""**⚠️ Rate Limit ⚠️**
    
My website uses an api key that is free, so it may hit a limit at some point
    
Try again later...
                                            """)
if __name__ == "__main__":
    main()
