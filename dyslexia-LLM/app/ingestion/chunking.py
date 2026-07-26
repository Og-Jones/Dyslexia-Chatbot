from dataclasses import dataclass, field
from semantic_text_splitter import TextSplitter
from app.ingestion.embeddings import create_embeddings
@dataclass(frozen=True)
class TextChunk:
    chunk_id: str
    source: str
    title: str
    url: str
    section: str
    text: str
    embedding: list[float] = field(default_factory=list)

# target chunk size in characters
MAX_SECTION_CHARS = 5000
splitter = TextSplitter(2500)

# Split text into overlapping chunks using semantic_text_splitter
def chunk_text_with_embeddings(title: str, url: str, section: str, text: str) -> list[TextChunk]:
    
    cleaned = text.strip()
    
    # Keep short sections whole and semantically split longer sections
    if len(cleaned) <= MAX_SECTION_CHARS:
        # keep whole section
        parts = [cleaned]
    else:
        # split with semantic splitter
        parts = list(splitter.chunks(cleaned))
        
    # Create all embeddings in one API request.
    embeddings = create_embeddings(parts)
    if len(parts) != len(embeddings):
        raise RuntimeError("The number of embeddings does not match the number of chunks.")
        
    return [
            TextChunk(
                chunk_id=f"{title}-{section}-{index}",
                source="Wikipedia",
                title=title,
                url=url,
                section=section,
                text=part,
                embedding=embedding,
            )
            for index, (part, embedding) in enumerate(
                zip(parts, embeddings, strict=True)
            )
        ]