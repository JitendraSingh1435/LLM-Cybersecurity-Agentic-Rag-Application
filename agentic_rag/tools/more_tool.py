def rewrite_query(query: str):
    return [
        query,
        f"Explain in detail: {query}",
        f"Technical explanation of {query}",
        f"Cybersecurity perspective of {query}"
    ]