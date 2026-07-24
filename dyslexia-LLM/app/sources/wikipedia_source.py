from dataclasses import dataclass
import wikipediaapi

@dataclass(frozen=True)
class WikipediaSection:
    title: str
    text: str
    
@dataclass(frozen=True)
class WikipediaDocument:
    title: str
    url: str
    summary: str
    sections: list[WikipediaSection]
    
    
wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="DyslexiaKnowledgeBot/0.1 (contact: oliver10jones220@gmail.com)",
)

def flatten_sections(sections) -> list[WikipediaSection]:
    results: list[WikipediaSection] = []

    for section in sections:
        if section.text.strip():
            results.append(WikipediaSection(title=section.title, text=section.text.strip()))
        results.extend(flatten_sections(section.sections))

    return results

def get_article(title: str) -> WikipediaDocument:
    page = wiki.page(title)

    if not page.exists():
        raise ValueError(f"Wikipedia page not found: {title}")

    return WikipediaDocument(title=page.title, url=page.fullurl, summary=page.summary, sections=flatten_sections(page.sections))