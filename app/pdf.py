from fastapi import UploadFile, File, Depends
from fastapi import APIRouter
from .deps import get_current_user

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), user=Depends(get_current_user)):
    content = await file.read()
    # TODO: save file, extract text, chunk, embed
    return {"filename": file.filename, "size": len(content)}
