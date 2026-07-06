# Preguntas frecuentes — Santo Pegasus Soluciones

Documento consolidado para consultas rápidas del agente. Fuente extendida: PDFs en `doc/conocimiento/`.

## Sobre la empresa y Agendio

**¿Qué es Santo Pegasus Soluciones?**
Empresa de tecnología especializada en productos digitales para salud. Su producto principal es **Agendio**, plataforma SaaS de agendamiento de consultas médicas en modelo multi-tenant para clínicas y consultorios en Brasil.

**¿Qué es Agendio?**
Plataforma que conecta pacientes, médicos y clínicas. Opera con microservicios (agendamiento, pagos, notificaciones, historiales médicos, autenticación, etc.) desplegados en AWS.

## Onboarding

**¿Cuánto tiempo tengo para ser plenamente productivo?**
El plan es 30/60/90 días. La Semana 1 se enfoca en entorno configurado y conocer al equipo. Productividad plena se espera alrededor del mes 3, según seniority.

**¿Qué debo tener listo al final de la Semana 1?**
1. Accesos activos (correo, Slack, GitHub, Jira, Confluence, VPN, 1Password).
2. Entorno local funcionando (`docker compose up -d` o `npm run dev`).
3. Primer PR de prueba abierto con Conventional Commits.
4. Checklist de onboarding firmado con tu Tech Lead.

**¿Puedo pushear directamente a `main` o `develop`?**
No. Esas ramas están protegidas; solo reciben código vía Pull Request aprobado.

**¿Cómo nombro una branch?**
Patrón: `[tipo]/[JIRA-TICKET]-[descripcion-corta-en-kebab-case]`. Ejemplo: `feature/PEG-142-cadastro-de-usuarios`.

**¿Qué pasa si rompo algo en local?**
El entorno local es para experimentar. No afecta producción. Podés reconstruir con `docker compose down -v && docker compose up -d` con ayuda de tu buddy.

**¿Puedo usar `System.out.println()` para debug?**
No en código que va al repositorio. Usar SLF4J con Logback.

## Incidentes y SRE

**¿Qué es un incidente SEV-1?**
Sistema completamente caído, impacto total en producción, todos los clientes afectados. SLA de respuesta: 15 minutos; actualización cada 30 minutos.

**¿Cuáles son las severidades y sus SLAs?**

| Nivel | Impacto | SLA respuesta | SLA actualización |
|-------|---------|---------------|-------------------|
| SEV-1 | Caída total | 15 min | Cada 30 min |
| SEV-2 | Degradación severa | 30 min | Cada 1 h |
| SEV-3 | Degradación leve con workaround | 4 h | Cada 4 h |
| SEV-4 | Anomalía sin impacto visible | Próximo día hábil | Al cierre |

**¿Cómo reporto un bug crítico en producción?**
1. Publicar en `#incidents` en Slack con servicio afectado y síntomas.
2. El on-call reconoce la alerta en PagerDuty (máx. 15 min).
3. El Incident Commander declara severidad y abre War Room si aplica.
4. Crear ticket Bug en Jira del squad.

**¿Qué es la cultura blameless?**
En post-mortems el foco es el sistema y los procesos, no culpar personas. Los incidentes son oportunidades de aprendizaje compartido.

**¿Cuándo debo escalar un incidente?**
Si el impacto crece, el workaround deja de funcionar, el tiempo de resolución supera el doble del SLA actual o hay riesgo económico/contractual.

## Arquitectura

**¿Cuál es el stack principal?**
Back-end: Java 17+, Spring Boot 3+, PostgreSQL/MongoDB/Redis. Front-end: React 18+, TypeScript, Vite, Tailwind. Infra: Docker, AWS ECS Fargate, SQS, API Gateway.

**¿Puedo acceder directamente a la base de datos de otro microservicio?**
No. Cada servicio tiene su propia base de datos (principio Database per Service).

**¿Cuáles son los microservicios principales de Agendio?**

| Servicio | Puerto | Base de datos | Squad |
|----------|--------|---------------|-------|
| `auth-service` | 8081 | PostgreSQL | Hermes |
| `user-service` | 8082 | PostgreSQL | Hermes |
| `agendio-scheduling-service` | 8083 | PostgreSQL | Agendio Core |
| `agendio-notification-service` | 8084 | Stateless | Agendio Core |
| `payment-service` | 8085 | PostgreSQL | Pagamentos |
| `medical-records-service` | 8086 | MongoDB | Clínico |
| `ai-assistant-service` | 8087 | Pinecone | IA |
| `audit-service` | 8088 | PostgreSQL | Governance |

## Front-end

**¿Qué versiones mínimas debo usar?**
TypeScript 5.0+, React 18+, Next.js 14+ (si aplica), Vite 5+, TanStack Query 5+, Tailwind CSS 3+.

**¿Dónde va el código reutilizable?**
Componentes UI en `src/components/ui/`; hooks compartidos en `src/hooks/`.

## RRHH y beneficios

**¿Cuáles son las core hours?**
10:00 a 17:00 (zona horaria del equipo); el resto del horario es flexible.

**¿Cuándo puedo solicitar cursos y certificaciones?**
Desde el primer mes, aunque se recomienda enfocarse en onboarding los primeros 90 días. Proceso: Tech Lead → formulario en Confluence → aprobación People (5 días hábiles).

## Seguridad

**¿Puedo hardcodear API keys o contraseñas?**
Nunca. Usar AWS Secrets Manager, variables de entorno y 1Password corporativo.

**¿Qué hago si detecto un incidente de seguridad?**
1. Notificar en `#incidents` con `@security-lead`.
2. Avisar al Tech Lead del squad.
3. No borrar evidencia ni modificar logs.

## Soporte interno

**¿Cómo contacto a IT?**
Email `it-support@santopegasus.com` (respuesta en 4 h hábiles) o `#it-support` en Slack (2 h hábiles).

**¿Cómo contacto a People?**
`people@santopegasus.com` o canal `#people-hr`.

**¿Cómo solicito accesos el Día 1?**
Enviar correo a `it-support@santopegasus.com` con asunto `[ONBOARDING] Solicitud de accesos — [Tu Nombre] — [Fecha de Ingreso]`, incluyendo rol, Tech Lead y squad.