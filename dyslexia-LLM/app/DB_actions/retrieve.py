import chromadb
from embeddings import create_embeddings

# Connect to the existing local ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db"
)

# Get the existing collection
collection = client.get_collection(
    name="dyslexia_knowledge"
)

# Find the most relevant chunks in ChromaDB for a user's question
def retrieve_chunks(query: str, n_results: int = 5):

    # Create an embedding for the user's question
    query_embedding = create_embeddings([query])[0]

    # Search ChromaDB using the query embedding
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results,)

    return results