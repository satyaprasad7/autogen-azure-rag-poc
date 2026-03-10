"""Tool functions for AutoGen agents.

In AutoGen AgentChat, agents can be provided with tools (plain Python callables) to perform actions.
The SelectorGroupChat docs show agents can be equipped with tools to collaborate. citeturn7search130

Here we expose a single tool: search_knowledge_base(query) -> str
which uses Azure AI Search and returns a formatted CONTEXT block.
"""

from __future__ import annotations

from .azure_search import search_topk, format_results


def search_knowledge_base(query: str, k: int = 4) -> str:
    """Retrieve top-k chunks from Azure AI Search and return a context string."""
    results = search_topk(query, k=k)
    context = format_results(results)
    if not context.strip():
        return "CONTEXT:
(No results found)"
    return "CONTEXT:
" + context
