# AutoGen + Azure AI Search – Agentic RAG POC

This repository demonstrates an **Agentic Retrieval‑Augmented Generation (RAG)** pattern using **Microsoft AutoGen** and **Azure AI Search**.

The system uses multiple AI agents to:
- decide whether retrieval is required,
- retrieve relevant enterprise content from Azure AI Search,
- and generate grounded answers **only from retrieved context**.

This is a **strict RAG** implementation — no hallucinations by design.

---

## 🧠 Architecture Overview
User Question
↓
Planner Agent
↓
Retriever Agent ────► Azure AI Search
↓
Answerer Agent
↓
FINAL

### Agents
- **Planner**  
  Decides whether retrieval from the knowledge base is required.
- **Retriever**  
  Calls Azure AI Search using a registered tool (`search_knowledge_base`).
- **Answerer**  
  Produces an answer **only from retrieved context**, with citations.

---

## 🚀 Tech Stack

- **Python 3.9+**
- **Microsoft AutoGen (AgentChat)**
- **Azure OpenAI**
- **Azure AI Search**
- **azure-search-documents SDK**
- **python-dotenv**

---

## 📁 Repository Structure


autogen-azure-rag-poc/
├─ src/
│  ├─ agents.py        # Planner / Retriever / Answerer agents
│  ├─ tools.py         # Azure AI Search retrieval tool
│  ├─ config.py        # Environment loading + model client
│  └─ run_chat.py      # Entry point
├─ .gitignore
├─ .env.example        # Environment variable template
├─ requirements.txt
└─ README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate    # Linux / macOS
.venv\Scripts\activate       # Windows

2️⃣ Install dependencies
Shellpip install -r requirements.txtShow more lines
3️⃣ Configure environment variables
Shellcp .env.example .envShow more lines
Fill in values for:

Azure OpenAI
Azure AI Search

⚠️ Do NOT commit .env — it is intentionally ignored.

▶️ Run the application
Shellpython -m src.run_chat --question "What is Azure AI Search?"Show more lines
Expected behavior

Planner decides retrieval is required
Retriever queries Azure AI Search
Answerer responds using retrieved content
Output ends with FINAL


✅ Design Principles

✅ Grounded answers only (no hallucination)
✅ Deterministic agent routing
✅ Tool‑based retrieval
✅ Clean termination conditions
✅ Secrets excluded from source control


🔮 Possible Enhancements

Semantic ranking
Vector / hybrid search
Fallback mode when no context is found
Evaluation & tracing hooks
CI pipeline (lint + smoke test)


 (recommended for POCs and demos)

---

# ✅ 2️⃣ `requirements.txt` (minimal & correct)

```txt
autogen-agentchat
autogen-ext[openai]
azure-search-documents
python-dotenv

✅ This is enough to:

run AutoGen agents
connect to Azure OpenAI
query Azure AI Search
load .env safely