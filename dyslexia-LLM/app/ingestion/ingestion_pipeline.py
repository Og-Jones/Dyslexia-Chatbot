from dataclasses import dataclass, field
from semantic_text_splitter import TextSplitter

from app.ingestion.embeddings import create_embeddings
from app.models.dataclasses import Document, TextChunk

# Maximum size before semantic splitting is required
MAX_SECTION_CHARS = 5000
# Semantic text splitter
splitter = TextSplitter(2500)

def chunk_document(document: Document) -> list[TextChunk]:

    text = document.text.strip()

    if not text: raise ValueError(f"Cannot chunk empty document: {document.title}")

    # Keep short documents whole
    if len(text) <= MAX_SECTION_CHARS:
        parts = [text]

    # Split longer documents into semantic chunks
    else:
        parts = list(splitter.chunks(text))

    # return a list of text chunks
    return [
        TextChunk(
            chunk_id=f"{document.title}-{index}",
            source=document.source,
            title=document.title,
            url=document.url,
            section=None,
            text=part,
        )
        for index, part in enumerate(parts)
    ]

def embed_chunks(chunks: list[TextChunk]) -> list[TextChunk]:

    if not chunks:
        return []

    texts = [chunk.text for chunk in chunks]

    embeddings = create_embeddings(texts)

    if len(chunks) != len(embeddings): raise RuntimeError("The number of embeddings does not match the number of chunks.")

    return [
        TextChunk(
            chunk_id=chunk.chunk_id,
            source=chunk.source,
            title=chunk.title,
            url=chunk.url,
            section=chunk.section,
            text=chunk.text,
            embedding=embedding,
        )
        for chunk, embedding in zip(
            chunks,
            embeddings,
            strict=True,
        )
    ]
    
def ingest_document(document: Document) -> list[TextChunk]:

    # 1. Chunk the document
    chunks = chunk_document(document)

    # 2. Create embeddings for those chunks
    embedded_chunks = embed_chunks(chunks)

    return embedded_chunks