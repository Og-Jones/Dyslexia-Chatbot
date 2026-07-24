from sources.wikipedia_source import get_article

document = get_article("Dyslexia")

print(document.title)
print(document.url)
print(document.text[:1_000])