from fastapi import FastAPI
from .db.database import engine, Base
from .routers import auth, repository, practice

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(repository.router)