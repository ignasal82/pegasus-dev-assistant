"""Pruebas de configuración: sin red y sin API key real."""

import pytest

from rag import config


def test_knowledge_dir_exists():
    assert config.KNOWLEDGE_DIR.is_dir()


def test_knowledge_files_son_exactamente_cinco():
    files = config.knowledge_files()
    assert len(files) == 5
    names = {f.name for f in files}
    assert "faq.md" in names
    assert "README.md" not in names


def test_knowledge_files_excluye_pdf():
    files = config.knowledge_files()
    assert all(f.suffix == ".md" for f in files)


def test_settings_defaults(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("RAG_TOP_K", raising=False)
    settings = config.load_settings()
    assert settings.embedding_model == "text-embedding-3-small"
    assert settings.chat_model == "gpt-4o-mini"
    assert settings.top_k == 4


def test_require_api_key_falla_sin_clave(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    settings = config.load_settings()
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        settings.require_api_key()


def test_require_api_key_ok(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    settings = config.load_settings()
    assert settings.require_api_key() == "sk-test"
