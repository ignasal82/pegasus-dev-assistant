"""Pruebas de la evaluación: sin red."""

from unittest.mock import patch

from rag import evaluate
from rag.evaluate import CASES, NEGATIVE_CASES, Case, check
from rag.retrieve import Retrieved


def test_hay_diez_preguntas_y_tres_negativas():
    assert len(CASES) == 10
    assert len(NEGATIVE_CASES) == 3


def test_check_acepta_alternativas():
    case = Case("¿SLA?", (("15 min", "15 minutos"),))
    assert check(case, "El SLA de respuesta es de 15 minutos.")
    assert check(case, "Responder en 15 min.")
    assert not check(case, "El SLA es de una hora.")


def test_check_exige_todos_los_grupos():
    case = Case("¿core hours?", (("10:00",), ("17:00",)))
    assert check(case, "De 10:00 a 17:00.")
    assert not check(case, "Empiezan a las 10:00.")


def test_check_es_case_insensitive():
    case = Case("¿front?", (("react",), ("18",)))
    assert check(case, "React 18 o superior según la guía.")


def test_run_cuenta_ok(monkeypatch, tmp_path):
    fake_retrieved = [
        Retrieved(
            text="…",
            source="doc/conocimiento/faq.md",
            heading="",
            distance=0.1,
        )
    ]

    def fake_answer(question):
        # Respuesta que satisface todos los casos positivos.
        return (
            "No. Según el FAQ: core hours 10:00 a 17:00, commits Conventional, "
            "SEV-1 con SLA de 15 minutos, canal #incidents, React 18, "
            "contacto it-support@santopegasus.com.",
            fake_retrieved,
        )

    output = tmp_path / "registro.md"
    with patch("rag.evaluate.answer", side_effect=lambda q: fake_answer(q)):
        ok = evaluate.run(include_negative=False, output=output)

    assert ok == 10
    content = output.read_text(encoding="utf-8")
    assert "10/10" in content
    assert "doc/conocimiento/faq.md" in content
