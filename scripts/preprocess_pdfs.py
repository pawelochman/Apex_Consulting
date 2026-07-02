import os
import fitz  # PyMuPDF
import numpy as np
import faiss
import pickle
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_FOLDER = os.path.join(BASE_DIR, "pdfs")          # Your PDF library folder
OUTPUT_FILE = os.path.join(BASE_DIR, "pdf_library.pkl")  # Saved embeddings/indexes


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
    """Walk through all PDFs (including subfolders), embed them, and save FAISS indexes."""
    pdf_library = {}

    for root, dirs, files in os.walk(PDF_FOLDER):
        for file in files:
            if not file.endswith(".pdf"):
                continue

            full_path = os.path.join(root, file)
            print(f"Processing: {full_path}")

            # Folder name becomes "make"
            make = os.path.basename(root)

            # File name (without .pdf) becomes "model"
            model = file.replace(".pdf", "")

            # Extract text
            text = extract_pdf_text(full_path)

            # Chunk text
            chunks = chunk_text(text)

            # Embed chunks
            embeddings = np.array([embed_text(c) for c in chunks])

            # Build FAISS index
            dim = embeddings.shape[1]
            index = faiss.IndexFlatL2(dim)
            index.add(embeddings)

            # Store in library
            pdf_library[f"{make}_{model}"] = {
                "index": index,
                "chunks": chunks
            }

    # Save library to disk
    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump(pdf_library, f)

    print(f"\nPDF library saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    process_pdf_library()
