

from standard_rag.basic_rag import create_rag_chain, answer_query
from agentic_rag.agent_graph import agentic_rag_pipeline
# from evaluation.ragas_eval import evaluate_single



def run_rag():
    print("\n🚀 Starting RAG + Agentic RAG System...\n")

    # Load Simple RAG components
    retriever, llm = create_rag_chain()

    print("\n✅ System Ready! Ask your questions.\n")

    while True:
        query = input("\n💬 Ask your question (type 'exit'): ")

        if query.lower() == "exit":
            break

        # 🔹 Simple RAG Answer
        # simple_answer = answer_query(query, retriever, llm)
        simple_answer, simple_context = answer_query(query, retriever, llm)

        # 🔹 Agentic RAG Answer (NEW)
        agentic_answer, agentic_context = agentic_rag_pipeline(query, retriever, llm)

        # 🔹 Separate Evaluation
        # simple_metrics = evaluate_single(query, simple_answer, simple_context)
        # agentic_metrics = evaluate_single(query, agentic_answer, agentic_context)

        
        # 🔥 OUTPUT
        print("\n" + "="*70)

        print("🔹 Simple RAG Answer:\n")
        print(simple_answer)

        # print("\n📊 Simple RAG Metrics:\n")
        # print(simple_metrics)

        print("\n" + "-"*70)

        print("🔹 Agentic RAG Answer:\n")
        print(agentic_answer)

        # print("\n📊 Agentic RAG Metrics:\n")
        # print(agentic_metrics)

        print("\n" + "="*70)


if __name__ == "__main__":
    run_rag()







# from standard_rag.basic_rag import create_rag_chain, answer_query
# from agentic_rag.agent_graph import agentic_rag_pipeline


# def run_rag():
#     print("\n🚀 Starting Basic RAG System...\n")

#     retriever, llm = create_rag_chain()

#     print("\n✅ System Ready! Ask your questions.\n")
    
#     while True:
#         query = input("\n💬 Ask your question (type 'exit'): ")

#         if query.lower() == "exit":
#             break

#         answer = answer_query(query, retriever, llm)

#         print("\n🧠 Answer:\n")
#         print(answer)
    
#         print("\n" + "="*60)


# if __name__ == "__main__":
#     run_rag()