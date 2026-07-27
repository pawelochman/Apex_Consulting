import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

API_KEY_ENV_VAR = "GOOGLE_API_KEY"
GOOGLE_API_KEY = os.getenv(API_KEY_ENV_VAR)
if not GOOGLE_API_KEY:
    raise RuntimeError(f"{API_KEY_ENV_VAR} environment variable is required")

genai.configure(api_key=GOOGLE_API_KEY)
client = genai.Client()
model = client.models

