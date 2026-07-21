"""Ingestión: chunking + embeddings OpenAI + persistencia en Chroma.

Uso:
    python -m rag.ingest            # crea el índice si no existe
    python -m rag.ingest --rebuild  # borra y reconstruye (gasta embeddings)
"""

from __future__ import annotations

import argparse

import chromadb
from openai import OpenAI

from rag import config
from rag.chunking import Chunk, chunk_file

EMBED_BATCH_SIZE = 64


def build_chunks() -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in config.knowledge_files():
        chunks.extend(chunk_file(path, config.REPO_ROOT))
    return chunks


def get_collection(create: bool = True) -> chromadb.Collection:
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    if create:
        return client.get_or_create_collection(config.COLLECTION_NAME)
    return client.get_collection(config.COLLECTION_NAME)


def embed_texts(texts: list[str], settings: config.Settings) -> list[list[float]]:
    client = OpenAI(api_key=settings.require_api_key())
    embeddings: list[list[float]] = []
    for i in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[i : i + EMBED_BATCH_SIZE]
        response = client.embeddings.create(model=settings.embedding_model, input=batch)
        embeddings.extend(item.embedding for item in response.data)
    return embeddings


def ingest(rebuild: bool = False) -> int:
    settings = config.load_settings()
    settings.require_api_key()

    chroma_client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    existing = {c.name for c in chroma_client.list_collections()}

    if config.COLLECTION_NAME in existing:
        if not rebuild:
            collection = chroma_client.get_collection(config.COLLECTION_NAME)
            count = collection.count()
            if count > 0:
                print(
                    f"El índice ya tiene {count} fragmentos. "
                    "Usá --rebuild para reconstruirlo."
                )
                return count
        else:
            chroma_client.delete_collection(config.COLLECTION_NAME)

    collection = chroma_client.get_or_create_collection(config.COLLECTION_NAME)

    chunks = build_chunks()
    print(f"Documentos: {len(config.knowledge_files())} | Fragmentos: {len(chunks)}")

    embeddings = embed_texts([c.text for c in chunks], settings)

    collection.add(
        ids=[f"chunk-{i:04d}" for i in range(len(chunks))],
        embeddings=embeddings,
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source, "heading": c.heading} for c in chunks],
    )
    print(f"Índice creado en {config.CHROMA_DIR} con {collection.count()} fragmentos.")
    return collection.count()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingesta la KB en Chroma.")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Borra el índice existente y lo reconstruye (vuelve a gastar embeddings).",
    )
    args = parser.parse_args()
    ingest(rebuild=args.rebuild)


if __name__ == "__main__":
    main()
