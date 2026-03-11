"""Tool functions for AutoGen agents.

In AutoGen AgentChat, agents can be provided with tools (plain Python callables) to perform actions.
The SelectorGroupChat docs show agents can be equipped with tools to collaborate. citeturn7search130

Here we expose a single tool: search_knowledge_base(query) -> str
which uses Azure AI Search and returns a formatted CONTEXT block.
"""

from __future__ import annotations

import os
from typing import List, Dict, Any

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient  # [2](https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.searchclient?view=azure-python)


def _get_search_client() -> SearchClient:
    endpoint = os.environ.get("AZURE_SEARCH_SERVICE_ENDPOINT", "").strip()
    index_name = os.environ.get("AZURE_SEARCH_INDEX_NAME", "").strip()
    api_key = os.environ.get("AZURE_SEARCH_API_KEY", "").strip()

    if not endpoint:
        raise ValueError("Missing AZURE_SEARCH_SERVICE_ENDPOINT")
    if not index_name:
        raise ValueError("Missing AZURE_SEARCH_INDEX_NAME")
    if not api_key:
        raise ValueError("Missing AZURE_SEARCH_API_KEY")

    # SearchClient(endpoint, index_name, AzureKeyCredential(key)) [2](https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.searchclient?view=azure-python)
    return SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(api_key))


def search_knowledge_base(query: str, top_k: int = 5) -> str:
    client = _get_search_client()

    results = client.search(
        search_text=query,
        top=top_k,
        select=["content", "source"],  
    )

    chunks = []
    for i, r in enumerate(results, start=1):
        content = r.get("content")
        source = r.get("source")

        # Guard against empty rows
        if not content:
            continue

        # Trim long content
        content = content.strip()
        if len(content) > 1200:
            content = content[:1200] + "..."

        chunks.append(
            f"[{i}] SOURCE: {source}\n"
            f"CONTENT: {content}\n"
        )

    if not chunks:
        return "CONTEXT:\n(No relevant content found in the search index.)\n"

    return "CONTEXT:\n\n" + "\n".join(chunks)