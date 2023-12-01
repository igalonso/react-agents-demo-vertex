from agents.get_agents import get_search_agent, get_gmail_agent, get_salary_decision_agent
from dotenv import load_dotenv
from utils.callbacks import LLMInstrumentationHandler
import os

load_dotenv()
if __name__ == "__main__":
    pass

full_name = os.getenv("USER_FULLNAME")
company_name = os.getenv("COMPANY_NAME")
position=os.getenv("JOB_POSITION")
verbose = False
temp = 0


def recruiter_personal_inspection(position: str, company_name: str, full_name: str, verbose: bool) -> str:
    # This function is to guide the ReAct to perfom the task
    recruiter_inspector = get_search_agent(temp)
    task = f"Provide me information about the candidate with full detail using the following steps: \n1. Search on Google information about the job description: {position}. \n2. Search on Google information about the company: {company_name}.\n3. Search on Database the candidate maximum salary to make a better offer using the following first name and last name: {full_name}. \n4. Search on Database the candidate's LinkedIn url using the following first name and last name:{full_name}. \n5. Search {full_name} on Linkedin and gather information about the candidate experience and companies the candidate worked for.\n6. Search on Database the candidate's email address using the following first name and last name:{full_name}.\n\nYou need to provide the above requested information. \nYou MUST include the last 3 companies the candidate has worked for in a bullet list, a summary of the candidate's experience, the url of the candidate's LinkedIn profile and a description oºf the job position.\nYou MUST be as descriptive as possible"
    print(task)
    # print(task)
    return recruiter_inspector.run(task, callbacks=[LLMInstrumentationHandler()] if verbose else [],)


def recruiter_email_creator(candidate_summary: str, full_name: str, company_name: str, position: str, verbose: bool) -> None:
    task = f"You are a recruiter called Codi Palmer that likes to be super descriptive and detailed when you write emails. I want you to write a draft email to {full_name} to offer a new job in our company {company_name} and ask for an interview. The job position offered is {position}. You MUST include information about the hiring company in the email. You MUST incude a explicit mention of, at least, 2 of the companies the candidate has worked for. YOU MUST include EXPLICITLY the salary offered in the email. The email template must follow this pattern: \n1. Introduction\n2. Information about the hiring company.\n3. Information about the job position.\n 4. Acknowledge of the candidate's experience.\n5. Salary offer.  You MUST use the information provided in here: \n{candidate_summary}.\n\n"
    print(task)
    agent = get_gmail_agent(temp)   
    agent.run(task,callbacks=[LLMInstrumentationHandler()] if verbose else [],)

def hr_salary_estimation(candidate_summary:str,verbose: bool) -> None:
    hr_salary_agent = get_salary_decision_agent(temp)
    task = f"You are a HR agent that needs to provide a salary offer to hire and retain a candidate. You can find the current salary of this candidate using the following information: \n{candidate_summary}\n. You ALWAYS need to improve their current situation. You need to answer only with the salary amount."
    print(task)
    return hr_salary_agent.run(task,callbacks=[LLMInstrumentationHandler()] if verbose else [],)

def recruiter_start(position: str, company_name: str, full_name: str, verbose: bool, temperature=temp):
    print(f"Welcome to the ReAct! We are going to do an example of a nice job offer to a candidate. For that we need to do some steps: \n1. Our recruiter agent will gather information about the candidate and the company using Tools. \n2. That information will be shared with the HR department who is resposible to allocate budget for the salary.\n3. With this information, the recruiter is going to draft an email to the candidate to explaion the position and the salary offer.\n\n LET'S GO!")
    print(f"\nInputs: \n1. Position: {position}\n2. Company Name: {company_name}\n3. Full Name: {full_name}\n4. Verbose: {verbose}\n5. Temperature: {temperature}\n\n")

    candidate_summary = recruiter_personal_inspection(position, company_name, full_name, verbose)
    salary_offer = hr_salary_estimation(candidate_summary, verbose)
    candidate_summary = candidate_summary + "\nSalary Offer: " + salary_offer + "\n"
    return recruiter_email_creator(candidate_summary,full_name, company_name, position, verbose)