"""Chat RAG por consola.

Uso:
    python -m rag.chat                  # modo interactivo
    python -m rag.chat "una pregunta"   # una sola pregunta
"""

from __future__ import annotations

import sys

from openai import OpenAI

from rag import config
from rag.prompts import build_user_message, load_system_prompt
from rag.retrieve import Retrieved, retrieve


def answer(question: str, settings: config.Settings | None = None) -> tuple[str, list[Retrieved]]:
    """Devuelve (respuesta, fragmentos usados)."""
    settings = settings or config.load_settings()
    retrieved = retrieve(question, settings)

    context_blocks = [(r.source, r.text) for r in retrieved]
    system_prompt = load_system_prompt()
    user_message = build_user_message(question, context_blocks)

    client = OpenAI(api_key=settings.require_api_key())
    response = client.chat.completions.create(
        model=settings.chat_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or "", retrieved


def _print_answer(question: str) -> None:
    try:
        text, retrieved = answer(question)
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return

    print(f"\n{text}\n")
    sources = sorted({r.source for r in retrieved})
    print("Fuentes consultadas:")
    for source in sources:
        print(f"  - {source}")


def main() -> None:
    if len(sys.argv) > 1:
        _print_answer(" ".join(sys.argv[1:]))
        return

    print("Pegasus Dev Assistant (local). Escribí 'salir' para terminar.")
    while True:
        try:
            question = input("\nPregunta> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question or question.lower() in {"salir", "exit", "quit"}:
            break
        _print_answer(question)


if __name__ == "__main__":
    main()
