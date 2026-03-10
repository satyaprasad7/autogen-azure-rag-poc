import os
import pytest

from src.config import get_azure_openai_config


def test_config_missing_env(monkeypatch):
    for k in [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_API_VERSION",
        "AZURE_OPENAI_DEPLOYMENT",
    ]:
        monkeypatch.delenv(k, raising=False)

    with pytest.raises(EnvironmentError):
        get_azure_openai_config()


def test_config_present_env(monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.openai.azure.com/")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "key")
    monkeypatch.setenv("AZURE_OPENAI_API_VERSION", "2024-06-01")
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "chat")
    monkeypatch.setenv("AZURE_OPENAI_MODEL", "gpt-4o-mini")

    cfg = get_azure_openai_config()
    assert cfg.endpoint.startswith("https://")
    assert cfg.deployment == "chat"
    assert cfg.model == "gpt-4o-mini"
