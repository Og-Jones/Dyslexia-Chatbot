from sources.wikipedia_source import get_article
from chunking import chunk_text

article = get_article("Dyslexia")

all_chunks = []

all_chunks.extend(
    chunk_text(
        title=article.title,
        url=article.url,
        section="Summary",
        text=article.summary,
    )
)

for section in article.sections:
    all_chunks.extend(
        chunk_text(
            title=article.title,
            url=article.url,
            section=section.title,
            text=section.text,
        )
    )

print(f"Article: {article.title}")
print(f"Sections: {len(article.sections)}")
print(f"Chunks: {len(all_chunks)}")

for chunk in all_chunks[:3]:
    print("\n---")
    print(chunk.chunk_id)
    print(chunk.section)
    print(chunk.text[:5000])