from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import collection

app = FastAPI()

app.include_router(collection.router, tags=['collection'], prefix='/collection')