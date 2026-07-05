from fastapi import APIRouter, UploadFile, File, Depends
from app.gemini import model
from app.deps import get_current_user

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/analyze")
async def analyze_pdf(file: UploadFile = File(...), user=Depends(get_current_user)):
    pdf_bytes = await file.read()
    response = model.generate_content([
        "Summarize and extract insights from this PDF.",
        {"mime_type": "application/pdf", "data": pdf_bytes}
    ])
    return {"summary": response.text}
