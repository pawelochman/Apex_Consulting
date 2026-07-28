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

DEFAULT_MODEL = os.getenv("GOOGLE_MODEL", "gemini-flash-lite-latest")
FALLBACK_MODELS = [
    os.getenv("GOOGLE_FALLBACK_MODEL_1", "gemini-3.1-flash-lite"),
    os.getenv("GOOGLE_FALLBACK_MODEL_2", "gemini-2.0-flash"),
]


def generate_content(prompt: str, model: str | None = None):
    candidate_models = []
    if model:
        candidate_models.append(model)
    else:
        candidate_models.append(DEFAULT_MODEL)

    for fallback_model in FALLBACK_MODELS:
        if fallback_model not in candidate_models:
            candidate_models.append(fallback_model)

    last_error = None
    for selected_model in candidate_models:
        try:
            response = client.models.generate_content(
                model=selected_model,
                contents=prompt,
            )
            return response.text
        except Exception as exc:
            last_error = exc
            print(f"Model {selected_model} failed: {type(exc).__name__}: {exc}")

    raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")

