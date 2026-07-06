# Preguntas frecuentes — Santo Pegasus Soluciones

Documento consolidado para consultas rápidas del agente **Pegasus Dev Assistant**.

**Fuentes extendidas:** archivos `.md` y `.pdf` en `doc/conocimiento/` (SRE, arquitectura, front-end, onboarding).

---

## Sobre la empresa y Agendio

**¿Qué es Santo Pegasus Soluciones?**
Empresa de tecnología especializada en productos digitales para salud. Su producto principal es **Agendio**, plataforma SaaS de agendamiento de consultas médicas en modelo multi-tenant para clínicas, hospitales de pequeño y medio porte y consultorios independientes en Brasil.

**¿Qué es Agendio?**
Plataforma que conecta pacientes, médicos y clínicas. Opera con microservicios (agendamiento, pagos, notificaciones, historiales médicos, autenticación, auditoría, IA) desplegados en AWS, con cumplimiento LGPD y alta exigencia de disponibilidad.

**¿Cuál es el modelo de negocio de Agendio?**
SaaS multi-tenant: cada clínica o consultorio opera en un tenant aislado lógicamente, compartiendo la infraestructura común de la plataforma.

**¿Qué squads existen en ingeniería?**

| Squad | Dominio | Stack principal |
|-------|---------|-----------------|
| Pegasus Core | API Gateway / plataforma central | Java + Spring Boot |
| Phoenix | Portal cliente / dashboard | React + TypeScript |
| Hermes | Integraciones y mensajería | SQS + Spring Boot |
| Athena | IA / RAG | LangChain + Pinecone |
| Atlas | Infra y DevOps | AWS + Docker + GitHub Actions |
| Agendio Core | Agendamiento y notificaciones | Java + PostgreSQL + SQS |

---

## Cultura y forma de trabajo

**¿Cómo trabajamos en Santo Pegasus?**
Modelo híbrido (mayoría remoto, encuentros presenciales puntuales). Scrum adaptado con sprints de 2 semanas: planning, daily, refinement y retrospectiva.

**¿Cuáles son las core hours?**
10:00 a 17:00 (zona horaria del equipo). El resto del horario es flexible.

**¿Qué herramientas usamos a diario?**
Slack (comunicación), Jira (tareas y sprints), Confluence (documentación), GitHub (código y CI/CD).

**¿Qué es la cultura blameless?**
En post-mortems el foco es el sistema y los procesos, no culpar personas. Los incidentes son oportunidades de aprendizaje compartido; los post-mortems son documentos de aprendizaje, no disciplinarios.

**¿Quién es mi buddy durante el onboarding?**
Un desarrollador Senior o Pleno asignado durante los primeros 30 días para guiarte en accesos, entorno local y primeras contribuciones.

---

## Onboarding y accesos

**¿Cuánto tiempo tengo para ser plenamente productivo?**
El plan es 30/60/90 días:

| Período | Objetivo |
|---------|----------|
| 30 días | Entorno dominado, primeras features entregadas con buddy |
| 60 días | Autonomía en tareas medianas, participación activa en code reviews |
| 90 días | Productividad plena según seniority, ownership de módulos del squad |

La Semana 1 se enfoca en entorno configurado y conocer al equipo.

**¿Qué debo tener listo al final de la Semana 1?**
1. Accesos activos (correo, Slack, GitHub, Jira, Confluence, VPN, 1Password).
2. Entorno local funcionando (`docker compose up -d` o `npm run dev`).
3. Primer PR de prueba abierto con Conventional Commits.
4. Guía de ingeniería del Chapter leída.
5. Sesión de bienvenida con Tech Lead (≥ 1 h).
6. Checklist de onboarding firmado con tu Tech Lead.

**¿Cuál es el formato del correo corporativo?**
`nombre.apellido@santopegasus.com` — debe estar activo antes del Día 1.

**¿Cómo solicito accesos el Día 1?**
1. Enviar correo a `it-support@santopegasus.com` con asunto: `[ONBOARDING] Solicitud de accesos — [Tu Nombre] — [Fecha de Ingreso]`.
2. Incluir: nombre completo, rol, Tech Lead y squad asignado.
3. IT responde con ticket en máximo **4 horas hábiles**.
4. Para GitHub y AWS, pedir también por Slack al Tech Lead el mismo Día 1.

**¿Qué accesos necesito y quién los gestiona?**

