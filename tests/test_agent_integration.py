"""Prueba de humo opcional contra el agente real (OpenAI + Chroma).

Se omite por defecto si falta la API key o el índice. Ejecutar con:

    pytest -m integration
"""

from __future__ import annotations

import os

import pytest

from rag import chat, config


def _integration_ready() -> bool:
    if not os.environ.get("OPENAI_API_KEY"):
        return False
    if not config.CHROMA_DIR.exists():
        return False
    try:
        import chromadb

        client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
        collection = client.get_collection(config.COLLECTION_NAME)
        return collection.count() > 0
    except Exception:
        return False


pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    not _integration_ready(),
    reason="Requiere OPENAI_API_KEY e índice Chroma (python -m rag.ingest)",
)
def test_agente_responde_core_hours_con_fuente():
    text, retrieved = chat.answer("¿Cuáles son las core hours del equipo?")

    assert "10:00" in text
    assert "17:00" in text
    assert retrieved
    sources = {item.source for item in retrieved}
    assert any(source.endswith("faq.md") for source in sources)


@pytest.mark.skipif(
    not _integration_ready(),
    reason="Requiere OPENAI_API_KEY e índice Chroma (python -m rag.ingest)",
)
def test_agente_no_inventa_salario():
    text, _retrieved = chat.answer("¿Cuál es el salario de un Staff Engineer?")
    lowered = text.lower()

    assert any(token in lowered for token in ("no", "people", "document"))
    assert "180" not in text
    assert "$" not in text
