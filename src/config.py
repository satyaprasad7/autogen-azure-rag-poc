from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv


def load_env(override: bool = False) -> None:
    repo_root = Path(__file__).resolve().parents[1]  # repo root (folder containing src/)
    dotenv_path = repo_root / ".env"
    load_dotenv(dotenv_path=dotenv_path, override=override)


def create_model_client() -> Any:
    """
    Creates and returns an AutoGen ChatCompletion model client.

    Expected .env / environment variables (recommended):
      - AZURE_OPENAI_ENDPOINT          e.g. https://<resource>.openai.azure.com/
      - AZURE_OPENAI_API_KEY
      - AZURE_OPENAI_CHAT_DEPLOYMENT_NAME  (or AZURE_OPENAI_DEPLOYMENT)
      - AZURE_OPENAI_API_VERSION       e.g. 2024-06-01
      - AZURE_OPENAI_MODEL             e.g. gpt-4o (optional but recommended)

    Notes:
    - AutoGen model clients live in autogen_ext. [1](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/components/model-clients.html)[2](https://autogen.linsoap.social/autogen/0.4.9/user-guide/agentchat-user-guide/tutorial/models.html)[3](https://github.com/microsoft/autogen/issues/3740)
    """
    # ---- Read env ----
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").strip()
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "").strip()
    deployment = (
        os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
        or os.environ.get("AZURE_OPENAI_DEPLOYMENT")
        or os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
        or ""
    ).strip()
    api_version = (os.environ.get("AZURE_OPENAI_API_VERSION") or "2024-06-01").strip()
    model = (os.environ.get("AZURE_OPENAI_MODEL") or "gpt-4o").strip()

    if not endpoint:
        raise ValueError("Missing AZURE_OPENAI_ENDPOINT in environment/.env")
    if not deployment:
        raise ValueError(
            "Missing deployment name. Set AZURE_OPENAI_CHAT_DEPLOYMENT_NAME (recommended) "
            "or AZURE_OPENAI_DEPLOYMENT."
        )

    # ---- Create client (API-key auth by default) ----
    # AzureOpenAIChatCompletionClient is the AutoGen model client for Azure OpenAI. [2](https://autogen.linsoap.social/autogen/0.4.9/user-guide/agentchat-user-guide/tutorial/models.html)[1](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/components/model-clients.html)
    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

    if api_key:
        return AzureOpenAIChatCompletionClient(
            azure_endpoint=endpoint,
            api_key=api_key,
            azure_deployment=deployment,
            model=model,
            api_version=api_version,
        )

    # ---- Optional: AAD auth fallback (no key) ----
    # AutoGen docs show Azure AD token provider usage for AzureOpenAIChatCompletionClient. [2](https://autogen.linsoap.social/autogen/0.4.9/user-guide/agentchat-user-guide/tutorial/models.html)
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )

    return AzureOpenAIChatCompletionClient(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        azure_deployment=deployment,
        model=model,
        api_version=api_version,
    )