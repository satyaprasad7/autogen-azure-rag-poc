"""AutoGen agents + team wiring.

This POC uses:
- AssistantAgent and UserProxyAgent
- RoundRobinGroupChat team
- Termination conditions to stop the chat

AutoGen's official AgentChat docs show using AssistantAgent/UserProxyAgent with RoundRobinGroupChat and Console. citeturn7search118
"""

from __future__ import annotations

import os
from typing import Optional

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from .tools import search_knowledge_base


def build_team(model_client: AzureOpenAIChatCompletionClient, input_func=input):
    """Create a small multi-agent team for RAG."""

    planner = AssistantAgent(
        name="planner",
        description="Breaks down the task and decides when retrieval is needed.",
        model_client=model_client,
        system_message=(
            "You are a planning agent. Decide if the user question needs retrieval from the knowledge base. "
            "If retrieval is needed, ask the retriever to search. Otherwise, instruct the answerer." 
            "Keep your messages short."
        ),
    )

    retriever = AssistantAgent(
        name="retriever",
        description="Retrieves relevant passages using the search_knowledge_base tool.",
        model_client=model_client,
        system_message=(
            "You are a retrieval agent. Use the search_knowledge_base tool to fetch context. "
            "Return ONLY the tool result (CONTEXT block)."
        ),
        tools=[search_knowledge_base],
    )

    answerer = AssistantAgent(
        name="answerer",
        description="Answers grounded only in the provided context.",
        model_client=model_client,
        system_message=(
            "You are the answering agent. Answer ONLY from the provided CONTEXT. "
            "If the context is insufficient, say: 'I don't know based on the provided context.' "
            "Cite sources like [1], [2] from the CONTEXT blocks. "
            "End your final message with the token: FINAL"
        ),
    )

    

    # Stop when answerer outputs FINAL, or after N messages to avoid loops
    termination = TextMentionTermination("FINAL") | MaxMessageTermination(
        max_messages=int(os.environ.get("MAX_MESSAGES", "12"))
    )

    team = RoundRobinGroupChat(
        participants=[ planner, retriever, answerer],
        termination_condition=termination,
    )
    return team
