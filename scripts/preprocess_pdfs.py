import os
import fitz  # PyMuPDF
import numpy as np
import faiss
import pickle
from dotenv import load_dotenv

# Correct Gemini SDK
from google.ai.generativelanguage import GenerativeServiceClient
from google.ai.generativelanguage import EmbedContentRequest

# Load environment variables
load_dotenv()
client = GenerativeServiceClient(api_key=os.getenv("GEMINI_API_KEY"))

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_FOLDER = os.path.join(BASE_DIR, "pdfs")
OUTPUT_FILE = os.path.join(BASE_DIR, "pdf_library.pkl")


def extract_pdf_text(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def chunk_text(text, chunk_size=800):
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)
        if len(current) >= chunk_size:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


def embed_text(text):
    request = EmbedContentRequest(
        model="models/embedding-001",
        content=text
    )
    result = client.embed_content(request)
    return np.array(result.embedding, dtype=np.float32)


def process_pdf_library():
    pdf_library = {}

    for root, dirs, files in os.walk(PDF_FOLDER):
        for file in files:
            if not file.endswith(".pdf"):
                continue

            full_path = os.path.join(root, file)
            print(f"Processing: {full_path}")

            make = os.path.basename(root)
            model = file.replace(".pdf", "")

            text = extract_pdf_text(full_path)
            chunks = chunk_text(text)

            embeddings = np.array([embed_text(c) for c in chunks])

            dim = embeddings.shape[1]
            index = faiss.IndexFlatL2(dim)
            index.add(embeddings)

            pdf_library[f"{make}_{model}"] = {
                "index": index,
                "chunks": chunks
            }

    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump(pdf_library, f)

    print(f"\nPDF library saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    process_pdf_library()
