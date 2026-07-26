from app.ingestion.ingestion_pipeline import ingest_document
from app.database.db_actions import store_chunks
from app.sources.html_source import get_website
from app.models.dataclasses import WebsiteSource

WEBSITES = [
    WebsiteSource(
        url="https://www.dyslexiacornwall.org.uk/what-is-dyslexia/",
        source="Dyslexia Cornwall",
    ),
    WebsiteSource(
        url="https://www.dyslexiacornwall.org.uk/what-is-dyslexia/identifying-dyslexia/",
        source="Dyslexia Cornwall",
    ),
    WebsiteSource(
        url="https://www.dyslexiacornwall.org.uk/am-i-dyslexic/",
        source="Dyslexia Cornwall",
    ),
]

def main():
    all_chunks = []

    for website in WEBSITES:
        
        print(f"\nFetching: {website.url}")
        
        document = get_website(url=website.url, source=website.source)
        chunks = ingest_document(document)
        all_chunks.extend(chunks)

        print(f"Article: {document.title}")
        print(f"Chunks: {len(all_chunks)}")
        
    print(f"\nTotal chunks: {len(all_chunks)}")
            
    # Store everything in ChromaDB
    store_chunks(all_chunks)
    
if __name__ == "__main__":
    main()