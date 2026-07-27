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

DEFAULT_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")


def generate_content(prompt: str, model: str | None = None):
    selected_model = model or DEFAULT_MODEL
    response = client.models.generate_content(
        model=selected_model,
        contents=prompt,
    )
    return response.text

