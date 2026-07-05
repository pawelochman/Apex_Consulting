from fastapi import APIRouter, UploadFile, File, Depends
from app.gemini import model
from app.deps import get_current_user

router = APIRouter(prefix="/image", tags=["Image"])

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...), user=Depends(get_current_user)):
    image_bytes = await file.read()
    response = model.generate_content([
        "Describe and interpret this image or diagram in detail.",
        {"mime_type": "image/png", "data": image_bytes}
    ])
    return {"analysis": response.text}
