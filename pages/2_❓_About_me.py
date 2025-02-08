import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="RubenXI",
    page_icon="logo.png"
)

def main():
    st.sidebar.title("❓ More about me")
    st.sidebar.text("If you want to know more about me and my experience you can read this page")

    st.markdown(
    """
    **Software Engineer**
    
    📍 **Spain**
    
    **My GitHub**  
    **[github.com/rubenxi](github.com/rubenxi)**
    
    # 📌 Profile
    I am a multidisciplinary software engineer aiming to be a DevOps. I
    like learning new technologies to grow as a developer. I’m a dedicated
    and hardworking individual who focuses intently on tasks and gives my
    all until they are completed. I take my job seriously and does not like to
    waste time. I adapt quickly and learn very fast anything I am asked to
    do. I have always been passionate about software development and
    technology, and I take every opportunity to learn more.
    I thrive in team environments and am confident in my ability to
    collaborate effectively to complete projects of any scope.
    I take a practical approach to my work and am committed to learning
    anything I don’t yet know in order to succeed. I am resilient and
    persistent, but if I encounter something beyond my capabilities, I am
    not afraid to seek help and prioritize teamwork over risking mistakes
    due to pride.
    
    # 💼 Professional Experience
    ## 🏢 Dekra 2024 — 2025
    During my internship at Dekra, I had the opportunity to learn from
    outstanding professionals about cybersecurity, the pentesting process,
    certification standards and system administration. I also gained valuable
    insight into the internal workings of a large organization like Dekra.
    Some of the key tasks I worked on included:
    - Developing applications and scripts in Python and Bash
    - Virtualization and containerization
    - Linux and Windows Server administration and problem solving
    - Detecting and documenting security flaws
    - Pentesting and system compromissing
    - Certification for different devices like Cisco routers
    
    # 🎯 Personal Interests
    ## 💻 Software development
    I’m passionate about Software development, and I worked on multiple
    applications such as Python scripts or a video game written in Java.
    I enjoy the process of developing Software and I can get inmersed into
    it a lot, which is something that always makes me focus in what I’m
    doing until I finish. Some of my projects can be found on my Github.
    ## 🐧 Linux and scripting
    I have been studying, using, and managing Linux-based systems
    daily for many years, acquiring deep and solid knowledge in the
    process. Scripts and tools I developed are available on my GitHub.
    # 🎓 Education
    ## Software Engineering
    - **Final degree project: “RejillaApp: Attention assessment and training App”**
    # 📜 Certifications
    - **Udemy 36 hours course: “Complete Linux Training Course to GetYour Dream IT Job 2024“**  
    The BEST Linux Administration course that prepares you for corporate jobs and for RHCSA, RHCE, LFCS, CLNP certifications”
    # 🛠 Skills
    - Java
    - Bash Shell Scripting
    - Python
    - AI scripting / management
    - Docker
    - Git
    - Visual Studio
    - IntelliJ IDEA
    - Eclipse
    - RHEL
    - Linux
    - Android
    - VMWare
    - Oracle VirtualBox
    - SQL
    - .NET
    - C#
    # 🤝 Soft skills
    - Problem-solving abilities
    - Open-minded
    - Willingness to learn
    - Critical thinking
    - Patience
    - Initiative
    - Pro-activity
    - Collaboration
    - Teamwork
    - Analytical mind
    # 🌍 Languages
    - Spanish: Native
    - English: Professional
    """
    )

if __name__ == "__main__":
    main()
