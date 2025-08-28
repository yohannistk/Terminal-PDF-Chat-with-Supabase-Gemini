# 📄 Terminal PDF Chat with Supabase & Gemini  

A lightweight Python app that lets you **upload PDFs, store them as embeddings in Supabase, and chat with them using Google Gemini** — all from your terminal.  

Every time you upload new PDFs, the database is **cleared and refreshed**, so you always query the **latest version** of your documents.  

---

## 🚀 Features  
- 📂 Upload all PDFs in a directory automatically  
- 🧠 Store embeddings in **Supabase** for semantic search  
- 🤖 Chat with your PDFs using **Google Gemini**  
- ⚡ Simple **terminal interface** — no web app required  
- 🔄 Always fresh data: database clears before each new upload  

---

## 📦 Installation  

1. **Clone this repository**  
```bash
git clone git clone https://github.com/yohannistk/Terminal-PDF-Chat-with-Supabase-Gemini.git
cd Terminal-PDF-Chat-with-Supabase-Gemini
```

2. **Set up a virtual environment**(recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```
3. **Install dependencies**

```bash
pip install -r requirements.txt
```
4. **Set environment variables**

Create a .env file in the root directory and add:

```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_api_key
GEMINI_API_KEY=your_gemini_api_key

```

## 🗄️ Supabase Table Setup

Run this SQL inside your Supabase project.

```sql
create extension if not exists vector with schema extensions;

-- Creating table for storing PDF document chunks
create table if not exists documents (
  id uuid primary key default gen_random_uuid(), -- Supabase convention for UUID primary key
  content text not null, -- Text content of the document chunk
  embedding vector(768), -- Gemini embedding size for vector similarity search
  created_at timestamp with time zone default now() -- Supabase convention for tracking creation time
);

-- Creating index for efficient vector similarity searches
create index if not exists documents_embedding_idx on documents using ivfflat (embedding vector_cosine_ops) with (lists = 100);

-- Creating function for document similarity search
create or replace function match_documents(
  query_embedding vector(768),
  match_count int
)
returns table (
  id uuid,
  content text,
  similarity float
)
language sql stable as $$
  select
    id,
    content,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where documents.embedding is not null
  order by documents.embedding <=> query_embedding
  limit match_count;
$$;

-- Commenting on the table for clarity
comment on table documents is 'Stores document chunks with their embeddings for similarity search';
```


## Project Structure

```bash
pdf-chat-gemini/
│── pdfs/                 # Place your PDFs here
│── upload_pdfs.py        # Uploads PDFs to Supabase
│── main.py     # Chat with your PDFs in terminal
│── requirements.txt      # Python dependencies
│── .env                  # API keys (not included in repo)
│── README.md             # Project docs
```

## ▶️ Usage

1. **Upload PDFs**
    Place your PDF files inside the pdfs/ folder, then run:

    ```bash
    python upload_pdfs.py
    ```
    This clears old records and uploads the new PDFs to Supabase.

2. **Chat with PDFs**
   Start the chat interface:

   ```bash
   python main.py
   ``` 
   Ask questions in natural language, and the app will answer using the PDF content.



