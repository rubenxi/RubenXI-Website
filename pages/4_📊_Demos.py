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
from google import genai
from google.genai import types
import json



st.set_page_config(
    layout="wide",
    page_title="RubenXI",
    page_icon="logo.png"
)

def tries_demos():
    st.session_state.tries_demos = st.session_state.tries_demos+1

def main():
    daily_questions = 10
    session_limit = 5
    date_file_demos = "date_file_demos.pkl"
    n_file_demos = "n_file_demos.pkl"
    st.sidebar.title("📊 Demo projects")
    st.sidebar.text("Here there are demos of some of my projects separated by tabs. You can click each tab to see the app and use it")
    news_tab, deepseek_tab, mbti_tab = st.tabs(["**News**", "**DeepSeek**", "**MBTI Test**"])
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

                if st.button("❓ About this project"):
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
                                                st.map(data, zoom=7, size=2000)

                                            with st.spinner("Loading map...", show_time=True):
                                                show_map()
                                else:
                                    break
    with deepseek_tab:

        api_key = st.secrets["api_key_d"]
        api_key_genai = st.secrets["api_key_genai"]

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
                        **This project is a chat written in Python that communicates with a HuggingFace model of DeepSeek (or some other ones) in the cloud or with Google Gemini. It uses the HuggingFace API and Gemini API to send the content of the message to the model online, getting then a response in stream format to output it to the chat.** 
                        
                        **You can choose a model with the menu "Model to use". The model will change and the new one will be used.**  
                        
                        **You can write a context for the AI that will be treated like the setup of the conversation, if you want to roleplay with a character this is where you write the description for it.**
                        
                        **The memory toggle will change between 2 processing modes:**   
                        - **Memory on: The AI will remember the conversation all along. It gets slower with time since parsing more context takes more resources. In this mode old messages will appear.**  
                        - **Memory off: The AI will answer every question like if it was the first message that was sent. In this mode the old messages disappear every time a new one is sent.**

                        ---

                        🚀 This project and many others can be found on my GitHub.           
                                    """)

            if st.button("❓ About this project", key="deep"):
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
                ("deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", "Qwen/Qwen2.5-72B-Instruct", "Qwen/Qwen2.5-Coder-32B-Instruct", "gemini-2.0-flash"), key = "model"
            )
        with col_c:
            context = st.text_area("Context for the conversation", max_chars=200)
            api_key_user = st.sidebar.text_input("🔑 Api key", placeholder="hf_...",
                                                 help="Set your own HuggingFace or Gemini api key. You can get one here: https://huggingface.co/settings/tokens/new?tokenType=read and here: https://aistudio.google.com/apikey")
        if "messages" not in st.session_state or not memory:
            st.session_state.messages = []

        def answer_question_server_simple_genai(question):
            client = genai.Client(api_key=api_key)

            with st.chat_message("assistant"):
                if context:
                    messages_stream = "context: " + context + " user: " + question + ", you: "
                else:
                    messages_stream = " user: " + question + ", you: "
                if memory:
                    messages = ""
                    for m in reversed(st.session_state.messages):
                        if m["role"] == "assistant":
                            messages += "you: " + m["content"]+", "
                        else:
                            messages += m["role"] + ": " + m["content"]+", "
                    if len(context) >= 1:
                        messages_stream = "context: " + context + "messages: " + messages + "you: "
                    else:
                        messages_stream = "messages: " + messages + "you: "

                stream = client.models.generate_content_stream(
                    model="gemini-2.0-flash",
                    config=types.GenerateContentConfig(
                        system_instruction="Answer the user."),
                    contents=messages_stream
                )
                for chunk in stream:
                    yield chunk.text

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
                if "tries_demos" not in st.session_state:
                    st.session_state.tries_demos = 1
                if len(question) > 300 or len(context) > 400 and not api_key_user:
                    st.chat_message("assistant", avatar="logo.png").write("⚠️ The question is too long ⚠️")
                elif st.session_state.tries_demos >= session_limit and not api_key_user:
                    st.chat_message("assistant", avatar="logo.png").write("⚠️ Too many messages, try again later ⚠️")
                else:
                    tries_demos()
                    if memory:
                        st.session_state.messages.insert(0, {"role": "user", "content": question})
                    else:
                        st.chat_message("user").write(question)
                    try:
                        with st.spinner("Thinking...", show_time=True):
                            if model == "gemini-2.0-flash":
                                if not api_key_user:
                                    api_key = st.secrets["api_key_genai"]
                                response = st.write_stream(answer_question_server_simple_genai(question))
                            else:
                                if not api_key_user:
                                    api_key = st.secrets["api_key_d"]
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
                            st.write("""**⚠️ Rate Limit ⚠️**
    
