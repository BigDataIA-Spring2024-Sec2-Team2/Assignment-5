from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import collection, questions

app = FastAPI()

app.include_router(collection.router, tags=['collection'], prefix='/collection')
app.include_router(questions.router, tags=['questions'], prefix='/questions')