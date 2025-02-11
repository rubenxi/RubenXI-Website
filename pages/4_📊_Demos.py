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

st.set_page_config(
    layout="wide",
    page_title="RubenXI",
    page_icon="logo.png"
)

def main():
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

        api_key = st.secrets["api_key"]

        template_server = """
        Answer the user.

        Context: {context}
        User said: 
        """

        def answer_question_server_simple(question):
            client = InferenceClient(api_key=api_key)

            messages = [
                {"role": "user", "content": template_server + question}
            ]

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
                    messages=messages,
                    temperature=0.5,
                    max_tokens=2048,
                    top_p=0.7,
                    stream=True
                )
                ended_thinking = False
                for chunk in stream:
                    if ended_thinking:
                        yield chunk.choices[0].delta.content
                    if "</think" in chunk.choices[0].delta.content:
                        ended_thinking = True

        question = st.chat_input("Question")

        if question:
            st.chat_message("user").write(question)
            with st.spinner("Thinking...", show_time=True):
                response = st.write_stream(answer_question_server_simple(question))


if __name__ == "__main__":
    main()
