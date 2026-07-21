# Pegasus Dev Assistant

Prototipo **RAG local** (Python + OpenAI + Chroma) para responder preguntas
sobre la documentación interna de Santo Pegasus / Agendio, con tres formas de
uso: **API HTTP**, **front-end web** y **consola interactiva**.

La integración con OCI se conserva como trabajo futuro, pero **no forma parte
del alcance activo**.

## Requisitos

- Python 3.11 o superior (probado con 3.12).
- Node.js 22+ (solo para el front-end).
- Una API key de OpenAI (para ingestión, chat y evaluación reales).
- PowerShell en Windows (los comandos usan esa sintaxis).

## Preparación común (obligatoria)

Todas las formas de uso comparten el mismo motor RAG, así que primero hay que
preparar el entorno, la clave y el índice. Todos los comandos se lanzan desde la
raíz del repositorio.

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

---

## 1. Desplegar la API

La API (FastAPI) vive en `api-agente/` y depende del motor RAG de este
proyecto.

```powershell
cd api-agente
..\.venv\Scripts\python.exe -m pip install -e .. -e ".[dev]"
..\.venv\Scripts\python.exe -m uvicorn agent_api.main:app --host 127.0.0.1 --port 8000
```

- Raíz (redirige a la doc): <http://127.0.0.1:8000>
- Documentación Swagger: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/health>

Endpoints principales:

| Método | Ruta | Para qué |
|--------|------|----------|
| `GET` | `/health` | Estado de API key, índice y prompt (sin exponer secretos) |
| `GET` | `/config` | Modelos y `top_k` públicos |
| `POST` | `/chat` | Pregunta al agente; devuelve `session_id` y fuentes |
| `DELETE` | `/sessions/{id}` | Limpia la memoria de esa conversación |

Detalle completo (contratos, CORS, sesiones) en `api-agente/README.md`.

---

## 2. Desplegar el front-end

El front-end (Angular 21 + Tailwind CSS 4) vive en `frontend-agente/`.
**Requiere la API corriendo** (sección 1), ya que el servidor de desarrollo
proxya `/api/*` hacia `http://127.0.0.1:8000`.

```powershell
cd frontend-agente
npm install
npm start
```

Abre <http://localhost:4200>. El proxy (`proxy.conf.json`) evita problemas de
CORS en local. Interfaz de chat con memoria de conversación, indicador de estado
de la API y botón de nueva conversación.

Build de producción:

```powershell
npm run build   # artefactos en dist/
```

Detalle completo en `frontend-agente/README.md`.

---

## 3. Desplegar solo la consola

Si no necesitás API ni front-end, podés conversar directamente por terminal.
Solo requiere la preparación común (entorno, `.env` e índice).

```powershell
.\.venv\Scripts\python.exe -m rag.console
```

Mantiene el hilo de la conversación (últimos 6 intercambios) y acepta comandos:
`/ayuda`, `/fuentes` (detalle de fragmentos), `/topk N`, `/historial`,
`/limpiar` y `/salir`.

Para una sola pregunta sin sesión interactiva:

```powershell
.\.venv\Scripts\python.exe -m rag.chat "¿Cuáles son las core hours del equipo?"
```

También podés evaluar las 10 preguntas del challenge (más 3 negativas):

```powershell
.\.venv\Scripts\python.exe -m rag.evaluate --negativas --salida validacion-rag-local.md
```

**Criterio de aceptación:** al menos **9/10** OK y ninguna respuesta inventada.
El registro vigente está versionado como evidencia en
[validacion-rag-local.md](./validacion-rag-local.md) (10/10 + 3 negativas OK).

---

## 4. Ejecutar los tests unitarios

La suite del motor RAG vive en `tests/` y se ejecuta con `pytest`. Está diseñada
en dos niveles para que el desarrollo diario **no dependa de la red ni de la API
key**.

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

Para los tests de la API:

```powershell
cd api-agente
..\.venv\Scripts\python.exe -m pytest -q
```

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

---

## Errores comunes

| Error | Solución |
|-------|----------|
| `Falta OPENAI_API_KEY` | Copiar `.env.example` a `.env` y completar la clave |
| `No existe el índice local` | Ejecutar `python -m rag.ingest` |
| `python` no encontrado | Usar `.\.venv\Scripts\python.exe` o reabrir la terminal |
| La prueba de integración se omite | Faltan `.env` o el índice; correr `rag.ingest` primero |
| El front-end no responde | Verificá que la API esté corriendo en el puerto 8000 |

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
- README de la API: `api-agente/README.md`
- README del front-end: `frontend-agente/README.md`
- Agente: `doc/metadatos/agente.md`
- KB: `doc/conocimiento/`
- Validación previa (docs): `doc/control/validacion-preguntas.md`
- Guía Alura: `doc/INSTRUCCIONES-PASO-A-PASO.md` (Paso 10)

## Estado de OCI

**Pendiente y fuera del alcance actual.** Cuando se retome, se decidirán región,
recursos y estrategia de despliegue usando como entrada el prototipo ya
validado. Desde Paraguay, la referencia actual sigue siendo São Paulo
(`sa-saopaulo-1`), salvo que Alura exija otra región.
