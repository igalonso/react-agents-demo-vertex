import streamlit as st
import base64

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
    # f'<div class="header"><figure><embed type="image/svg+xml" src="web/img/sdr.svg" /><figcaption></figcaption></figure><h3> React Agents Demo with Vertex AI (Google Cloud) </h3></div>',
    f"<div class='header'><h3> React Agents Demo with Vertex AI</h3><h3>(Google Cloud) </h3></div>",
    unsafe_allow_html=True,
)
st.markdown(
    f'<div>Welcome to the ReAct! We are going to do an example of a nice job offer to a candidate. For that we need to do some steps:<ul><li>Our recruiter agent will gather information about the candidate and the company using Tools.</li><li>That information will be shared with the HR department who is resposible to allocate budget for the salary.</li><li>With this information, the recruiter is going to draft an email to the candidate to explaion the position and the salary offer.</li></ul>LETS GO!</div>',
    unsafe_allow_html=True
)
# """### gif from local file"""
# file_ = open("web/img/demo.gif", "rb")
# contents = file_.read()
# data_url = base64.b64encode(contents).decode("utf-8")
# file_.close()

# st.markdown(
#     f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
#     unsafe_allow_html=True,
# )

#st.image("web/img/sdr.jpeg", width=300)

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
        st.success("Agent finished! - Now you can access your mail to find out the draft offer")
        st.write("[gmail link to drafts](https://mail.google.com/mail/u/0/#drafts)")

local_css("web/css/frontend.css")
remote_css("https://fonts.googleapis.com/icon?family=Material+Icons")
remote_css(
    "https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700&display=swap"
)