"""Pruebas del prompt: sin red."""

from rag.prompts import _FALLBACK_PROMPT, build_user_message, load_system_prompt
import rag.prompts as prompts


def test_system_prompt_no_vacio():
    prompt = load_system_prompt()
    assert len(prompt) > 100
    assert "Pegasus Dev Assistant" in prompt


def test_system_prompt_prohibe_inventar():
    prompt = load_system_prompt()
    assert "invent" in prompt.lower()


def test_system_prompt_usa_fallback_si_falta_archivo(monkeypatch, tmp_path):
    monkeypatch.setattr(prompts.config, "PROMPT_FILE", tmp_path / "no-existe.md")
    assert load_system_prompt() == _FALLBACK_PROMPT


def test_system_prompt_usa_fallback_si_no_hay_bloque_text(monkeypatch, tmp_path):
    fake = tmp_path / "prompt.md"
    fake.write_text("# sin bloque\n\nSolo texto.", encoding="utf-8")
    monkeypatch.setattr(prompts.config, "PROMPT_FILE", fake)
    assert load_system_prompt() == _FALLBACK_PROMPT


def test_build_user_message_incluye_contexto_y_pregunta():
    blocks = [
        ("doc/conocimiento/faq.md", "Las core hours son 10:00-17:00."),
        ("doc/conocimiento/onboarding/manual.md", "Horario flexible."),
    ]
    message = build_user_message("¿Cuáles son las core hours?", blocks)
    assert "doc/conocimiento/faq.md" in message
    assert "10:00-17:00" in message
    assert "¿Cuáles son las core hours?" in message
    assert "ÚNICAMENTE" in message
    assert "Fragmento 1" in message
    assert "Fragmento 2" in message


def test_build_user_message_sin_contexto_sigue_incluyendo_pregunta():
    message = build_user_message("¿Hay salario?", [])
    assert "¿Hay salario?" in message
    assert "Contexto recuperado" in message
