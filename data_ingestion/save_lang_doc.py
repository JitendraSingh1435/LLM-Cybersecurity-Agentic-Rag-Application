import os
import json
from tqdm import tqdm
from loader import load_all_documents


def save_documents(docs, file_path):
    print(f"\n💾 Saving documents to {file_path}")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    data = []

    for doc in tqdm(docs, desc="💾 Saving documents"):
        data.append({
            "page_content": doc.page_content.strip(),
            "metadata": doc.metadata
        })

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✅ Documents saved successfully!")


if __name__ == "__main__":
    all_docs = load_all_documents()

    print(f"📂 Total documents to save: {len(all_docs)}")

    save_documents(all_docs, "../data/processed/langchain_docs_v4.json")