import os
from dotenv import load_dotenv
from agent import recruiter_start

load_dotenv()
if __name__ == "__main__":
    pass

full_name = os.getenv("USER_FULLNAME")
company_name = os.getenv("COMPANY_NAME")
position=os.getenv("JOB_POSITION")
verbose = False
temp = 0

recruiter_start(position, company_name, full_name, verbose)