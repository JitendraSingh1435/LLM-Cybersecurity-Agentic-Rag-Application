import os
import json
from tqdm import tqdm
from langchain_core.documents import Document

from data_ingestion.chunking import chunk_documents
from vectorstore.faiss_store import create_vector_store, save_vector_store


# ===============================
# 📂 LOAD PROCESSED DOCUMENTS
# ===============================
def load_processed_docs(path="data/processed/langchain_docs_v4.json"):
    print("\n📂 Loading processed LangChain documents...\n")

    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []

    # 🔥 Progress bar added here
    for item in tqdm(data, desc="📥 Loading documents"):
        doc = Document(
            page_content=item["page_content"],
            metadata=item.get("metadata", {})
        )
        documents.append(doc)

    print(f"\n✅ Loaded {len(documents)} documents from processed file")

    return documents


# ===============================
# 🚀 MAIN PIPELINE
# ===============================
def run_pipeline():
    print("🚀 Starting Processed → Chunk → FAISS Pipeline...\n")

    # 🔥 SKIP if already exists
    if os.path.exists("vectorstore/db_faiss/index.faiss"):
        print("✅ Vector DB already exists. Skipping pipeline.")
        return

    # STEP 1: LOAD
    documents = load_processed_docs()

    # STEP 2: CHUNK
    chunks = chunk_documents(documents)

    if not chunks:
        raise ValueError("❌ No chunks created. Check your data!")

    print(f"✂️ Total chunks created: {len(chunks)}")

    # STEP 3: VECTOR STORE
    print("\n🧠 Creating embeddings + FAISS index...\n")
    vectorstore = create_vector_store(chunks)

    # STEP 4: SAVE
    print("\n💾 Saving vector store...\n")
    save_vector_store(vectorstore)

    print("\n========== 🎯 PIPELINE SUMMARY ==========")
    print(f"📄 Documents Loaded: {len(documents)}")
    print(f"✂️ Chunks Created: {len(chunks)}")

    print("\n✅ Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()






# from data_ingestion.loader import load_all_documents
# from data_ingestion.chunking import chunk_documents
# from vectorstore.faiss_store import create_vector_store, save_vector_store


# def run_pipeline():
#     print("🚀 Starting Full RAG Pipeline...\n")

#     # ===============================
#     # 📘 STEP 1: LOAD DATA
#     # ===============================
#     documents = load_all_documents()

#     # ===============================
#     # ✂️ STEP 2: CHUNKING
#     # ===============================
#     chunks = chunk_documents(documents)

#     # ===============================
#     # 🧠 STEP 3: EMBEDDINGS + FAISS
#     # ===============================
#     # (Embeddings are internally used inside FAISS)
#     vectorstore = create_vector_store(chunks)

#     # ===============================
#     # 💾 STEP 4: SAVE VECTOR STORE
#     # ===============================
#     save_vector_store(vectorstore)

#     # ===============================
#     # 🎯 SUMMARY
#     # ===============================
#     print("\n========== 🎯 PIPELINE SUMMARY ==========")
#     print(f"📄 Original Docs: {len(documents)}")
#     print(f"✂️ Chunks Created: {len(chunks)}")

#     print("\n✅ Pipeline completed successfully!")


# if __name__ == "__main__":
#     run_pipeline()





# # from loader import load_all_documents
# # from chunking import chunk_documents
# # from vectorstore.faiss_store import create_vector_store, save_vector_store


# # def run_pipeline():
# #     print("🚀 Starting Full RAG Pipeline...\n")

# #     # ===============================
# #     # 📘 STEP 1: LOAD DATA
# #     # ===============================
# #     documents = load_all_documents()

# #     # ===============================
# #     # ✂️ STEP 2: CHUNKING
# #     # ===============================
# #     chunks = chunk_documents(documents)

# #     # ===============================
# #     # 🧠 STEP 3: EMBEDDINGS + FAISS
# #     # ===============================
# #     vectorstore = create_vector_store(chunks)

# #     # ===============================
# #     # 💾 STEP 4: SAVE VECTOR STORE
# #     # ===============================
# #     save_vector_store(vectorstore)

# #     print("\n🎯 Pipeline Summary:")
# #     print(f"📄 Original Docs: {len(documents)}")
# #     print(f"✂️ Chunks Created: {len(chunks)}")

# #     print("\n✅ Pipeline completed successfully!")


# # if __name__ == "__main__":
# #     run_pipeline()