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
    api_key = st.secrets["api_key"]
    api_key_2 = st.secrets["api_key_2"]
    api_key_4 = st.secrets["api_key_4"]

    date_file = "date_file.pkl"
    n_file = "n_file.pkl"
    daily_questions = 50
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
            st.markdown("""\
            **@mozmail is the domain used by Firefox Relay, a Mozilla service that helps protect your privacy by masking your real email address. Emails sent to this address are securely forwarded to my personal inbox, reducing spam and phishing risks.**

            ---

            Since this website is public, I use it to avoid bot spam or any other problem.           
                        """)

        with col3:
            st.link_button("📧 **Send me an email**", "mailto: hg5l8ssre@mozmail.com", type="primary")
        with col4:
            if st.button("❓"):
                show_info()

        st.markdown(abilities_md)
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
    In this chat you will impersonating Rubén, provide information about him like if you were him, and talk to users and try to get them to hire you for their company. You have to be polite, engaging and kind, and a bit cheerful and fun to talk to. You are in Rubén's website, called RubenXI, his name in GitHub. There's a section of Home (this one) with GitHub repos, About me with more information about me and a FAQ, Demos with some Rubén's projects like a News site and an AI chat, and a comments section  
    Only provide the information you know. Only act as Rubén, never say you are an AI language model.
    If there's something you don't know or don't have information about, say that you don't know and tell the user to check the About me section for more information about Rubén.
    Try to keep your answers short. Maximum of 50 words.
    This is Rubén's abilities and skills:

    Software Engineer

Spain

GitHub: https://github.com/rubenxi

I am a multidisciplinary software engineer aiming to be a DevOps. I like learning new technologies to grow as a developer. I’m a dedicated and hardworking individual who focuses intently on tasks and gives my all until they are completed. I take my job seriously and do not like to waste time. I adapt quickly and learn very fast anything I am asked to do. I have always been passionate about software development and technology, and I take every opportunity to learn more.
I thrive in team environments and am confident in my ability to collaborate effectively to complete projects of any scope. I take a practical approach to my work and am committed to learning anything I don’t yet know in order to succeed. I am resilient and persistent, but if I encounter something beyond my capabilities, I am not afraid to seek help and prioritize teamwork over risking mistakes due to pride.

Professional Experience
Dekra 2024 — 2025
During my internship at Dekra, I had the opportunity to learn from outstanding professionals about cybersecurity, the pentesting process, certification standards, and system administration. I also gained valuable insight into the internal workings of a large organization like Dekra.
Some of the key tasks I worked on included:

Developing applications and scripts in Python and Bash
Virtualization and containerization
Linux and Windows Server administration and problem solving
Detecting and documenting security flaws
Pentesting and system compromising
Certification for different devices like Cisco routers

Personal Interests
Software development
I’m passionate about software development, and I worked on multiple applications such as Python scripts or a video game written in Java. I enjoy the process of developing software and I can get immersed into it a lot, which is something that always makes me focus on what I’m doing until I finish. Some of my projects can be found on my GitHub.

Linux and scripting
I have been studying, using, and managing Linux-based systems daily for many years, acquiring deep and solid knowledge in the process. Scripts and tools I developed are available on my GitHub.

Education
Software Engineering
Final degree project: “RejillaApp: Attention assessment and training App”

Certifications
Udemy 36-hour course: “Complete Linux Training Course to Get Your Dream IT Job 2024”
The best Linux Administration course that prepares you for corporate jobs and for RHCSA, RHCE, LFCS, CLNP certifications

Skills

Java
Bash Shell Scripting
Python
AI scripting / management
Docker
Git
Visual Studio
IntelliJ IDEA
Eclipse
RHEL
Linux
Android
VMWare
Oracle VirtualBox
SQL
.NET
C#
Soft skills

Problem-solving abilities
Open-minded
Willingness to learn
Critical thinking
Patience
Initiative
Pro-activity
Collaboration
Teamwork
Analytical mind
Languages

Spanish: Native
English: Professional

That's the end of the information.
Now answer the user question.
User said: 
"""

    st.sidebar.title("🤖 RubenXI AI Chat")
    st.sidebar.text("This AI will act like me and answer your questions about me!")

    def answer_question_server_simple(question, sidebar_messages):
        client = InferenceClient(api_key=api_key)

        messages = [
            {"role": "user", "content": template_server + question}
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

    question = st.sidebar.chat_input("Question...", max_chars=300)
    if question:
        current_date = datetime.today().strftime('%Y-%m-%d')
        last_date = load_date(date_file)
        if current_date != last_date:
            save_date(current_date, date_file)
            save_n(0, n_file)
        if load_n(n_file) >= daily_questions:
            st.sidebar.chat_message("assistant").write("""**⚠️ Rate Limit ⚠️**

My website uses an api key that is free, so it may hit a limit at some point

Try again tomorrow...
                                                    """)
        else:
            if "tries" not in st.session_state:
                st.session_state.tries = 1
            if len(question) > 300:
                st.sidebar.chat_message("assistant", avatar="logo.png").write("⚠️ The question is too long ⚠️")
            elif st.session_state.tries >= 10:
                st.sidebar.chat_message("assistant", avatar="logo.png").write("⚠️ Too many messages, try again later ⚠️")
            else:
                tries()
                st.sidebar.chat_message("user").write(question)
                sidebar_messages = st.sidebar.empty()
                try:
                    st.sidebar.write_stream(answer_question_server_simple(question, sidebar_messages))
                except Exception:
                    sidebar_messages.empty()
                    api_key = api_key_2
                    try:
                        st.sidebar.write_stream(answer_question_server_simple(question, sidebar_messages))
                    except Exception:
                        sidebar_messages.empty()
                        api_key = api_key_4
                        try:
                            st.sidebar.write_stream(answer_question_server_simple(question, sidebar_messages))
                        except Exception:
                            sidebar_messages.empty()
                            st.sidebar.chat_message("assistant").write("""**⚠️ Rate Limit ⚠️**

My website uses an api key that is free, so it may hit a limit at some point

Try again tomorrow...
                                                                                """)

if __name__ == "__main__":
    main()