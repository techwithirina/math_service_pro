# main.py
from fastapi import FastAPI
from db import init_db
from api import router
from worker import start_worker
from dotenv import load_dotenv


load_dotenv()  # Load .env before anything else


app = FastAPI(title="Math Microservice")
app.include_router(router)


@app.on_event("startup")
def startup_event():
    init_db()
    start_worker()
