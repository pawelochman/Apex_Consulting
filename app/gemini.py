import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Text + vision model (Gemini 1.5 Pro handles PDFs, images, diagrams)
model = genai.GenerativeModel("gemini-1.5-pro")
