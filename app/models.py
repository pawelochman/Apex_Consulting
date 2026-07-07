from sqlalchemy import Column, Integer, String
from .database import Base

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(contents)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
