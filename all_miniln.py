import os
import re
import time
from typing import List

import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import chromadb
import ollama
from langchain_ollama import OllamaEmbeddings


# ==========================================
# CONFIGURATION
# ==========================================

MIN_TEXT_THRESHOLD = 500
EMBED_MODEL = "nomic-embed-text:latest"   # Consistent embedding model
COLLECTION_NAME = "stri_saksham_db"
CHROMADB_DIR = "chromadb_store"
    
CHUNK_SIZE = 640
CHUNK_OVERLAP = 120
BATCH_SIZE = 50


# ==========================================
# PDF AUTO-DISCOVERY
# ==========================================

def get_all_pdfs_in_current_folder() -> List[str]:
    current_dir = os.getcwd()
    pdf_files = [
        f for f in os.listdir(current_dir)
        if f.lower().endswith(".pdf") and os.path.isfile(f)
    ]
    pdf_files.sort()
    return pdf_files


# ==========================================
# HYBRID PDF LOADER
# ==========================================

class HybridPdfLoader:
    def __init__(self, persist_directory=CHROMADB_DIR):
        print("=" * 60)
        print("Initializing Clean ChromaDB Knowledge Base")
        print("=" * 60)

        self.chroma_client = chromadb.PersistentClient(path=persist_directory)

        # Ensure embedding model exists
        try:
            ollama.show(EMBED_MODEL)
            print(f"Ollama embedding model available: {EMBED_MODEL}")
        except Exception:
            print(f"Pulling embedding model: {EMBED_MODEL}")
            os.system(f"ollama pull {EMBED_MODEL}")

        self.embedder = OllamaEmbeddings(model=EMBED_MODEL)

        # Always rebuild clean collection
        try:
            self.chroma_client.delete_collection(COLLECTION_NAME)
            print("Deleted existing collection.")
        except Exception:
            pass

        self.collection = self.chroma_client.create_collection(
            name=COLLECTION_NAME
        )
        print(f"Created fresh collection: {COLLECTION_NAME}")

    # --------------------------------------

    def extract_text_pymupdf(self, pdf_path: str) -> str:
        try:
            doc = fitz.open(pdf_path)
            full_text = ""

            for page in doc:
                text = page.get_text("text")
                if text:
                    text = re.sub(r"\s+", " ", text)  # Clean whitespace only
                    full_text += text + " "

            doc.close()
            return full_text.strip()

        except Exception as e:
            print(f"    PyMuPDF extraction failed: {e}")
            return ""

    # --------------------------------------

    def extract_text_ocr(self, pdf_path: str) -> str:
        try:
            print("    OCR fallback triggered")
            images = convert_from_path(pdf_path, dpi=200, fmt="jpeg")
            full_text = ""

            for img in images:
                try:
                    page_text = pytesseract.image_to_string(img, lang="eng")
                    if page_text.strip():
                        page_text = re.sub(r"\s+", " ", page_text)
                        full_text += page_text + " "
                except Exception:
                    continue

            return full_text.strip()

        except Exception as e:
            print(f"    OCR extraction failed: {e}")
            return ""

    # --------------------------------------

    def smart_extract_text(self, pdf_path: str) -> str:
        print(f"Extracting text: {pdf_path}")
        text = self.extract_text_pymupdf(pdf_path)

        if len(text) >= MIN_TEXT_THRESHOLD:
            print(f"    Extracted {len(text)} characters (PyMuPDF)")
            return text

        print(f"    Insufficient text ({len(text)} chars). Trying OCR...")
        ocr_text = self.extract_text_ocr(pdf_path)

        if len(ocr_text) > len(text):
            print(f"    Extracted {len(ocr_text)} characters (OCR)")
            return ocr_text

        return text

    # --------------------------------------

    def chunk_text(
        self,
        text: str,
        chunk_size: int = CHUNK_SIZE,
        overlap: int = CHUNK_OVERLAP
    ) -> List[str]:

        if len(text) <= chunk_size:
            return [text] if text.strip() else []

        chunks = []
        start = 0
        total_len = len(text)

        print(f"    Chunking {total_len} characters")

        while start < total_len:
            end = min(start + chunk_size, total_len)

            # Try to split at sentence boundary
            last_punct = max(
                text.rfind(".", start, end),
                text.rfind("!", start, end),
                text.rfind("?", start, end),
            )

            if last_punct > start + (chunk_size // 2):
                end = last_punct + 1

            chunk = text[start:end].strip()

            if chunk and len(chunk) > 80:
                chunks.append(chunk)

            start = end - overlap if end < total_len else end
            if start < 0:
                start = 0

        print(f"    Created {len(chunks)} chunks")
        return chunks

    # --------------------------------------

    def add_pdf_to_chromadb(self, pdf_path: str):
        full_text = self.smart_extract_text(pdf_path)

        if not full_text or len(full_text) < 200:
            print(f"    Skipping {pdf_path} (insufficient content)")
            return

        chunks = self.chunk_text(full_text)
        if not chunks:
            return

        print(f"Embedding {len(chunks)} chunks")

        pdf_name = os.path.basename(pdf_path)

        for i in range(0, len(chunks), BATCH_SIZE):
            batch_chunks = chunks[i:i + BATCH_SIZE]

            embeddings = self.embedder.embed_documents(batch_chunks)

            ids = [
                f"{pdf_name}_{i+j}_{int(time.time())}"
                for j in range(len(batch_chunks))
            ]

            metadatas = [
                {"source": pdf_name, "chunk_id": i+j}
                for j in range(len(batch_chunks))
            ]

            try:
                self.collection.add(
                    documents=batch_chunks,
                    embeddings=embeddings,
                    ids=ids,
                    metadatas=metadatas,
                )
                print(f"    Added batch {(i // BATCH_SIZE) + 1}")

            except Exception as e:
                print(f"    Batch failed: {e}")

    # --------------------------------------

    def process_all_pdfs(self, pdf_files: List[str]):
        print("\n" + "=" * 60)
        print(f"PROCESSING {len(pdf_files)} PDF FILES")
        print("=" * 60)

        start_time = time.time()

        for i, pdf_file in enumerate(pdf_files):
            print(f"\n[{i + 1}/{len(pdf_files)}] {pdf_file}")
            print("-" * 50)
            self.add_pdf_to_chromadb(pdf_file)

        total_time = time.time() - start_time

        print("\n" + "=" * 60)
        print("PROCESSING COMPLETE")
        print("=" * 60)
        print(f"Total time: {total_time:.1f}s")
        print(f"Total chunks in KB: {self.collection.count()}")
        print("=" * 60)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    pdf_files = get_all_pdfs_in_current_folder()

    if not pdf_files:
        print("No PDF files found in current directory.")
    else:
        print(f"Found {len(pdf_files)} PDF files.")
        loader = HybridPdfLoader()
        loader.process_all_pdfs(pdf_files)