My website uses an api key that is free, so it may hit a limit at some point
    
Try again later...
                                            """)

    def load_questions():
        with open("questions.json", "r", encoding="utf-8") as f:
            return json.load(f)

    questions_data = load_questions()

    with mbti_tab:
        col1, col2, col3 = st.columns(3)
        mbti_emojis = {
            "ESTP": "🏎️",
            "ISTP": "🛠️",
            "ESFP": "🎉",
            "ISFP": "🎨",
            "ENTP": "🧠",
            "INTP": "🔬",
            "ENFP": "🌈",
            "INFP": "🦋",
            "ESTJ": "📋",
            "ISTJ": "📚",
            "ESFJ": "🤝",
            "ISFJ": "🧺",
            "ENTJ": "🏰",
            "INTJ": "♟️",
            "ENFJ": "🌟",
            "INFJ": "🔮"
        }

        mbti_functions_colors = {
            "Ni": "#6B4C9A",
            "Te": "#D62828",
            "Fe": "#D63384",
            "Se": "#FFD700",
            "Ne": "#2ECC71",
            "Ti": "#808080",
            "Si": "#87CEFA",
            "Fi": "#FFB6C1"
        }

        if "traits" not in st.session_state:
            st.session_state.traits = {
        "egoist": 0,
        "altruist": 0,
        "feeler": 0,
        "thinker": 0,
        "future_present": 0,
        "past_present": 0,
        "intuitive": 0,
        "sensor": 0
        }

        with col1:
            st.header("MBTI Test (WIP)")
        with col2:
            @st.dialog("Python MBTI Personality Test")
            def show_info():
                st.markdown("""\
                                    **This project consists of a Python test using data from a JSON object that processes user input to create a profile that shows the more approximate personality based on the 16 available.**

                                    ---

                                    🚀 This project and many others can be found on my GitHub.           
                                                """)

            if st.button("❓ About this project", key="mbti"):
                show_info()
        with col3:
            st.link_button("🚀 View on GitHub", "https://github.com/rubenxi/Python-MBTI-Personality-Test", type="primary")

        if "start" not in st.session_state:
            st.session_state.start = False
        if "balloons" not in st.session_state:
            st.session_state.balloons = False
        if "step" not in st.session_state:
            st.session_state.step = 0

        if not st.session_state.start:
            col_pic_mbti, col_desc_mbti = st.columns(2)
            with col_pic_mbti:
                st.image("mbti.png", width=600)

            with col_desc_mbti:
                st.markdown(f"""
**MBTI (Myers–Briggs Type Indicator) is a self-report questionnaire that uses pseudoscientific psychology knowledge to categorize individuals into 16 distinct personality types.**

There are 8 cognitive functions, each personality has 4, and the order they are used defines what specific personality a person is.

The functions are:

- <span style="color:{mbti_functions_colors["Se"]}">SE</span>: Extraverted Sensing
- <span style="color:{mbti_functions_colors["Ni"]}">NI</span>: Introverted Intuition
- <span style="color:{mbti_functions_colors["Si"]}">SI</span>: Introverted Sensing
- <span style="color:{mbti_functions_colors["Ne"]}">NE</span>: Extraverted Intuition
- <span style="color:{mbti_functions_colors["Ti"]}">TI</span>: Introverted Thinking
- <span style="color:{mbti_functions_colors["Fe"]}">FE</span>: Extraverted Feeling
- <span style="color:{mbti_functions_colors["Te"]}">TE</span>: Extraverted Thinking
- <span style="color:{mbti_functions_colors["Fi"]}">FI</span>: Introverted Feeling

                """,
                help="More information: https://www.16personalities.com", unsafe_allow_html=True
            )
            if st.button("📝 **Begin test**", type="primary"):
                st.session_state.start = True
                st.rerun()
            with st.expander("📊 **Personalities**"):
                markdown_personalities = f"""
### <span style="color:{mbti_functions_colors["Se"]}">{mbti_emojis["ESTP"]} ESTP</span> = <span style="color:{mbti_functions_colors["Se"]}">SE</span> <span style="color:{mbti_functions_colors["Ti"]}">TI</span> <span style="color:{mbti_functions_colors["Fe"]}">FE</span> <span style="color:{mbti_functions_colors["Ni"]}">NI</span> / <span style="color:{mbti_functions_colors["Si"]}">SI</span> <span style="color:{mbti_functions_colors["Te"]}">TE</span> <span style="color:{mbti_functions_colors["Fi"]}">FI</span> <span style="color:{mbti_functions_colors["Ne"]}">NE</span>

