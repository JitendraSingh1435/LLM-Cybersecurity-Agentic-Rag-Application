
import os
import json
import re
from tqdm import tqdm
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# OCR imports
import pytesseract
from pdf2image import convert_from_path


# ===============================
# 🔥 TEXT SPLITTER (GLOBAL)
# ===============================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50
)


# ===============================
# 🔥 HELPER FUNCTIONS
# ===============================
def extract_attack_type(text):
    text = text.lower()

    if "remote code execution" in text or "rce" in text:
        return "RCE"
    elif "xss" in text or "cross-site scripting" in text:
        return "XSS"
    elif "sql injection" in text:
        return "SQL Injection"
    elif "csrf" in text:
        return "CSRF"
    elif "directory traversal" in text or "path traversal" in text:
        return "Path Traversal"
    elif "use-after-free" in text:
        return "Use-After-Free"
    elif "out-of-bounds" in text or "oob" in text:
        return "Buffer Overflow"
    elif "null pointer" in text:
        return "Null Pointer Dereference"
    elif "race condition" in text:
        return "Race Condition"
    elif "memory leak" in text:
        return "Memory Leak"
    elif "integer overflow" in text:
        return "Integer Overflow"
    elif "denial of service" in text or "dos" in text:
        return "DoS"
    else:
        return "Unknown"


def extract_year(date_str):
    if not date_str:
        return None
    return int(date_str[:4])


def clean_text(text):
    return " ".join(text.strip().split()) if text else ""


def extract_product(text):
    text = text.lower()

    if "linux kernel" in text:
        return "Linux Kernel"
    elif "wordpress" in text:
        return "WordPress"
    elif "apache" in text:
        return "Apache"
    elif "nginx" in text:
        return "Nginx"
    elif "openssl" in text:
        return "OpenSSL"
    elif "docker" in text:
        return "Docker"
    elif "kubernetes" in text:
        return "Kubernetes"

    match = re.search(r"in ([a-zA-Z0-9\-\s]+?)(?:,|\.|\s)", text)
    if match:
        return match.group(1).strip().title()

    return "Unknown"


def generate_tags(text, attack_type, product):
    text = text.lower()
    tags = set()

    if attack_type != "Unknown":
        tags.add(attack_type.lower())

    if product != "Unknown":
        tags.add(product.lower())

    if "kernel" in text:
        tags.add("kernel")
    if "network" in text:
        tags.add("network")
    if "memory" in text:
        tags.add("memory")
    if "overflow" in text:
        tags.add("overflow")

    return list(tags)


# ===============================
# 🔥 CVSS EXTRACTION (FIXED)
# ===============================
def extract_cvss(metrics):
    cvss_score = None
    severity = None

    try:
        if "cvssMetricV31" in metrics:
            data = metrics["cvssMetricV31"][0]["cvssData"]
        elif "cvssMetricV30" in metrics:
            data = metrics["cvssMetricV30"][0]["cvssData"]
        elif "cvssMetricV2" in metrics:
            data = metrics["cvssMetricV2"][0]["cvssData"]
        else:
            return None, None

        cvss_score = data.get("baseScore")
        severity = data.get("baseSeverity")

    except Exception:
        pass

    return cvss_score, severity


# ===============================
# OCR FUNCTION
# ===============================
def extract_text_with_ocr(pdf_path):
    text = ""
    try:
        images = convert_from_path(pdf_path)
        for img in tqdm(images, desc="📝 OCR Pages", leave=False):
            text += pytesseract.image_to_string(img)
    except Exception as e:
        print(f"❌ OCR failed: {e}")
    return text


# ===============================
# BOOKS LOADER
# ===============================
def load_books(data_path: str):
    documents = []

    all_files = []
    for root, _, files in os.walk(data_path):
        for f in files:
            all_files.append(os.path.join(root, f))

    print(f"\n📂 Total book files: {len(all_files)}")

    for path in tqdm(all_files, desc="📘 Loading Books"):
        try:
            if path.endswith(".pdf"):
                loader = PyPDFLoader(path)
                docs = loader.load()

                for d in docs:
                    text = clean_text(d.page_content)
                    chunks = text_splitter.split_text(text)

                    for i, chunk in enumerate(chunks):
                        documents.append(
                            Document(
                                page_content=chunk,
                                metadata={
                                    "source": path,
                                    "source_type": "book",
                                    "category": "cybersecurity_text",
                                    "doc_id": os.path.basename(path),
                                    "chunk_id": f"{os.path.basename(path)}_{i}",
                                    "tags": ["cybersecurity", "theory"],
                                }
                            )
                        )

        except Exception as e:
            print(f"❌ Error loading {path}: {e}")

    print(f"✅ Total book documents: {len(documents)}")
    return documents


