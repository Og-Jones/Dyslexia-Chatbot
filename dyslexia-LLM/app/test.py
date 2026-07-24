from embeddings import create_embeddings

texts = [ "Dyslexia is a learning difference that primarily affects reading and spelling.", "People with dyslexia may have difficulties with phonological processing.", ]

embeddings = create_embeddings(texts)

print(f"Number of embeddings: {len(embeddings)}") 

for i, embedding in enumerate(embeddings): 
    print(f"\nEmbedding {i + 1}:") 
    print(f"Type: {type(embedding)}") 
    print(f"Dimensions: {len(embedding)}") 
    print(f"First 10 values: {embedding[:10]}")