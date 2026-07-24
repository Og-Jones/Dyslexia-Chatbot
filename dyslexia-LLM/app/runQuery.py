from generate import generate_answer

def main():

    query = input(
        "Ask a question about dyslexia: "
    )

    answer, sources = generate_answer(
        query=query,
        n_results=5,
    )

    print("\nAnswer:")
    print(answer)

    print("\nSources:")

    # Avoid displaying duplicate sources
    displayed_sources = set()

    for source in sources:

        source_key = (
            source["title"],
            source["section"],
            source["url"],
        )

        if source_key in displayed_sources:
            continue

        displayed_sources.add(source_key)

        print(
            f"\n- {source['title']}"
        )

        print(
            f"  Section: {source['section']}"
        )

        print(
            f"  URL: {source['url']}"
        )


if __name__ == "__main__":
    main()