### <span style="color:{mbti_functions_colors["Ti"]}">{mbti_emojis["ISTP"]} ISTP</span> = <span style="color:{mbti_functions_colors["Ti"]}">TI</span> <span style="color:{mbti_functions_colors["Se"]}">SE</span> <span style="color:{mbti_functions_colors["Ni"]}">NI</span> <span style="color:{mbti_functions_colors["Fe"]}">FE</span> / <span style="color:{mbti_functions_colors["Te"]}">TE</span> <span style="color:{mbti_functions_colors["Si"]}">SI</span> <span style="color:{mbti_functions_colors["Ne"]}">NE</span> <span style="color:{mbti_functions_colors["Fi"]}">FI</span>

### <span style="color:{mbti_functions_colors["Fe"]}">{mbti_emojis["ENFJ"]} ENFJ</span> = <span style="color:{mbti_functions_colors["Fe"]}">FE</span> <span style="color:{mbti_functions_colors["Ni"]}">NI</span> <span style="color:{mbti_functions_colors["Se"]}">SE</span> <span style="color:{mbti_functions_colors["Ti"]}">TI</span> / <span style="color:{mbti_functions_colors["Fi"]}">FI</span> <span style="color:{mbti_functions_colors["Ne"]}">NE</span> <span style="color:{mbti_functions_colors["Si"]}">SI</span> <span style="color:{mbti_functions_colors["Te"]}">TE</span>

### <span style="color:{mbti_functions_colors["Ni"]}">{mbti_emojis["INFJ"]} INFJ</span> = <span style="color:{mbti_functions_colors["Ni"]}">NI</span> <span style="color:{mbti_functions_colors["Fe"]}">FE</span> <span style="color:{mbti_functions_colors["Ti"]}">TI</span> <span style="color:{mbti_functions_colors["Se"]}">SE</span> / <span style="color:{mbti_functions_colors["Ne"]}">NE</span> <span style="color:{mbti_functions_colors["Fi"]}">FI</span> <span style="color:{mbti_functions_colors["Te"]}">TE</span> <span style="color:{mbti_functions_colors["Si"]}">SI</span>

---

### <span style="color:{mbti_functions_colors["Se"]}">{mbti_emojis["ESFP"]} ESFP</span> = <span style="color:{mbti_functions_colors["Se"]}">SE</span> <span style="color:{mbti_functions_colors["Fi"]}">FI</span> <span style="color:{mbti_functions_colors["Te"]}">TE</span> <span style="color:{mbti_functions_colors["Ni"]}">NI</span> / <span style="color:{mbti_functions_colors["Si"]}">SI</span> <span style="color:{mbti_functions_colors["Fe"]}">FE</span> <span style="color:{mbti_functions_colors["Ti"]}">TI</span> <span style="color:{mbti_functions_colors["Ne"]}">NE</span>

### <span style="color:{mbti_functions_colors["Fi"]}">{mbti_emojis["ISFP"]} ISFP</span> = <span style="color:{mbti_functions_colors["Fi"]}">FI</span> <span style="color:{mbti_functions_colors["Se"]}">SE</span> <span style="color:{mbti_functions_colors["Ni"]}">NI</span> <span style="color:{mbti_functions_colors["Te"]}">TE</span> / <span style="color:{mbti_functions_colors["Fe"]}">FE</span> <span style="color:{mbti_functions_colors["Si"]}">SI</span> <span style="color:{mbti_functions_colors["Ne"]}">NE</span> <span style="color:{mbti_functions_colors["Ti"]}">TI</span>

### <span style="color:{mbti_functions_colors["Te"]}">{mbti_emojis["ENTJ"]} ENTJ</span> = <span style="color:{mbti_functions_colors["Te"]}">TE</span> <span style="color:{mbti_functions_colors["Ni"]}">NI</span> <span style="color:{mbti_functions_colors["Se"]}">SE</span> <span style="color:{mbti_functions_colors["Fi"]}">FI</span> / <span style="color:{mbti_functions_colors["Ti"]}">TI</span> <span style="color:{mbti_functions_colors["Ne"]}">NE</span> <span style="color:{mbti_functions_colors["Si"]}">SI</span> <span style="color:{mbti_functions_colors["Fe"]}">FE</span>

