
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents):
    print("\n✂️ Smart chunking started...\n")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,              # 🔥 increased
        chunk_overlap=150,           # 🔥 better context retention
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunked_docs = []

    for doc in documents:
        source_type = doc.metadata.get("source_type")

        # ===============================
        # 📘 BOOKS (heavy chunking)
        # ===============================
        if source_type == "book":
            chunks = splitter.split_documents([doc])

            for chunk in chunks:
                chunk.metadata.update(doc.metadata)  # preserve metadata

            chunked_docs.extend(chunks)

        # ===============================
        # 🛡️ CISA (threat_intel)
        # ===============================
        elif source_type == "threat_intel":
            # Usually already structured → minimal splitting
            if len(doc.page_content) > 1200:
                chunks = splitter.split_documents([doc])

                for chunk in chunks:
                    chunk.metadata.update(doc.metadata)
                chunked_docs.extend(chunks)
            else:
                chunked_docs.append(doc)

        # ===============================
        # 🧨 NVD (more verbose than CISA)
        # ===============================
        elif source_type == "nvd":
            # NVD descriptions can be long → moderate chunking
            if len(doc.page_content) > 800:
                chunks = splitter.split_documents([doc])

                for chunk in chunks:
                    chunk.metadata.update(doc.metadata)

                chunked_docs.extend(chunks)
            else:
                chunked_docs.append(doc)


        # if source_type == "book":
        #     chunks = splitter.split_documents([doc])

        #     for chunk in chunks:
        #         chunk.metadata.update(doc.metadata)  # 🔥 preserve metadata

        #     chunked_docs.extend(chunks)

        # elif source_type == "threat_intel":
        #     # 🔥 Slight splitting for long CVE entries
        #     if len(doc.page_content) > 1000:
        #         chunks = splitter.split_documents([doc])
        #         for chunk in chunks:
        #             chunk.metadata.update(doc.metadata)
        #         chunked_docs.extend(chunks)
        #     else:
        #         chunked_docs.append(doc)

    print(f"✅ Total chunks: {len(chunked_docs)}")
    return chunked_docs










# from langchain_text_splitters import RecursiveCharacterTextSplitter

# def chunk_documents(documents):
#     print("\n✂️ Smart chunking started...\n")

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=800,
#         chunk_overlap=150,
#         separators=["\n\n", "\n", ".", " ", ""]
#     )

#     chunked_docs = []

#     for doc in documents:
#         # Only chunk books
#         if doc.metadata.get("source_type") == "book":
#             chunks = splitter.split_documents([doc])
#             chunked_docs.extend(chunks)
#         else:
#             # Keep CISA & NVD as-is
#             chunked_docs.append(doc)

#     print(f"✅ Total chunks: {len(chunked_docs)}")

#     return chunked_docs