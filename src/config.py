"""Configuration helpers.

Creates the AutoGen Azure OpenAI model client used by AgentChat agents.

AutoGen docs show AgentChat agents such as AssistantAgent/UserProxyAgent can be wired with model clients.
They also list AzureOpenAIChatCompletionClient as the Azure OpenAI model client. citeturn7search118turn7search128turn7search129
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient


@dataclass(frozen=True)
class AzureOpenAIConfig:
    endpoint: str
    api_key: str
    api_version: str
    deployment: str
    model: str


def load_env(override: bool = False) -> None:
    """Load .env into environment variables (local dev)."""
    load_dotenv(override=override)


def get_azure_openai_config() -> AzureOpenAIConfig:
    """Read Azure OpenAI config from env and validate required keys."""
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").strip()
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "").strip()
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "").strip()
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "").strip()
    model = os.environ.get("AZURE_OPENAI_MODEL", "").strip() or "gpt-4o-mini"

    missing = [
        name
        for name, value in [
            ("AZURE_OPENAI_ENDPOINT", endpoint),
            ("AZURE_OPENAI_API_KEY", api_key),
            ("AZURE_OPENAI_API_VERSION", api_version),
            ("AZURE_OPENAI_DEPLOYMENT", deployment),
        ]
        if not value
    ]
    if missing:
        raise EnvironmentError(
            "Missing required environment variables: " + ", ".join(missing)
        )

    return AzureOpenAIConfig(
        endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
        deployment=deployment,
        model=model,
    )


def build_model_client() -> AzureOpenAIChatCompletionClient:
    """Create the AutoGen Azure OpenAI chat completion client."""
    cfg = get_azure_openai_config()
    return AzureOpenAIChatCompletionClient(
        azure_endpoint=cfg.endpoint,
        api_key=cfg.api_key,
        api_version=cfg.api_version,
        azure_deployment=cfg.deployment,
        model=cfg.model,
        temperature=0.2,
    )