### <span style="color:{mbti_functions_colors["Ni"]}">{mbti_emojis["INTJ"]} INTJ</span> = <span style="color:{mbti_functions_colors["Ni"]}">NI</span> <span style="color:{mbti_functions_colors["Te"]}">TE</span> <span style="color:{mbti_functions_colors["Fi"]}">FI</span> <span style="color:{mbti_functions_colors["Se"]}">SE</span> / <span style="color:{mbti_functions_colors["Ne"]}">NE</span> <span style="color:{mbti_functions_colors["Ti"]}">TI</span> <span style="color:{mbti_functions_colors["Fe"]}">FE</span> <span style="color:{mbti_functions_colors["Si"]}">SI</span>

---

### <span style="color:{mbti_functions_colors["Te"]}">{mbti_emojis["ESTJ"]} ESTJ</span> = <span style="color:{mbti_functions_colors["Te"]}">TE</span> <span style="color:{mbti_functions_colors["Si"]}">SI</span> <span style="color:{mbti_functions_colors["Ne"]}">NE</span> <span style="color:{mbti_functions_colors["Fi"]}">FI</span> / <span style="color:{mbti_functions_colors["Ti"]}">TI</span> <span style="color:{mbti_functions_colors["Se"]}">SE</span> <span style="color:{mbti_functions_colors["Ni"]}">NI</span> <span style="color:{mbti_functions_colors["Fe"]}">FE</span>

### <span style="color:{mbti_functions_colors["Si"]}">{mbti_emojis["ISTJ"]} ISTJ</span> = <span style="color:{mbti_functions_colors["Si"]}">SI</span> <span style="color:{mbti_functions_colors["Te"]}">TE</span> <span style="color:{mbti_functions_colors["Fi"]}">FI</span> <span style="color:{mbti_functions_colors["Ne"]}">NE</span> / <span style="color:{mbti_functions_colors["Se"]}">SE</span> <span style="color:{mbti_functions_colors["Ti"]}">TI</span> <span style="color:{mbti_functions_colors["Fe"]}">FE</span> <span style="color:{mbti_functions_colors["Ni"]}">NI</span>

### <span style="color:{mbti_functions_colors["Ne"]}">{mbti_emojis["ENFP"]} ENFP</span> = <span style="color:{mbti_functions_colors["Ne"]}">NE</span> <span style="color:{mbti_functions_colors["Fi"]}">FI</span> <span style="color:{mbti_functions_colors["Te"]}">TE</span> <span style="color:{mbti_functions_colors["Si"]}">SI</span> / <span style="color:{mbti_functions_colors["Ni"]}">NI</span> <span style="color:{mbti_functions_colors["Fe"]}">FE</span> <span style="color:{mbti_functions_colors["Ti"]}">TI</span> <span style="color:{mbti_functions_colors["Se"]}">SE</span>

### <span style="color:{mbti_functions_colors["Fi"]}">{mbti_emojis["INFP"]} INFP</span> = <span style="color:{mbti_functions_colors["Fi"]}">FI</span> <span style="color:{mbti_functions_colors["Ne"]}">NE</span> <span style="color:{mbti_functions_colors["Si"]}">SI</span> <span style="color:{mbti_functions_colors["Te"]}">TE</span> / <span style="color:{mbti_functions_colors["Fe"]}">FE</span> <span style="color:{mbti_functions_colors["Ni"]}">NI</span> <span style="color:{mbti_functions_colors["Se"]}">SE</span> <span style="color:{mbti_functions_colors["Ti"]}">TI</span>

---

### <span style="color:{mbti_functions_colors["Fe"]}">{mbti_emojis["ESFJ"]} ESFJ</span> = <span style="color:{mbti_functions_colors["Fe"]}">FE</span> <span style="color:{mbti_functions_colors["Si"]}">SI</span> <span style="color:{mbti_functions_colors["Ne"]}">NE</span> <span style="color:{mbti_functions_colors["Ti"]}">TI</span> / <span style="color:{mbti_functions_colors["Fi"]}">FI</span> <span style="color:{mbti_functions_colors["Se"]}">SE</span> <span style="color:{mbti_functions_colors["Ni"]}">NI</span> <span style="color:{mbti_functions_colors["Te"]}">TE</span>

