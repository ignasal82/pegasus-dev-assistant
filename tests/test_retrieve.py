"""Pruebas de retrieval y chat con mocks: sin red."""

from unittest.mock import MagicMock, patch

import pytest

from rag import chat, config, retrieve


def _fake_openai_embeddings():
    fake = MagicMock()
    response = MagicMock()
    response.data = [MagicMock(embedding=[0.1, 0.2])]
    fake.embeddings.create.return_value = response
    return fake


def test_retrieve_falla_sin_indice(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setattr(config, "CHROMA_DIR", tmp_path / "no-existe")
    monkeypatch.setattr(retrieve.config, "CHROMA_DIR", tmp_path / "no-existe")
    with pytest.raises(RuntimeError, match="rag.ingest"):
        retrieve.retrieve("pregunta")


def test_retrieve_mapea_resultados(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    settings = config.load_settings()

    fake_collection = MagicMock()
    fake_collection.query.return_value = {
        "documents": [["texto del fragmento"]],
        "metadatas": [[{"source": "doc/conocimiento/faq.md", "heading": "Horarios"}]],
        "distances": [[0.12]],
    }

    with (
        patch("rag.retrieve._get_collection", return_value=fake_collection),
        patch("rag.retrieve.OpenAI", return_value=_fake_openai_embeddings()),
    ):
        results = retrieve.retrieve("¿core hours?", settings)

    assert len(results) == 1
    assert results[0].source == "doc/conocimiento/faq.md"
    assert results[0].heading == "Horarios"


def test_answer_usa_contexto_y_devuelve_fuentes(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    settings = config.load_settings()

    retrieved = [
        retrieve.Retrieved(
            text="Core hours: 10:00 a 17:00.",
            source="doc/conocimiento/faq.md",
            heading="Horarios",
            distance=0.1,
        )
    ]

    fake_chat_client = MagicMock()
    completion = MagicMock()
    completion.choices = [MagicMock(message=MagicMock(content="Según el FAQ, 10:00–17:00."))]
    fake_chat_client.chat.completions.create.return_value = completion

    with (
        patch("rag.chat.retrieve", return_value=retrieved),
        patch("rag.chat.OpenAI", return_value=fake_chat_client),
    ):
        text, sources = chat.answer("¿Cuáles son las core hours?", settings)

    assert "10:00" in text
    assert sources[0].source == "doc/conocimiento/faq.md"

    # El mensaje enviado al modelo debe contener el contexto recuperado
    sent_messages = fake_chat_client.chat.completions.create.call_args.kwargs["messages"]
    user_message = sent_messages[1]["content"]
    assert "Core hours: 10:00 a 17:00." in user_message
    assert sent_messages[0]["role"] == "system"
