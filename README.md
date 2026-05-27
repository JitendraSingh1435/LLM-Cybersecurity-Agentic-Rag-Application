
## 👨‍💻 Author

* **Jitendra Singh** ( [@JitendraSingh1435 ](https://github.com/JitendraSingh1435) )
* M.Tech in Computer Science & Engineering
* Indian Institute of Information Technology (IIIT), Una

# 🛡️ LLM-Powered Cybersecurity Application using Agentic RAG

An intelligent cybersecurity assistant powered by Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) for providing accurate, context-aware, and reasoning-oriented cybersecurity guidance.

This project compares Standard RAG and Agentic RAG architectures to evaluate improvements in retrieval quality, contextual understanding, and reasoning capability for cybersecurity-related queries.


## 🎯 Objectives

- Develop an AI-powered cybersecurity assistant using Agentic RAG
- Provide accurate and context-aware cybersecurity guidance
- Compare Standard RAG and Agentic RAG architectures
- Improve retrieval quality using multi-query mechanisms
- Reduce hallucinations in LLM-generated responses
- Enable personalized cybersecurity assistance
## Features

- 🔐 AI-Powered Cybersecurity Assistant
- 🧠 Retrieval-Augmented Generation (RAG)
- 🤖 Agentic RAG with Multi-Step Reasoning
- 📚 Vector Database-Based Knowledge Retrieval
- 🛡️ Hallucination Reduction using Verification Layer
- ⚡ Real-Time Threat Intelligence Support
- 🎯 Scam & Phishing Detection Assistance
- 🔍 Multi-Query Retrieval Mechanism
- 📊 Evaluation using RAGAS & DeepEval
- 🌐 Streamlit-based Interactive UI
- 🔄 Switch between Local Ollama Models and Gemini API


## 📚 Knowledge Base

This repository features a comprehensive library of curated reference materials, official standards, and textbooks covering cybersecurity, penetration testing, and digital forensics. Total 65 books are used for knowledge base which includes:

### 🎓 Professional Certifications & Guides
* **CISSP All-In-One Exam Guide (8th Edition)** – Comprehensive coverage of the CISSP domains.
* **CISSP Study Guide (3rd Edition)** – Core concepts and preparation strategy for the examination.
* **Official (ISC)² Guide to the CISSP CBK** – The official body of knowledge reference framework.

### 🏛️ Standards, Frameworks & Compliance
* **NIST SP 800-Series** – Extensive collection of National Institute of Standards and Technology guidelines:
  * **SP 800-53** – Security and privacy controls for information systems.
  * **SP 800-61** – Computer security incident handling guide.
  * **SP 800-63** – Digital identity guidelines.
* **FIPS 140-2** – Security requirements for cryptographic modules.
* **NIST.CSWP.29** – Cybersecurity Framework (CSF) resources.

### 🛡️ Ethical Hacking & Penetration Testing
* **Hacking: The Art of Exploitation** (Jon Erickson) – Core fundamentals of hacking and C programming vulnerabilities.
* **Penetration Testing: A Hands-On Introduction** – Practical methodology for network and system testing.
* **The Web Application Hacker's Handbook** – Defacto standard for finding and exploiting web flaws.
* **iOS Application Security** – Security architecture and exploitation vectors for mobile iOS systems.
* **Attacking Network Protocols** – Techniques for analyzing and finding flaws in custom protocols.

### 🔬 Malware Analysis & Forensics
* **Practical Malware Analysis** (Michael Sikorski) – Hands-on guide to dissecting malicious Windows binaries.
* **Practical Forensics Imaging** – Methodologies for securing data and legally defensible digital evidence.
* **Practical Vulnerability Management** – Frameworks for continuous scanning, assessing, and remediating risks.

### 🔐 Cryptography & Foundations
* **Applied Cryptography (2nd Edition)** (Bruce Schneier) – The definitive textbook on cryptographic protocols.
* **Cryptography and Network Security (6th Edition)** (William Stallings) – Principles and practice of network encryption.
* **Introduction to Cyber Security** – Fundamental building blocks of modern information defense systems.

## 🧰 Tech Stack

* **Programming Language:** Python
* **Large Language Model:** Mistral (`mistral:latest`) / **Gemini API key**
* **LLM Hosting Platform:** Ollama
* **Embedding Model:** Sentence Transformers (`all-MiniLM-L6-v2`)
* **Vector Database:** FAISS
* **Retrieval Framework:** LangChain
* **User Interface:** Streamlit (Web-based UI)

## 🏗️ System Architecture

- Knowledge Base
- Embedding Model
- Vector Database
- Retrieval Module
- Multi-Query Layer
- Standard RAG Pipeline
- Agentic RAG Pipeline
- Mistral LLM via Ollama
- Web-based User Interface


## 🏗️ System Architecture


| 1. Standard RAG Workflow | 2. Agentic RAG Workflow |
| :---: | :---: |
| ![Standard RAG](https://kroki.io/mermaid/svg/eNp9jj2PgkAQhnt_xSS2t81RSWGC8hFzEuPhXbOhWGCQjSNLZtdT__2RhcLKqSZ5nnfeObMaOjjFCxgnkj8WGY435GcJQqxhI5NrhU2j-zNk2CMrp01fenvjja1Mo11RwC_WzjAUqLjuJmHrhViezCC-4Bsda_xTNMHYw0TmN3Ja-EpINTnksWtSEq-kMtfWsSLY73M4EKmrmnjqeSbnx7AZO-xgeovlwgvWPQkhglYThct21X6Mh8wFw2UQBPMu7rpxXfg5PF4i2RypqveRfwyFYSs=) | ![Agentic RAG](https://kroki.io/mermaid/svg/eNp9jrtuwzAMRfd8BYGMqZd6qocCjh07BmK0TdouggeloRUiqmxIzOvvK0gZPJUTwXPuBZWV4xE-yxn4ycWXQwsfZ7T3DpLkFZYiV2gY3rU0Bm0XtGVAhQgebPFqicmoCIsAS9GeNVMSlRp9VjINJjplcFai4XC-IFR5s9v5KraEF6mjtgpaJYrBMN4YcqUsqklPFYRabFG6wfgXYAHfaKmnn4lVB2stWnJspYbNpoU3reWvjHwdeCMqMp7GPB78M24cjMNuFizHd42QQ09aZ_P-pX_ybcMJs3mapo89udKBj9nzeJtEmkdkv_8_8gekjnkx) |

> **Note:** The Agentic RAG pipeline introduces planning and reasoning-based retrieval mechanisms to significantly improve contextual understanding and response quality over the standard workflow.


## 🧠 Multi-Query Retrieval Mechanism

The project integrates Multi-Query Retrieval in both pipelines to improve retrieval relevance and response quality.

* **Generate** multiple semantically related queries.
* **Improve** contextual coverage.
* **Retrieve** information from multiple perspectives.
* **Reduce** missing relevant cybersecurity documents.
* **Improve** response completeness.
### 📈 Evaluation Metrics Breakdown


| Metric | Standard RAG | Agentic RAG | Description |
| :--- | :---: | :---: | :--- |
| **Context Relevance** | 🔹 | 🔹 | Evaluates if the retrieved documents are relevant to the query. |
| **Faithfulness (Groundedness)** | 🔹 | 🔹 | Measures if the generated response is strictly based on the context. |
| **Answer Relevance** | 🔹 | 🔹 | Checks how directly the final response addresses the user's prompt. |
| **Plan Fidelity** | ❌ | 🔹 | Tracks if the agent planner strictly followed its generated execution plan. |
| **Tool Success Rate** | ❌ | 🔹 | Measures the accuracy and efficiency of external tools/vector lookups called. |
| **Reasoning Traceability** | ❌ | 🔹 | Evaluates the transparency of the chain-of-thought verification logs. |
| **Task Completion Rate** | ❌ | 🔹 | Confirms whether the agent successfully resolved complex, multi-step queries. |


## 📈 Key Observations & Insights

The comparative analysis across both pipeline setups demonstrates several key performance differences:

* **Standard RAG Baseline:** Performs effective, single-step contextual retrieval for straightforward data inquiries.
* **Query Reformulation:** Agentic RAG actively optimizes retrieval quality through autonomous query reformulation.
* **Domain Depth:** Agentic RAG consistently generates more detailed, comprehensive cybersecurity explanations.
* **Complex Reasoning:** Incorporating multi-step reasoning cycles significantly increases response quality for multi-layered queries.
* **Search Enrichment:** Integrating multi-query retrieval successfully enhances keyword relevance across both architectures.

## 💡 Example Use Cases

This system serves as an intelligent assistant tailored for various security operations and education scenarios:

* 🛑 **Scam Detection Assistance** – Identify common social engineering tactics and fraudulent schemes.
* 📷 **QR Code Fraud Awareness** – Understand "quishing" vectors and how to detect malicious QR links.
* 🎣 **Phishing Detection Guidance** – Analyze suspicious email structures, headers, and deceptive indicators.
* 🎓 **Cybersecurity Awareness Training** – Create interactive training scenarios and educational content for teams.
* 🔍 **Vulnerability Understanding** – Break down complex CVEs, software bugs, and technical exposures simply.
* 🛡️ **Security Recommendations** – Generate proactive hardening steps and defensive configurations for systems.
* 🚨 **Incident Response Guidance** – Provide immediate, structured triage steps during initial threat discovery.


## Query Demonstration

The system evaluates reasoning quality and contextual understanding by directly comparing outputs generated side-by-side:

### 📥 Sample Prompt
> **Query:** *"Today, i recieved 5000 rupees from someone's UPI then after few minutes i got a call on on which a person told me that hes has send me the 5000 rupees by mistake and 
asked me to return that money on a QR code. What should i do ? "*

### 📺 Demo Screenshot
[![Screenshot-(879).png](https://i.postimg.cc/CL1GS6f3/Screenshot-(879).png)](https://postimg.cc/JtfDQxxx)

[![Screenshot-(879).png](https://i.postimg.cc/KYHz7JYk/Screenshot-(879).png)](https://postimg.cc/Z9644Pp4)

[![Screenshot.png](https://i.postimg.cc/k5p4Nf5J/Screenshot.png)](https://postimg.cc/zLT88wW6)


The system compares responses generated by:
* **Standard RAG** — Evaluates direct, single-pass contextual information retrieval.
* **Agentic RAG** — Evaluates advanced multi-step planning, query reformulation, and verification loops.



## 📌 Current System Capabilities

The current implementation can:
* **Accept** cybersecurity-related natural language queries.
* **Perform** semantic retrieval using FAISS.
* **Generate** context-aware responses using Mistral.
* **Compare** Standard RAG and Agentic RAG outputs side-by-side.
* **Display** retrieved cybersecurity sources and references.
* **Generate** reasoning-oriented responses via agent planning.

### 🔄 Pipeline Sequence
The complete processing pipeline operates sequentially as follows:

```text
User Query ──> Retrieval ──> Multi-Query ──> Generation ──> Final Response
```




## 🚀 Run Application

Follow these step-by-step instructions to set up, initialize, and run the RAG + Agentic RAG Cybersecurity system on your local machine.

---

### 📋 Prerequisites

Before running the application, make sure you have the following installed:
* **Python 3.10+** or **Python 3.11+**
* [Ollama](https://ollama.com/) (if using the default local LLM setup)
* [uv](https://github.com/astral-sh/uv) (optional, but highly recommended for fast package management)

---

### ⚙️ Step 1: Environment Setup

#### 1. Create a Virtual Environment
You can set up your virtual environment using either the ultra-fast `uv` tool or the built-in python `venv` utility.

**Using `uv` (Recommended):**
```bash
# Create the virtual environment
uv venv

# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Activate the virtual environment (Linux/macOS)
source .venv/bin/activate
```

**Using Standard `venv`:**
```bash
# Create the virtual environment
python -m venv .venv

# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Activate the virtual environment (Linux/macOS)
source .venv/bin/activate
```

#### 2. Install Required Dependencies
Once your virtual environment is active, install the packages defined in `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### 🔑 Step 2: Configure LLM Provider (API Keys & Local Models)

The codebase supports switching between Ollama (Local) and Google Gemini (Cloud) via `utils/helpers.py`.

#### Option A: Running Locally with Ollama (Default)
Ensure the Ollama background service is running. Download and run the default Mistral model in your terminal:
```bash
ollama run mistral:latest
```

#### Option B: Running with Google Gemini
Open or create the `.env` file at the root of the project. Add your Google Gemini API Key:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

### 🧠 Step 3: Initialize the Vector Database (First-Time Setup Only)

> ⚠️ **IMPORTANT**  
> The RAG application relies on a local FAISS Vector Database to retrieve cybersecurity context. If the `vectorstore/db_faiss/` folder is empty or deleted, launching the application directly will crash with a `FileNotFoundError`.

To generate the embeddings and construct the vector database from preprocessed datasets, run:
```bash
python data_ingestion/pipeline.py
```

* **How it works:** It loads preprocessed LangChain documents from `data/processed/`, segments them using custom chunking guidelines, embeds them locally using the MiniLM embedding model, and saves the FAISS index files (`index.faiss` and `index.pkl`) inside the `vectorstore/db_faiss/` directory.
* **Auto-Skip Feature:** If the database files already exist, the pipeline script will automatically recognize them and skip the build process to save time.

---

### 🎯 Step 4: Run the Application

You can interact with the application using either a modern browser dashboard (Web UI) or an interactive command-line terminal.

#### 🌐 Method A: Run the Web Dashboard (Recommended)
This runs a FastAPI backend with a premium, responsive web interface and auto-launches your browser.
```bash
python -m ui.api
```
* **URL:** Once running, navigate to `http://127.0.0.1:8000` (the script will try to open it automatically).
* **Features:** Allows side-by-side comparison of Simple RAG vs. Agentic RAG, provides real-time response times/metrics, displays rewritten queries, and shows source citations.

#### 💻 Method B: Run Interactive Terminal CLI
If you prefer running a quick conversation loop directly in your console:
```bash
python main.py
```
* Type your question at the prompt. 
* To exit the session, type `exit`.
