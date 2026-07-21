"""Configuración central del RAG local.

Lee variables desde el entorno (o un archivo .env en la raíz del repo) y
resuelve todas las rutas con pathlib para funcionar bien en Windows.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(REPO_ROOT / ".env")

KNOWLEDGE_DIR = REPO_ROOT / "doc" / "conocimiento"
PROMPT_FILE = REPO_ROOT / "plan-impl" / "prompt-sistema.md"
CHROMA_DIR = REPO_ROOT / "rag" / "data" / "chroma"
COLLECTION_NAME = "pegasus-conocimiento"

# Solo los .md temáticos; el README es un índice humano y los PDF duplican
# el contenido de los resúmenes Markdown.
EXCLUDED_FILENAMES = {"README.md"}


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = field(default="", repr=False)
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"
    top_k: int = 4

    def require_api_key(self) -> str:
        if not self.openai_api_key:
            raise RuntimeError(
                "Falta OPENAI_API_KEY. Copiá .env.example a .env en la raíz "
                "del proyecto y completá tu clave de OpenAI."
            )
        return self.openai_api_key


def load_settings() -> Settings:
    return Settings(
        openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
        embedding_model=os.environ.get("RAG_EMBEDDING_MODEL", "text-embedding-3-small"),
        chat_model=os.environ.get("RAG_CHAT_MODEL", "gpt-4o-mini"),
        top_k=int(os.environ.get("RAG_TOP_K", "4")),
    )


def knowledge_files() -> list[Path]:
    """Devuelve los Markdown de la base de conocimiento, orden determinista."""
    files = [
        p
        for p in sorted(KNOWLEDGE_DIR.rglob("*.md"))
        if p.name not in EXCLUDED_FILENAMES
    ]
    return files
