from openai import OpenAI
from DB_actions.retrieve import retrieve_chunks
from prompts import SYSTEM_PROMPT, create_rag_prompt

client = OpenAI()
MODEL = "gpt-4o-mini"

# Retrieve relevant chunks from ChromaDB and generate an answer using gpt-4o-mini
def generate_answer(query: str, n_results: int = 5):
    
    # retrieve relevatnt chunks from chromaDB
    results = retrieve_chunks(query=query, n_results=n_results)
    
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    
    # Build the context that will be sent to the LLM
    context_parts = []
    
    for i, document in enumerate(documents):
        metadata = metadatas[i]
        context_parts.append(
            f"Source: {metadata['source']}\n"
            f"Title: {metadata['title']}\n"
            f"Section: {metadata['section']}\n"
            f"URL: {metadata['url']}\n\n"
            f"Content:\n{document}"
        )

    context = "\n\n---\n\n".join(context_parts)

    # Create the user prompt
    user_prompt = create_rag_prompt(query=query, context=context)

    # Generate answer
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    answer = response.choices[0].message.content

    return answer, metadatas