# Base de conocimiento — Santo Pegasus Soluciones

Documentación organizada para el agente **Pegasus Dev Assistant**.

## Estructura de carpetas (Paso 3)

```
doc/
??? INSTRUCCIONES-PASO-A-PASO.md
??? metadatos/
?   ??? contexto-negocio.md      ? Paso 1: contexto del negocio
?   ??? agente.md                ? Paso 2: nombre, tono y reglas del agente
??? conocimiento/
    ??? README.md                ? este índice
    ??? faq.md                   ? preguntas frecuentes consolidadas
    ??? sre/
    ?   ??? protocolo-incidentes-postmortems.pdf
    ??? arquitectura/
    ?   ??? arquitectura-microservicios-mapa-dominios.pdf
    ??? ingenieria-frontend/
    ?   ??? guia-ingenieria-frontend.pdf
    ??? onboarding/
        ??? manual-onboarding-desarrolladores.pdf
```

## Documentos por categoría

| Carpeta | Archivo | Descripción |
|---------|---------|-------------|
| `sre/` | `protocolo-incidentes-postmortems.pdf` | Severidades, on-call, rollback ECS, post-mortems, SLI/SLO/SLA, Error Budget |
| `arquitectura/` | `arquitectura-microservicios-mapa-dominios.pdf` | Microservicios Agendio, AWS, API Gateway, squads, ADRs |
| `ingenieria-frontend/` | `guia-ingenieria-frontend.pdf` | React, TypeScript, Tailwind, pruebas, CI/CD front-end |
| `onboarding/` | `manual-onboarding-desarrolladores.pdf` | Día 1, entorno local, Git, RRHH, checklist semana 1 |
| *(raíz)* | `faq.md` | FAQ sintetizado para consultas rápidas del agente |

## Origen

Los PDFs provienen de `doc-politicas/` y fueron renombrados y distribuidos en carpetas temáticas para facilitar la búsqueda del agente.
