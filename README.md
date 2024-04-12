# Assignment-5

## Live application Links
[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)](https://docs.google.com/document/d/1uM3pyBVNURT9fq-ySvNWs54Kkx8Pw9LZH0hw7yaW0CM/edit#heading=h.j0flkct7g8l6)

- Airflow: https://34.139.115.254:8080
- Authentication Service: https://34.23.189.28:8000
- Fast API: https://34.23.189.28:8000
- Streamlit Application: https://35.229.36.63:8051
  

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

## Project Structure
```
📦 Assignment-5
├─ airflow
│  ├─ dags
│  ├─ Dockerfile
│  ├─ docker-compose.yml
│  └─ requirements.txt
├─ cloudfunction_generateMarkdown
│  ├─ main.py
│  └─ requirements.txt
├─ cloudfunction_generateMarkdownEmbedding
│  ├─ main.py
│  └─ requirements.txt
├─ cloudfunction_generateQuestioEmbedding
│  ├─ main.py
│  └─ requirements.txt
├─ coludfuntion_generateAnswers
│  ├─ demo_1.py
│  ├─ part4.py
│  └─ requirements.txt
├─ fastapi_auth
│  ├─ Dockerfile
│  ├─ docker-compose.yml
│  └─ requirements.txt
├─ fastapi_service
│  └─ routers
│     ├─ collection.py
│     ├─ Dockerfile
│     └─ main.py
script_generateQuestion
│  ├─ main.py
│  └─ requirements.txt
├─ script_generateQuestionEmbedding
│  └─ main.py
├─ script_setup
│  ├─ pdf-extraction.py
│  └─ webscrape.py
├─ streamlit_app
│  └─ components
│     ├─ data_collection.py
│     ├─ login_signup.py
│     ├─ navigation.py
│     ├─ Dockerfile
│     └─ main.py
├─ .gitignore
├─ Assignment 5 diagram.png
├─ Assignment_5_flow_diagram.ipynb
└─ README.md
```
©generated by [Project Tree Generator](https://woochanleee.github.io/project-tree-generator)

## How to run Application Locally


## Project run outline

CodeLab - [Documentation]([https://docs.google.com/document/d/1YvvKu38ZeIrlWY-Pgls1Gwes7ZaCuarZ1gx1VVb-qKI/edit#heading=h.iq9nlyp04yle](https://docs.google.com/document/d/1uM3pyBVNURT9fq-ySvNWs54Kkx8Pw9LZH0hw7yaW0CM/edit#heading=h.j0flkct7g8l6)) 

## References

- https://www.cfainstitute.org/en/membership/professional-development/refresher-readings#sort=%40refreadingcurriculumyear%20descending
- https://pypdf.readthedocs.io/en/stable/
- https://diagrams.mingrammer.com/
- https://airflow.apache.org/
- https://openai.com/blog/openai-api

    Name | Contribution %| Contributions |
  --- |--- | --- |
  Anshul Chaudhary  | 33.3% | Web scraping, airflow, streamlit, mongo, Pinecone, GCP |
  Agash Uthayasuriyan | 33.3% | Openai, Pinecone, RAG, mongo, report generation |
  Narayani Arun Patil | 33.3% | Question generation, Openai, mongo, GCP Bucket, PDF parsing |
