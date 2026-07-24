from dataclasses import dataclass
import wikipediaapi

@dataclass(frozen=True)
class WikipediaDocument:
    title: str
    url: str
    text: str
    
wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="DyslexiaKnowledgeBot/0.1 (contact: oliver10jones220@gmail.com)",
)

def get_article(title: str) -> WikipediaDocument:
    page = wiki.page(title)

    if not page.exists():
        raise ValueError(f"Wikipedia page not found: {title}")

    return WikipediaDocument(title=page.title, url=page.fullurl, text=page.text)