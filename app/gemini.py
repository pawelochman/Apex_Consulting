import os
import google.genai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Text + vision model (Gemini 1.5 Pro handles PDFs, images, diagrams)
response = client.models.generate(
    model="gemini-1.5-flash",
    contents=contents
)

