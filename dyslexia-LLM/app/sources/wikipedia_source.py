import wikipediaapi

from app.models.dataclasses import Document
wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="DyslexiaKnowledgeBot/0.1",
)


def get_article(title: str) -> Document:

    page = wiki.page(title)

    if not page.exists():
        raise ValueError(
            f"Wikipedia page not found: {title}"
        )

    return Document(
        title=page.title,
        url=page.fullurl,
        text=page.summary + "\n\n" + page.text,
        source="Wikipedia",
    )