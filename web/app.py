import streamlit as st
import base64

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '')

import agent
import os

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

full_name = st.text_input("Full Name of Candidate", value="Ignacio Garcia")
company_name = st.text_input("Full Name of the company offering", value="Nintendo")
position=st.text_input("Full Name of the postion offered",value="Solutions Architect")
testing = st.checkbox("Testing", value=True)
model_for_information_gathering = st.selectbox("Select a model for information gathering", ("text-bison@002","text-bison@001", "text-unicorn","gemini-pro"))
model_for_hr_salary_decision = st.selectbox("Select a model for HR salary decision", ("text-bison@001","text-bison@002", "text-unicorn","gemini-pro"))
model_for_email_draft = st.selectbox("Select a model for email draft", ("text-unicorn", "text-bison@001","text-bison@002","gemini-pro"))
verbose = False
temp = 0


generate = st.button("Run Agent🤖")
#stop = st.button("Stop Agent🤖")

if generate:
    with st.spinner("Agent running..."):
        os.environ["VERTEX_MODEL_GATHERING"] = model_for_information_gathering
        os.environ["VERTEX_MODEL_SALARY"] = model_for_hr_salary_decision
        os.environ["VERTEX_MODEL_EMAIL"] = model_for_email_draft
        os.environ["TESTING"] = str(testing)
        agent.recruiter_start(position, company_name, full_name, verbose)
        st.balloons()
        st.success("Agent finished! - Now you can access your mail to find out the draft offer")
        st.write("[gmail link to drafts](https://mail.google.com/mail/u/0/#drafts)")
# if stop:
#     st.stop()

local_css("web/css/frontend.css")
remote_css("https://fonts.googleapis.com/icon?family=Material+Icons")
remote_css(
    "https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700&display=swap"
)