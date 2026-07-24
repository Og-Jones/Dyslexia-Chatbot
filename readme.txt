Workflow for a user prompt

1. User asks question
2. Vector embedding is created for that question
3. Search ChromaDB database for stored text embeddings
- compare user query embedding to stored embeddings via semantic similarity
- retrieve top 5 most semantically similar chunks
4. Build the prompt context from those 5 chunks
5. Insert the question + context into prompt
6. Send the prompt to OpenAI GPT mini
7. GPT generates response and sends back