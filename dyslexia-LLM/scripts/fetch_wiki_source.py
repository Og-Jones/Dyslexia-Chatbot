from app.sources.wikipedia_source import get_article
from app.ingestion.ingestion_pipeline import ingest_document
from app.database.db_actions import store_chunks


def main():

    document = get_article("Dyslexia")

    print(
        f"\nFetching: {document.title}"
    )

    chunks = ingest_document(document)

    print(
        f"Chunks: {len(chunks)}"
    )

    store_chunks(chunks)


if __name__ == "__main__":
    main()