import os
from dotenv import load_dotenv
from supabase import create_client
import google.generativeai as genai


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)

def embed_text(text: str):
    res = genai.embed_content(model="models/embedding-001", content=text)
    return res["embedding"]

  