# ===============================
# CISA LOADER
# ===============================
def load_cisa(file_path: str):
    documents = []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    vulnerabilities = data.get("vulnerabilities", [])

    for item in tqdm(vulnerabilities, desc="🛡️ Loading CISA KEV"):
        desc = clean_text(item.get("shortDescription", ""))

        attack_type = extract_attack_type(desc)
        product = item.get("product") or extract_product(desc)
        tags = generate_tags(desc, attack_type, product)

        chunks = text_splitter.split_text(desc)

        for i, chunk in enumerate(chunks):
            documents.append(
                Document(
                    page_content=f"{chunk} (CVE: {item.get('cveID')})",
                    metadata={
                        "cve_id": item.get("cveID"),
                        "vendor": item.get("vendorProject"),
                        "product": product,
                        "attack_type": attack_type,
                        "tags": tags,
                        "source": "CISA",
                        "source_type": "threat_intel",
                        "year": extract_year(item.get("dateAdded")),
                        "doc_id": item.get("cveID"),
                        "chunk_id": f"{item.get('cveID')}_{i}"
                    }
                )
            )

    return documents


# ===============================
# NVD LOADER (FIXED)
# ===============================
def load_nvd(file_paths: list):
    documents = []

    for file_path in file_paths:
        print(f"\n📂 Processing: {os.path.basename(file_path)}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        vulnerabilities = data.get("vulnerabilities", [])

        for item in tqdm(vulnerabilities, desc=f"🧨 {os.path.basename(file_path)}"):
            cve = item.get("cve", {})

            desc = ""
            for d in cve.get("descriptions", []):
                if d.get("lang") == "en":
                    desc = d.get("value")

            desc = clean_text(desc)

            attack_type = extract_attack_type(desc)
            product = extract_product(desc)
            tags = generate_tags(desc, attack_type, product)

            # ✅ FIXED
            metrics = cve.get("metrics", {})
            cvss_score, severity = extract_cvss(metrics)

            chunks = text_splitter.split_text(desc)

            for i, chunk in enumerate(chunks):  # ✅ FIXED (enumerate)
                documents.append(
                    Document(
                        page_content=f"{chunk} (CVE: {cve.get('id')})",
                        metadata={
                            "cve_id": cve.get("id"),
                            "attack_type": attack_type,
                            "product": product,
                            "tags": tags,
                            "year": extract_year(cve.get("published")),
                            "source": "NVD",
                            "source_type": "threat_intel",
                            "cvss_score": cvss_score,
                            "severity": severity,
                            "doc_id": cve.get("id"),
                            "chunk_id": f"{cve.get('id')}_{i}"
                        }
                    )
                )

    return documents


# ===============================
# MAIN LOADER
# ===============================
def load_all_documents():
    print("🚀 Starting Data Loading...\n")

    books = load_books("../data/raw/books")
    cisa = load_cisa("../data/raw/cisa/known_exploited_vulnerabilities.json")
    nvd = load_nvd([
        "../data/raw/nvd/nvdcve-2.0-modified.json",
        "../data/raw/nvd/nvdcve-2.0-recent.json"
    ])

    all_docs = books + cisa + nvd

    # 🔥 Deduplication
    unique_docs = {}
    for doc in all_docs:
        key = doc.page_content.strip()
        if key not in unique_docs:
            unique_docs[key] = doc

    final_docs = list(unique_docs.values())

    print(f"\n🧹 After Deduplication: {len(final_docs)} documents")

    return final_docs


# import os
# import json
# import re
# from tqdm import tqdm
# from langchain_community.document_loaders import PyPDFLoader, TextLoader
# from langchain_core.documents import Document
# # from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_text_splitters import RecursiveCharacterTextSplitter


# # OCR imports
# import pytesseract
# from pdf2image import convert_from_path


# # ===============================
# # 🔥 TEXT SPLITTER (GLOBAL)
# # ===============================
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=400,
#     chunk_overlap=50
# )


# # ===============================
# # 🔥 HELPER FUNCTIONS
# # ===============================
# def extract_attack_type(text):
#     text = text.lower()

#     if "remote code execution" in text or "rce" in text:
#         return "RCE"
#     elif "xss" in text or "cross-site scripting" in text:
#         return "XSS"
#     elif "sql injection" in text:
#         return "SQL Injection"
#     elif "csrf" in text:
#         return "CSRF"
#     elif "directory traversal" in text or "path traversal" in text:
#         return "Path Traversal"
#     elif "use-after-free" in text:
#         return "Use-After-Free"
#     elif "out-of-bounds" in text or "oob" in text:
#         return "Buffer Overflow"
#     elif "null pointer" in text:
#         return "Null Pointer Dereference"
#     elif "race condition" in text:
#         return "Race Condition"
#     elif "memory leak" in text:
#         return "Memory Leak"
#     elif "integer overflow" in text:
#         return "Integer Overflow"
#     elif "denial of service" in text or "dos" in text:
#         return "DoS"
#     else:
#         return "Unknown"


# def extract_year(date_str):
#     if not date_str:
#         return None
#     return int(date_str[:4])


# def clean_text(text):
#     return " ".join(text.strip().split())


# def extract_product(text):
#     text = text.lower()

#     if "linux kernel" in text:
#         return "Linux Kernel"
#     elif "wordpress" in text:
#         return "WordPress"
#     elif "apache" in text:
#         return "Apache"
#     elif "nginx" in text:
#         return "Nginx"
#     elif "openssl" in text:
#         return "OpenSSL"
#     elif "docker" in text:
#         return "Docker"
#     elif "kubernetes" in text:
#         return "Kubernetes"

#     match = re.search(r"in ([a-zA-Z0-9\-\s]+?)(?:,|\.|\s)", text)
#     if match:
#         return match.group(1).strip().title()

#     return "Unknown"


# def generate_tags(text, attack_type, product):
#     text = text.lower()
#     tags = set()

#     if attack_type != "Unknown":
#         tags.add(attack_type.lower())

#     if product != "Unknown":
#         tags.add(product.lower())

#     if "kernel" in text:
#         tags.add("kernel")
#     if "network" in text:
#         tags.add("network")
#     if "memory" in text:
#         tags.add("memory")
#     if "overflow" in text:
#         tags.add("overflow")

#     return list(tags)


# # ===============================
# # OCR FUNCTION
# # ===============================
# def extract_text_with_ocr(pdf_path):
#     text = ""
#     try:
#         images = convert_from_path(pdf_path)
#         for img in tqdm(images, desc="📝 OCR Pages", leave=False):
#             text += pytesseract.image_to_string(img)
#     except Exception as e:
#         print(f"❌ OCR failed: {e}")
#     return text


# # ===============================
# # BOOKS LOADER
# # ===============================
# def load_books(data_path: str):
#     documents = []

#     all_files = []
#     for root, _, files in os.walk(data_path):
#         for f in files:
#             all_files.append(os.path.join(root, f))

#     print(f"\n📂 Total book files: {len(all_files)}")

#     for path in tqdm(all_files, desc="📘 Loading Books"):

#         try:
#             if path.endswith(".pdf"):
#                 loader = PyPDFLoader(path)
#                 docs = loader.load()

#                 for d in tqdm(docs, desc="📄 PDF Pages", leave=False):
#                     text = clean_text(d.page_content)

#                     chunks = text_splitter.split_text(text)

#                     for chunk in chunks:
#                         documents.append(
#                             Document(
#                                 page_content=chunk,
#                                 metadata={
#                                     "source": path,
#                                     "source_type": "book",
#                                     "category": "cybersecurity_text",
#                                     "doc_id": os.path.basename(path),
#                                     "tags": ["cybersecurity", "theory"],
#                                 }
#                             )
#                         )

#             elif path.endswith(".txt"):
#                 loader = TextLoader(path)
#                 docs = loader.load()

#                 for d in tqdm(docs, desc="📄 TXT Chunks", leave=False):
#                     text = clean_text(d.page_content)

#                     chunks = text_splitter.split_text(text)

#                     for chunk in chunks:
#                         documents.append(
#                             Document(
#                                 page_content=chunk,
#                                 metadata={
#                                     "source": path,
#                                     "source_type": "book",
#                                     "category": "cybersecurity_text"
#                                 }
#                             )
#                         )

#         except Exception as e:
#             print(f"❌ Error loading {path}: {e}")

#     print(f"✅ Total book documents: {len(documents)}")
#     return documents


# # ===============================
# # CISA LOADER (WITH CHUNKING)
# # ===============================
# def load_cisa(file_path: str):
#     documents = []

#     with open(file_path, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     vulnerabilities = data.get("vulnerabilities", [])

#     for item in tqdm(vulnerabilities, desc="🛡️ Loading CISA KEV"):
#         desc = clean_text(item.get("shortDescription", ""))

#         attack_type = extract_attack_type(desc)
#         product = item.get("product") or extract_product(desc)
#         tags = generate_tags(desc, attack_type, product)

#         chunks = text_splitter.split_text(desc)

#         for i, chunk in enumerate(chunks):
#             documents.append(
#                 Document(
#                     page_content=f"{chunk} (CVE: {item.get('cveID')})",
#                     metadata={
#                         "cve_id": item.get("cveID"),
#                         "vendor": item.get("vendorProject"),
#                         "product": product,
#                         "attack_type": attack_type,
#                         "tags": tags,
#                         "source": "CISA",
#                         "source_type": "threat_intel",
#                         "year": extract_year(item.get("dateAdded")),
#                         "doc_id": item.get("cveID"),
#                         "chunk_id": f"{item.get('cveID')}_{i}"
#                     }
#                 )
#             )

#     print(f"✅ Loaded {len(documents)} CISA docs")
#     return documents


# # ===============================
# # NVD LOADER (WITH CHUNKING)
# # ===============================
# def load_nvd(file_paths: list):
#     documents = []

#     for file_path in file_paths:
#         print(f"\n📂 Processing: {os.path.basename(file_path)}")

#         with open(file_path, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         vulnerabilities = data.get("vulnerabilities", [])

#         for item in tqdm(vulnerabilities, desc=f"🧨 {os.path.basename(file_path)}"):
#             cve = item.get("cve", {})

#              # Extract Description
#             desc = ""
#             for d in cve.get("descriptions", []):
#                 if d.get("lang") == "en":
#                     desc = d.get("value")

#             desc = clean_text(desc)

#             # Extract Metadata
#             attack_type = extract_attack_type(desc)
#             product = extract_product(desc)
#             tags = generate_tags(desc, attack_type, product)
            
#             # ✅ FIX: CVSS Extraction
#             metrics = cve.get("metrics", {})
#             cvss_score, severity = extract_cvss(metrics)

#             # Chunking
#             chunks = text_splitter.split_text(desc)

#             # FIX: enumerate for chunk_id
#             for i, chunk in enumerates(chunks):
#                 documents.append(
#                     Document(
#                         page_content=f"{chunk} (CVE: {cve.get('id')})",
#                         metadata={
#                             "cve_id": cve.get("id"),
#                             "attack_type": attack_type,
#                             "product": product,
#                             "tags": tags,
#                             "year": extract_year(cve.get("published")),
#                             "source": "NVD",
#                             "source_type": "threat_intel",
#                             "cvss_score": cvss_score,
#                             "severity": severity,
#                             "doc_id": cve.get("id"),
#                             "chunk_id": f"{cve.get('id')}_{i}"
#                         }
#                     )
#                 )

#     print(f"✅ Loaded {len(documents)} NVD docs")
#     return documents


# ===============================
# MAIN LOADER
# ===============================
def load_all_documents():
    print("🚀 Starting Data Loading...\n")

    books = load_books("../data/raw/books")
    cisa = load_cisa("../data/raw/cisa/known_exploited_vulnerabilities.json")
    nvd = load_nvd([
        "../data/raw/nvd/nvdcve-2.0-modified.json",
        "../data/raw/nvd/nvdcve-2.0-recent.json"
    ])

    total = len(books) + len(cisa) + len(nvd)

    print("\n========== 📊 SUMMARY ==========")
    print(f"📘 Books: {len(books)}")
    print(f"🛡️ CISA: {len(cisa)}")
    print(f"🧨 NVD: {len(nvd)}")
    print(f"📦 TOTAL: {total}")

    # return books + cisa + nvd
    all_docs = books + cisa + nvd

    # 🔥 Deduplication
    unique_docs = {}
    for doc in all_docs:
        key = doc.page_content.strip()
        if key not in unique_docs:
            unique_docs[key] = doc

    final_docs = list(unique_docs.values())

    print(f"\n🧹 After Deduplication: {len(final_docs)} documents")

    return final_docs



# -----------------------------------------------------------------------------------------------------------------------------------------

# import os
# import json
# import re
# from tqdm import tqdm
# from langchain_community.document_loaders import PyPDFLoader, TextLoader
# from langchain_core.documents import Document

# # OCR imports
# import pytesseract
# from pdf2image import convert_from_path


# # ===============================
# # 🔥 HELPER FUNCTIONS (same)
# # ===============================
# def extract_attack_type(text):
#     text = text.lower()
#     if "xss" in text or "cross-site scripting" in text:
#         return "XSS"
#     elif "rce" in text or "remote code execution" in text:
#         return "RCE"
#     elif "sql injection" in text:
#         return "SQL Injection"
#     elif "csrf" in text:
#         return "CSRF"
#     elif "directory traversal" in text:
#         return "Path Traversal"
#     else:
#         return "Unknown"


# def extract_year(date_str):
#     if not date_str:
#         return None
#     return int(date_str[:4])


# def clean_text(text):
#     return " ".join(text.strip().split())


# def extract_product(text):
#     match = re.search(r"plugin for ([\w\s\-]+)", text.lower())
#     if match:
#         return match.group(1).strip().title()
#     return "Unknown"


# def generate_tags(text, attack_type):
#     tags = []
#     if "wordpress" in text.lower():
#         tags.append("wordpress")
#     if "plugin" in text.lower():
#         tags.append("plugin")
#     if attack_type != "Unknown":
#         tags.append(attack_type.lower())
#     return tags


# # ===============================
# # OCR FUNCTION (WITH PROGRESS)
# # ===============================
# def extract_text_with_ocr(pdf_path):
#     text = ""
#     try:
#         images = convert_from_path(pdf_path)
#         for img in tqdm(images, desc="📝 OCR Pages", leave=False):
#             text += pytesseract.image_to_string(img)
#     except Exception as e:
#         print(f"❌ OCR failed: {e}")
#     return text


# # ===============================
# # BOOKS LOADER (WITH PROGRESS)
# # ===============================
# def load_books(data_path: str):
#     documents = []

#     all_files = []
#     for root, _, files in os.walk(data_path):
#         for f in files:
#             all_files.append(os.path.join(root, f))

#     print(f"\n📂 Total book files: {len(all_files)}")

#     for path in tqdm(all_files, desc="📘 Loading Books"):

#         try:
#             if path.endswith(".pdf"):
#                 loader = PyPDFLoader(path)
#                 docs = loader.load()

#                 for d in tqdm(docs, desc="📄 PDF Pages", leave=False):
#                     text = clean_text(d.page_content)

#                     documents.append(
#                         Document(
#                             page_content=text,
#                             metadata={
#                                 "source": path,
#                                 "source_type": "book",
#                                 "category": "cybersecurity_text"
#                             }
#                         )
#                     )

#             elif path.endswith(".txt"):
#                 loader = TextLoader(path)
#                 docs = loader.load()

#                 for d in tqdm(docs, desc="📄 TXT Chunks", leave=False):
#                     text = clean_text(d.page_content)

#                     documents.append(
#                         Document(
#                             page_content=text,
#                             metadata={
#                                 "source": path,
#                                 "source_type": "book",
#                                 "category": "cybersecurity_text"
#                             }
#                         )
#                     )

#         except Exception as e:
#             print(f"❌ Error loading {path}: {e}")

#     print(f"✅ Total book documents: {len(documents)}")
#     return documents


# # ===============================
# # CISA LOADER (WITH PROGRESS)
# # ===============================
# def load_cisa(file_path: str):
#     documents = []

#     with open(file_path, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     vulnerabilities = data.get("vulnerabilities", [])

#     for item in tqdm(vulnerabilities, desc="🛡️ Loading CISA KEV"):
#         desc = clean_text(item.get("shortDescription", ""))

#         attack_type = extract_attack_type(desc)

#         content = f"{desc} (CVE: {item.get('cveID')})"

#         documents.append(
#             Document(
#                 page_content=content,
#                 metadata={
#                     "cve_id": item.get("cveID"),
#                     "vendor": item.get("vendorProject"),
#                     "product": item.get("product"),
#                     "attack_type": attack_type,
#                     "tags": generate_tags(desc, attack_type),
#                     "source": "CISA",
#                     "source_type": "threat_intel",
#                     "year": extract_year(item.get("dateAdded"))
#                 }
#             )
#         )

#     print(f"✅ Loaded {len(documents)} CISA docs")
#     return documents


# # ===============================
# # NVD LOADER (WITH PROGRESS)
# # ===============================
# def load_nvd(file_paths: list):
#     documents = []

#     for file_path in file_paths:
#         print(f"\n📂 Processing: {os.path.basename(file_path)}")

#         with open(file_path, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         vulnerabilities = data.get("vulnerabilities", [])

#         for item in tqdm(vulnerabilities, desc=f"🧨 {os.path.basename(file_path)}"):
#             cve = item.get("cve", {})

#             desc = ""
#             for d in cve.get("descriptions", []):
#                 if d.get("lang") == "en":
#                     desc = d.get("value")

#             desc = clean_text(desc)

#             attack_type = extract_attack_type(desc)
#             product = extract_product(desc)

#             content = f"{desc} (CVE: {cve.get('id')})"

#             documents.append(
#                 Document(
#                     page_content=content,
#                     metadata={
#                         "cve_id": cve.get("id"),
#                         "attack_type": attack_type,
#                         "product": product,
#                         "tags": generate_tags(desc, attack_type),
#                         "year": extract_year(cve.get("published")),
#                         "source": "NVD",
#                         "source_type": "threat_intel"
#                     }
#                 )
#             )

#     print(f"✅ Loaded {len(documents)} NVD docs")
#     return documents


# # ===============================
# # MAIN LOADER (WITH SUMMARY)
# # ===============================
# def load_all_documents():
#     print("🚀 Starting Data Loading...\n")

#     books = load_books("../data/raw/books")
#     cisa = load_cisa("../data/raw/cisa/known_exploited_vulnerabilities.json")
#     nvd = load_nvd([
#         "../data/raw/nvd/nvdcve-2.0-modified.json",
#         "../data/raw/nvd/nvdcve-2.0-recent.json"
#     ])

#     total = len(books) + len(cisa) + len(nvd)

#     print("\n========== 📊 SUMMARY ==========")
#     print(f"📘 Books: {len(books)}")
#     print(f"🛡️ CISA: {len(cisa)}")
#     print(f"🧨 NVD: {len(nvd)}")
#     print(f"📦 TOTAL: {total}")

#     return books + cisa + nvd


# ----------------------------------------------------------------------------------------------------------------------------------------------------

# import os
# import json
# from tqdm import tqdm
# from langchain_community.document_loaders import PyPDFLoader, TextLoader
# from langchain_core.documents import Document

# # OCR imports
# import pytesseract
# from pdf2image import convert_from_path


# # ===============================
# #  OCR FUNCTION
# # ===============================
# def extract_text_with_ocr(pdf_path):
#     print(f"🔍 Running OCR on: {pdf_path}")
#     text = ""

#     try:
#         images = convert_from_path(pdf_path)
#         print(f"📸 Converted {len(images)} pages to images")

#         for i, img in enumerate(images):
#             print(f"📝 OCR processing page {i+1}")
#             text += pytesseract.image_to_string(img)

#     except Exception as e:
#         print(f"❌ OCR failed for {pdf_path}: {e}")

#     return text


# # ===============================
# #  BOOKS LOADER (PDF + OCR)
# # ===============================
# def load_books(data_path: str):
#     print(f"\n📂 Scanning folder: {data_path}")
#     documents = []

#     files = []
#     for root, _, filenames in os.walk(data_path):
#         for f in filenames:
#             files.append(os.path.join(root, f))

#     print(f"📊 Total files found: {len(files)}")

#     for file_path in tqdm(files, desc="📘 Loading Books (PDF + OCR)"):
#         print(f"\n➡️ Processing file: {file_path}")

#         try:
#             if file_path.endswith(".pdf"):
#                 print("📄 Detected PDF")

#                 loader = PyPDFLoader(file_path)
#                 docs = loader.load()

#                 print(f"📑 Pages loaded: {len(docs)}")

#                 extracted_text = " ".join([d.page_content.strip() for d in docs])

#                 if len(extracted_text) < 50:
#                     print("⚠️ Low text detected → Switching to OCR")

#                     ocr_text = extract_text_with_ocr(file_path)

#                     documents.append(
#                         Document(
#                             page_content=ocr_text,
#                             metadata={
#                                 "source": file_path,
#                                 "source_type": "book",
#                                 "ocr_used": True
#                             }
#                         )
#                     )
#                 else:
#                     print("✅ Normal text extraction successful")

#                     for d in docs:
#                         d.metadata["source_type"] = "book"
#                         d.metadata["ocr_used"] = False

#                     documents.extend(docs)

#             elif file_path.endswith(".txt"):
#                 print("📄 Detected TXT")

#                 loader = TextLoader(file_path)
#                 docs = loader.load()

#                 print(f"📑 Loaded {len(docs)} text chunks")

#                 for d in docs:
#                     d.metadata["source_type"] = "book"
#                     d.metadata["ocr_used"] = False

#                 documents.extend(docs)

#             else:
#                 print("⚠️ Skipped unsupported file")

#         except Exception as e:
#             print(f"❌ Error loading {file_path}: {e}")

#     print(f"\n✅ Total documents loaded from books: {len(documents)}")
#     return documents


# # ===============================
# #  CISA LOADER
# # ===============================
# def load_cisa(file_path: str):
#     print(f"\n🛡️ Loading CISA file: {file_path}")
#     documents = []

#     if not os.path.exists(file_path):
#         print("❌ CISA file not found!")
#         return documents

#     with open(file_path, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     vulnerabilities = data.get("vulnerabilities", [])
#     print(f"📊 Total CISA vulnerabilities: {len(vulnerabilities)}")

#     for item in tqdm(vulnerabilities, desc="🛡️ Loading CISA KEV"):
#         documents.append(
#             Document(
#                 page_content=f"""
#                     CVE ID: {item.get('cveID')}
#                     Vendor: {item.get('vendorProject')}
#                     Product: {item.get('product')}
#                     Name: {item.get('vulnerabilityName')}
#                     Description: {item.get('shortDescription')}
#                     Required Action: {item.get('requiredAction')}
#                     Due Date: {item.get('dueDate')}
#                 """,
#                 metadata={
#                     "source": "CISA",
#                     "cve_id": item.get("cveID"),
#                     "vendor": item.get("vendorProject"),
#                     "product": item.get("product"),
#                     "source_type": "threat_intel",
#                     "type": "cve"
#                 }
#             )
#         )

#     print(f"✅ Loaded {len(documents)} CISA documents")
#     return documents


# # ===============================
# #  NVD LOADER
# # ===============================
# def load_nvd(file_paths: list):
#     print(f"\n🧨 Loading NVD files...")
#     documents = []

#     for file_path in file_paths:
#         if not os.path.exists(file_path):
#             print(f"❌ File not found: {file_path}")
#             continue

#         print(f"\n📂 Processing NVD file: {file_path}")

#         with open(file_path, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         vulnerabilities = data.get("vulnerabilities", [])
#         print(f"📊 Total vulnerabilities: {len(vulnerabilities)}")

#         for item in tqdm(vulnerabilities, desc=f"🧨 {os.path.basename(file_path)}"):
#             cve = item.get("cve", {})
#             descriptions = cve.get("descriptions", [])

#             desc_text = ""
#             for d in descriptions:
#                 if d.get("lang") == "en":
#                     desc_text = d.get("value")

#             documents.append(
#                 Document(
#                     page_content=f"""
#                         CVE ID: {cve.get('id')}
#                         Description: {desc_text}
#                         Published: {cve.get('published')}
#                         Last Modified: {cve.get('lastModified')}
#                     """,
#                     metadata={
#                         "source": "NVD",
#                         "cve_id": cve.get("id"),
#                         "published": cve.get("published"),
#                         "last_modified": cve.get("lastModified"),
#                         "severity": item.get("cve", {}).get("metrics", {}),
#                         "source_type": "nvd",
#                         "type": "cve"
#                     }
#                 )
#             )




#     print(f"\n✅ Total NVD documents loaded: {len(documents)}")
#     return documents

# def load_all_documents():
#     print("🚀 Starting Data Ingestion Pipeline...\n")

#     # 🔥 SET YOUR PATHS HERE (IMPORTANT)
#     books_path = "../data/raw/books"
#     cisa_path = "../data/raw/cisa/known_exploited_vulnerabilities.json"
#     nvd_paths = [
#         "../data/raw/nvd/nvdcve-2.0-modified.json",
#         "../data/raw/nvd/nvdcve-2.0-recent.json"
#     ]

#     print("📍 Books Path:", books_path)
#     print("📍 CISA Path:", cisa_path)
#     print("📍 NVD Paths:", nvd_paths)

#     # Load all
#     books = load_books(books_path)
#     cisa_docs = load_cisa(cisa_path)
#     nvd_docs = load_nvd(nvd_paths)

#     # Combine
#     all_docs = books + cisa_docs + nvd_docs




#     # Summary
#     print("\n========== 🎯 FINAL SUMMARY ==========")
#     print(f"📘 Books: {len(books)}")
#     print(f"🛡️ CISA: {len(cisa_docs)}")
#     print(f"🧨 NVD: {len(nvd_docs)}")
#     print(f"📦 TOTAL DOCUMENTS: {len(all_docs)}")

#     if len(all_docs) > 0:
#         print("\n📄 Sample Preview:")
#         print(all_docs[0].page_content[:300])

#     return all_docs



# # ===============================
# #  MAIN EXECUTION
# # ===============================
# if __name__ == "__main__":
#     all_docs = load_all_documents()
    


# ------------------------------------------------------------------------------------------------------------------------------------------------


# import os
# import json
# from tqdm import tqdm
# # from langchain.document_loaders import PyPDFLoader, TextLoader
# from langchain_community.document_loaders import PyPDFLoader, TextLoader
# # from langchain.schema import Document
# from langchain_core.documents import Document

# # OCR imports
# import pytesseract
# from pdf2image import convert_from_path


# # ===============================
# # 🔍 OCR FUNCTION
# # ===============================
# def extract_text_with_ocr(pdf_path):
#     text = ""

#     try:
#         images = convert_from_path(pdf_path)

#         for img in images:
#             text += pytesseract.image_to_string(img)

#     except Exception as e:
#         print(f"OCR failed for {pdf_path}: {e}")

#     return text


# # ===============================
# # 📘 BOOKS LOADER (PDF + OCR)
# # ===============================
# def load_books(data_path: str):
#     documents = []

#     files = []
#     for root, _, filenames in os.walk(data_path):
#         for f in filenames:
#             files.append(os.path.join(root, f))

#     for file_path in tqdm(files, desc="📘 Loading Books (PDF + OCR)"):

#         try:
#             # ===============================
#             # 📄 PDF FILE
#             # ===============================
#             if file_path.endswith(".pdf"):

#                 loader = PyPDFLoader(file_path)
#                 docs = loader.load()

#                 extracted_text = " ".join([d.page_content.strip() for d in docs])

#                 # ✅ If empty → use OCR
#                 if len(extracted_text) < 50:
#                     ocr_text = extract_text_with_ocr(file_path)

#                     documents.append(
#                         Document(
#                             page_content=ocr_text,
#                             metadata={
#                                 "source": file_path,
#                                 "source_type": "book",
#                                 "ocr_used": True
#                             }
#                         )
#                     )

#                 else:
#                     for d in docs:
#                         d.metadata["source_type"] = "book"
#                         d.metadata["ocr_used"] = False
#                     documents.extend(docs)

#             # ===============================
#             # 📄 TXT FILE
#             # ===============================
#             elif file_path.endswith(".txt"):

#                 loader = TextLoader(file_path)
#                 docs = loader.load()

#                 for d in docs:
#                     d.metadata["source_type"] = "book"
#                     d.metadata["ocr_used"] = False

#                 documents.extend(docs)

#         except Exception as e:
#             print(f"Error loading {file_path}: {e}")

#     return documents


# # ===============================
# # 🛡️ CISA LOADER
# # ===============================
# def load_cisa(file_path: str):
#     documents = []

#     with open(file_path, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     vulnerabilities = data.get("vulnerabilities", [])

#     for item in tqdm(vulnerabilities, desc="🛡️ Loading CISA KEV"):

#         text = f"""
#         CVE ID: {item.get('cveID')}
#         Vendor: {item.get('vendorProject')}
#         Product: {item.get('product')}
#         Name: {item.get('vulnerabilityName')}
#         Description: {item.get('shortDescription')}
#         Required Action: {item.get('requiredAction')}
#         Due Date: {item.get('dueDate')}
#         """

#         documents.append(
#             Document(
#                 page_content=text,
#                 metadata={
#                     "source": "CISA",
#                     "cve_id": item.get("cveID"),
#                     "source_type": "threat_intel"
#                 }
#             )
#         )

#     return documents


# # ===============================
# # 🧨 NVD LOADER
# # ===============================
# def load_nvd(file_paths: list):
#     documents = []

#     for file_path in file_paths:

#         with open(file_path, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         vulnerabilities = data.get("vulnerabilities", [])

#         for item in tqdm(vulnerabilities, desc=f"🧨 Loading {os.path.basename(file_path)}"):

#             cve = item.get("cve", {})
#             descriptions = cve.get("descriptions", [])

#             desc_text = ""
#             for d in descriptions:
#                 if d.get("lang") == "en":
#                     desc_text = d.get("value")

#             text = f"""
#             CVE ID: {cve.get('id')}
#             Description: {desc_text}
#             Published: {cve.get('published')}
#             Last Modified: {cve.get('lastModified')}
#             """

#             documents.append(
#                 Document(
#                     page_content=text,
#                     metadata={
#                         "source": "NVD",
#                         "cve_id": cve.get("id"),
#                         "source_type": "threat_intel"
#                     }
#                 )
#             )

#     return documents