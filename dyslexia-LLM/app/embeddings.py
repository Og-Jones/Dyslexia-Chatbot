from openai import OpenAI
from cleantext import clean
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBEDDING_MODEL = "text-embedding-3-small"

# Use openai embedding endpoint to turn text into embeddings
def create_embeddings(texts: list[str]) -> list[list[float]]:
    
    # clean-text library
    cleaned_texts = [
        clean(
            texts,
            fix_unicode=True,
            to_ascii=False,
            lower=False,
            no_line_breaks=True,
            no_urls=False,
            no_emails=False,
            no_phone_numbers=False,
            no_numbers=False,
            no_digits=False,
            no_currency_symbols=False,
            no_punct=False,
            replace_with_punct=" ",
            replace_with_url=" ",
            replace_with_email=" ",
        ).strip()
        for text in texts
    ]

    if not cleaned_texts:
        raise ValueError("Cannot embed empty text.")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=cleaned_texts,
    )

    return [item.embedding for item in response.data]