import cohere

from app.core.config import settings

# Use settings here instead of os.getenv
co = cohere.Client(settings.COHERE_API_KEY)

def embedding_chunks(queries):
    if isinstance(queries, str):
        queries = [queries]
        
    response = co.embed(
        texts=queries,
        model="embed-english-light-v3.0", 
        input_type="search_document" 
    )
    
    return response.embeddings