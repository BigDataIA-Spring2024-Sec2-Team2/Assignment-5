# Assignment-5

## Live application Links
[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)](https://docs.google.com/document/d/1uM3pyBVNURT9fq-ySvNWs54Kkx8Pw9LZH0hw7yaW0CM/edit#heading=h.j0flkct7g8l6)

- Airflow: http://35.188.172.153:8080
- Fast API: http://35.224.202.134:8001
- Streamlit Application: http://35.222.74.248:8501

## Problem Statement 
Build an intelligent applications for knowledge retrieval and Q/A tasks.

## Project Goals
1. Creating knowledge summaries using OpenAI’s GPT
2. Generating a knowledge base (Q/A) providing context
3. Using a vector database to find and answer questions.
4. Use the knowledge summaries from 1 to answer questions.

## Technologies Used
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Apache Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)](https://airflow.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-%232496ED?style=for-the-badge&logo=Docker&color=blue&logoColor=white)](https://www.docker.com)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-%234169E1?style=for-the-badge&logo=MongoDB&logoColor=%234169E1&color=black)](https://www.postgresql.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)

## Pre requisites
1. Python Knowledge
2. Pinecone API Key
3. Openai API Key
4. Docker Desktop
5. MongoDB database knowledge
6. Vector database knowledge
8. Stremlit implementation
9. Airflow pipeline knowledge
10. Google Cloud Platform account and hosting knowledge

```
📦 
├─ .gitignore
├─ README.md
├─ airflow
│  ├─ Dockerfile
│  ├─ dags
│  │  ├─ configuration.properties.example
│  │  └─ dag_embedding.py
│  ├─ docker-compose.yml
│  └─ requirements.txt
├─ architecture_diagram
│  ├─ Assignment 5 diagram.png
│  └─ Assignment_5_flow_diagram.ipynb
├─ cloudfunction_generateMarkdown
│  ├─ main.py
│  └─ requirements.txt
├─ cloudfunction_generateMarkdownEmbedding
│  ├─ main.py
│  └─ requirements.txt
├─ cloudfunction_generateQuestioEmbedding
│  ├─ main.py
│  └─ requirements.txt
├─ fastapi_auth
│  ├─ Dockerfile
│  ├─ configuration.properties.example
│  ├─ docker-compose.yml
│  ├─ main.py
│  └─ requirements.txt
├─ fastapi_service
│  ├─ Dockerfile
│  ├─ configuration.properties.example
│  ├─ docker-compose.yml
│  ├─ main.py
│  ├─ requirements.txt
│  └─ routers
│     ├─ collection.py
│     ├─ questions.py
│     └─ report.py
├─ script_generateAnswers
│  ├─ part3.py
│  ├─ part4.py
│  └─ requirements.txt
├─ script_generateQuestion
│  ├─ main.py
│  └─ requirements.txt
├─ script_generateQuestionEmbedding
│  ├─ configuration.properties.example
│  └─ main.py
├─ script_setup
│  ├─ configuration.properties.example
│  ├─ pdf-extraction.py
│  ├─ requirements.txt
│  └─ webscrape.py
└─ streamlit_app
   ├─ Dockerfile
   ├─ components
   │  ├─ data_collection.py
   │  ├─ login_signup.py
   │  ├─ navigation.py
   │  ├─ part3_report.py
   │  ├─ part4_report.py
   │  └─ question_data.py
   ├─ configuration.properties.example
   ├─ docker-compose.yml
   ├─ main.py
   └─ requirements.txt
```
©generated by [Project Tree Generator](https://woochanleee.github.io/project-tree-generator)

## How to run Application Locally
1. Clone repository
2. Go to path each folder where requirementss.txt is present.
3. Create configurations.example files where requirements is present and add your respsctive creadentials for
   - AWS S3 bucket:
     Access key = "",
     Secret Key = "",
     Bucket = ""
 
   - MongoDB:
     mongo-username= "",
     mongo-password = "",
     mongo-cluster = ""
 
   - Airflow:
    airflow_un = "",
    airflow_pas = ""
  - Pinecone 

5. Create code env and activate it.
6. run pip install -r requirements.txt
7. Since each service is dockerised, just run docker compose up --build


## References

- https://www.cfainstitute.org/en/membership/professional-development/refresher-readings#sort=%40refreadingcurriculumyear%20descending
- https://pypdf.readthedocs.io/en/stable/
- https://diagrams.mingrammer.com/
- https://airflow.apache.org/
- https://openai.com/blog/openai-api

    Name | Contribution %| Contributions |
  --- |--- | --- |
  Anshul Chaudhary  | 33.3% | Web scraping, markdown genreation & embedding, airflow, streamlit, mongo, Pinecone, GCP, FastAPI, Hosting |
  Agash Uthayasuriyan | 33.3% | Openai, Pinecone, RAG, mongo, report generation |
  Narayani Arun Patil | 33.3% | Question generation, Openai, mongo, GCP Bucket, PDF parsing |
