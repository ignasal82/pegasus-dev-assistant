"""Pruebas de interacción con el agente por CLI: sin red."""

from __future__ import annotations

import sys
from unittest.mock import patch

import pytest

from rag import chat


def test_print_answer_muestra_respuesta_y_fuentes(capsys, sample_retrieved, agent_reply):
    with patch("rag.chat.answer", return_value=(agent_reply, sample_retrieved)):
        chat._print_answer("¿Cuáles son las core hours del equipo?")

    out = capsys.readouterr().out
    assert "10:00" in out
    assert "17:00" in out
    assert "Fuentes consultadas:" in out
    assert "doc/conocimiento/faq.md" in out
    assert "manual-onboarding-desarrolladores.md" in out


def test_print_answer_deduplica_fuentes(capsys):
    duplicated = [
        chat.Retrieved(
            text="a",
            source="doc/conocimiento/faq.md",
            heading="",
            distance=0.1,
        ),
        chat.Retrieved(
            text="b",
            source="doc/conocimiento/faq.md",
            heading="",
            distance=0.2,
        ),
    ]
    with patch("rag.chat.answer", return_value=("ok", duplicated)):
        chat._print_answer("pregunta")

    out = capsys.readouterr().out
    assert out.count("doc/conocimiento/faq.md") == 1


def test_print_answer_maneja_error_comprensible(capsys):
    with patch(
        "rag.chat.answer",
        side_effect=RuntimeError("Falta OPENAI_API_KEY. Copiá .env.example"),
    ):
        chat._print_answer("¿core hours?")

    out = capsys.readouterr().out
    assert out.startswith("Error:")
    assert "OPENAI_API_KEY" in out
    assert "Fuentes consultadas" not in out


def test_print_answer_indice_ausente(capsys):
    with patch(
        "rag.chat.answer",
        side_effect=RuntimeError("No existe el índice local. Ejecutá primero: python -m rag.ingest"),
    ):
        chat._print_answer("¿core hours?")

    out = capsys.readouterr().out
    assert "Error:" in out
    assert "rag.ingest" in out


def test_main_modo_una_pregunta(monkeypatch, capsys, sample_retrieved, agent_reply):
    monkeypatch.setattr(sys, "argv", ["rag.chat", "¿Cuáles", "son", "las", "core", "hours?"])
    with patch("rag.chat.answer", return_value=(agent_reply, sample_retrieved)) as mocked:
        chat.main()

    mocked.assert_called_once_with("¿Cuáles son las core hours?")
    out = capsys.readouterr().out
    assert "10:00" in out
    assert "Fuentes consultadas:" in out


def test_main_interactivo_pregunta_y_salir(monkeypatch, capsys, sample_retrieved, agent_reply):
    inputs = iter(["¿Cuáles son las core hours del equipo?", "salir"])
    monkeypatch.setattr(sys, "argv", ["rag.chat"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))

    with patch("rag.chat.answer", return_value=(agent_reply, sample_retrieved)) as mocked:
        chat.main()

    mocked.assert_called_once_with("¿Cuáles son las core hours del equipo?")
    out = capsys.readouterr().out
    assert "Pegasus Dev Assistant" in out
    assert "10:00" in out
    assert "Fuentes consultadas:" in out


@pytest.mark.parametrize("exit_word", ["salir", "exit", "quit", "SALIR", "Exit"])
def test_main_interactivo_termina_con_palabra_de_salida(monkeypatch, capsys, exit_word):
    inputs = iter([exit_word])
    monkeypatch.setattr(sys, "argv", ["rag.chat"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))

    with patch("rag.chat.answer") as mocked:
        chat.main()

    mocked.assert_not_called()
    assert "Pegasus Dev Assistant" in capsys.readouterr().out


def test_main_interactivo_ignora_entrada_vacia(monkeypatch, capsys):
    inputs = iter(["   ", "salir"])
    monkeypatch.setattr(sys, "argv", ["rag.chat"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))

    with patch("rag.chat.answer") as mocked:
        chat.main()

    mocked.assert_not_called()


def test_main_interactivo_varias_preguntas(monkeypatch, capsys, sample_retrieved):
    inputs = iter(
        [
            "¿Puedo pushear a main?",
            "¿Qué formato usan los commits?",
            "quit",
        ]
    )
    monkeypatch.setattr(sys, "argv", ["rag.chat"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))

    replies = {
        "¿Puedo pushear a main?": (
            "No. main está protegida; solo vía PR.",
            sample_retrieved,
        ),
        "¿Qué formato usan los commits?": (
            "Conventional Commits: tipo(scope): descripción.",
            sample_retrieved,
        ),
    }

    def fake_answer(question: str):
        return replies[question]

    with patch("rag.chat.answer", side_effect=fake_answer) as mocked:
        chat.main()

    assert mocked.call_count == 2
    out = capsys.readouterr().out
    assert "protegida" in out
    assert "Conventional Commits" in out
    assert out.count("Fuentes consultadas:") == 2


def test_main_interactivo_eof_termina(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["rag.chat"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": (_ for _ in ()).throw(EOFError))

    with patch("rag.chat.answer") as mocked:
        chat.main()

    mocked.assert_not_called()
    assert "Pegasus Dev Assistant" in capsys.readouterr().out


def test_main_interactivo_keyboard_interrupt_termina(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["rag.chat"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt="": (_ for _ in ()).throw(KeyboardInterrupt),
    )

    with patch("rag.chat.answer") as mocked:
        chat.main()

    mocked.assert_not_called()


def test_answer_propaga_settings_al_modelo(monkeypatch, sample_retrieved):
    from unittest.mock import MagicMock

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("RAG_CHAT_MODEL", "gpt-test-local")
    settings = chat.config.load_settings()

    fake_client = MagicMock()
    completion = MagicMock()
    completion.choices = [MagicMock(message=MagicMock(content="respuesta"))]
    fake_client.chat.completions.create.return_value = completion

    with (
        patch("rag.chat.retrieve", return_value=sample_retrieved),
        patch("rag.chat.OpenAI", return_value=fake_client),
        patch("rag.chat.load_system_prompt", return_value="system-prompt"),
    ):
        text, retrieved = chat.answer("¿core hours?", settings)

    assert text == "respuesta"
    assert retrieved is sample_retrieved
    kwargs = fake_client.chat.completions.create.call_args.kwargs
    assert kwargs["model"] == "gpt-test-local"
    assert kwargs["temperature"] == 0.2
    assert kwargs["messages"][0] == {"role": "system", "content": "system-prompt"}
    assert "¿core hours?" in kwargs["messages"][1]["content"]
    assert "10:00 a 17:00" in kwargs["messages"][1]["content"]
