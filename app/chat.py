from fastapi import APIRouter, Depends
from .deps import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
def chat(query: str, user=Depends(get_current_user)):
    # TODO: search vector DB, send to Gemini, return answer
    return {"answer": f"Placeholder response to: {query}"}
