from langchain.llms import VertexAI
from tools.tools import get_google_search, get_sql_database,get_scrape_linkedin_profile, get_next_available_date, search_llm, get_salary_data, get_what_day_is_today, get_recruiter_email_template
from langchain.agents import initialize_agent, Tool, AgentExecutor
from langchain.agents import AgentType
from langchain.agents.agent_toolkits import GmailToolkit

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI as OpenAI

from dotenv import load_dotenv
import os
load_dotenv()
if __name__ == "__main__":
    pass
openai_model = "gpt-4"
#openai_model = "gpt-3.5-turbo-16k"


gmail_toolkit = GmailToolkit()
google_search = Tool(
    name="GoogleSearch",
    func=get_google_search,
    description="useful for when you need get a google search result",
)
sql_database = Tool(
    name="SQLDatabase_data_retrieval",
    func=get_sql_database,
    description="useful for when you need to query a database for candidates. The table is called scouted_candidates. Fields are: candidate_id, first_name, last_name, hire_date, min_salary, max_salary, email, phone_number, location, experience_years, linkedin_url, notes",
)
recruiter_email_template = Tool(
    name="RecruiterEmailTemplate",
    func=get_recruiter_email_template,
    description="useful for when you need to get a recruiter email template in the final answer",
)
scrape_linkedin_profile= Tool(
    name="scrape_linkedin_profile",
    func=get_scrape_linkedin_profile,
    description="useful for getting information on a Linkedin profile url",
)
next_available_date= Tool(
    name="next_available_date",
    func=get_next_available_date,
    description="use this tool to get the next available date for an interview",
)
salary_data = Tool(
    name="get_salary_data",
    func=get_salary_data,
    description="useful for getting the salary data for a candidate on a specific location and role",
)
what_day_is_today = Tool(
    name="what_day_is_today",
    func=get_what_day_is_today,
    description="use this tool to current day today"
)

def getLLM():
    llm_type = os.getenv("LLM_TYPE")
    if llm_type == "openai":
        llm = OpenAI(model_name=openai_model)
    elif llm_type == "vertexai":
        llm = VertexAI(temperature=0.3, verbose=True, max_output_tokens=2047,model_name="text-bison-32k")
    return llm

gmail_tools = [gmail_toolkit.get_tools()[0]]

def get_gmail_agent(temperture=1) -> AgentExecutor:
    #print(f"Temperature: {temperture}")
    print("*" * 79)
    print("AGENT: Recruiter Email Crafter Agent!")
    print("*" * 79)
    llm = getLLM()
    
    agent = initialize_agent(
        gmail_tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    return agent

def get_search_agent(temperture=1) -> AgentExecutor:
    #print(f"Temperature: {temperture}")
    print("*" * 79)
    print("AGENT: Recruiter information retrieval Agent!")
    print("*" * 79)
    llm = getLLM()
    tools_for_agent = [
        google_search,
        sql_database,
        scrape_linkedin_profile,
        salary_data
    ]

    agent = initialize_agent(
        tools_for_agent,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent

def get_salary_decision_agent(temperature=1)-> AgentExecutor:
    print("*" * 79)
    print("AGENT: HR salary decision Agent!")
    print("*" * 79)
    #print(f"Temperature: {temperature}")
    llm = getLLM()
    tools_for_agent = [
        google_search
    ]

    agent = initialize_agent(
        tools_for_agent,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent