
from vectorstore.retriever import CustomRetriever
from utils.helpers import get_llm

# =========================================
# INITIALIZE ONLY ONCE
# =========================================

print("\n🤖 Loading Standard RAG...\n")

retriever = CustomRetriever(k=8)

# =========================================
# STANDARD RAG PIPELINE
# =========================================

def basic_rag_pipeline(query: str, model_choice: str = "ollama"):

    try:
        
        llm = get_llm(model_choice)

        docs = retriever.get_relevant_documents(query)

        # Context
        context = "\n\n".join([
            doc.page_content for doc in docs
        ])

        # Sources
        sources = []

        for doc in docs:

            if "source" in doc.metadata:
                sources.append(doc.metadata["source"])

        # Prompt
        prompt = f"""

    You are a cybersecurity assistant designed to answer questions strictly based on retrieved context.

    ----------------------------------
    📌 INSTRUCTIONS:
    ----------------------------------
    - Carefully read the provided context before answering.
    - Your answer must be fully grounded in the context.

    ----------------------------------
    🔒 STRICT RULES:
    ----------------------------------

    -> Keep the answer clear, concise, and directly relevant to the question.
    -> If source information is available in metadata, include it.
    -> Do NOT generate or assume sources if they are not present in the metadata.
    -> Do NOT repeat the same information multiple times.
    -> If you are providing steps or a list, use bullet points (e.g., * Step 1) and keep each step on a new line with proper spacing.
    -> Keep formatting clean and readable.
    -> Use short paragraphs where needed.
    ------------------------------
    Give summary of overall answer at the last after 2 line spacing.
    ------------------------------


Context:
{context}

Question:
{query}

Answer:
"""

        # LLM Response
        response = llm.invoke(prompt)
        if hasattr(response, 'content'):
            response = response.content

        return {
            "answer": response,
            "context": context,
            "sources": sources
        }

    except Exception as e:

        return {
            "answer": f"Error: {str(e)}",
            "context": "",
            "sources": []
        }


# # from vectorstore.retriever import load_vector_store, get_retriever
# from multiprocessing import context

# from vectorstore.retriever import CustomRetriever
# # from langchain.llms import Ollama  # or use any LLM
# # from langchain_community.llms import Ollama
# from langchain_community.llms import Ollama


# def create_rag_chain():
#     print("\n🤖 Initializing RAG pipeline...\n")

#     # vectorstore = load_vector_store()
#     # retriever = CustomRetriever(vectorstore, k=3)
#     retriever = CustomRetriever(k=8)

#     llm = Ollama(model="mistral:latest")  # or llama3
#     # llm = Ollama(model="llama3")  # or llama3

#     return retriever, llm

# def answer_query(query, retriever, llm):
#     docs = retriever.get_relevant_documents(query)

#     # 🔥 DEBUG: show retrieved docs
#     print("\n🔍 Retrieved Context Preview:\n")
#     for i, doc in enumerate(docs):
#         print(f"\n--- Doc {i+1} ---")
#         print(doc.page_content[:200])
#         print("Metadata:", doc.metadata)

#     context = "\n\n".join([doc.page_content for doc in docs])






#     # print("\n📚 CONTEXT:\n")
#     # print(context[:2000])


#     # 🔥 STRONG ANTI-HALLUCINATION PROMPT

#     prompt = f"""
    
#     You are a cybersecurity assistant designed to answer questions strictly based on retrieved context.

#     -----------------------------
#     📌 INSTRUCTIONS:
#     -----------------------------
#     - Carefully read the provided context before answering.
#     - Your answer must be fully grounded in the context.

#     -----------------------------
#     🔒 STRICT RULES:
#     -----------------------------
#     1. Use ONLY the information provided in the context to answer the question.
#     2. If the context does NOT contain sufficient information, respond exactly with:
#     "I can't answer this, not found in context".
#     3. Do NOT use any prior knowledge, assumptions, or external information.
#     4. Do NOT make up or infer details that are not explicitly stated in the context.
#     5. Keep the answer clear, concise, and directly relevant to the question.
#     6. If multiple relevant points exist, summarize them briefly.
#     7. If source information is available in metadata, include it.
#     8. Do NOT generate or assume sources if they are not present in the metadata.
#     9. Do NOT repeat the same information multiple times.

#     --------------------------------
#     Give summary of overall answer at the last.
#     --------------------------------

    

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#     response = llm.invoke(prompt)

#     # 🔥 Hallucination warning
#     if "I can't answer this, not found in context" not in response and len(docs) == 0:
#         print("\n⚠️ WARNING: Possible hallucination")

#     return response, context





    # You are a cybersecurity assistant.

    # Firstly use the information provided in the context below to answer the question.
    # If the context does not contain the answer, respond it with your own knowledge.



    # You are a cybersecurity assistant.

    # *** Strict Rules to answer the question: ***

    # 1. Only use the information provided in the context below to answer the question.
    # 2. If the context does not contain the answer, respond with "I don't know".
    # 3. Do not make up answers or use any information not present in the context.
    # 4. Be concise and to the point.
    # 5. If source is available in metadata, include it. Otherwise do not generate sources.
    # 6. Do not make up answers by your own knowledgebase.





    # 📌 STRICT RULES:

    # 1. First, try to answer using ONLY the information in the given context.
    # 2. If the context contains the answer → respond based ONLY on the context.
    # 3. If the context does NOT contain the answer → you MAY use your own knowledge.
    # 4. If using your own knowledge, you MUST clearly state:
    #     "⚠️ This answer is based on my general knowledge, not from the retrieved context."
    # 5. Do NOT mix context-based and general knowledge in the same answer.
    # 6. Be clear, concise, and structured.
    # 7. Do NOT generate fake sources or links.
    


    #  1. Use ONLY the information provided in the context to answer the question.
    # 2. If the context does NOT contain sufficient information, respond exactly with:
    # "I can't answer this, not found in context".
    # 3. Do NOT use any prior knowledge, assumptions, or external information.
    # 4. Do NOT make up or infer details that are not explicitly stated in the context.
    # 5. Keep the answer clear, concise, and directly relevant to the question.
    # 6. If multiple relevant points exist, summarize them briefly.
    # 7. If source information is available in metadata, include it.
    # 8. Do NOT generate or assume sources if they are not present in the metadata.
    # 9. Do NOT repeat the same information multiple times.
    # 10. If answer contains steps, keep them on separate lines.
    # 11. Keep formatting clean and readable.
    # 12. Use short paragraphs where needed.




    # 1. Answer using ONLY the information in the given context.
    # 4. Keep the answer clear, concise, and directly relevant to the question.
    # 5. If multiple relevant points exist, summarize them briefly.
    # 6. If source information is available in metadata, include it.
    # 7. Do NOT generate or assume sources if they are not present in the metadata.
    # 8. Do NOT repeat the same information multiple times.
    # 9. If you are providing steps or a list, use bullet points (e.g., * Step 1) and keep each step on a new line with proper spacing.
    # 10. Keep formatting clean and readable.
    # 11. Use short paragraphs where needed.

    # --------------------------------
    # Give summary of overall answer at the last.
    # --------------------------------





    # --------------------------------------------------------------------------------------------------------------------------------

     