# Paso 1 — Contexto del negocio

## Negocio elegido

**Santo Pegasus Soluciones — Plataforma SaaS de agendamiento médico (Agendio)**

## Contexto

| Campo | Detalle |
|-------|---------|
| **Tipo** | SaaS / Plataforma digital para el sector salud |
| **Producto principal** | Agendio — plataforma de agendamiento de consultas médicas |
| **Mercado** | Redes de clínicas, hospitales de pequeño y medio porte y consultorios independientes en Brasil |
| **Modelo** | Multi-tenant, con cumplimiento LGPD y alta exigencia de disponibilidad |
| **Stack** | Java 17+, Spring Boot 3+, React 18+, TypeScript, AWS (ECS, RDS, SQS, SES), Docker |

## Problema que resuelve el agente

Los desarrolladores e ingenieros de Santo Pegasus necesitan respuestas rápidas sobre arquitectura, onboarding, estándares de front-end, respuesta a incidentes y procesos internos. El agente actúa como **asistente de documentación técnica interna**, apoyándose en los PDFs oficiales de la empresa.

## Documentos fuente (origen: `doc-politicas/`)

| Documento | Carpeta destino | Contenido principal |
|-----------|-----------------|---------------------|
| Protocolo de Incidentes y Post-Mortems | `conocimiento/sre/` | SRE, severidades SEV-1 a SEV-4, SLI/SLO/SLA, Error Budget |
| Arquitectura de Microservicios | `conocimiento/arquitectura/` | Catálogo de microservicios, AWS, API Gateway, dominios Agendio |
| Guía de Ingeniería Front-end | `conocimiento/ingenieria-frontend/` | React, TypeScript, Tailwind, estándares de código y pruebas |
| Manual de Onboarding | `conocimiento/onboarding/` | Cultura, accesos Día 1, Git, beneficios RRHH, FAQ de onboarding |

## Línea resumen (Paso 1)

```
Santo Pegasus Soluciones — Empresa SaaS de salud; el agente asiste a ingenieros con documentación técnica interna de Agendio.
```
