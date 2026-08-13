import os
import cohere

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def embedding_chunks(queries):
    if isinstance(queries, str):
        queries = [queries]
        
    response = co.embed(
        texts=queries,
        model="embed-english-light-v3.0", 
        input_type="search_document" 
    )
    
    return response.embeddings