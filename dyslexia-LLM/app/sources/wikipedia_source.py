import wikipediaapi
from dataclasses import dataclass

from app.models.dataclasses import Document
wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="DyslexiaKnowledgeBot/0.1",
)

@dataclass(frozen=True)
class WikipediaSection:
    title: str
    text: str


@dataclass(frozen=True)
class WikipediaArticle:
    title: str
    url: str
    summary: str
    sections: list[WikipediaSection]


def flatten_sections(
    sections,
) -> list[WikipediaSection]:

    results = []

    for section in sections:

        if section.text.strip():
            results.append(
                WikipediaSection(
                    title=section.title,
                    text=section.text.strip(),
                )
            )

        results.extend(
            flatten_sections(section.sections)
        )

    return results


def get_article(
    title: str,
) -> WikipediaArticle:

    page = wiki.page(title)

    if not page.exists():
        raise ValueError(
            f"Wikipedia page not found: {title}"
        )

    return WikipediaArticle(
        title=page.title,
        url=page.fullurl,
        summary=page.summary,
        sections=flatten_sections(
            page.sections
        ),
    )