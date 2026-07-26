from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Dyslexia Help API",
    description=("A RAG-based API for answering questions about dyslexia using trusted sources."),
    version="0.1.0",
)

app.include_router(router)