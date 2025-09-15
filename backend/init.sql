-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a test table to verify pgvector is working
CREATE TABLE IF NOT EXISTS test_vectors (
    id SERIAL PRIMARY KEY,
    embedding vector(1536),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert a test vector
INSERT INTO test_vectors (embedding, content) 
VALUES ('[0.1,0.2,0.3]'::vector, 'Test vector for pgvector setup');

-- Verify the extension is working
SELECT * FROM test_vectors;
