from fastapi import FastAPI
from pydantic import BaseModel
from google.genai import Client
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = Client(api_key=GOOGLE_API_KEY)

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "ok", "service": "Apex Consulting HVAC Q&A"}