| Sistema | Para qué | Solicitar a | Plazo |
|---------|----------|-------------|-------|
| Google Workspace | Correo, calendario, Drive | IT/Soporte | Antes del Día 1 |
| Slack | Comunicación interna | IT/Soporte | Antes del Día 1 |
| GitHub | Repositorios | Tech Lead del Chapter | Día 1 (primeras 2 h) |
| Jira | Sprints y tickets | Tech Lead o PM | Día 1 |
| Confluence | Documentación | Tech Lead o PM | Día 1 |
| AWS Console (read-only) | Cloud | Tech Lead DevOps | Día 1–2 |
| Datadog | Logs y métricas | Tech Lead DevOps | Día 1–2 |
| VPN corporativa | Recursos internos | IT/Soporte | Día 1 |
| 1Password | Credenciales | IT/Soporte | Día 1 |
| SonarQube | Calidad de código | IT/Soporte | Día 1–2 |
| Figma (front-end) | Diseño UI | Tech Lead Front-end | Día 2–3 |

**¿Qué canales de Slack debo unirme el Día 1?**
`#general`, `#back-end`, `#front-end`, `#devops`, `#incidents` (lectura), `#code-reviews`, `#aprendizaje`, `#random` y el canal de tu squad.

**¿Cuándo puedo solicitar cursos y certificaciones?**
Desde el primer mes, aunque se recomienda enfocarse en onboarding los primeros 90 días. Proceso: Tech Lead → formulario en Confluence → aprobación People (5 días hábiles).

---

## Entorno local

**¿Qué requisitos de hardware necesito?**
macOS 13+, Ubuntu 22.04+ o Windows 11 con WSL2. Mínimo 16 GB RAM, 50 GB disco libre y VPN activa.

**¿Cómo configuro el entorno back-end?**
1. Instalar SDKMAN e Java 17 Temurin: `sdk install java 17.0.11-tem`.
2. Instalar IntelliJ IDEA (licencia Ultimate corporativa) con plugins: SonarLint, Lombok, Docker.
3. Instalar Docker Desktop y verificar con `docker ps`.
4. Clonar repositorio del squad con SSH.
5. Crear `.env` con variables obligatorias (solicitar plantilla al buddy).
6. Ejecutar `docker compose up -d`.
7. Verificar `http://localhost:8080/actuator/health` → `UP`.
8. Ejecutar `./mvnw test` sin fallos.

**¿Cómo configuro el entorno front-end?**
1. Instalar NVM y Node.js 20 LTS.
2. Instalar VS Code con extensiones: ESLint, Prettier, Tailwind IntelliSense.
3. Clonar repo front-end, crear `.env`, ejecutar `npm install`.
4. `npm run dev` → `http://localhost:5173`.
5. `npm run test` y `npm run build` sin errores.

**¿Qué pasa si rompo algo en local?**
El entorno local es para experimentar. No afecta producción. Podés reconstruir con `docker compose down -v && docker compose up -d` con ayuda de tu buddy.

**¿Puedo usar `System.out.println()` para debug?**
No en código que va al repositorio. Usar SLF4J con Logback.

---

## Git, ramas y Pull Requests

**¿Puedo pushear directamente a `main` o `develop`?**
No. Esas ramas están protegidas; solo reciben código vía Pull Request aprobado con CI verde.

**¿Cómo funciona el flujo de ramas (GitFlow)?**

| Rama | Uso |
|------|-----|
| `main` | Producción — solo merges desde `release/` o `hotfix/` |
| `develop` | Integración de features |
| `feature/` | Nuevas funcionalidades desde `develop` |
| `release/` | Preparación de release hacia `main` |
| `hotfix/` | Correcciones urgentes en producción |

**¿Cómo nombro una branch?**
Patrón: `[tipo]/[JIRA-TICKET]-[descripcion-corta-en-kebab-case]`. Ejemplo: `feature/PEG-142-cadastro-de-usuarios`.

**¿Qué formato usan los commits?**
Conventional Commits: `<tipo>(<scope>): <descripción>`. Tipos: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `ci`.

**¿Cuál es el proceso para abrir un Pull Request?**
1. Ejecutar `./mvnw test` o `npm run test` en local.
2. Push de la branch y abrir PR con template completo.
3. Mínimo 1 aprobación del reviewer asignado.
4. Merge solo tras CI verde; nunca push directo a `main`/`develop`.

**¿Cuántas aprobaciones necesita un PR de front-end?**
Al menos 1 aprobación de un Senior del Chapter Front-end. Checklist: tipado estricto, sin `any` innecesarios, accesibilidad básica y pruebas incluidas.

---

## Arquitectura y microservicios

**¿Cuál es el stack principal?**

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

**¿Cuáles son los principios arquitectónicos clave?**
1. **Database per Service:** cada microservicio posee su BD.
2. **API First:** contratos OpenAPI antes de implementar.
3. **Security by Default:** mTLS interno, JWT validado por `auth-service`.
4. **Observability by Design:** logs estructurados, métricas y tracing.
5. **Fail Fast:** circuit breakers, timeouts y retry con backoff exponencial.
6. **Infrastructure as Code:** Terraform/AWS CDK; sin recursos manuales en producción.

