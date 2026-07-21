"""Pruebas de ingestión con mocks: sin red ni API key real."""

from unittest.mock import MagicMock, patch

import pytest

from rag import config, ingest


def test_build_chunks_cubre_las_cinco_fuentes():
    chunks = ingest.build_chunks()
    sources = {c.source for c in chunks}
    assert len(sources) == 5
    assert "doc/conocimiento/faq.md" in sources


def test_build_chunks_excluye_readme_y_pdf():
    chunks = ingest.build_chunks()
    assert all(c.source.endswith(".md") for c in chunks)
    assert not any("README" in c.source for c in chunks)


def test_ingest_falla_sin_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        ingest.ingest()


def test_embed_texts_respeta_batches(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    settings = config.load_settings()

    fake_client = MagicMock()

    def fake_create(model, input):  # noqa: A002 - firma del SDK
        response = MagicMock()
        response.data = [MagicMock(embedding=[0.0, 1.0]) for _ in input]
        return response

    fake_client.embeddings.create.side_effect = fake_create

    with patch("rag.ingest.OpenAI", return_value=fake_client):
        texts = [f"texto {i}" for i in range(ingest.EMBED_BATCH_SIZE + 10)]
        embeddings = ingest.embed_texts(texts, settings)

    assert len(embeddings) == len(texts)
    assert fake_client.embeddings.create.call_count == 2
