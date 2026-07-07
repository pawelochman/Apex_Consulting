import os
import google.genai as genai
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in .env")

genai.configure(api_key=GOOGLE_API_KEY)

MODEL_NAME = "gemini-1.5-flash"  # or your preferred model

app = FastAPI()

# CORS so WordPress frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://apex-consultingllc.com", "http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    history: Optional[List[dict]] = None  # optional chat history


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {"status": "ok", "service": "Apex Consulting HVAC Q&A"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    system_prompt = (
        "You are an HVAC equipment selection and technical Q&A assistant for Apex Consulting LLC. "
        "Answer clearly, concisely, and only about HVAC, building systems, and related topics. "
        "If the question is outside that domain, say you are specialized in HVAC and cannot answer."
    )

    contents = [
        {"role": "system", "parts": [system_prompt]},
        {"role": "user", "parts": [req.question]},
    ]

    # If you later want to add history, you can append it here.

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(contents)
        answer = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {e}")

    return ChatResponse(answer=answer)
