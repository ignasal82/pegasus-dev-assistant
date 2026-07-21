# Pegasus Dev Assistant

Guía práctica del prototipo **RAG local** (Python + OpenAI + Chroma): cómo
ejecutar el proyecto de punta a punta y cómo está organizada la batería de
pruebas.

La integración con OCI se conserva como trabajo futuro, pero **no forma parte
del alcance activo**.

## Requisitos

- Python 3.11 o superior (probado con 3.12).
- Una API key de OpenAI (solo para ingestión, chat y evaluación reales).
- PowerShell en Windows (los comandos usan esa sintaxis).

## Cómo ejecutar el proyecto

Todos los comandos se lanzan desde la raíz del repositorio.

### 1. Instalar el entorno

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

`.[dev]` instala las dependencias del RAG (`openai`, `chromadb`,
`python-dotenv`) y las de pruebas (`pytest`).

### 2. Configurar la clave

```powershell
Copy-Item .env.example .env
# Editar .env y completar OPENAI_API_KEY (nunca commitear el .env real)
```

Variables opcionales (con sus valores por defecto): `RAG_EMBEDDING_MODEL`
(`text-embedding-3-small`), `RAG_CHAT_MODEL` (`gpt-4o-mini`) y `RAG_TOP_K` (`4`).

### 3. Indexar la base de conocimiento (una sola vez)

```powershell
.\.venv\Scripts\python.exe -m rag.ingest
```

Indexa solo los cinco `.md` temáticos de `doc/conocimiento/` (FAQ, SRE,
arquitectura, front-end, onboarding) en un índice Chroma persistente bajo
`rag/data/chroma/` (ignorado por Git). Para reconstruirlo desde cero usá
`python -m rag.ingest --rebuild` (repite embeddings, evitá hacerlo sin motivo).

### 4. Chatear con el agente

```powershell
.\.venv\Scripts\python.exe -m rag.chat "¿Cuáles son las core hours del equipo?"
```

Recupera los fragmentos top-k, responde con OpenAI y muestra las fuentes
consultadas. Sin argumento entra en modo interactivo.

Para una sesión de conversación con memoria y comandos utilitarios, usá la
consola interactiva:

```powershell
.\.venv\Scripts\python.exe -m rag.console
```

Mantiene el hilo de la conversación (últimos 6 intercambios) y acepta comandos:
`/ayuda`, `/fuentes` (detalle de fragmentos), `/topk N`, `/historial`,
`/limpiar` y `/salir`.

### 5. Evaluar las preguntas del challenge

```powershell
.\.venv\Scripts\python.exe -m rag.evaluate --negativas --salida validacion-rag-local.md
```

Corre las 10 preguntas (más las 3 negativas con `--negativas`) y escribe un
registro en Markdown. **Criterio de aceptación:** al menos **9/10** OK y ninguna
respuesta inventada. Si una falla, corregí el documento fuente en
`doc/conocimiento/`, reconstruí el índice y repetí.

El registro vigente está versionado como evidencia en
[validacion-rag-local.md](./validacion-rag-local.md) (10/10 + 3 negativas OK).

## Método de pruebas

La suite vive en `tests/` y se ejecuta con `pytest`. Está diseñada en dos
niveles para que el desarrollo diario **no dependa de la red ni de la API key**.

### Filosofía

- **Rápidas y deterministas por defecto:** las pruebas unitarias no llaman a
  OpenAI ni tocan Chroma real; usan `monkeypatch` y `unittest.mock` para simular
  el SDK y el vector store.
- **Integración opcional y aislada:** la única prueba que golpea servicios
  reales está marcada como `integration` y se **omite por defecto**.
- **Sin secretos en los artefactos:** las pruebas de evaluación verifican que el
  registro generado no contenga claves (`sk-`, `OPENAI_API_KEY`).

### Categorías

