from app.ingestion.chunking import chunk_text_with_embeddings
from app.database.db_actions import store_chunks

from app.sources.html_source import get_website

WEBSITES = [
        "https://www.dyslexiacornwall.org.uk/what-is-dyslexia/",
        "https://www.dyslexiacornwall.org.uk/what-is-dyslexia/identifying-dyslexia/",
        "https://www.dyslexiacornwall.org.uk/am-i-dyslexic/"
]

def main():
    all_chunks = []

    for url in WEBSITES:
        
        print(f"\nFetching: {url}")
        article = get_website(url)
        
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
        
    print(f"\nTotal chunks: {len(all_chunks)}")
            
    # Store everything in ChromaDB
    store_chunks(all_chunks)
    
if __name__ == "__main__":
    main()