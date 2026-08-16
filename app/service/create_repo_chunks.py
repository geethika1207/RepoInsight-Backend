# Create chunks 

def chunk_repository(repo_files, chunk_size:int, overlap:int, Repo_name : str, Repo_owner : str):
    chunks = []

    for file in repo_files:

        start = 0
        chunk_index = 0 

        file_path = file["file_path"]
        content = file["content"]
        repo_file_id = file["repo_files_id"]

        while start < len(content):

            end = start + chunk_size
            chunk_text = content[start:end]

            chunks.append({
                "file_path" : file_path,
                "Repo_name" : Repo_name,
                "Repo_owner" : Repo_owner,
                "chunk_index" : chunk_index,
                "chunk_text" : chunk_text,
                "repository_file_id" : repo_file_id
            })

            chunk_index += 1
            start = end - overlap

    return chunks 