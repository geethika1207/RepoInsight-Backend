SUPPORTED_EXTENSIONS = {
    ".py", ".md", ".txt", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".js", ".ts", ".jsx", ".tsx",
    ".java", ".cpp", ".c", ".cs", ".go", ".rs",
    ".php", ".html", ".css", ".sql"
}

def read_repository(repo_path):

    repository_files = []

    for file in repo_path.rglob("*"):

        if not file.is_file():
            continue

        if not file.suffix.lower() in SUPPORTED_EXTENSIONS:
            continue

        try:
            #read_text() accepts keyword arguments, not a dictionary
            content = file.read_text(    
                encoding = "utf-8",
                errors = "ignore"                              # Path.read_text() accepts errors, not error
            )

            if "\x00" in content:
                continue 

            repository_files.append({
                "file_path" : str(file.relative_to(repo_path)),
                "content" : content
            })

        except Exception:
            continue

    return repository_files   



# Create chunks 

def chunk_repository(repo_files, chunk_size:int, overlap:int, Repo_name : str, Repo_owner : str):
    chunks = []

    for file in repo_files:

        start = 0
        chunk_index = 0 

        file_path = file["file_path"]
        content = file["content"]

        while start < len(content):

            end = start + chunk_size
            chunk_text = content[start:end]

            chunks.append({
                "file_path" : file_path,
                "Repo_name" : Repo_name,
                "Repo_owner" : Repo_owner,
                "chunk_index" : chunk_index,
                "chunk_text" : chunk_text,
            })

            chunk_index += 1
            start = end - overlap

    return chunks 



from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embedding_chunks(chunks):

    for chunk in chunks:

        embedding_chunk = model.encode(chunk["chunk_text"])

        chunk["embedding"] = embedding_chunk.tolist()

    return chunks 