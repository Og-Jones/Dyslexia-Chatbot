from sources.wikipedia_source import get_article
from chunking import chunk_text_with_embeddings
from store import store_chunks

def main():
    article = get_article("Dyslexia")

    all_chunks = []

    all_chunks.extend(
        chunk_text_with_embeddings(
            title=article.title,
            url=article.url,
            section="Summary",
            text=article.summary,
        )
    )

    # process each section of the wiki article
    for section in article.sections:
        all_chunks.extend(
            chunk_text_with_embeddings(
                title=article.title,
                url=article.url,
                section=section.title,
                text=section.text,
            )
        )
        
    # Store everything in ChromaDB
    store_chunks(all_chunks)