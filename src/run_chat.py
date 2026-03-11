"""CLI entrypoint.

Runs the AutoGen AgentChat team and streams to console.
The AgentChat docs show using Console + run_stream() to stream results. citeturn7search118
"""

from __future__ import annotations

import argparse
import asyncio
import logging

from autogen_agentchat.ui import Console
from autogen_core import EVENT_LOGGER_NAME  # AutoGen event logger name [1](https://learning.cloud.microsoft/detail/2e9aab2e-25df-4bed-bebe-31676e44bb04?context={%22subEntityId%22:{%22source%22:%22M365Search%22}})

from .config import load_env, create_model_client
from .agents import build_team


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AutoGen + Azure AI Search RAG POC")
    p.add_argument("--question", type=str, default="What is this page about?", help="User question")
    return p.parse_args()


async def main() -> None:
    args = _parse_args()
    load_env()

    # ---- Debug logging for model calls ----
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(EVENT_LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    client = create_model_client()
    team = build_team(model_client=client)

    task = (
        "USER QUESTION:\n"
        f"{args.question}\n\n"
        "INSTRUCTIONS:\n"
        "- Planner: decide if retrieval is needed.\n"
        "- Retriever: call search_knowledge_base and return CONTEXT.\n"
        "- Answerer: answer ONLY from CONTEXT with citations [1],[2]...\n"
    )

    stream = team.run_stream(task=task)
    await Console(stream)


if __name__ == "__main__":
    asyncio.run(main())