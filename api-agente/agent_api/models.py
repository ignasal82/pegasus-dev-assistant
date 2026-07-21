"""Contratos HTTP de la API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    session_id: str | None = None


class SourceResponse(BaseModel):
    source: str
    heading: str
    distance: float


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[SourceResponse]


class HealthResponse(BaseModel):
    status: str
    api_key_configured: bool
    index_available: bool
    prompt_available: bool


class ConfigResponse(BaseModel):
    chat_model: str
    embedding_model: str
    top_k: int


class DeleteSessionResponse(BaseModel):
    deleted: bool
