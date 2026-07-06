# Manual de onboarding para nuevos desarrolladores

**Empresa:** Santo Pegasus Soluciones  
**Versión:** 1.0.0 (Junio 2026)  
**Fuente completa:** `manual-onboarding-desarrolladores.pdf`

## Bienvenida

Manual para que la **Semana 1** sea productiva. Cada nuevo integrante tiene un **buddy** (Senior/Pleno) durante los primeros 30 días. Meta del día 7: entorno listo, equipo conocido y primeras contribuciones reales.

## Cultura y forma de trabajo

- Modelo **híbrido** (mayoría remoto, encuentros presenciales puntuales).
- **Scrum adaptado:** sprints de 2 semanas (planning, daily, refinement, retro).
- **Core hours:** 10:00–17:00 (zona horaria del equipo); resto flexible.
- Herramientas: Slack (comunicación), Jira (tareas), Confluence (docs), GitHub (código).

## Día 1 — Accesos

### Correo corporativo

Formato: `nombre.apellido@santopegasus.com` (debe estar activo antes del Día 1).

### Tabla de accesos

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

### Cómo solicitar accesos

1. Enviar correo a `it-support@santopegasus.com` con asunto: `[ONBOARDING] Solicitud de accesos — [Tu Nombre] — [Fecha de Ingreso]`.
2. Incluir: nombre completo, rol, Tech Lead y squad asignado.
3. IT responde con ticket en **máximo 4 horas hábiles**.
4. Para GitHub/AWS, pedir también por Slack al Tech Lead el mismo Día 1.

### Canales Slack obligatorios (Día 1)

`#general`, `#back-end`, `#front-end`, `#devops`, `#incidents` (lectura), `#code-reviews`, `#aprendizaje`, `#random` y el canal de tu squad.

## Entorno local — Back-end

### Requisitos

- macOS 13+, Ubuntu 22.04+ o Windows 11 con WSL2.
- 16 GB RAM, 50 GB disco libre, VPN activa.

### Pasos de configuración

1. Instalar SDKMAN e Java 17 Temurin: `sdk install java 17.0.11-tem`.
2. Instalar IntelliJ IDEA (licencia Ultimate corporativa) con plugins: SonarLint, Lombok, Docker.
3. Instalar Docker Desktop y verificar con `docker ps`.
4. Clonar repositorio del squad con SSH.
5. Crear `.env` con variables obligatorias (solicitar plantilla al buddy).
6. Ejecutar `docker compose up -d`.
7. Verificar `http://localhost:8080/actuator/health` → `UP`.
8. Ejecutar `./mvnw test` sin fallos.

## Entorno local — Front-end

1. Instalar NVM y Node.js 20 LTS.
2. Instalar VS Code con extensiones: ESLint, Prettier, Tailwind IntelliSense.
3. Clonar repo front-end, crear `.env`, ejecutar `npm install`.
4. `npm run dev` → `http://localhost:5173`.
5. `npm run test` y `npm run build` sin errores.

## Git y flujo de trabajo

### Ramas (GitFlow)

| Rama | Uso |
|------|-----|
| `main` | Producción — solo merges desde `release/` o `hotfix/` |
| `develop` | Integración de features |
| `feature/` | Nuevas funcionalidades desde `develop` |
| `release/` | Preparación de release hacia `main` |
| `hotfix/` | Correcciones urgentes en producción |

### Nomenclatura de branch

`[tipo]/[JIRA-TICKET]-[descripcion-corta-en-kebab-case]`

### Conventional Commits

Formato: `<tipo>(<scope>): <descripción>`

Tipos: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `ci`.

### Proceso de Pull Request

1. `./mvnw test` o `npm run test` en local.
2. Push de la branch y abrir PR con template completo.
3. Mínimo 1 aprobación del reviewer asignado.
4. Merge solo tras CI verde; nunca push directo a `main`/`develop`.

## Plan 30/60/90 días

| Período | Objetivo |
|---------|----------|
| 30 días | Entorno dominado, primeras features entregadas con buddy |
| 60 días | Autonomía en tareas medianas, participación activa en code reviews |
| 90 días | Productividad plena según seniority, ownership de módulos del squad |

## Beneficios y formación

- Cursos y certificaciones: solicitar desde el mes 1 vía Tech Lead → formulario Confluence → People (5 días hábiles).
- Home office: ver políticas en Confluence / People.

## Seguridad desde el Día 1

- Activar **2FA** en GitHub, Google Workspace y AWS.
- Nunca compartir credenciales personales; usar roles y 1Password.
- Incidente de seguridad: `#incidents` + `@security-lead`, avisar Tech Lead, no borrar evidencia.

## Checklist Semana 1 (resumen)

- [ ] Todos los accesos de la tabla confirmados.
- [ ] Entorno local con health check OK.
- [ ] Primer PR de prueba mergeado o en review.
- [ ] Guía de ingeniería del Chapter leída.
- [ ] Sesión de bienvenida con Tech Lead (≥ 1 h).
- [ ] Plan 30/60/90 acordado y página de onboarding en Confluence.

## Contactos útiles

| Área | Canal |
|------|-------|
| IT / accesos | `it-support@santopegasus.com`, `#it-support` (2–4 h hábiles) |
| People / RRHH | `people@santopegasus.com`, `#people-hr` |
| Incidentes producción | `#incidents` + on-call PagerDuty |
| Seguridad | `@security-lead` en `#incidents` |
| Dirección de Ingeniería | `engineering@santopegasus.com` |