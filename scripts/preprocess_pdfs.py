import os
import fitz  # PyMuPDF
import numpy as np
import faiss
import pickle
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PDF_FOLDER = "pdfs"  # put your PDFs here
OUTPUT_FILE = "pdf_library.pkl"


def extract_pdf_text(path):
    """Extract text from a PDF file."""
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def chunk_text(text, chunk_size=800):
    """Split text into chunks for embedding."""
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
    """Generate OpenAI embeddings."""
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return np.array(response.data[0].embedding)


def process_pdf_library():
    pdf_library = {}

    for file in os.listdir(PDF_FOLDER):
        if not file.endswith(".pdf"):
            continue

        print(f"Processing: {file}")

        # Extract make/model from filename
        name = file.replace(".pdf", "")  # e.g., Samsung_AR18CSFCMWKNCV
        make, model = name.split("_", 1)

        path = os.path.join(PDF_FOLDER, file)
        text = extract_pdf_text(path)
        chunks = chunk_text(text)

        # Embed all chunks
        embeddings = np.array([embed_text(c) for c in chunks])

        # Build FAISS index
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)

        pdf_library[f"{make}_{model}"] = {
            "index": index,
            "chunks": chunks
        }

    # Save library
    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump(pdf_library, f)

    print(f"\nPDF library saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    process_pdf_library()
