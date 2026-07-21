# RAG local — Pegasus Dev Assistant

Prototipo RAG en Python que indexa los Markdown de `doc/conocimiento/` y
responde preguntas con OpenAI, citando las fuentes.

## Requisitos

- Python 3.11 o superior
- Una API key de OpenAI

## Instalación (PowerShell)

```powershell
# Desde la raíz del proyecto
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"

# Configurar la clave (nunca commitear .env)
Copy-Item .env.example .env
# Editar .env y completar OPENAI_API_KEY
```

## Comandos

| Comando | Qué hace |
|---------|----------|
| `python -m rag.ingest` | Indexa los 5 Markdown en Chroma (fase 2) |
| `python -m rag.chat` | Chat interactivo con fuentes (fase 3) |
| `python -m rag.evaluate` | Corre las 10 preguntas del challenge (fase 4) |
| `pytest` | Pruebas unitarias, sin red |

## Estructura

```
rag/
├── config.py      # rutas, modelos, top-k, descubrimiento de archivos
├── chunking.py    # división por encabezados (fase 2)
├── ingest.py      # embeddings + Chroma (fase 2)
├── retrieve.py    # búsqueda top-k (fase 3)
├── prompts.py     # carga de prompt-sistema.md (fase 3)
├── chat.py        # CLI de chat (fase 3)
├── evaluate.py    # batería de 10 preguntas (fase 4)
└── data/chroma/   # índice persistente (ignorado por Git)
```

## Qué se indexa

Solo los 5 `.md` temáticos de `doc/conocimiento/` (FAQ, SRE, arquitectura,
front-end, onboarding). Se excluyen `README.md` y los PDF.
