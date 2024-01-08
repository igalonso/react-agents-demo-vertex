import requests
from langchain_community.utilities import SerpAPIWrapper
from langchain.sql_database import SQLDatabase
from langchain_community.llms import VertexAI
import os
import json
import datetime
from dotenv import load_dotenv
from langchain_community.retrievers import GoogleVertexAISearchRetriever
from langchain.chains import RetrievalQA
import vertexai 
from vertexai.language_models import TextGenerationModel
from datetime import datetime

load_dotenv()
if __name__ == "__main__":
    pass
testing = os.getenv("TESTING")
# Wrapper around Google Search.
class CustomSerpAPIWrapper(SerpAPIWrapper):
    def __init__(self):
        super(CustomSerpAPIWrapper, self).__init__()

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from SerpAPI."""
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
            toret = res["answer_box"]["answer"]
        elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
            toret = res["answer_box"]["snippet"]
        elif (
            "answer_box" in res.keys()
            and "snippet_highlighted_words" in res["answer_box"].keys()
        ):
            toret = res["answer_box"]["snippet_highlighted_words"][0]
        elif (
            "sports_results" in res.keys()
            and "game_spotlight" in res["sports_results"].keys()
        ):
            toret = res["sports_results"]["game_spotlight"]
        elif (
            "knowledge_graph" in res.keys()
            and "description" in res["knowledge_graph"].keys()
        ):
            toret = res["knowledge_graph"]["description"]
        elif "snippet" in res["organic_results"][0].keys():
            toret = res["organic_results"][0]["link"]

        else:
            toret = "No good search result found"
        return toret

def query_text_bison_llm(query: str):
    project_id = os.environ["PROJECT_ID"]
    location = "europe-west1"
    vertexai.init(project=project_id, location=location)
    parameters = {
        "temperature": 0,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 2040,  # Token limit determines the maximum amount of text output.
        "top_p": 0.8,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        query,
        **parameters,
    )
    print(f"Response from Model: {response.text}")
    return response.text

# Searches on Google.
def get_google_search(query: str):
    """Searches on Google."""
    # super dirty hack to avoid API calls
    if testing ==  "True":
        with open("utils/search_response.json", "r") as f:
            data = json.load(f)
        if "salary" in query:
            return data["salary_sales_engineer"]
        elif "Solutions Architect" in query: 
            return data["solutions_architect"]
        elif "solutions architect" in query: 
            return data["solutions_architect"]
        elif "Apple" in query:  
            return data["apple"]
        elif "HubSpot" in query:
            return data["hubspot"]
        elif "Google" in query:
            return data["google"]
        elif "average salary of a Lawyer" in query:
            return data["salary_lawyer"]
        elif "Cepsa" in query:
            return data["cepsa"]
        elif "Amazon" in query:
            return data["amazon"]
        elif "Microsoft" in query:
            return data["microsoft"]
        elif "Facebook" in query:
            return data["facebook"]
        elif "Talgo" in query:
            return data["talgo"]
        else:
            return query_text_bison_llm(query)
        


    search = CustomSerpAPIWrapper()
    res = search.run(f"{query}")
    return res.strip()
# Returns a SQL database. The tables are scouted_candidates and fields in this table are:  candidate_id, first_name, last_name, hire_date, min_salary, max_salary, email, phone_number, location, experience_years, linkedin_url, notes 
def get_sql_database(query: str):
    """Returns a SQL database. The tables are scouted_candidates and fields in this table are:  candidate_id, first_name, last_name, hire_date, min_salary, max_salary, email, phone_number, location, experience_years, linkedin_url, notes """
    sql = SQLDatabase.from_uri(os.environ["SQL_DATABASE_URI"])
    try:
        res = sql.run(f"{query}")
    except Exception as e:
        res = "You used a wrong query. Please try again with these fields candidate_id, first_name, last_name, hire_date, min_salary, max_salary, email, phone_number, location, experience_years, linkedin_url, notes \n"
        res = res + str(e)
    return res
# Searches on Wikipedia.
def get_wikipedia_search(query: str):
    """Searches on Wikipedia."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data
#scrape information from LinkedIn profiles, Manually scrape the information from the LinkedIn profile
def get_scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"

    header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}

    response = requests.get(
        api_endpoint,
        params={"url": linkedin_profile_url, "extra": "include"},
        headers=header_dic,
    )
    data = response.json()
    if testing==True or ("code" in data and data["code"] != "200"):
        with open("utils/linkedin_profile.json", "r") as f:
            data = json.load(f)
    experiences = data["experiences"]
    headline = data["headline"]
    summary = data["summary"]
    occupation = data["occupation"]
    experiences = []
    for experience in data["experiences"]:
        experiences.append([experience["company"], experience["title"], experience["starts_at"], experience["ends_at"]])
    educations = []
    for education in data["education"]:
        educations.append([education["school"], education["degree_name"], education["starts_at"], education["ends_at"]])
    final_response = {"headline": headline, "summary": summary, "experiences": experiences, "education": education, "occupation": occupation}
    return final_response
def get_recruiter_email_template(query: str):
    """Returns an email template."""
    template = """
    Subject: {subject}
    Body:{body}
    """
    return template.format(subject=query, body=query)
def get_what_day_is_today(query: str):
    """Returns the date of today."""

    today = datetime.date.today()
    return today.strftime("%m/%d/%Y, %H:%M:%S")
def get_next_available_date(query: str):
    """Returns the next available date."""
    today = datetime.date.today()
    next_available_date = today + datetime.timedelta(days=7)
    return next_available_date
def get_salary_data(query: str):
    """Returns the salary data."""
    url = "https://job-salary-data.p.rapidapi.com/job-salary"
    querystring = {"job_title":query,"location":query,"radius":"200"}

    headers = {
        "X-RapidAPI-Key": os.environ.get("X_RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "job-salary-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    # print(f"\nResponse: {response.json()}")
    data = response.json()
    if data["message"] == "You are not subscribed to this API.":
        with open("utils/job_salary.json", "r") as f:
            data = json.load(f)
    return data

def get_interview_feedback(query: str):
    #print(query)
    retriever = GoogleVertexAISearchRetriever(
        project_id=os.environ["PROJECT_ID"],
        location_id=os.environ["LOCATION_ID"],
        data_store_id=os.environ["DATA_STORE_ID"],
        max_documents=3,
        max_extractive_answer_count=3,
        get_extractive_answers=True,
    )
    llm = VertexAI(temperature=0, verbose=True,model_name="text-bison@001")
    retrieval_qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
    )
    result = retrieval_qa({"query": query})
    return result["result"]