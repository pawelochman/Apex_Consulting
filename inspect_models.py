import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
print("api_key set", bool(api_key))
client = genai.Client(api_key=api_key)
print("has models attr", hasattr(client, "models"))
try:
    models = list(client.models.list_models())
    print("models count", len(models))
    for m in models:
        print(m.name)
except Exception as e:
    print(type(e).__name__, e)
