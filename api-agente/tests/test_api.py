"""Pruebas HTTP de la API sin llamadas reales a OpenAI."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from agent_api import main
from rag.retrieve import Retrieved


client = TestClient(main.app)


def test_root_redirige_a_docs():
    response = client.get("/", follow_redirects=False)
    assert response.status_code in {307, 302}
    assert response.headers["location"] == "/docs"


@pytest.fixture(autouse=True)
def clean_sessions():
    main.sessions.clear()
    yield
    main.sessions.clear()


@pytest.fixture
def retrieved() -> list[Retrieved]:
    return [
        Retrieved(
            text="Core hours: 10:00 a 17:00.",
            source="doc/conocimiento/faq.md",
            heading="Horarios",
            distance=0.12,
        )
    ]


def test_health_ready(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setattr(main.config, "CHROMA_DIR", tmp_path)
    prompt = tmp_path / "prompt.md"
    prompt.write_text("prompt", encoding="utf-8")
    monkeypatch.setattr(main.config, "PROMPT_FILE", prompt)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "api_key_configured": True,
        "index_available": True,
        "prompt_available": True,
    }


def test_health_degraded_no_expone_clave(monkeypatch, tmp_path: Path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(main.config, "CHROMA_DIR", tmp_path / "no-index")
    monkeypatch.setattr(main.config, "PROMPT_FILE", tmp_path / "no-prompt")

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "degraded"
    assert response.json()["api_key_configured"] is False
    assert "sk-" not in response.text


def test_config_devuelve_solo_valores_publicos(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-secreto")
    monkeypatch.setenv("RAG_CHAT_MODEL", "modelo-chat")
    monkeypatch.setenv("RAG_EMBEDDING_MODEL", "modelo-embedding")
    monkeypatch.setenv("RAG_TOP_K", "5")

    response = client.get("/config")

    assert response.status_code == 200
    assert response.json() == {
        "chat_model": "modelo-chat",
        "embedding_model": "modelo-embedding",
        "top_k": 5,
    }
    assert "sk-secreto" not in response.text


def test_chat_crea_sesion_y_devuelve_fuentes(retrieved):
    with patch(
        "agent_api.main.ask",
        return_value=("Las core hours son de 10:00 a 17:00.", retrieved),
    ):
        response = client.post("/chat", json={"question": "¿Cuáles son las core hours?"})

    assert response.status_code == 200
    body = response.json()
    assert body["session_id"]
    assert "10:00" in body["answer"]
    assert body["sources"] == [
        {
            "source": "doc/conocimiento/faq.md",
            "heading": "Horarios",
            "distance": 0.12,
        }
    ]


def test_chat_reutiliza_sesion(retrieved):
    with patch("agent_api.main.ask", return_value=("respuesta", retrieved)) as mocked:
        first = client.post("/chat", json={"question": "primera"}).json()
        second = client.post(
            "/chat",
            json={"question": "segunda", "session_id": first["session_id"]},
        ).json()

    assert second["session_id"] == first["session_id"]
    assert mocked.call_count == 2
    assert mocked.call_args_list[0].args[0] is mocked.call_args_list[1].args[0]


@pytest.mark.parametrize("question", ["", "   "])
def test_chat_rechaza_pregunta_vacia(question):
    response = client.post("/chat", json={"question": question})
    assert response.status_code == 422


def test_chat_rechaza_session_id_invalido():
    response = client.post(
        "/chat",
        json={"question": "hola", "session_id": "no-es-uuid"},
    )
    assert response.status_code == 422
    assert "UUID" in response.json()["detail"]


def test_chat_traduce_error_de_configuracion():
    with patch(
        "agent_api.main.ask",
        side_effect=RuntimeError("No existe el índice local."),
    ):
        response = client.post("/chat", json={"question": "hola"})

    assert response.status_code == 503
    assert "índice" in response.json()["detail"]


def test_chat_oculta_error_inesperado():
    with patch("agent_api.main.ask", side_effect=Exception("sk-secreto-interno")):
        response = client.post("/chat", json={"question": "hola"})

    assert response.status_code == 502
    assert "sk-secreto-interno" not in response.text


def test_delete_session(retrieved):
    with patch("agent_api.main.ask", return_value=("respuesta", retrieved)):
        session_id = client.post("/chat", json={"question": "hola"}).json()["session_id"]

    first = client.delete(f"/sessions/{session_id}")
    second = client.delete(f"/sessions/{session_id}")

    assert first.status_code == 200
    assert first.json() == {"deleted": True}
    assert second.json() == {"deleted": False}


def test_delete_rechaza_uuid_invalido():
    response = client.delete("/sessions/no-es-uuid")
    assert response.status_code == 422
