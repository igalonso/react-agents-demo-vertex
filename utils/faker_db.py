from faker import Faker
import random
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to the database
conn = sqlite3.connect("db/mytest.db")

# Create a cursor object
cursor = conn.cursor()

faker = Faker()

cursor.execute("DROP TABLE IF EXISTS scouted_candidates")
cursor.execute(
    """
    CREATE TABLE scouted_candidates (
    candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    hire_date DATE,
    min_salary INTEGER,
    max_salary INTEGER,
    email TEXT UNIQUE,
    phone_number TEXT,
    location TEXT,
    experience_years INTEGER,
    linkedin_url TEXT,
    notes TEXT
);""")

# create a table for companies
cursor.execute("DROP TABLE IF EXISTS companies")
cursor.execute(
    """
    CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    company_size INTEGER,
    company_location TEXT,
    company_industry TEXT,
    company_website TEXT,
    company_description TEXT
);""")

# Commit the changes
conn.commit()

# Generate 100 fake candidates
for i in range(100):
    # Generate data for each column
    first_name = faker.name().split()[0]
    last_name = faker.name().split()[1]
    current_hiring_date = faker.date_between(start_date="-1y", end_date="+1y")        
    min_salary = random.randint(50000, 150000)
    max_salary = random.randint(54000, 154000)
    email = faker.email()
    phone_number = faker.phone_number()
    location = faker.city()
    linkedin_url = faker.url()
    notes = faker.paragraph()

    # Insert the data into the table
    cursor.execute(
        """
        INSERT INTO scouted_candidates (
            first_name, last_name, hire_date, min_salary, max_salary, email,
            phone_number, location, linkedin_url, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            first_name,
            last_name,
            current_hiring_date,
            min_salary,
            max_salary,
            email,
            phone_number,
            location,
            linkedin_url,
            notes,
        ),
    )



# Commit the changes
conn.commit()
full_name = os.getenv("USER_FULLNAME")
array_name = full_name.split(" ")
array_name = full_name.split(" ")
query = f"""
INSERT INTO scouted_candidates (
            first_name, last_name, hire_date, min_salary, max_salary, email,
            phone_number, location, linkedin_url, notes
        ) VALUES ('{array_name[0]}', '{array_name[1]}', '2023-11-21', '80000','120000', 'igngar@google.com', '+1234567890', 'Seattle, WA','https://www.linkedin.com/in/igngar/', 'Talented software engineer with strong expertise in JavaScript and React.')
"""
cursor.execute(query)

# Commit the changes
conn.commit()
query = "SELECT count(*) from scouted_candidates;"
query = "SELECT * from scouted_candidates WHERE first_name = 'Ignacio' AND last_name = 'Garcia';"
cursor.execute(query)
totalRows = cursor.fetchone()
print("Total rows are:  ", totalRows)
cursor.close()

# Close the connection
conn.close()