**¿Puedo acceder directamente a la base de datos de otro microservicio?**
No. Cada servicio tiene su propia base de datos. Usar la API REST del servicio o eventos SQS.

**¿Cómo se comunican los microservicios?**
Comunicación síncrona REST entre servicios (con Resilience4j) y eventos de dominio vía AWS SQS (ej. `appointment-created.fifo` → `agendio-notification-service`). Toda comunicación interna debe estar autenticada.

**¿Cuáles son los microservicios principales de Agendio?**

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

**¿Cuál es el servicio más crítico de Agendio?**
`agendio-scheduling-service` — gestiona crear, confirmar, cancelar, reagendar consultas, slots y reglas por clínica. Depende de `user-service` y `payment-service` (REST), y de `audit-service` y `agendio-notification-service` (SQS).

**¿Cómo fluye el tráfico desde el cliente?**
1. Clientes (Web React, mobile, partners) → **AWS API Gateway** (TLS 1.3, rate limiting, validación JWT).
2. Gateway enruta a microservicios por dominio.
3. Comunicación síncrona REST y eventos asíncronos vía SQS.

**¿Dónde documento decisiones arquitectónicas?**
Como ADR (Architecture Decision Record) en Confluence. Los cambios de contrato API requieren versionado y revisión del squad owner.

**¿A quién consulto dudas de arquitectura?**
Tech Lead del squad owner del servicio, o `engineering@santopegasus.com` para temas transversales.

---

## Incidentes y SRE

**¿Qué es un incidente?**
Evento no planificado que degrada o interrumpe servicios en producción con impacto real o potencial en usuarios o SLOs.

**¿Qué es un incidente SEV-1?**
Sistema completamente caído, impacto total en producción, todos los clientes afectados. Ejemplos: Agendio inaccesible, API Gateway caída, auth totalmente caída. SLA de respuesta: 15 minutos; actualización cada 30 minutos.

**¿Cuáles son las severidades y sus SLAs?**

| Nivel | Impacto | Ejemplos | SLA respuesta | SLA actualización |
|-------|---------|----------|---------------|-------------------|
| SEV-1 | Caída total | Agendio inaccesible, API Gateway caída | 15 min | Cada 30 min |
| SEV-2 | Degradación severa | Agendamiento falla para ~40 % usuarios, P99 > 5 s | 30 min | Cada 1 h |
| SEV-3 | Degradación leve con workaround | Reportes lentos, búsqueda desactualizada | 4 h | Cada 4 h |
| SEV-4 | Anomalía sin impacto visible | Aumento de 4xx, CPU alta sin afectar flujo crítico | Próximo día hábil | Al cierre |

**¿Quién declara la severidad de un incidente?**
Solo el **Incident Commander (IC)**. Escalar severidad si crece el impacto, falla el workaround, el tiempo supera el doble del SLA o hay riesgo económico/contractual.

**¿Cuáles son los roles durante un incidente?**

| Rol | Responsabilidad |
|-----|-----------------|
| Incident Commander (IC) | Coordina, declara severidad, decide rollback, cierra incidente |
| Communications Lead | Actualiza `#incidents`, clientes y dirección según SLA |
| Technical Lead | Lidera diagnóstico, mitigación y rollback técnico |
| SME | Especialista convocado (RDS, ECS, SQS/SES, Spring Security, etc.) |

**¿Cómo reporto un bug crítico en producción?**
1. Publicar en `#incidents` en Slack con servicio afectado y síntomas.
2. El on-call reconoce la alerta en PagerDuty (máx. 15 min).
3. El IC declara severidad y abre War Room si aplica (`#sev1-war-room` o `#sev2-war-room`).
4. Crear ticket Bug en Jira del squad.

**¿Cómo funciona el on-call?**
Rotación semanal con Primary + Secondary on-call (Senior y Pleno obligatorios). SEV-1/SEV-2 notifican al Primary vía PagerDuty. Si Primary no reconoce en 5 min → Secondary; si Secondary no responde en 5 min más → IC de plantón y Tech Lead. El on-call tiene hasta **15 minutos** para declarar el incidente o descartarlo documentando en `#incidents`.

**¿Cuándo debo escalar un incidente?**
Si el impacto crece, el workaround deja de funcionar, el tiempo de resolución supera el doble del SLA actual o hay riesgo económico/contractual.

**¿Cómo se hace rollback en AWS ECS?**
1. Identificar la revisión estable anterior en ECS (task definition).
2. Technical Lead propone rollback al IC.
3. Ejecutar deploy de la revisión anterior vía pipeline o consola (solo con aprobación IC).
4. Verificar health checks y métricas de SLO.
5. Documentar en War Room y post-mortem.

