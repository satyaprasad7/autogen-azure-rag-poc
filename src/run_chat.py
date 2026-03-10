"""CLI entrypoint.

Runs the AutoGen AgentChat team and streams to console.
The AgentChat docs show using Console + run_stream() to stream results. citeturn7search118
"""

from __future__ import annotations

import argparse
import asyncio

from autogen_agentchat.ui import Console

from .config import load_env, build_model_client
from .agents import build_team


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AutoGen + Azure AI Search RAG POC")
    p.add_argument("--question", type=str, default="What is this page about?", help="User question")
    return p.parse_args()


async def main() -> None:
    args = _parse_args()
    load_env()

    model_client = build_model_client()
    team = build_team(model_client=model_client, input_func=input)

    task = (
        "USER QUESTION:
"
        f"{args.question}

"
        "INSTRUCTIONS:
"
        "- Planner: decide if retrieval is needed.
"
        "- Retriever: call search_knowledge_base and return CONTEXT.
"
        "- Answerer: answer ONLY from CONTEXT with citations [1],[2]... and end with FINAL.
"
    )

    stream = team.run_stream(task=task)
    await Console(stream)


if __name__ == "__main__":
    asyncio.run(main())
