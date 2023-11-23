import streamlit as st

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '')

import agent

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
st.set_page_config(
    page_icon="web/img/robot-1.1s-200px.png",
    layout="wide",
    page_title="React Agents Demo with Vertex AI (Google Cloud)",
    initial_sidebar_state="expanded",
)

st.markdown(
    f'<div class="header"><figure><embed type="image/svg+xml" src="/web/img/sdr.svg" /><figcaption></figcaption></figure><h3> React Agents Demo with Vertex AI (Google Cloud) </h3></div>',
    unsafe_allow_html=True,
)

st.image("web/img/sdr.jpeg", width=300)

full_name = st.text_input("Full Name of Candidate")
company_name = st.text_input("Full Name of the company offering")
position=st.text_input("Full Name of the postion offered")
verbose = False
temp = 0


generate = st.button("Run Agent🤖")

if generate:
    with st.spinner("Agent running..."):
        agent.recruiter_start(position, company_name, full_name, verbose)
        st.balloons()

local_css("web/css/frontend.css")
remote_css("https://fonts.googleapis.com/icon?family=Material+Icons")
remote_css(
    "https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700&display=swap"
)