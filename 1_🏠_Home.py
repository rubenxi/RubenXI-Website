import streamlit as st
from streamlit import container, button
from utils import get_repos_github
import streamlit.components.v1 as components
from huggingface_hub import InferenceClient

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

def main():

    st.sidebar.title("RubenXI")
    st.sidebar.text("Some information about me and my projects. \nYou can check my GitHub repos or ask the AI in this menu about me.")

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
            st.link_button("📧 **Send me an email**","mailto: hg5l8ssre@mozmail.com", type="primary")
        with col4:
            if st.button("❓"):
                show_info()

        st.divider()
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
                            if j*3+i < len(repos):
                                repo_col = st.columns(2)
                                repo = repos[j*3+i]
                                repo_col[0].markdown("**"+repo[0]+"**")
                                repo_col[1].markdown("**"+str(repo[4])+"**")
                                st.markdown("⭐**" + str(repo[3]) + "**")
                                st.divider()
                                st.markdown("**"+repo[1]+"**")
                                st.link_button("🚀 View on GitHub", repo[2], type="primary")
                                with st.expander("See readme"):
                                    st.markdown(repo[5])
                            else:
                                break

    path_to_html = "./penguin.html"
    with open(path_to_html, 'r') as f:
        html_data = f.read()
    st.components.v1.html(html_data, height=50)


    api_key = st.secrets["api_key"]

    template_server = """
    In this chat you will act as Rubén, provide information about him like if you were him, and talk to users and try to get them to hire you for their company. You have to be polite, engaging and kind, and a bit cheerful and fun to talk to. 
    Only provide the information you know.
    If there's something you don't know or don't have information about, say it and tell the user to check the About me section for more information about Rubén.
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
    st.sidebar.divider()
    st.sidebar.header("RubenXI AI chat")
    st.sidebar.text("This AI will act like me and answer your questions about me!")

    def answer_question_server_simple(question):
        client = InferenceClient(api_key=api_key)

        messages = [
            {"role": "user", "content": template_server + question}
        ]

        with st.sidebar.chat_message("assistant",avatar="logo.png"):
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

    question = st.sidebar.chat_input("Question")

    if question:
        st.sidebar.chat_message("user").write(question)
        st.sidebar.write_stream(answer_question_server_simple(question))


if __name__ == "__main__":
    main()