### <span style="color:{mbti_functions_colors["Si"]}">{mbti_emojis["ISFJ"]} ISFJ</span> = <span style="color:{mbti_functions_colors["Si"]}">SI</span> <span style="color:{mbti_functions_colors["Fe"]}">FE</span> <span style="color:{mbti_functions_colors["Ti"]}">TI</span> <span style="color:{mbti_functions_colors["Ne"]}">NE</span> / <span style="color:{mbti_functions_colors["Se"]}">SE</span> <span style="color:{mbti_functions_colors["Fi"]}">FI</span> <span style="color:{mbti_functions_colors["Te"]}">TE</span> <span style="color:{mbti_functions_colors["Ni"]}">NI</span>

### <span style="color:{mbti_functions_colors["Ne"]}">{mbti_emojis["ENTP"]} ENTP</span> = <span style="color:{mbti_functions_colors["Ne"]}">NE</span> <span style="color:{mbti_functions_colors["Ti"]}">TI</span> <span style="color:{mbti_functions_colors["Fe"]}">FE</span> <span style="color:{mbti_functions_colors["Si"]}">SI</span> / <span style="color:{mbti_functions_colors["Ni"]}">NI</span> <span style="color:{mbti_functions_colors["Te"]}">TE</span> <span style="color:{mbti_functions_colors["Fi"]}">FI</span> <span style="color:{mbti_functions_colors["Se"]}">SE</span>

### <span style="color:{mbti_functions_colors["Ti"]}">{mbti_emojis["INTP"]} INTP</span> = <span style="color:{mbti_functions_colors["Ti"]}">TI</span> <span style="color:{mbti_functions_colors["Ne"]}">NE</span> <span style="color:{mbti_functions_colors["Si"]}">SI</span> <span style="color:{mbti_functions_colors["Fe"]}">FE</span> / <span style="color:{mbti_functions_colors["Te"]}">TE</span> <span style="color:{mbti_functions_colors["Ni"]}">NI</span> <span style="color:{mbti_functions_colors["Se"]}">SE</span> <span style="color:{mbti_functions_colors["Fi"]}">FI</span>
"""
                st.markdown(markdown_personalities, unsafe_allow_html=True)
        else:
            questions = [q["question"] for q in questions_data]
            funcs_mbti_yes = [q["func_mbti_yes"] for q in questions_data]
            funcs_mbti_no = [q["func_mbti_no"] for q in questions_data]

            col_q_1, col_q_2 = st.columns(2)
            with col_q_1:
                if st.session_state.step <= len(questions) - 1:
                    st.markdown(questions[st.session_state.step], help="✅ " + funcs_mbti_yes[st.session_state.step] + " / " + "❌ " + funcs_mbti_no[st.session_state.step])
                    st.divider()
                    col_yes, col_no, col_aux_1, col_aux_2 = st.columns(4)
                    with col_yes:
                        if st.button("✅ Yes"):
                            st.session_state.traits[funcs_mbti_yes[st.session_state.step]] += 1
                            st.session_state.step += 1
                            if st.session_state.step > len(questions) - 1:
                                st.session_state.balloons=True
                            st.rerun()
                    with col_no:
                        if st.button("❌ No"):
                            st.session_state.traits[funcs_mbti_no[st.session_state.step]] += 1
                            st.session_state.step += 1
                            if st.session_state.step > len(questions) - 1:
                                st.session_state.balloons=True
                            st.rerun()
                else:
                    if st.session_state.balloons:
                        st.balloons()
                        st.session_state.balloons=False
                    decision = ""
                    perception = ""
                    if st.session_state.traits["egoist"] >= st.session_state.traits["altruist"]:
                        if st.session_state.traits["feeler"] >= st.session_state.traits["thinker"]:
                            decision = "Fi"
                        else:
                            decision = "Te"
                    else:
                        if st.session_state.traits["feeler"] >= st.session_state.traits["thinker"]:
                            decision = "Fe"
                        else:
                            decision = "Ti"
                    if st.session_state.traits["future_present"] >= st.session_state.traits[
                        "past_present"]:
                        if st.session_state.traits["intuitive"] >= st.session_state.traits["sensor"]:
                            perception = "Ni"
                        else:
                            perception = "Se"
                    else:
                        if st.session_state.traits["intuitive"] >= st.session_state.traits["sensor"]:
                            perception = "Ne"
                        else:
                            perception = "Si"
                    #WIP: Add filter to get final personality based on functions ordered. Also add shadow. Add spanish
                    st.markdown(f"""
                    
You have: <span style="color:{mbti_functions_colors[decision]}">{decision}</span> / <span style="color:{mbti_functions_colors[perception]}">{perception}</span> or shadow
                    
                    """, unsafe_allow_html=True)
                    st.markdown("Your personality is: A MISTERY (WIP)")


if __name__ == "__main__":
    main()
