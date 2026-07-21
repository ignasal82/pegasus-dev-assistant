"""División de documentos Markdown en fragmentos para embeddings.

Estrategia: separar por encabezados (#, ##, ###) y, si una sección supera
MAX_CHARS, partirla por párrafos con solapamiento para no cortar contexto.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

MAX_CHARS = 1000
OVERLAP_CHARS = 150

_HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$", re.MULTILINE)


@dataclass(frozen=True)
class Chunk:
    text: str
    source: str  # ruta relativa al repo, ej. doc/conocimiento/faq.md
    heading: str


def _split_long_text(text: str) -> list[str]:
    """Parte texto largo por párrafos, con solapamiento entre partes."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    parts: list[str] = []
    current = ""
    for para in paragraphs:
        candidate = f"{current}\n\n{para}".strip() if current else para
        if len(candidate) <= MAX_CHARS or not current:
            current = candidate
        else:
            parts.append(current)
            overlap = current[-OVERLAP_CHARS:]
            current = f"{overlap}\n\n{para}"
    if current:
        parts.append(current)
    return parts


def split_markdown(text: str, source: str) -> list[Chunk]:
    """Divide un documento Markdown en chunks con metadatos."""
    matches = list(_HEADING_RE.finditer(text))
    chunks: list[Chunk] = []

    if not matches:
        for part in _split_long_text(text):
            chunks.append(Chunk(text=part, source=source, heading=""))
        return chunks

    # Texto antes del primer encabezado (si existe)
    preamble = text[: matches[0].start()].strip()
    if preamble:
        for part in _split_long_text(preamble):
            chunks.append(Chunk(text=part, source=source, heading=""))

    for i, match in enumerate(matches):
        heading = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if not body:
            continue
        section_text = f"{match.group(0)}\n{body}"
        for part in _split_long_text(section_text):
            chunks.append(Chunk(text=part, source=source, heading=heading))

    return chunks


def chunk_file(path: Path, repo_root: Path) -> list[Chunk]:
    text = path.read_text(encoding="utf-8")
    source = path.relative_to(repo_root).as_posix()
    return split_markdown(text, source)
