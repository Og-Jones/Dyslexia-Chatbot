import chromadb
from ..ingestion.embeddings import create_embeddings

# Connect to the existing local ChromaDB
client = chromadb.PersistentClient(path="./data/chroma_db")

# Get the existing collection
collection = client.get_or_create_collection(name="dyslexia_knowledge")

# Store chunks
def store_chunks(chunks):

    collection.upsert(
        ids=[chunk.chunk_id for chunk in chunks],
        documents=[chunk.text for chunk in chunks],
        embeddings=[chunk.embedding for chunk in chunks],
        metadatas=[
            {
                "source": chunk.source,
                "title": chunk.title,
                "url": chunk.url,
                "section": chunk.section,
            }
            for chunk in chunks
        ]
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")

# Find the most relevant chunks in ChromaDB for a user's question
def retrieve_chunks(query: str, n_results: int = 5):

    # Create an embedding for the user's question
    query_embedding = create_embeddings([query])[0]

    # Search ChromaDB using the query embedding
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results,)

    return results

