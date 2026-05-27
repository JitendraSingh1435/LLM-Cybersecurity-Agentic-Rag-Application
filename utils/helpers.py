
from sentence_transformers import CrossEncoder


class CrossEncoderReranker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        print("⚡ Loading Cross-Encoder Reranker...")
        self.model = CrossEncoder(model_name)

    def rerank(self, query, docs, top_k=5):
        if not docs:
            return []

        print("🔄 Reranking documents...")

        pairs = [(query, doc.page_content) for doc in docs]

        scores = self.model.predict(pairs)

        scored_docs = list(zip(docs, scores))

        ranked_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)

        top_docs = [doc for doc, score in ranked_docs[:top_k]]

        print(f"✅ Top-{top_k} documents selected after reranking")

        return top_docs

# ------------------------------------------------------------------------------------------------------------------------------------



# from sentence_transformers import CrossEncoder

# class CrossEncoderReranker:
#     def __init__(self):
#         print("⚡ Loading Cross-Encoder Reranker...")
#         self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

#     def rerank(self, query, docs, top_k=5):
#         pairs = [(query, doc.page_content) for doc in docs]

#         scores = self.model.predict(pairs)

#         # attach scores
#         scored_docs = list(zip(docs, scores))

#         # sort by score
#         ranked_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)

#         # return top_k docs
#        return [doc for doc, score in ranked_docs[:top_k]]

from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm(model_choice="ollama"):
    if model_choice == "gemini":
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    else:
        return Ollama(model="mistral:latest")