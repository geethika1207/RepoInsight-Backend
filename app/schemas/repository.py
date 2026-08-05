from pydantic import BaseModel

class RequestURL(BaseModel):
    url : str

class Analysis(BaseModel):
    chunk_text : str 