| Tipo | Archivos | Qué cubre | Red |
|------|----------|-----------|-----|
| Configuración | `test_config.py` | rutas, 5 fuentes, defaults, API key requerida | No |
| Chunking | `test_chunking.py` | división por encabezados y metadatos | No |
| Ingestión | `test_ingest.py` | 5 fuentes, exclusiones, batches de embeddings (mock) | No |
| Recuperación | `test_retrieve.py` | top-k, mapeo de resultados, respuesta vacía (mock) | No |
| Prompt | `test_prompts.py` | carga, fallback y armado del mensaje de usuario | No |
| Evaluación | `test_evaluation.py` | conteo OK, casos negativos, sin secretos | No |
| Interacción CLI | `test_agent_interaction.py` | impresión de respuesta y deduplicación de fuentes | No |
| Consola | `test_console.py` | memoria, comandos, top-k y manejo de errores | No |
| Fixtures | `conftest.py` | `sample_retrieved` y `agent_reply` compartidas | — |
| Integración | `test_agent_integration.py` | smoke real contra OpenAI + Chroma | **Sí** |

### Marcador `integration`

Definido en `pyproject.toml`, que además configura `addopts = -m "not integration"`
para excluirlo por defecto:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-m \"not integration\""
markers = [
    "integration: prueba real contra OpenAI e índice local (requiere .env e ingest)",
]
```

La prueba de integración además se auto-omite (`skipif`) si falta la API key o
el índice Chroma, así que nunca falla por entorno incompleto.

### Cómo correr las pruebas

```powershell
# Suite rápida por defecto (sin red, excluye integración)
.\.venv\Scripts\python.exe -m pytest

# Solo la prueba de integración (requiere .env + python -m rag.ingest antes)
.\.venv\Scripts\python.exe -m pytest -m integration

# Absolutamente todo
.\.venv\Scripts\python.exe -m pytest -m "integration or not integration"

# Un archivo o una prueba puntual
.\.venv\Scripts\python.exe -m pytest tests/test_retrieve.py
.\.venv\Scripts\python.exe -m pytest tests/test_retrieve.py::test_retrieve_respeta_top_k

# Salida detallada
.\.venv\Scripts\python.exe -m pytest -v
```

## Errores comunes

| Error | Solución |
|-------|----------|
| `Falta OPENAI_API_KEY` | Copiar `.env.example` a `.env` y completar la clave |
| `No existe el índice local` | Ejecutar `python -m rag.ingest` |
| `python` no encontrado | Usar `.\.venv\Scripts\python.exe` o reabrir la terminal |
| La prueba de integración se omite | Faltan `.env` o el índice; correr `rag.ingest` primero |

## Prompt del sistema

Las instrucciones del agente viven en [rag/prompt-sistema.md](./rag/prompt-sistema.md)
(versionado). Si el archivo faltara, `rag/prompts.py` usa una variante corta
embebida como fallback.

## Documentos del plan (locales, no versionados)

La carpeta `plan-impl/` está excluida de Git vía `.git/info/exclude`; sus
documentos son notas de trabajo locales:

| Archivo | Para qué |
|---------|----------|
| `plan-impl/00-rag-python-local.md` | **Plan activo**, fases, pruebas y commits |
| `plan-impl/checklist.md` | Checklist del prototipo local |
| `plan-impl/04-pruebas-e-iteracion.md` | Preguntas y criterios de evaluación |

### Referencias futuras de OCI

Estos documentos quedan abiertos, sin ejecutarse todavía (también locales):

- `plan-impl/01-prerrequisitos-oci.md`
- `plan-impl/02-object-storage-y-kb.md`
- `plan-impl/03-agente-rag-y-prompt.md`

## Referencias del repo

- README técnico del RAG: `rag/README.md`
- Agente: `doc/metadatos/agente.md`
- KB: `doc/conocimiento/`
- Validación previa (docs): `doc/control/validacion-preguntas.md`
- Guía Alura: `doc/INSTRUCCIONES-PASO-A-PASO.md` (Paso 10)

## Estado de OCI

**Pendiente y fuera del alcance actual.** Cuando se retome, se decidirán región,
recursos y estrategia de despliegue usando como entrada el prototipo ya
validado. Desde Paraguay, la referencia actual sigue siendo São Paulo
(`sa-saopaulo-1`), salvo que Alura exija otra región.
