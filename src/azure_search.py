"""Azure AI Search retrieval.

This module performs a simple Search REST call (classic/hybrid style) to fetch top-k chunks.
Microsoft Learn describes Azure AI Search as a retrieval system for RAG patterns. citeturn4search70

NOTE: Index schema varies. By default we expect a searchable field named `content` and an optional `source`.
Override with env vars: AZURE_SEARCH_CONTENT_FIELD, AZURE_SEARCH_SOURCE_FIELD.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List

import requests


@dataclass(frozen=True)
class AzureSearchConfig:
    endpoint: str
    api_key: str
    index: str
    api_version: str
    content_field: str = "content"
    source_field: str = "source"


def get_search_config() -> AzureSearchConfig:
    endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT", "").strip()
    api_key = os.environ.get("AZURE_SEARCH_KEY", "").strip()
    index = os.environ.get("AZURE_SEARCH_INDEX", "").strip()
    api_version = os.environ.get("AZURE_SEARCH_API_VERSION", "2023-11-01").strip()
    content_field = os.environ.get("AZURE_SEARCH_CONTENT_FIELD", "content").strip() or "content"
    source_field = os.environ.get("AZURE_SEARCH_SOURCE_FIELD", "source").strip() or "source"

    missing = [
        name
        for name, value in [
            ("AZURE_SEARCH_ENDPOINT", endpoint),
            ("AZURE_SEARCH_KEY", api_key),
            ("AZURE_SEARCH_INDEX", index),
        ]
        if not value
    ]
    if missing:
        raise EnvironmentError(
            "Missing required environment variables: " + ", ".join(missing)
        )

    return AzureSearchConfig(
        endpoint=endpoint,
        api_key=api_key,
        index=index,
        api_version=api_version,
        content_field=content_field,
        source_field=source_field,
    )


def search_topk(query: str, k: int | None = None) -> List[Dict[str, Any]]:
    """Run a top-k search against Azure AI Search."""
    cfg = get_search_config()
    top_k = k if k is not None else int(os.environ.get("AZURE_SEARCH_TOP_K", "4"))

    # Normalize endpoint
    endpoint = cfg.endpoint.rstrip("/")
    url = f"{endpoint}/indexes/{cfg.index}/docs/search?api-version={cfg.api_version}"

    headers = {
        "Content-Type": "application/json",
        "api-key": cfg.api_key,
    }

    payload = {
        "search": query,
        "top": top_k,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("value", [])


def format_results(results: List[Dict[str, Any]], max_chars: int = 1200) -> str:
    """Format Azure AI Search results into a compact context block."""
    cfg = get_search_config()

    blocks: List[str] = []
    for i, doc in enumerate(results, start=1):
        content = doc.get(cfg.content_field, "")
        if content is None:
            content = ""
        content = str(content).strip()
        if len(content) > max_chars:
            content = content[: max_chars - 3] + "..."

        source = doc.get(cfg.source_field, "") or doc.get("url", "") or doc.get("id", "")
        source = str(source).strip() or "azure-ai-search"

        blocks.append(f"[{i}] source={source}
{content}")

    return "

".join(blocks)
