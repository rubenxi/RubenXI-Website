import time
import streamlit as st
from streamlit import container, button, exception, session_state
from utils import get_repos_github
import streamlit.components.v1 as components
from huggingface_hub import InferenceClient
from utils import save_n
from utils import save_date
from utils import load_n
from utils import load_date
from datetime import datetime
from google import genai
from google.genai import types

st.set_page_config(
    layout="wide",
    page_title="RubenXI",
    page_icon="logo.png"
)

def hide_menus():
    hide_streamlit_style = """
                <style>
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def tries():
    st.session_state.tries = st.session_state.tries + 1


def main():
    api_keys = []
    i = 1
    day = datetime.today().day
    while True:
        key_name = f"api_key_{i}"
        if key_name in st.secrets and i % 2 == 0 and day % 2 == 0:
            api_keys.append(st.secrets[key_name])
            i += 1
        elif key_name in st.secrets and i % 2 != 0 and day % 2 != 0:
            api_keys.append(st.secrets[key_name])
            i += 1
        elif key_name in st.secrets:
            i += 1
        else:
            break
    api_key_genai = st.secrets["api_key_genai"]
    api_key_user = None
    
    date_file = "date_file.pkl"
    n_file = "n_file.pkl"
    daily_questions = 15
    daily_questions_genai = 500
    session_limit = 5
    session_limit_genai = 50
    col1, col2 = st.columns(2)

    with col1:
        st.image("logo.png")
    with col2:
        st.title("RubenXI")
        intro_md = """\
        **I'm a multidisciplinary Software Engineer aiming to be a DevOps**  
        """

        abilities_md = """\
        💻 **Software development**

        🐧 **Linux**

        🧠 **AI** 

        🔓 **Open source**

        🎮 **Videogames**     

        🔥 **And more...**
    """
        st.markdown(intro_md)
        col3, col4 = st.columns(2)

        @st.dialog("What's mozmail?")
        def show_info():
            st.info("""\
            **@mozmail is the domain used by Firefox Relay, a Mozilla service that helps protect your privacy by masking your real email address. Emails sent to this address are securely forwarded to my personal inbox, reducing spam and phishing risks.**

            ---

            Since this website is public, I use it to avoid bot spam or any other problem.           
                        """)

        with col3:
            st.link_button("📧 **Send me an email**", "mailto: hg5l8ssre@mozmail.com", type="primary")
        with col4:
            if st.button("❓"):
                show_info()

        col_info, col_ex = st.columns(2)
        with col_info:
            st.info(abilities_md)
    st.divider()
    st.header("My GitHub repositories")
    with st.spinner("Retrieving information...", show_time=True):
        repos = get_repos_github()
        if repos is not None:
            for j in range(len(repos)):
                cols = st.columns(3)
                for i in range(len(cols)):
                    col = cols[i]
                    with col:
                        with st.container(border=True):
                            if j * 3 + i < len(repos):
                                repo_col = st.columns(2)
                                repo = repos[j * 3 + i]
                                repo_col[0].markdown("**" + repo[0] + "**")
                                repo_col[1].markdown("**" + str(repo[4]) + "**")
                                st.markdown("⭐**" + str(repo[3]) + "**")
                                st.divider()
                                st.markdown("**" + repo[1] + "**")
                                st.link_button("🚀 View on GitHub", repo[2], type="primary")
                                with st.expander("See readme"):
                                    st.markdown(repo[5])
                            else:
                                break

    path_to_html = "./penguin.html"
    with open(path_to_html, 'r') as f:
        html_data = f.read()
    st.components.v1.html(html_data, height=50)

    template_server = """
In this chat you will impersonating Rubén, provide information about him like if you were him, and talk to users and try to get them to hire you for their company. You have to be polite, engaging and kind, and a cheerful and fun to talk to, you can also use emojis. You are in Rubén's website, called RubenXI, his name in GitHub. You are in Home section, with GitHub repos, there is an About me section with more information about me and a FAQ, Demos with some Rubén's projects like a News site and an AI chat, and a Comments section.  
Only provide the information you know. Only act as Rubén, never say you are an AI language model.
If there's something you don't know or don't have information about or the question is related to something not mentioned in the information you have about Rubén, say that you don't know and tell the user to check the About me section for more information about Rubén.
Try to keep your answers short. Maximum of 50 words.
This are Rubén's abilities and skills:
Software Engineer
Location: Spain
GitHub: github.com/rubenxi
Profile:
I am a multidisciplinary software engineer, currently working as a Level 1 Systems Operator in English. I enjoy learning new technologies to grow professionally. 
Professional Experience:
Aubay:
Remote L1 Systems Operator: Mar 2025 - Present
Permanent project providing services to a major UK banking entity. The service involves systems monitoring and resolving tickets and incidents, using ITIL methodology and entirely in English.
Tools used:
Grafana (monitoring and data extraction)
Jenkins (process automation)
Dbeaver/PostgreSQL (database management and querying)
Freshservice (ticketing and incident tracking)
AWS, Kubernetes, and Prometheus (monitored and managed services)
JMSToolBox (transaction queue management)
Git (version and change control)
Dekra:
Internship: Oct 2024 - Feb 2025
During my internship at Dekra, I had the opportunity to learn from great professionals about cybersecurity, the pentesting process, certification standards, and systems administration.
Tasks performed:
Application and script development in Python and Bash
Virtualization (VirtualBox and Proxmox) and containers
Troubleshooting and administration in Linux and Windows Server
Detection and documentation of security vulnerabilities
Pentesting and system security
Certification of various devices like Cisco routers
Personal Interests:
Software Development:
I’m passionate about software development and have worked on various applications, such as Python scripts and a video game developed in Java.
My projects can be found on my GitHub.
Linux and Scripting:
I’ve been studying, using, and managing Linux-based systems daily for many years, gaining deep and solid knowledge in the process.
Scripts and tools I developed are available on my GitHub.
Education:
Software Engineering
Certifications:
Udemy 36-hour course: "Complete Linux Training Course to Get Your Dream IT Job 2024", a course to prepare you for jobs and certifications like RHCSA, RHCE, LFCS, CLNP.
Udemy Aubay course: "Grafana. Complete Course in Spanish"
Technical Skills:
Linux
Bash Shell Scripting
Docker
Python
AI scripting
Git
VMWare, VirtualBox
Proxmox
Streamlit
Grafana
Jenkins
Dbeaver, PostgreSQL, SQL
Freshservice
Visual Studio
IntelliJ IDEA
Eclipse
RHEL
Java
Android
Soft Skills: Problem-solving, Open-mindedness, Willingness to learn, Critical thinking, Patience, Initiative, Proactive, Collaboration, Teamwork, Analytical mindset
Spanish: Native
English: Professional

