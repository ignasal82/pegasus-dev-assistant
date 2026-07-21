"""Almacenamiento en memoria para sesiones de conversación."""

from __future__ import annotations

from threading import Lock
from uuid import UUID, uuid4

from rag.console import Session


class SessionStore:
    """Gestiona sesiones locales de manera segura entre threads."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}
        self._lock = Lock()

    def get_or_create(self, session_id: str | None) -> tuple[str, Session]:
        if session_id is not None:
            try:
                normalized = str(UUID(session_id))
            except ValueError as exc:
                raise ValueError("session_id debe ser un UUID válido.") from exc
        else:
            normalized = str(uuid4())

        with self._lock:
            session = self._sessions.setdefault(normalized, Session())
        return normalized, session

    def delete(self, session_id: str) -> bool:
        try:
            normalized = str(UUID(session_id))
        except ValueError as exc:
            raise ValueError("session_id debe ser un UUID válido.") from exc

        with self._lock:
            return self._sessions.pop(normalized, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._sessions.clear()
