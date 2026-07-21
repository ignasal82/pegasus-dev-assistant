"""Consola interactiva para conversar con Pegasus Dev Assistant.

A diferencia de `rag.chat` (una pregunta por vez, sin estado), esta consola
mantiene memoria de la conversación y ofrece comandos utilitarios.

Uso:
    python -m rag.console

Comandos disponibles dentro de la consola:
    /ayuda        muestra esta ayuda
    /fuentes      alterna el detalle de fragmentos recuperados
    /topk N       cambia cuántos fragmentos se recuperan (1-10)
    /historial    muestra las preguntas de la sesión
    /limpiar      borra la memoria de la conversación
    /salir        termina la sesión
"""

from __future__ import annotations

from dataclasses import dataclass, field

from openai import OpenAI

from rag import config
from rag.prompts import build_user_message, load_system_prompt
from rag.retrieve import Retrieved, retrieve

# Cantidad máxima de intercambios (pregunta + respuesta) que se reenvían al
# modelo como memoria. Evita que el contexto crezca sin límite.
MAX_TURNS_IN_MEMORY = 6

BANNER = """
=====================================================
  Pegasus Dev Assistant — consola interactiva (local)
=====================================================
Preguntá sobre las políticas internas de Santo Pegasus.
Escribí /ayuda para ver los comandos disponibles.
"""

HELP_TEXT = """Comandos:
  /ayuda        muestra esta ayuda
  /fuentes      alterna el detalle de fragmentos recuperados (actualmente: {estado})
  /topk N       cambia cuántos fragmentos se recuperan (actual: {topk})
  /historial    muestra las preguntas de la sesión
  /limpiar      borra la memoria de la conversación
  /salir        termina la sesión (también: salir, exit, quit)"""


@dataclass
class Session:
    """Estado de la conversación: memoria, preferencias y ajustes."""

    settings: config.Settings = field(default_factory=config.load_settings)
    show_fragments: bool = False
    # Mensajes previos (user/assistant) que se reenvían como memoria.
    memory: list[dict[str, str]] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)

    def remember(self, question: str, answer_text: str) -> None:
        self.questions.append(question)
        self.memory.append({"role": "user", "content": question})
        self.memory.append({"role": "assistant", "content": answer_text})
        # Recorta la memoria a los últimos MAX_TURNS_IN_MEMORY intercambios.
        max_messages = MAX_TURNS_IN_MEMORY * 2
        if len(self.memory) > max_messages:
            self.memory = self.memory[-max_messages:]

    def set_top_k(self, value: int) -> None:
        if not 1 <= value <= 10:
            raise ValueError("top-k debe estar entre 1 y 10.")
        self.settings = config.Settings(
            openai_api_key=self.settings.openai_api_key,
            embedding_model=self.settings.embedding_model,
            chat_model=self.settings.chat_model,
            top_k=value,
        )


def ask(session: Session, question: str) -> tuple[str, list[Retrieved]]:
    """Recupera contexto, arma los mensajes con memoria y consulta al modelo."""
    retrieved = retrieve(question, session.settings)
    context_blocks = [(r.source, r.text) for r in retrieved]
    user_message = build_user_message(question, context_blocks)

    messages: list[dict[str, str]] = [
        {"role": "system", "content": load_system_prompt()},
        *session.memory,
        {"role": "user", "content": user_message},
    ]

    client = OpenAI(api_key=session.settings.require_api_key())
    response = client.chat.completions.create(
        model=session.settings.chat_model,
        messages=messages,
        temperature=0.2,
    )
    text = response.choices[0].message.content or ""
    # En memoria se guarda la pregunta original, sin el contexto inyectado,
    # para no arrastrar fragmentos viejos en turnos futuros.
    session.remember(question, text)
    return text, retrieved


def print_answer(text: str, retrieved: list[Retrieved], show_fragments: bool) -> None:
    print(f"\n{text}\n")
    sources = sorted({r.source for r in retrieved})
    print("Fuentes consultadas:")
    for source in sources:
        print(f"  - {source}")
    if show_fragments:
        print("\nFragmentos recuperados:")
        for i, r in enumerate(retrieved, start=1):
            heading = f" — {r.heading}" if r.heading else ""
            print(f"  [{i}] {r.source}{heading} (distancia: {r.distance:.3f})")


def handle_command(session: Session, command: str) -> bool:
    """Procesa un comando. Devuelve False si hay que terminar la sesión."""
    parts = command.split()
    name = parts[0].lower()

    if name == "/salir":
        return False
    if name == "/ayuda":
        estado = "activado" if session.show_fragments else "desactivado"
        print(HELP_TEXT.format(estado=estado, topk=session.settings.top_k))
    elif name == "/fuentes":
        session.show_fragments = not session.show_fragments
        estado = "activado" if session.show_fragments else "desactivado"
        print(f"Detalle de fragmentos: {estado}.")
    elif name == "/topk":
        if len(parts) != 2 or not parts[1].isdigit():
            print("Uso: /topk N  (por ejemplo: /topk 6)")
        else:
            try:
                session.set_top_k(int(parts[1]))
                print(f"top-k actualizado a {session.settings.top_k}.")
            except ValueError as exc:
                print(f"Error: {exc}")
    elif name == "/historial":
        if not session.questions:
            print("Todavía no hay preguntas en esta sesión.")
        else:
            for i, q in enumerate(session.questions, start=1):
                print(f"  {i}. {q}")
    elif name == "/limpiar":
        session.memory.clear()
        session.questions.clear()
        print("Memoria de la conversación borrada.")
    else:
        print(f"Comando desconocido: {name}. Escribí /ayuda para ver los comandos.")
    return True


def main() -> None:
    session = Session()
    print(BANNER)

    while True:
        try:
            line = input("Vos> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue
        if line.lower() in {"salir", "exit", "quit"}:
            break
        if line.startswith("/"):
            if not handle_command(session, line):
                break
            continue

        try:
            text, retrieved = ask(session, line)
        except RuntimeError as exc:
            print(f"Error: {exc}")
            continue
        print_answer(text, retrieved, session.show_fragments)

    print("¡Hasta luego!")


if __name__ == "__main__":
    main()
