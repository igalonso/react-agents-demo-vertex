FROM python:3.11-slim

COPY . app/

RUN pip install -r app/requirements.txt

EXPOSE 8080

CMD cd app && streamlit run web/app.py --server.port 8080