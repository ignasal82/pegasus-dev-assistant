"""Pruebas de la evaluación: sin red."""

from unittest.mock import patch

from rag import evaluate
from rag.evaluate import CASES, NEGATIVE_CASES, Case, check
from rag.retrieve import Retrieved


def test_hay_diez_preguntas_y_tres_negativas():
    assert len(CASES) == 10
    assert len(NEGATIVE_CASES) == 3


def test_casos_positivos_cubren_temas_clave():
    questions = " ".join(case.question.lower() for case in CASES)
    for keyword in ("core hours", "main", "commits", "sev-1", "jwt", "it"):
        assert keyword in questions


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


def test_check_casos_negativos_tipicos():
    salario = NEGATIVE_CASES[0]
    hardcode = NEGATIVE_CASES[1]
    medico = NEGATIVE_CASES[2]

    assert check(salario, "No está en la KB; contactá a People.")
    assert check(hardcode, "No. Usá AWS Secrets Manager o 1Password.")
    assert check(medico, "Eso queda fuera del alcance de la documentación técnica.")
    assert not check(salario, "El salario es USD 180000.")


def test_run_cuenta_ok(tmp_path):
    fake_retrieved = [
        Retrieved(
            text="…",
            source="doc/conocimiento/faq.md",
            heading="",
            distance=0.1,
        )
    ]

    def fake_answer(question):
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
    assert "sk-" not in content
    assert "OPENAI_API_KEY" not in content


def test_run_con_negativas_no_cuenta_en_score_de_diez(tmp_path, capsys):
    fake_retrieved = [
        Retrieved(
            text="…",
            source="doc/conocimiento/faq.md",
            heading="",
            distance=0.1,
        )
    ]

    def fake_answer(question: str):
        if "salario" in question.lower():
            return ("No está documentado; contactá a People.", fake_retrieved)
        if "hardcodear" in question.lower():
            return ("No. Usá Secrets Manager o 1Password.", fake_retrieved)
        if "médico" in question.lower() or "medico" in question.lower():
            return ("No está en la documentación interna.", fake_retrieved)
        return (
            "No. Según el FAQ: core hours 10:00 a 17:00, commits Conventional, "
            "SEV-1 con SLA de 15 minutos, canal #incidents, React 18, "
            "contacto it-support@santopegasus.com.",
            fake_retrieved,
        )

    output = tmp_path / "registro.md"
    with patch("rag.evaluate.answer", side_effect=fake_answer):
        ok = evaluate.run(include_negative=True, output=output)

    assert ok == 10
    out = capsys.readouterr().out
    assert "[13/13]" in out
    assert "-> OK" in out
    content = output.read_text(encoding="utf-8")
    assert content.count("| OK |") == 13
