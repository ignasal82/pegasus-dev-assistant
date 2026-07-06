# Preguntas frecuentes — Santo Pegasus Soluciones

## Sobre la empresa y Agendio

**¿Qué es Santo Pegasus Soluciones?**
Empresa de tecnología especializada en productos digitales para salud y servicios profesionales. Su producto principal es **Agendio**, plataforma SaaS de agendamiento de consultas médicas en modelo multi-tenant para clínicas y consultorios en Brasil.

**¿Qué es Agendio?**
Plataforma que conecta pacientes, médicos y clínicas. Opera con microservicios (agendamiento, pagos, notificaciones, historiales médicos, autenticación, etc.) desplegados en AWS.

## Onboarding

**¿Cuánto tiempo tengo para ser plenamente productivo?**
El plan es 30/60/90 días. La Semana 1 se enfoca en entorno configurado y conocer al equipo. Productividad plena se espera alrededor del mes 3, según seniority.

**¿Puedo pushear directamente a `main` o `develop`?**
No. Esas ramas están protegidas; solo reciben código vía Pull Request aprobado.

**¿Qué pasa si rompo algo en local?**
El entorno local es para experimentar. No afecta producción. Podés reconstruir con `docker compose down -v && docker compose up -d` con ayuda de tu buddy.

**¿Puedo usar `System.out.println()` para debug?**
No en código que va al repositorio. Usar SLF4J con Logback.

## Incidentes y SRE

**¿Qué es un incidente SEV-1?**
Sistema completamente caído, impacto total en producción, todos los clientes afectados. SLA de respuesta: 15 minutos; actualización cada 30 minutos.

**¿Cómo reporto un bug crítico en producción?**
Notificar primero en `#incidents` en Slack y luego crear ticket Bug en Jira del squad.

**¿Qué es la cultura blameless?**
En post-mortems el foco es el sistema y los procesos, no culpar personas. Los incidentes son oportunidades de aprendizaje compartido.

## Arquitectura

**¿Cuál es el stack principal?**
Back-end: Java 17+, Spring Boot 3+, PostgreSQL/MongoDB/Redis. Front-end: React 18+, TypeScript, Vite, Tailwind. Infra: Docker, AWS ECS Fargate, SQS, API Gateway.

**¿Puedo acceder directamente a la base de datos de otro microservicio?**
No. Cada servicio tiene su propia base de datos (principio Database per Service).

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
Notificar en `#incidents` con `@security-lead`, avisar al Tech Lead y no borrar evidencia.

## Soporte interno

**¿Cómo contacto a IT?**
Email `it-support@santopegasus.com` (4 h hábiles) o `#it-support` en Slack (2 h hábiles).

**¿Cómo contacto a People?**
`people@santopegasus.com` o canal `#people-hr`.
