# Pegasus Agent API

API FastAPI para consumir Pegasus Dev Assistant desde un front-end. Este
directorio es un repositorio Git independiente y depende del paquete
`pegasus-rag` ubicado en el directorio padre.

## Requisitos

- Python 3.11 o superior.
- Proyecto `proyecto_challenger` disponible en `..`.
- `.env` configurado en el proyecto padre.
- Índice creado mediante `python -m rag.ingest` en el proyecto padre.

## Instalación

Desde `api-agente/`:

```powershell
C:\ruta\a\python.exe -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .. -e ".[dev]"
```

La primera instalación editable corresponde al motor RAG del repositorio padre;
la segunda instala esta API y sus dependencias.

## Ejecución

```powershell
.\.venv\Scripts\python.exe -m uvicorn agent_api.main:app --reload --port 8000
```

- Documentación Swagger: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/health>

## Endpoints

### `GET /health`

Indica si la API key, el índice y el prompt están disponibles. Nunca expone la
clave.

### `GET /config`

Devuelve modelos y `top_k` públicos.

### `POST /chat`

Primera pregunta:

```json
{
  "question": "¿Cuáles son las core hours?"
}
```

La respuesta incluye un `session_id`. Para conservar la memoria, enviarlo en
las preguntas siguientes:

```json
{
  "session_id": "UUID-DEVUELTO-POR-LA-API",
  "question": "¿Y el resto del horario?"
}
```

### `DELETE /sessions/{session_id}`

Elimina la memoria de una conversación. Las sesiones residen en memoria y se
pierden al reiniciar el servidor.

## CORS

Por defecto solo se acepta `http://localhost:5173`. Para configurar más
orígenes, separar sus URL con comas:

```env
API_CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
