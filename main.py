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

@app.post("/chat")
def chat(q: Question):
    contents = [{"role": "user", "parts": [{"text": q.question}]}]

    response = client.models.generate(
        model="gemini-1.5-flash",
        contents=contents
    )

    return {"answer": response.text}
