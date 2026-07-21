"""Pruebas de la consola interactiva con memoria: sin red."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from rag import console


@pytest.fixture
def session(monkeypatch) -> console.Session:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    return console.Session()


def _fake_completion(text: str) -> MagicMock:
    completion = MagicMock()
    completion.choices = [MagicMock(message=MagicMock(content=text))]
    return completion


def test_ask_incluye_memoria_previa(session, sample_retrieved):
    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value = _fake_completion("respuesta 2")
    session.memory = [
        {"role": "user", "content": "pregunta previa"},
        {"role": "assistant", "content": "respuesta previa"},
    ]

    with (
        patch("rag.console.retrieve", return_value=sample_retrieved),
        patch("rag.console.OpenAI", return_value=fake_client),
        patch("rag.console.load_system_prompt", return_value="system-prompt"),
    ):
        text, retrieved = console.ask(session, "¿core hours?")

    assert text == "respuesta 2"
    assert retrieved is sample_retrieved
    messages = fake_client.chat.completions.create.call_args.kwargs["messages"]
    assert messages[0] == {"role": "system", "content": "system-prompt"}
    assert messages[1]["content"] == "pregunta previa"
    assert messages[2]["content"] == "respuesta previa"
    assert "¿core hours?" in messages[3]["content"]


def test_ask_guarda_pregunta_original_en_memoria(session, sample_retrieved):
    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value = _fake_completion("ok")

    with (
        patch("rag.console.retrieve", return_value=sample_retrieved),
        patch("rag.console.OpenAI", return_value=fake_client),
        patch("rag.console.load_system_prompt", return_value="sp"),
    ):
        console.ask(session, "¿core hours?")

    # La memoria guarda la pregunta limpia, sin el contexto inyectado.
    assert session.memory[-2] == {"role": "user", "content": "¿core hours?"}
    assert session.memory[-1] == {"role": "assistant", "content": "ok"}
    assert session.questions == ["¿core hours?"]


def test_memoria_se_recorta_al_maximo(session):
    for i in range(console.MAX_TURNS_IN_MEMORY + 3):
        session.remember(f"pregunta {i}", f"respuesta {i}")

    assert len(session.memory) == console.MAX_TURNS_IN_MEMORY * 2
    # Se conservan los intercambios más recientes.
    assert session.memory[-2]["content"] == f"pregunta {console.MAX_TURNS_IN_MEMORY + 2}"


def test_set_top_k_valida_rango(session):
    session.set_top_k(6)
    assert session.settings.top_k == 6
    with pytest.raises(ValueError):
        session.set_top_k(0)
    with pytest.raises(ValueError):
        session.set_top_k(11)


def test_print_answer_sin_fragmentos(capsys, sample_retrieved, agent_reply):
    console.print_answer(agent_reply, sample_retrieved, show_fragments=False)

    out = capsys.readouterr().out
    assert "10:00" in out
    assert "Fuentes consultadas:" in out
    assert "Fragmentos recuperados" not in out


def test_print_answer_con_fragmentos(capsys, sample_retrieved, agent_reply):
    console.print_answer(agent_reply, sample_retrieved, show_fragments=True)

    out = capsys.readouterr().out
    assert "Fragmentos recuperados:" in out
    assert "Horarios y disponibilidad" in out
    assert "0.110" in out


def test_comando_fuentes_alterna(session, capsys):
    assert console.handle_command(session, "/fuentes") is True
    assert session.show_fragments is True
    console.handle_command(session, "/fuentes")
    assert session.show_fragments is False


def test_comando_topk_actualiza(session, capsys):
    console.handle_command(session, "/topk 7")
    assert session.settings.top_k == 7
    assert "7" in capsys.readouterr().out


def test_comando_topk_invalido(session, capsys):
    console.handle_command(session, "/topk abc")
    console.handle_command(session, "/topk 99")
    out = capsys.readouterr().out
    assert "Uso: /topk N" in out
    assert "entre 1 y 10" in out
    assert session.settings.top_k == 4


def test_comando_historial_y_limpiar(session, capsys):
    session.remember("¿core hours?", "10 a 17")
    console.handle_command(session, "/historial")
    assert "¿core hours?" in capsys.readouterr().out

    console.handle_command(session, "/limpiar")
    assert session.memory == []
    assert session.questions == []
    console.handle_command(session, "/historial")
    assert "Todavía no hay preguntas" in capsys.readouterr().out


def test_comando_salir_termina(session):
    assert console.handle_command(session, "/salir") is False


def test_comando_desconocido(session, capsys):
    assert console.handle_command(session, "/nada") is True
    assert "Comando desconocido" in capsys.readouterr().out


def test_main_pregunta_y_salir(monkeypatch, capsys, sample_retrieved, agent_reply):
    inputs = iter(["¿Cuáles son las core hours del equipo?", "salir"])
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))

    with patch("rag.console.ask", return_value=(agent_reply, sample_retrieved)) as mocked:
        console.main()

    mocked.assert_called_once()
    assert mocked.call_args.args[1] == "¿Cuáles son las core hours del equipo?"
    out = capsys.readouterr().out
    assert "Pegasus Dev Assistant" in out
    assert "10:00" in out
    assert "¡Hasta luego!" in out


def test_main_error_no_corta_la_sesion(monkeypatch, capsys, sample_retrieved, agent_reply):
    inputs = iter(["primera", "segunda", "quit"])
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))

    results = iter(
        [
            RuntimeError("No existe el índice local. Ejecutá primero: python -m rag.ingest"),
            (agent_reply, sample_retrieved),
        ]
    )

    def fake_ask(_session, _question):
        result = next(results)
        if isinstance(result, Exception):
            raise result
        return result

    with patch("rag.console.ask", side_effect=fake_ask):
        console.main()

    out = capsys.readouterr().out
    assert "Error:" in out
    assert "rag.ingest" in out
    assert "10:00" in out


def test_main_eof_termina(monkeypatch, capsys):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setattr(
        "builtins.input", lambda _prompt="": (_ for _ in ()).throw(EOFError)
    )

    with patch("rag.console.ask") as mocked:
        console.main()

    mocked.assert_not_called()
    assert "¡Hasta luego!" in capsys.readouterr().out
