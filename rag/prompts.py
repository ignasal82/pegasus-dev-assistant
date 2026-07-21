"""Carga del prompt de sistema desde plan-impl/prompt-sistema.md."""

from __future__ import annotations

import re

from rag import config

_FALLBACK_PROMPT = (
    "Eres Pegasus Dev Assistant (Santo Pegasus / Agendio). Responde en español, "
    "tono técnico y breve. Usa solo el contexto proporcionado. No inventes "
    "políticas, SLAs ni contactos. Si no hay dato, dilo y deriva a IT "
    "(#it-support / it-support@santopegasus.com), People, o #incidents según "
    "el caso. Prioriza el FAQ; cita la fuente."
)


def load_system_prompt() -> str:
    """Extrae el primer bloque ```text del archivo de prompt.

    Si el archivo no existe (por ejemplo, en otra máquina sin plan-impl/),
    usa una variante corta embebida para no bloquear el chat.
    """
    if not config.PROMPT_FILE.is_file():
        return _FALLBACK_PROMPT

    content = config.PROMPT_FILE.read_text(encoding="utf-8")
    match = re.search(r"```text\n(.*?)```", content, re.DOTALL)
    if not match:
        return _FALLBACK_PROMPT
    prompt = match.group(1).strip()
    return prompt or _FALLBACK_PROMPT


def build_user_message(question: str, context_blocks: list[tuple[str, str]]) -> str:
    """Combina contexto recuperado y pregunta en un solo mensaje.

    context_blocks: lista de tuplas (source, texto).
    """
    parts = ["Contexto recuperado de la base de conocimiento:\n"]
    for i, (source, text) in enumerate(context_blocks, start=1):
        parts.append(f"--- Fragmento {i} (fuente: {source}) ---\n{text}\n")
    parts.append(
        "\nRespondé la siguiente pregunta usando ÚNICAMENTE el contexto anterior. "
        "Indicá la fuente. Si el contexto no alcanza, decilo claramente.\n"
    )
    parts.append(f"Pregunta: {question}")
    return "\n".join(parts)
