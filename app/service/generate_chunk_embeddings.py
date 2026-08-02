from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embedding_chunks(chunks):

    for chunk in chunks:

        embedding_chunk = model.encode(chunk["chunk_text"])

        chunk["embedding"] = embedding_chunk.tolist()

    return chunks 
