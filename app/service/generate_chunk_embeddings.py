from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embedding_chunks(queries):

    embedding_chunk = model.encode(queries)

    return embedding_chunk.tolist()
