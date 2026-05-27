from langchain_community.embeddings import HuggingFaceEmbeddings
import os


def get_embedding_model():
    print("\n🧠 Loading LOCAL MiniLM embedding model...\n")

    # model_path = os.path.abspath("models/nomic-embed")
    model_path = os.path.abspath("embeddings\emb_model\MiniLM+embeddings_model\emb_model")  # ✅ LOCAL PATH

    model = HuggingFaceEmbeddings(
        model_name=model_path,   # ✅ LOCAL PATH
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True,
            "batch_size": 64
        }
    )

    print(f"✅ Local embedding model loaded from: {model_path}")

    return model



# -------------------------------------------------- Nomin Embedding Model (LOCAL) --------------------------------------------------


# from langchain_community.embeddings import OllamaEmbeddings


# def get_embedding_model():
#     print("\n🚀 Loading Nomic Embedding Model via Ollama...\n")

#     model = OllamaEmbeddings(
#         model="nomic-embed-text:latest"
#     )

#     print("✅ Nomic embedding model loaded (Ollama)")

#     return model





# ----------------------------------------------------------------------------------------------------------------------------------------------
# from langchain_community.embeddings import HuggingFaceEmbeddings
# import os


# def get_embedding_model():
#     print("\n🧠 Loading LOCAL Nomic embedding model...\n")

#     # model_path = os.path.abspath("models/nomic-embed")
#     model_path = os.path.abspath("embeddings/emb_model/nomic_embeddings_model/model")  # ✅ LOCAL PATH

#     model = HuggingFaceEmbeddings(
#         model_name=model_path,   # ✅ LOCAL PATH
#         model_kwargs={
#             "device": "cpu",
#             "trust_remote_code": True
#         },
#         encode_kwargs={
#             "normalize_embeddings": True,
#             "batch_size": 64
#         }
#     )

#     print(f"✅ Local embedding model loaded from: {model_path}")

#     return model









# ---------------------------------------------------------------------------------------------------------------------

# from langchain_community.embeddings import HuggingFaceEmbeddings


# def get_embedding_model():
#     print("\n🧠 Loading Nomic embedding model...\n")

#     model = HuggingFaceEmbeddings(
#         model_name="nomic-ai/nomic-embed-text-v1.5",
#         model_kwargs={"device": "cpu", "trust_remote_code": True},
#         encode_kwargs={
#             "normalize_embeddings": True,
#             "batch_size": 32}
#     )

#     print("✅ Nomic embedding model ready!")

#     return model