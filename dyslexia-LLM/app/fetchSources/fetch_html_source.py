from chunking import chunk_text_with_embeddings
from DB_actions.store import store_chunks

from sources.wikipedia_source import get_article
from sources.html_source import get_website

def main():
    
    #article = get_website("https://www.dyslexiacornwall.org.uk/what-is-dyslexia/")
    article = get_website("https://www.dyslexiacornwall.org.uk/what-is-dyslexia/identifying-dyslexia/")

    all_chunks = []

    all_chunks.extend(
        chunk_text_with_embeddings(
            title=article.title,
            url=article.url,
            section="Website Content",
            text=article.text,
        )
    )

    print(f"Article: {article.title}")
    print(f"Chunks: {len(all_chunks)}")
        
    # Store everything in ChromaDB
    store_chunks(all_chunks)
    
if __name__ == "__main__":
    main()