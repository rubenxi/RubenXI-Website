import streamlit as st
from utils import get_repos_github

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

st.sidebar.title("RubenXI")
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
    st.divider()
    st.markdown(abilities_md)

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
                            st.link_button("🚀 View on GitHub", repo[2])
                            with st.expander("See readme"):
                                st.markdown(repo[5])
                        else:
                            break


