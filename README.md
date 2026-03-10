# AutoGen + Azure OpenAI + Azure AI Search — RAG POC (GitHub Desktop friendly)

This repo is a **POC** for a **multi-agent RAG** assistant using:

- **Microsoft AutoGen AgentChat** (multi-agent orchestration) — `AssistantAgent`, `UserProxyAgent`, and team workflows like `RoundRobinGroupChat`. citeturn7search118turn4search76
- **Azure OpenAI** for chat completions via `AzureOpenAIChatCompletionClient`. citeturn7search128turn7search129
- **Azure AI Search** as the retrieval layer for RAG (query → top-k chunks). citeturn4search70

> Your original assignment requirement is a RAG system (load → chunk → embed → vector store → retrieve → answer) with an optional conversational experience. citeturn1search1

---

## 1) Create/Manage with GitHub Desktop

1. **File → Add local repository…** (or **File → New repository…** if starting fresh)
2. Create the folder structure shown below (or unzip the provided template) into the repo directory.
3. In GitHub Desktop:
   - You will see file changes in the left pane.
   - Add a commit message like: `Initial AutoGen Azure RAG POC scaffold`
   - Click **Commit to main**
   - Click **Push origin**

---

## 2) Project structure

```text
src/
  config.py        # Azure OpenAI model client creation
  azure_search.py  # Azure AI Search REST calls
  tools.py         # Tool wrapper that returns formatted context
  agents.py        # AutoGen agents + team wiring
  run_chat.py      # CLI entrypoint

tests/
  test_01_config.py
  test_02_search_format.py

.env.example
requirements.txt
requirements-dev.txt
.gitignore
README.md
```

---

## 3) Setup

### 3.1 Create a virtual environment

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 3.2 Install dependencies

```bash
pip install -U pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

AutoGen install guidance shows installing `autogen-agentchat` and `autogen-ext[openai]` for model clients. citeturn4search76turn7search118

---

## 4) Configuration

Copy the example env file and fill values:

```bash
cp .env.example .env
```

### Required env vars

**Azure OpenAI (chat model)**
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_DEPLOYMENT` (your deployment name)
- `AZURE_OPENAI_MODEL` (model name for capabilities, e.g., gpt-4o / gpt-4o-mini)

**Azure AI Search**
- `AZURE_SEARCH_ENDPOINT`
- `AZURE_SEARCH_KEY`
- `AZURE_SEARCH_INDEX`

---

## 5) Run the POC

### 5.1 Quick run (single question)

```bash
python -m src.run_chat --question "What is this page about?"
```

This uses a small multi-agent team:
- Planner Agent (decides if retrieval is needed)
- Retriever Agent (calls Azure AI Search tool)
- Answer Agent (answers only from retrieved context and ends with `FINAL`)

The POC uses AutoGen AgentChat primitives shown in the official docs examples (`AssistantAgent`, `UserProxyAgent`, `RoundRobinGroupChat`, and `Console`). citeturn7search118turn7search130

---

## 6) Test each section individually

### 6.1 Unit tests (no cloud calls)

```bash
pytest -q
```

The included tests validate:
- env/config parsing
- Azure AI Search result formatting

### 6.2 Integration tests (optional)

To validate against real Azure services, run the app and verify:
1) `src.azure_search.search_topk()` returns results
2) The retriever agent returns a `CONTEXT` block
3) The answer agent responds with citations like `[1]` and ends with `FINAL`

---

## 7) Notes / Next improvements

- Add ingestion (webpage → chunking → embeddings → index) to fully automate RAG indexing.
- Add `SelectorGroupChat` to dynamically pick which agent speaks next. citeturn7search130
- Add Azure hosting (Functions/App Service) + App Insights for production monitoring.

---

## References

- Assignment definition of RAG pipeline and conversational requirement. citeturn1search1
- AutoGen framework install + AgentChat usage. citeturn4search76turn7search118
- AutoGen model clients and Azure OpenAI usage. citeturn7search128turn7search129
- Azure AI Search RAG overview. citeturn4search70
