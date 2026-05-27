
from vectorstore.retriever import CustomRetriever
from utils.helpers import get_llm

from agentic_rag.tools.more_tool import rewrite_query

# =========================================
# INITIALIZE
# =========================================

print("\n🤖 Loading Agentic RAG...\n")

retriever = CustomRetriever(k=8)


# =========================================
# AGENTIC RAG PIPELINE
# =========================================

def agentic_rag_pipeline(query: str, model_choice: str = "ollama"):

    try:
        llm = get_llm(model_choice)

        # =================================
        # STEP 1 — Query Rewriting
        # =================================

        rewritten_queries = rewrite_query(query)

        # =================================
        # STEP 2 — Multi Retrieval
        # =================================

        contexts = []

        all_sources = []

        for q in rewritten_queries:

            docs = retriever.get_relevant_documents(q)

            for doc in docs[:2]:

                contexts.append(doc.page_content)

                if "source" in doc.metadata:
                    all_sources.append(doc.metadata["source"])

        # =================================
        # STEP 3 — Aggregate Context
        # =================================

        final_context = "\n\n".join(contexts)

        # =================================
        # STEP 4 — Agent Prompt
        # =================================

        prompt = f"""

        You are a cybersecurity assistant designed to answer questions related to Cybersecurity and general kind of frauds and scams type of questions.

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
{final_context}

Question:
 {query}

Answer:
"""

        # =================================
        # STEP 5 — Generate
        # =================================

        answer = llm.invoke(prompt)
        if hasattr(answer, 'content'):
            answer = answer.content

        # =================================
        # STEP 6 — Confidence Check
        # =================================

        if len(final_context.strip()) < 50:

            answer = "⚠️ Low confidence answer (insufficient context)"

        return {
            "answer": answer,
            "context": final_context,
            "sources": list(set(all_sources)),
            "rewritten_queries": rewritten_queries
        }

    except Exception as e:

        return {
            "answer": f"Error: {str(e)}",
            "context": "",    
            "sources": [],
            "rewritten_queries": []
        }


# You are an advanced cybersecurity AI assistant.

# Your primary task is to answer using the retrieved cybersecurity context.

# Rules:
# 1. Use retrieved context as primary evidence.
# 2. If context is partially relevant, provide a grounded practical answer.
# 3. Avoid unsupported technical claims.
# 4. If context is completely unrelated, say:
#    "I can't answer this, not found in context"
# 5. Prefer practical cybersecurity advice and safe guidance.



# ------------------------------------------------------

# from agentic_rag.tools.more_tool import rewrite_query


# def agentic_rag_pipeline(query: str, retriever, llm):

#     # Step 1: Rewrite query
#     queries = rewrite_query(query)

#     # Step 2: Multi-retrieval
#     contexts = []
#     for q in queries:
#         docs = retriever.get_relevant_documents(q)
#         context = "\n".join([doc.page_content for doc in docs[:2]])
#         contexts.append(context)

#     # Step 3: Aggregate context
#     final_context = "\n\n".join(contexts)

#     # Step 4: LLM reasoning
#     prompt = f"""
# You are a cybersecurity expert.

# Use ONLY the context below to answer.

# Context:
# {final_context}

# Question:
# {query}
# """

#     answer = llm.invoke(prompt)

#     # Step 5: Simple verification
#     if len(final_context.strip()) < 50:
#         return "⚠️ Low confidence answer (insufficient context)"

#     return answer, final_context


#  You are a cybersecurity assistant designed to answer questions strictly based on retrieved context.

#         -----------------------------
#         📌 INSTRUCTIONS:
#         -----------------------------
#         - Carefully read the provided context before answering.
#         - Your answer must be fully grounded in the context.

#         -----------------------------
#         🔒 STRICT RULES:
#         -----------------------------
#         1. Answer using ONLY the information in the given context.
#         4. Keep the answer clear, concise, and directly relevant to the question.
#         5. If multiple relevant points exist, summarize them briefly.
#         6. If source information is available in metadata, include it.
#         7. Do NOT generate or assume sources if they are not present in the metadata.
#         8. Do NOT repeat the same information multiple times.
#         9. If you are providing steps or a list, use bullet points (e.g., * Step 1) and keep each step on a new line with proper spacing.
#         10. Keep formatting clean and readable.
#         11. Use short paragraphs where needed.

#         --------------------------------
#         Give summary of overall answer at the last.
#         --------------------------------

# --------------------------------------------------------------------------------------------------------------------------

