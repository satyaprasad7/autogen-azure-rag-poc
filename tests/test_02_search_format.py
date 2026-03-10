import pytest

from src.azure_search import format_results


def test_format_results_basic(monkeypatch):
    # Provide minimal env to satisfy get_search_config inside format_results
    monkeypatch.setenv("AZURE_SEARCH_ENDPOINT", "https://example.search.windows.net")
    monkeypatch.setenv("AZURE_SEARCH_KEY", "key")
    monkeypatch.setenv("AZURE_SEARCH_INDEX", "idx")
    monkeypatch.setenv("AZURE_SEARCH_CONTENT_FIELD", "content")
    monkeypatch.setenv("AZURE_SEARCH_SOURCE_FIELD", "source")

    results = [
        {"content": "hello", "source": "doc1"},
        {"content": "world", "source": "doc2"},
    ]

    txt = format_results(results, max_chars=10)
    assert "[1]" in txt
    assert "source=doc1" in txt
    assert "hello" in txt


def test_format_results_truncates(monkeypatch):
    monkeypatch.setenv("AZURE_SEARCH_ENDPOINT", "https://example.search.windows.net")
    monkeypatch.setenv("AZURE_SEARCH_KEY", "key")
    monkeypatch.setenv("AZURE_SEARCH_INDEX", "idx")

    results = [{"content": "x" * 1000, "source": "s"}]
    txt = format_results(results, max_chars=20)
    assert txt.count("...") == 1
