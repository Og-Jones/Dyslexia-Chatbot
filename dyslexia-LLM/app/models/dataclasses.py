from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class WebsiteSource:
    url: str
    source: str

@dataclass
class Document:
    title: str
    url: str
    text: str
    source: str
    retrieved_at: datetime | None = None
    
@dataclass
class TextChunk:
    chunk_id: str
    source: str
    title: str
    url: str
    section: str
    text: str
    embedding: list[float] = field(default_factory=list)