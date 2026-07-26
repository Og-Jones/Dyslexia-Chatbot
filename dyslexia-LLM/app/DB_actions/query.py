import chromadb

client = chromadb.PersistentClient(path="../chroma_db")
collection = client.get_collection(name="dyslexia_knowledge")

print(f"Number of stored chunks: {collection.count()}")

results = collection.get(
    include=[
        "documents",
        "metadatas",
    ]
)

for i, document in enumerate(results["documents"]):

    print("\n" + "=" * 60)

    print(f"ID: {results['ids'][i]}")

    print(f"\nMetadata:")
    print(results["metadatas"][i])

    print(f"\nDocument:")
    print(document)