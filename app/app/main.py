from fastapi import FastAPI
from app.pdf import router as pdf_router
from app.image import router as image_router

app = FastAPI(title="Apex Consulting Gemini AI")

app.include_router(pdf_router)
app.include_router(image_router)
