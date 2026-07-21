"""Fixtures compartidas para las pruebas del RAG."""

from __future__ import annotations

import pytest

from rag.retrieve import Retrieved


@pytest.fixture
def sample_retrieved() -> list[Retrieved]:
    return [
        Retrieved(
            text="Core hours: 10:00 a 17:00 (zona horaria del equipo).",
            source="doc/conocimiento/faq.md",
            heading="Horarios y disponibilidad",
            distance=0.11,
        ),
        Retrieved(
            text="El resto del horario es flexible según acuerdo con el Tech Lead.",
            source="doc/conocimiento/onboarding/manual-onboarding-desarrolladores.md",
            heading="Horario",
            distance=0.22,
        ),
    ]


@pytest.fixture
def agent_reply() -> str:
    return (
        "Según el FAQ, las core hours son de 10:00 a 17:00 "
        "(zona horaria del equipo)."
    )
