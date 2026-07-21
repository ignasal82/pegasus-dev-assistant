"""Aplicación FastAPI para Pegasus Dev Assistant."""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from rag import config
from rag.console import ask

from agent_api.models import (
    ChatRequest,
    ChatResponse,
    ConfigResponse,
    DeleteSessionResponse,
    HealthResponse,
    SourceResponse,
)
from agent_api.sessions import SessionStore


def _cors_origins() -> list[str]:
    raw = os.environ.get("API_CORS_ORIGINS", "http://localhost:5173")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(
    title="Pegasus Agent API",
    description="API para conversar con Pegasus Dev Assistant.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type"],
)

sessions = SessionStore()


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """La raíz no es un endpoint de negocio; redirige a la documentación."""
    return RedirectResponse(url="/docs")


@app.get("/health", response_model=HealthResponse, tags=["sistema"])
def health() -> HealthResponse:
    settings = config.load_settings()
    api_key_configured = bool(settings.openai_api_key)
    index_available = config.CHROMA_DIR.exists()
    prompt_available = config.PROMPT_FILE.is_file()
    ready = api_key_configured and index_available and prompt_available
    return HealthResponse(
        status="ready" if ready else "degraded",
        api_key_configured=api_key_configured,
        index_available=index_available,
        prompt_available=prompt_available,
    )


@app.get("/config", response_model=ConfigResponse, tags=["sistema"])
def public_config() -> ConfigResponse:
    settings = config.load_settings()
    return ConfigResponse(
        chat_model=settings.chat_model,
        embedding_model=settings.embedding_model,
        top_k=settings.top_k,
    )


@app.post("/chat", response_model=ChatResponse, tags=["agente"])
def chat(payload: ChatRequest) -> ChatResponse:
    question = payload.question.strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="La pregunta no puede estar vacía.",
        )

    try:
        session_id, session = sessions.get_or_create(payload.session_id)
        answer_text, retrieved = ask(session, question)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No se pudo obtener una respuesta del agente.",
        ) from exc

    sources = [
        SourceResponse(
            source=item.source,
            heading=item.heading,
            distance=item.distance,
        )
        for item in retrieved
    ]
    return ChatResponse(
        session_id=session_id,
        answer=answer_text,
        sources=sources,
    )


@app.delete(
    "/sessions/{session_id}",
    response_model=DeleteSessionResponse,
    tags=["agente"],
)
def delete_session(session_id: str) -> DeleteSessionResponse:
    try:
        deleted = sessions.delete(session_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)
        ) from exc
    return DeleteSessionResponse(deleted=deleted)
