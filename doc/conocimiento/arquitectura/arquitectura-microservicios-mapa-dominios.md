# Arquitectura de microservicios y mapa de dominios

**Empresa:** Santo Pegasus Soluciones — Agendio  
**Versión:** 1.0.0 (Junio 2026)  
**Fuente completa:** `arquitectura-microservicios-mapa-dominios.pdf`

## Visión general

Agendio es una plataforma SaaS multi-tenant de agendamiento médico para clínicas y consultorios en Brasil. La arquitectura de microservicios prioriza disponibilidad, LGPD, seguridad y auditabilidad.

## Stack tecnológico

| Capa | Tecnologías |
|------|-------------|
| Back-end | Java 17+, Spring Boot 3+, Spring Security, Spring Cloud |
| Front-end | React 18+, TypeScript, Vite, Tailwind CSS |
| Bases de datos | PostgreSQL, MongoDB/DocumentDB, Redis/ElastiCache |
| Mensajería | AWS SQS |
| Infra | Docker, AWS ECS Fargate, API Gateway, RDS |
| Observabilidad | SLF4J/Logback, Actuator, Micrometer, Prometheus, Datadog |
| CI/CD | GitHub Actions, Flyway/Liquibase |
| Secretos | AWS Secrets Manager, Spring Cloud Config |

## Principios arquitectónicos

1. **Database per Service:** cada microservicio posee su BD; acceso cruzado directo está prohibido.
2. **API First:** contratos OpenAPI antes de implementar.
3. **Security by Default:** mTLS interno, JWT validado por `auth-service`.
4. **Observability by Design:** logs estructurados, métricas y tracing desde el scaffolding.
5. **Fail Fast:** circuit breakers, timeouts y retry con backoff exponencial.
6. **Infrastructure as Code:** Terraform/AWS CDK; sin recursos manuales en producción.

## Catálogo de microservicios

| Servicio | Puerto | Responsabilidad | BD | Squad |
|----------|--------|-----------------|-----|-------|
| `auth-service` | 8081 | JWT, OAuth 2.0, login/logout | PostgreSQL | Hermes |
| `user-service` | 8082 | Perfiles pacientes, médicos, clínicas | PostgreSQL | Hermes |
| `agendio-scheduling-service` | 8083 | Agendamiento, cancelación, reagendamiento | PostgreSQL | Agendio Core |
| `agendio-notification-service` | 8084 | Email (SES) y SMS (SNS) | Stateless | Agendio Core |
| `payment-service` | 8085 | Pagos y facturación | PostgreSQL | Pagamentos |
| `medical-records-service` | 8086 | Historial clínico | MongoDB | Clínico |
| `ai-assistant-service` | 8087 | Asistencia IA / RAG | Pinecone | IA |
| `audit-service` | 8088 | Auditoría y compliance LGPD | PostgreSQL | Governance |

## Flujo de tráfico (alto nivel)

1. Clientes (Web React, mobile, partners) → **AWS API Gateway** (TLS 1.3, rate limiting, validación JWT).
2. Gateway enruta a microservicios por dominio.
3. Comunicación síncrona REST entre servicios con Resilience4j.
4. Eventos de dominio vía **AWS SQS** (ej. `appointment-created.fifo` → notification-service).

## `agendio-scheduling-service` (servicio crítico)

**Responsabilidad:** toda la lógica de agendamiento (crear, confirmar, cancelar, reagendar, slots, reglas por clínica).

**APIs principales:**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/v1/appointments` | Crear agendamiento |
| GET | `/v1/appointments/{id}` | Consultar por ID |
| PATCH | `/v1/appointments/{id}/cancel` | Cancelar consulta |
| PATCH | `/v1/appointments/{id}/reschedule` | Reagendar |
| GET | `/v1/schedules/doctor/{doctorId}` | Disponibilidad del médico |

**Dependencias:** `user-service`, `payment-service` (REST); `audit-service`, `agendio-notification-service` (SQS).

## Mapa de squads

| Squad | Dominio | Stack principal |
|-------|---------|-----------------|
| Pegasus Core | API Gateway / plataforma central | Java + Spring Boot |
| Phoenix | Portal cliente / dashboard | React + TypeScript |
| Hermes | Integraciones y mensajería | SQS + Spring Boot |
| Athena | IA / RAG | LangChain + Pinecone |
| Atlas | Infra y DevOps | AWS + Docker + GitHub Actions |
| Agendio Core | Agendamiento y notificaciones | Java + PostgreSQL + SQS |

## Reglas para desarrolladores

- No consultar la BD de otro servicio; usar su API o eventos SQS.
- Toda comunicación interna autenticada; endpoints sin validación están prohibidos.
- Decisiones arquitectónicas relevantes se documentan como ADR en Confluence.
- Cambios de contrato API requieren versionado y revisión del squad owner.

## Contacto

- Dudas de arquitectura: Tech Lead del squad owner del servicio.
- Dirección de Ingeniería: `engineering@santopegasus.com`.