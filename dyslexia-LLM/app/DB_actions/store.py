import chromadb

# Create ChromaDB client. Saves DB locally
client = chromadb.PersistentClient(
    path="./chroma_db"
)

# Create or get the collection to store chunks, embeddings and misc
collection = client.get_or_create_collection(
    name="dyslexia_knowledge"
)

# Store chunks
def store_chunks(chunks):

    collection.add(
        ids=[
            chunk.chunk_id
            for chunk in chunks
        ],
        
        documents=[
            chunk.text
            for chunk in chunks
        ],
        
        embeddings=[
            chunk.embedding
            for chunk in chunks
        ],
        
        metadatas=[
            {
                "source": chunk.source,
                "title": chunk.title,
                "url": chunk.url,
                "section": chunk.section,
            }
            for chunk in chunks
        ],
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")