**¿Qué son SLI, SLO, SLA y Error Budget?**
- **SLI:** métrica medible de confiabilidad (disponibilidad, latencia P99, tasa de error).
- **SLO:** objetivo acordado sobre el SLI (ej. 99.9 % disponibilidad mensual en agendamiento).
- **SLA:** compromiso contractual con clientes (consecuencias si se incumple).
- **Error Budget:** margen de indisponibilidad permitido antes de congelar deploys de features y priorizar estabilidad.

**¿Qué canales de Slack uso para incidentes?**

| Canal | Uso |
|-------|-----|
| `#incidents` | Declaración y seguimiento de todos los incidentes |
| `#sev1-war-room` | War Room exclusiva SEV-1 |
| `#sev2-war-room` | War Room SEV-2 |
| `#incidents-resolved` | Histórico y links a post-mortems |

---

## Ingeniería front-end

**¿Qué versiones mínimas debo usar?**
TypeScript 5.0+, React 18+, Next.js 14+ (si aplica SSR/SSG), Vite 5+, TanStack Query 5+, Zustand 4+, React Hook Form 7+, Zod 3+, Axios 1.6+, Tailwind CSS 3+.

**¿Dónde va el código reutilizable?**
Componentes UI en `src/components/ui/`; componentes por dominio en `src/components/features/`; hooks compartidos en `src/hooks/`; clientes API en `src/services/`; stores en `src/stores/`.

**¿Cómo consumo APIs desde el front-end?**
1. Definir funciones en `src/services/` con Axios configurado (interceptores JWT, manejo de errores).
2. Usar TanStack Query para cache, revalidación y estados loading/error.
3. No hacer `fetch` directo dentro de componentes de UI.

**¿Cómo manejo formularios?**
Schema Zod para validación tipada + React Hook Form para performance. Mensajes de error accesibles en español o portugués según el producto.

**¿Qué pruebas debo ejecutar antes de un PR?**
`npm run test` y `npm run build`. Cobertura esperada: unitarias con Vitest + Testing Library (componentes y hooks críticos), E2E con Playwright (flujos principales).

**¿Cuáles son los objetivos de Web Vitals?**

| Métrica | Objetivo |
|---------|----------|
| LCP | < 2.5 s |
| INP | < 200 ms |
| CLS | < 0.1 |

**¿Puedo guardar tokens JWT en localStorage?**
No sin evaluación de riesgo. Preferir cookies httpOnly cuando el back-end lo soporte. No exponer secretos en variables `VITE_*` ni en `.env` commiteados.

**¿A quién contacto del Chapter Front-end?**
Canal `#front-end` en Slack. Tech Lead Front-end: solicitar vía People o `#people-hr` si no está asignado.

---

## Seguridad

**¿Puedo hardcodear API keys o contraseñas?**
Nunca. Usar AWS Secrets Manager, variables de entorno y 1Password corporativo.

**¿Qué medidas de seguridad debo activar desde el Día 1?**
2FA en GitHub, Google Workspace y AWS. Nunca compartir credenciales personales; usar roles y 1Password.

**¿Qué hago si detecto un incidente de seguridad?**
1. Notificar en `#incidents` con `@security-lead`.
2. Avisar al Tech Lead del squad.
3. No borrar evidencia ni modificar logs.

**¿Puedo crear recursos en AWS manualmente en producción?**
No. Toda infraestructura se gestiona con Infrastructure as Code (Terraform/AWS CDK).

---

## CI/CD y calidad de código

**¿Cómo es el pipeline de front-end en GitHub Actions?**
1. `npm ci` → 2. `npm run lint` → 3. `npm run test` → 4. `npm run build` → 5. Deploy según branch (`develop` → staging, `main` → producción).

**¿Qué herramientas de calidad de código usamos?**
SonarQube (análisis estático), SonarLint en IntelliJ, ESLint y Prettier en VS Code.

**¿Cuándo se congelan deploys de features?**
Cuando el Error Budget de un servicio se agota; en ese caso se prioriza estabilidad sobre nuevas funcionalidades.

---

## Soporte interno

**¿Cómo contacto a IT?**
Email `it-support@santopegasus.com` (respuesta en 4 h hábiles) o `#it-support` en Slack (2 h hábiles).

**¿Cómo contacto a People?**
`people@santopegasus.com` o canal `#people-hr`.

**¿Cómo escalo un incidente de producción?**
Tech Lead del squad + `#incidents` + on-call PagerDuty.

**¿Cómo contacto a Dirección de Ingeniería?**
`engineering@santopegasus.com`.

---

## Referencia rápida de documentos

| Tema | Archivo |
|------|---------|
| Incidentes y SRE | `sre/protocolo-incidentes-postmortems.md` |
| Arquitectura | `arquitectura/arquitectura-microservicios-mapa-dominios.md` |
| Front-end | `ingenieria-frontend/guia-ingenieria-frontend.md` |
| Onboarding | `onboarding/manual-onboarding-desarrolladores.md` |
