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
| `python -m rag.console` | Consola con memoria de conversación y comandos (`/ayuda`) |
| `python -m rag.evaluate` | Corre las 10 preguntas del challenge (fase 4) |
| `pytest` | Pruebas unitarias e interacción CLI (sin red) |
| `pytest -m integration` | Smoke real contra OpenAI + índice local |

## Estructura

```
rag/
├── config.py      # rutas, modelos, top-k, descubrimiento de archivos
├── chunking.py    # división por encabezados (fase 2)
├── ingest.py      # embeddings + Chroma (fase 2)
├── retrieve.py    # búsqueda top-k (fase 3)
├── prompt-sistema.md  # instrucciones del sistema del agente
├── prompts.py     # carga de prompt-sistema.md (fase 3)
├── chat.py        # CLI de chat (fase 3)
├── console.py     # consola interactiva con memoria y comandos
├── evaluate.py    # batería de 10 preguntas (fase 4)
└── data/chroma/   # índice persistente (ignorado por Git)
```

## Qué se indexa

Solo los 5 `.md` temáticos de `doc/conocimiento/` (FAQ, SRE, arquitectura,
front-end, onboarding). Se excluyen `README.md` y los PDF.

## Flujo completo (con API key configurada)

```powershell
# 1. Indexar la base de conocimiento (una sola vez; usa embeddings de OpenAI)
.\.venv\Scripts\python.exe -m rag.ingest

# 2. Probar el chat
.\.venv\Scripts\python.exe -m rag.chat "¿Cuáles son las core hours del equipo?"

# 3. Correr la evaluación del challenge (10 preguntas + registro)
.\.venv\Scripts\python.exe -m rag.evaluate --negativas --salida validacion-rag-local.md
```

Criterio de aceptación: al menos **9/10** preguntas OK y ninguna respuesta
inventada. Si una falla, corregir el documento fuente en `doc/conocimiento/`,
reconstruir el índice con `python -m rag.ingest --rebuild` y repetir.

## Costos

La KB completa son ~37 KB de texto: la ingestión con `text-embedding-3-small`
cuesta fracciones de centavo, y cada pregunta con `gpt-4o-mini` es igualmente
barata. Evitá `--rebuild` innecesarios para no repetir embeddings.

## Errores comunes

| Error | Solución |
|-------|----------|
| `Falta OPENAI_API_KEY` | Copiar `.env.example` a `.env` y completar la clave |
| `No existe el índice local` | Ejecutar `python -m rag.ingest` |
| `python` no encontrado | Usar `.\.venv\Scripts\python.exe` o reabrir la terminal |
