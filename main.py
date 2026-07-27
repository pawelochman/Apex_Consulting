from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.genai.errors import ClientError
from app.gemini import model

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "ok", "service": "Apex Consulting HVAC Q&A"}

@app.post("/hvac")
def hvac_answer(payload: Question):
    try:
        response = model.generate_content(
            model="gemini-1.5-flash",
            contents=f"Answer this HVAC question: {payload.question}"
        )
    except ClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal service error") from exc

    if not response.candidates:
        return {"answer": "Model returned no candidates."}

    parts = response.candidates[0].content.parts
    answer = "".join(getattr(p, "text", "") for p in parts)

    return {"answer": answer or "Model returned no text content."}
