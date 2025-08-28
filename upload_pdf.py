import os
import uuid
from dotenv import load_dotenv
from supabase import create_client
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai

# Load environment
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)

TABLE_NAME = "documents"
PDF_FOLDER = "pdfs"  # folder containing all PDF files

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    return " ".join([page.extract_text() or "" for page in reader.pages])

def chunk_text(text: str, chunk_size=800, overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)


def embed_text(text: str):
    res = genai.embed_content(model="models/embedding-001", content=text)
    return res["embedding"]


def embed_and_store(chunks, doc_id):
    for chunk in chunks:
        embedding = embed_text(chunk)
        supabase.table(TABLE_NAME).insert({
            "id": str(uuid.uuid4()),
            "doc_id": doc_id,
            "content": chunk,
            "embedding": embedding
        }).execute()

def main():
    if not os.path.exists(PDF_FOLDER):
        print(f"❌ Folder '{PDF_FOLDER}' not found.")
        return

    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"❌ No PDF files found in '{PDF_FOLDER}'.")
        return

    for pdf_file in pdf_files:
        file_path = os.path.join(PDF_FOLDER, pdf_file)
        print(f"⏳ Processing: {pdf_file}")
        text = extract_text_from_pdf(file_path)
        chunks = chunk_text(text)
        doc_id = str(uuid.uuid4())
        embed_and_store(chunks, doc_id)
        print(f"✅ Uploaded '{pdf_file}' with doc_id={doc_id}")

    print("🎉 All PDFs uploaded successfully!")

if __name__ == "__main__":
    main()
