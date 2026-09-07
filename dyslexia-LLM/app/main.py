from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Dyslexia Help API",
    description=("A RAG-based API for answering questions about dyslexia using trusted sources."),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        
        # development urls
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        
        # production urls
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(router)