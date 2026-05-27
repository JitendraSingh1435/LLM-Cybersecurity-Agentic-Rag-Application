from standard_rag.basic_rag import simple_rag_pipeline
from standard_rag.basic_rag import retriever  # if accessible


def search_rag(query: str, k: int = 3):
    docs = retriever.get_relevant_documents(query)

    context = "\n".join([doc.page_content for doc in docs[:k]])

    return context