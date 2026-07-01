from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()

from .database import Base, engine
from .models import User
from .auth import hash_password, verify_password, create_access_token
from .deps import get_db, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure PDF Chatbot")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.post("/auth/register")
def register(email: str, password: str, full_name: str | None = None, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created"}

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "full_name": current_user.full_name
    }
