from app.models.dataclasses import Document
from app.sources.wikipedia_source import get_article
from app.ingestion.ingestion_pipeline import ingest_document
from app.database.db_actions import store_chunks


def main():

    article = get_article("Dyslexia")

    all_chunks = []

    # Ingest summary
    summary_document = Document(
        title=article.title,
        url=article.url,
        text=article.summary,
        source="Wikipedia",
    )

    all_chunks.extend(
        ingest_document(
            document=summary_document,
            section="Summary",
        )
    )

    # Ingest each Wikipedia section
    for section in article.sections:

        section_document = Document(
            title=article.title,
            url=article.url,
            text=section.text,
            source="Wikipedia",
        )

        all_chunks.extend(
            ingest_document(
                document=section_document,
                section=section.title,
            )
        )

    print(
        f"Article: {article.title}"
    )

    print(
        f"Chunks: {len(all_chunks)}"
    )

    store_chunks(all_chunks)


if __name__ == "__main__":
    main()