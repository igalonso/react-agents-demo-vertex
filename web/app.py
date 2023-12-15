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
st.image("web/img/diagram.png", width=700)
col1, col2, col3 = st.columns(3)
with col1:
    full_name = st.text_input("Full Name of Candidate", value="Ignacio Garcia")
    company_name = st.text_input("Full Name of the company offering", value="Nintendo")
    position=st.text_input("Full Name of the postion offered",value="Solutions Architect")
    testing = st.checkbox("Testing", value=True)
with col2:
    
    model_for_information_gathering = st.selectbox("Select a model for information gathering", ("text-bison@002","text-bison@001", "text-unicorn","gemini-pro"))
    model_for_hr_salary_decision = st.selectbox("Select a model for HR salary decision", ("text-bison@001","text-bison@002", "text-unicorn","gemini-pro"))
    model_for_email_draft = st.selectbox("Select a model for email draft", ("text-unicorn", "text-bison@001","text-bison@002","text-bison-32k"))
    temperature_slider = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    temperature_slider_email = st.slider("Temperature for email", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    verbose = False
    generate = st.button("Run Agent🤖")
    os.environ["TEMPERATURE_AGENTS"] = str(temperature_slider)
    os.environ["TEMPERATURE_EMAIL"] = str(temperature_slider_email)

#info_agent = st.image('img/info_agent.gif')
file_ = open(os.getcwd()+"/web/img/info_agent.gif", "rb")
contents = file_.read()
info_agent_image = base64.b64encode(contents).decode("utf-8")
file_.close()
file_ = open(os.getcwd()+"/web/img/hr_agent.gif", "rb")
contents = file_.read()
hr_agent_image = base64.b64encode(contents).decode("utf-8")
file_.close()
file_ = open(os.getcwd()+"/web/img/email_agent.gif", "rb")
contents = file_.read()
email_agent_image = base64.b64encode(contents).decode("utf-8")
file_.close()
#stop = st.button("Stop Agent🤖")

if generate:

    with st.spinner("Agent running..."):
        os.environ["VERTEX_MODEL_GATHERING"] = model_for_information_gathering
        os.environ["VERTEX_MODEL_SALARY"] = model_for_hr_salary_decision
        os.environ["VERTEX_MODEL_EMAIL"] = model_for_email_draft
        os.environ["TESTING"] = str(testing)

        

        with col3:
            info_agent_md = st.markdown(
                f'<div class="gif_holder"><img  src="data:image/gif;base64,{info_agent_image}" alt="Info Agent GIF" style="border: solid red; width: 100%"></div>',
                unsafe_allow_html=True,
            )
            # output = st.empty()
            # output.style
            # with st_capture(output.text):
        candidate_summary = agent.recruiter_personal_inspection(position, company_name, full_name, verbose)
            # output.empty()
        with col3:
            info_agent_md.empty()
            hr_agent_md = st.markdown(
            f'<div class="gif_holder"><img  src="data:image/gif;base64,{hr_agent_image}" alt="HR Agent GIF" style="border: solid red; width: 100%"></div>',
                unsafe_allow_html=True,
            )
        # output = st.empty()
        # with st_capture(output.text):
        salary_offer = agent.hr_salary_estimation(candidate_summary, verbose)
        candidate_summary = candidate_summary + "\n- Salary Offer: " + salary_offer + "\n"
        # output.empty()
        with col3:
            hr_agent_md.empty()
            email_agent_md = st.markdown(
                f'<div class="gif_holder"><img  src="data:image/gif;base64,{email_agent_image}" alt="HR Agent GIF" style="border: solid red; width: 100%"></div>',
                unsafe_allow_html=True,
            )
            # output = st.empty()
            # with st_capture(output.text):
        agent.recruiter_email_creator(candidate_summary,full_name, company_name, position, verbose)
            # output.empty()
        email_agent_md.empty()
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