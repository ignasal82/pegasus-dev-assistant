"""Pruebas del prompt: sin red."""

from rag.prompts import build_user_message, load_system_prompt


def test_system_prompt_no_vacio():
    prompt = load_system_prompt()
    assert len(prompt) > 100
    assert "Pegasus Dev Assistant" in prompt


def test_system_prompt_prohibe_inventar():
    prompt = load_system_prompt()
    assert "invent" in prompt.lower()


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
