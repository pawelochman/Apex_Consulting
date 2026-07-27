import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv(override=True)

api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")

print("API key present:", bool(api_key))
print("Model:", model_name)

if not api_key:
    raise SystemExit("GOOGLE_API_KEY is not set. Add it to your .env or environment variables.")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model=model_name,
        contents="Reply with 'OK' only."
    )
    print("Connection OK")
    print("Response:", response.text)
except Exception as e:
    print("Connection failed:", type(e).__name__, e)
    raise
