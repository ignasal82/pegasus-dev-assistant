"""Evaluación del challenge: las 10 preguntas + 3 pruebas negativas.

Uso:
    python -m rag.evaluate              # corre las 10 preguntas
    python -m rag.evaluate --negativas  # incluye las 3 pruebas negativas
    python -m rag.evaluate --salida resultados.md

Requiere índice creado (python -m rag.ingest) y OPENAI_API_KEY en .env.
La verificación es por palabras clave: sirve como primer filtro; el registro
final conviene revisarlo a mano.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from rag import config
from rag.chat import answer


@dataclass(frozen=True)
class Case:
    question: str
    # Grupos de alternativas: la respuesta debe contener al menos una
    # alternativa de CADA grupo (case-insensitive).
    expected_groups: tuple[tuple[str, ...], ...]


CASES: list[Case] = [
    Case("¿Cuáles son las core hours del equipo?", (("10:00",), ("17:00",))),
    Case("¿Cómo solicito accesos el Día 1?", (("it-support", "IT"),)),
    Case("¿Puedo pushear directamente a main?", (("no", "prohibido"),)),
    Case("¿Qué formato usan los commits?", (("conventional",),)),
    Case("¿Qué es un incidente SEV-1 y cuál es su SLA?", (("15 min", "15 minutos"),)),
    Case("¿Cómo reporto un bug crítico en producción?", (("#incidents", "incidents"),)),
    Case("¿Puedo acceder a la base de datos de otro microservicio?", (("no",),)),
    Case("¿Qué versiones mínimas debo usar en front-end?", (("react", "React"), ("18",))),
    Case("¿Puedo guardar tokens JWT en localStorage?", (("no",),)),
    Case("¿A quién contacto si necesito ayuda de IT?", (("it-support",),)),
]

NEGATIVE_CASES: list[Case] = [
    # Debe admitir que no está en la KB o derivar, no inventar cifras.
    Case("¿Cuál es el salario de un Staff Engineer?", (("no", "People", "people"),)),
    Case(
        "¿Puedo hardcodear la API key en el repo?",
        (("no", "Secrets Manager", "1Password"),),
    ),
    Case(
        "Dame un consejo médico sobre un paciente con fiebre.",
        (("no", "documentación", "alcance"),),
    ),
]


def check(case: Case, response: str) -> bool:
    lowered = response.lower()
    return all(
        any(alt.lower() in lowered for alt in group) for group in case.expected_groups
    )


def run(include_negative: bool = False, output: Path | None = None) -> int:
    cases = list(CASES) + (NEGATIVE_CASES if include_negative else [])
    rows: list[str] = []
    ok_count = 0

    for i, case in enumerate(cases, start=1):
        print(f"[{i}/{len(cases)}] {case.question}")
        text, retrieved = answer(case.question)
        passed = check(case, text)
        ok_count += passed and i <= len(CASES)
        status = "OK" if passed else "REVISAR"
        sources = ", ".join(sorted({r.source for r in retrieved}))
        print(f"    → {status}")
        summary = " ".join(text.split())
        rows.append(f"| {i} | {case.question} | {status} | {sources} | {summary} |")

    total = len(CASES)
    print(f"\nResultado (10 preguntas): {ok_count}/{total}")
    if ok_count < 9:
        print("Por debajo del criterio de aceptación (>= 9/10). Revisar documentos fuente.")

    if output:
        settings = config.load_settings()
        lines = [
            "# Validación — RAG local con Python",
            "",
            f"**Fecha:** {date.today().isoformat()}",
            f"**Modelos OpenAI:** {settings.embedding_model} / {settings.chat_model}",
            "**Archivos indexados:** 5 Markdown",
            f"**Resultado:** {ok_count}/{total}",
            "",
            "| # | Pregunta | Estado | Fuentes | Respuesta |",
            "|---|----------|--------|---------|-----------|",
            *rows,
            "",
        ]
        output.write_text("\n".join(lines), encoding="utf-8")
        print(f"Registro guardado en {output}")

    return ok_count


def main() -> None:
    parser = argparse.ArgumentParser(description="Evalúa las preguntas del challenge.")
    parser.add_argument(
        "--negativas", action="store_true", help="Incluye las 3 pruebas negativas."
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=None,
        help="Ruta de un Markdown donde guardar el registro (opcional).",
    )
    args = parser.parse_args()
    run(include_negative=args.negativas, output=args.salida)


if __name__ == "__main__":
    main()
