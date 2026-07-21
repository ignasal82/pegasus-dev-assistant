"""Recuperación top-k desde el índice Chroma."""

from __future__ import annotations

from dataclasses import dataclass

import chromadb
from openai import OpenAI

from rag import config


@dataclass(frozen=True)
class Retrieved:
    text: str
    source: str
    heading: str
    distance: float


def _get_collection() -> chromadb.Collection:
    if not config.CHROMA_DIR.exists():
        raise RuntimeError(
            "No existe el índice local. Ejecutá primero: python -m rag.ingest"
        )
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    try:
        return client.get_collection(config.COLLECTION_NAME)
    except Exception as exc:
        raise RuntimeError(
            "El índice no está inicializado. Ejecutá: python -m rag.ingest"
        ) from exc


def retrieve(question: str, settings: config.Settings | None = None) -> list[Retrieved]:
    settings = settings or config.load_settings()
    collection = _get_collection()

    client = OpenAI(api_key=settings.require_api_key())
    response = client.embeddings.create(
        model=settings.embedding_model, input=[question]
    )
    query_embedding = response.data[0].embedding

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=settings.top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved: list[Retrieved] = []
    for text, meta, distance in zip(
        result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        retrieved.append(
            Retrieved(
                text=text,
                source=str(meta.get("source", "desconocida")),
                heading=str(meta.get("heading", "")),
                distance=float(distance),
            )
        )
    return retrieved
