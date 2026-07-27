import os
from dotenv import load_dotenv
import google.genai as genai

# Load .env values and override any existing env vars so the repo's key is authoritative.
load_dotenv(override=True)

API_KEY_ENV_VAR = "GOOGLE_API_KEY"
GOOGLE_API_KEY = os.getenv(API_KEY_ENV_VAR)
if not GOOGLE_API_KEY:
    raise RuntimeError(f"{API_KEY_ENV_VAR} environment variable is required")

if "GEMINI_API_KEY" in os.environ:
    del os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=GOOGLE_API_KEY)
model = client.models

