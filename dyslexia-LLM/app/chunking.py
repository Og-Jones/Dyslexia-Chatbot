from dataclasses import dataclass
from semantic_text_splitter import TextSplitter

@dataclass(frozen=True)
class TextChunk:
    chunk_id: str
    source: str
    title: str
    url: str
    section: str
    text: str

# target chunk size in characters
MAX_SECTION_CHARS = 5000
splitter = TextSplitter(2500)

# Split text into overlapping chunks using semantic_text_splitter
def chunk_text(title: str, url: str, section: str, text: str) -> list[TextChunk]:
    
    cleaned = text.strip()
    
    # Keep short sections whole and semantically split longer sections
    if len(cleaned) <= MAX_SECTION_CHARS:
        # keep whole section
        parts = [cleaned]
    else:
        # split with semantic splitter
        parts = list(splitter.chunks(cleaned))
    
    return [
        TextChunk(
            chunk_id=f"{title}-{section}-{index}",
            source="Wikipedia",
            title=title,
            url=url,
            section=section,
            text=part,
        )
        for index, part in enumerate(parts)
    ]