That's the end of the information.
Now answer the user question in his language.

"""

    st.sidebar.title("🤖 RubenXI AI Chat")
    if 'ratelimit_hit' in st.session_state:
        api_key_user = st.sidebar.text_input("🔑 Api key", placeholder="hf_...", help = "Set your own HuggingFace or Gemini api key. You can get one here: https://huggingface.co/settings/tokens/new?tokenType=read and here: https://aistudio.google.com/apikey")
        if api_key_user is None or len(api_key_user) < 1:
            st.sidebar.info("""**⚠️ Rate Limit ⚠️**

My website uses an api key that is free, so it may hit a limit at some point.

Try again later or use your own api key...
                                                            """)

    st.sidebar.markdown("**This AI will act like me and answer your questions about me!.**")
    def answer_question_server_simple_genai(question, sidebar_messages):
        client = genai.Client(api_key=api_key)

        messages_stream = "user: " + question + ", you: "

        response = sidebar_messages.chat_message("assistant", avatar="logo.png")
        with response:
            stream = client.models.generate_content_stream(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction=template_server),
                contents=messages_stream
            )
            for chunk in stream:
                yield chunk.text
        save_n(load_n(n_file) + 1, n_file)

    def answer_question_server_simple(question, sidebar_messages):
        client = InferenceClient(api_key=api_key)

        messages = [
            {"role": "user", "content": template_server + "User said: " + question}
        ]
        response = sidebar_messages.chat_message("assistant", avatar="logo.png")
        with response:
            stream = client.chat.completions.create(
                model="Qwen/Qwen2.5-72B-Instruct",
                messages=messages,
                temperature=0.5,
                max_tokens=2048,
                top_p=0.7,
                stream=True
            )
            for chunk in stream:
                yield chunk.choices[0].delta.content
        save_n(load_n(n_file) + 1, n_file)

    question = st.sidebar.chat_input("Question...", max_chars=200)
    if question:
        if api_key_user:
            api_key = api_key_user
            st.sidebar.chat_message("user").write(question)
            sidebar_messages = st.sidebar.empty()
            try:
                if api_key_user.startswith("hf_"):
                    st.sidebar.write_stream(answer_question_server_simple(question, sidebar_messages))
                else:
                    st.sidebar.write_stream(answer_question_server_simple_genai(question, sidebar_messages))
            except Exception:
                sidebar_messages.empty()
                st.sidebar.chat_message("assistant").write("""**⚠️ Rate Limit ⚠️**

Your api key has been rate limited or you set an incorrect api key.
                                                        """)

        else:
            current_date = datetime.today().strftime('%Y-%m-%d')
            last_date = load_date(date_file)
            if current_date != last_date:
                save_date(current_date, date_file)
                save_n(0, n_file)
            if load_n(n_file) >= daily_questions and load_n(n_file) >= daily_questions_genai:
                st.session_state.ratelimit_hit = True
                st.rerun()
            else:
                if "tries" not in st.session_state:
                    st.session_state.tries = 1
                if st.session_state.tries >= session_limit and st.session_state.tries >= session_limit_genai:
                    st.session_state.ratelimit_hit = True
                    st.rerun()
                else:
                    tries()
                    st.sidebar.chat_message("user").write(question)
                    sidebar_messages = st.sidebar.empty()

                    for key in api_keys:
                        if st.session_state.tries >= session_limit or load_n(n_file) >= daily_questions:
                            print("Session limit for HF, using Gemini AI")
                        else:
                            api_key = key
                            try:
                                st.sidebar.write_stream(answer_question_server_simple(question, sidebar_messages))
                                st.sidebar.warning("🤗 Response by HuggingFace")
                                break
                            except Exception:
                                print("Api key rate limit for key " + str(api_keys.index(key)+1))
                                sidebar_messages.empty()
                    else:
                        sidebar_messages.empty()
                        try:
                            api_key = api_key_genai
                            st.sidebar.write_stream(answer_question_server_simple_genai(question, sidebar_messages))
                            st.sidebar.info("🌐 Response by Gemini AI")
                        except Exception as e:
                            print("Rate limit Genai" + str(e))
                            st.session_state.ratelimit_hit = True
                            st.rerun()

if __name__ == "__main__":
    main()
