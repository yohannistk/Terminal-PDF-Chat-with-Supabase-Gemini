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

  
def chat_with_pdfs(query):
    query_embedding = embed_text(query)
    response = supabase.rpc("match_documents", {
        "query_embedding": query_embedding,
        "match_count": 5,
    }).execute()
    if not response.data:
        return "No relevant context found in the PDFs."

    context = " ".join([r["content"] for r in response.data])

    chat_model = genai.GenerativeModel("gemini-1.5-flash")
    result = chat_model.generate_content(
    f"""Using the provided PDF content, generate a response that adheres to the user's 
    specific instructions (e.g., summarize, answer in a specific format, or limit to a 
    certain number of lines). Ensure the response is accurate, relevant, and directly 
    addresses the question while leveraging the context 
    provided.\n\nContext:\n{context}\n\nUser Request: {query}"""
     )
    return result.text  

def main():
    print("📄 Chat with latest PDFs")

    while True:
        query = input("\nAsk a question (or 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break

        answer = chat_with_pdfs(query)
        print("\n🤖 Answer:", answer)

if __name__ == "__main__":
    main()