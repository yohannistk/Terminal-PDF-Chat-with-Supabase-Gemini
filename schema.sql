create extension if not exists vector with schema extensions;
-- Creating table for storing PDF document chunks
create table if not exists documents (
  id uuid primary key default gen_random_uuid(), -- Supabase convention for UUID primary key
  doc_id text not null, -- Identifier for grouping chunks of the same source document
  content text not null, -- Text content of the document chunk
  embedding vector(768), -- Gemini embedding size for vector similarity search
  created_at timestamp with time zone default now() -- Supabase convention for tracking creation time
);

-- Creating index for efficient vector similarity searches
create index if not exists documents_embedding_idx on documents using ivfflat (embedding vector_cosine_ops) with (lists = 100);

-- Creating function for document similarity search
create or replace function match_documents(
  query_embedding vector(768),
  match_count int,
  filter_doc_id text
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
  where documents.doc_id = filter_doc_id
    and documents.embedding is not null
  order by documents.embedding <=> query_embedding
  limit match_count;
$$;

-- Commenting on the table for clarity
comment on table documents is 'Stores document chunks with their embeddings for similarity search';
comment on column documents.doc_id is 'Identifier to group chunks belonging to the same source document';