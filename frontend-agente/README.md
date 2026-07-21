# Pegasus Dev Assistant — Frontend

Interfaz de chat construida con **Angular 21** y **Tailwind CSS 4** para
conversar con Pegasus Dev Assistant a través de la API FastAPI (`api-agente`).
Este directorio es un repositorio Git independiente.

## Requisitos

- Node.js 22+.
- La API corriendo en `http://127.0.0.1:8000` (ver `../api-agente/README.md`).

## Ejecución en desarrollo

```powershell
npm install
npm start
```

Abre <http://localhost:4200>. El servidor de desarrollo proxya `/api/*` hacia
`http://127.0.0.1:8000` (ver `proxy.conf.json`), por lo que no hay problemas de
CORS en local.

## Estructura

```
src/app/
├── chat/
│   ├── chat.models.ts        # contratos de la API
│   ├── chat.service.ts       # estado de la conversación (signals) + HTTP
│   ├── chat-header/          # encabezado con estado de la API
│   ├── chat-messages/        # historial de mensajes y burbujas
│   └── chat-input/           # caja de texto y envío
└── app.ts                    # página principal del chat
```

## Build de producción

```powershell
npm run build
```

Los artefactos quedan en `dist/`. En producción, servir el frontend detrás del
mismo dominio que la API o configurar `API_CORS_ORIGINS` en la API.
