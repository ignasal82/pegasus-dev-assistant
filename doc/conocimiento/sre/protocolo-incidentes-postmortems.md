# Protocolo de respuesta a incidentes y post-mortems

**Empresa:** Santo Pegasus Soluciones — Chapter SRE  
**Versión:** 1.0.0 (Junio 2026)  
**Fuente completa:** `protocolo-incidentes-postmortems.pdf`

## Propósito

Define cómo detectar, gestionar, mitigar y documentar incidentes en producción de Agendio y demás microservicios. Aplica a back-end, DevOps, SRE, Tech Leads y PMs que operen sistemas productivos.

## Definiciones clave

**Incidente:** evento no planificado que degrada o interrumpe servicios en producción con impacto real o potencial en usuarios o SLOs.

**Problema:** causa raíz subyacente de uno o más incidentes recurrentes.

**Cambio planificado:** alteración coordinada con aprobación del IC, comunicación 48 h antes, plan de rollback y ventana de mantenimiento acordada.

## Clasificación de severidad

| Nivel | Impacto | Ejemplos | SLA respuesta | SLA actualización |
|-------|---------|----------|---------------|-------------------|
| SEV-1 | Caída total, todos los clientes | Agendio inaccesible, API Gateway caída, auth totalmente caída | 15 min | Cada 30 min |
| SEV-2 | Degradación severa en función crítica | Agendamiento falla para ~40 % usuarios, SES detenido, P99 > 5 s | 30 min | Cada 1 h |
| SEV-3 | Función no crítica afectada con workaround | Reportes lentos, búsqueda desactualizada | 4 h | Cada 4 h |
| SEV-4 | Anomalía sin impacto visible al usuario | Aumento de 4xx, CPU alta sin afectar flujo crítico | Próximo día hábil | Al cierre |

**Escalar severidad si:** crece el impacto, falla el workaround, el tiempo supera el doble del SLA o hay riesgo económico/contractual.

**Autoridad:** solo el Incident Commander (IC) declara o modifica la severidad.

## Roles durante un incidente

| Rol | Responsabilidad principal |
|-----|---------------------------|
| Incident Commander (IC) | Coordina, declara severidad, decide rollback, cierra incidente |
| Communications Lead | Actualiza `#incidents`, clientes y dirección según SLA |
| Technical Lead | Lidera diagnóstico, mitigación y rollback técnico |
| SME | Especialista convocado (RDS, ECS, SQS/SES, Spring Security, etc.) |

## Canales de comunicación

| Canal | Uso |
|-------|-----|
| `#incidents` | Declaración y seguimiento de todos los incidentes |
| `#sev1-war-room` | War Room exclusiva SEV-1 |
| `#sev2-war-room` | War Room SEV-2 |
| `#incidents-resolved` | Histórico y links a post-mortems |
| PagerDuty | Alertas on-call y escalada automática |

## On-call y PagerDuty

- Rotación semanal: Primary + Secondary on-call (Senior y Pleno obligatorios).
- SEV-1/SEV-2 notifican al Primary vía PagerDuty.
- Si Primary no reconoce en 5 min → Secondary; si Secondary no responde en 5 min más → IC de plantón y Tech Lead.
- El on-call tiene hasta **15 minutos** para declarar el incidente o descartarlo documentando en `#incidents`.

## Proceso de respuesta (resumen)

1. **Detección (T+0):** alerta PagerDuty/Datadog → reconocer → validar logs, traces y health en ECS.
2. **Declaración (T+0 a T+5 min):** publicar en `#incidents` → IC asume → severidad → War Room → asignar roles.
3. **Diagnóstico y mitigación:** Technical Lead coordina hipótesis, rollback o fix temporal.
4. **Comunicación:** Communications Lead actualiza según SLA de la severidad.
5. **Cierre:** IC confirma estabilidad y abre proceso de post-mortem.
6. **Post-mortem:** documento blameless con causa raíz, timeline y acciones preventivas.

## Rollback en AWS ECS (pasos)

1. Identificar la revisión estable anterior en ECS (task definition).
2. Technical Lead propone rollback al IC.
3. Ejecutar deploy de la revisión anterior vía pipeline o consola (solo con aprobación IC).
4. Verificar health checks y métricas de SLO.
5. Documentar en War Room y post-mortem.

## SLI, SLO y Error Budget

- **SLI:** métrica medible de confiabilidad (disponibilidad, latencia P99, tasa de error).
- **SLO:** objetivo acordado sobre el SLI (ej. 99.9 % disponibilidad mensual en agendamiento).
- **SLA:** compromiso contractual con clientes (consecuencias si se incumple).
- **Error Budget:** margen de indisponibilidad permitido antes de congelar deploys de features y priorizar estabilidad.

## Cultura blameless

Los post-mortems analizan sistemas y procesos, no personas. Son documentos de aprendizaje, no disciplinarios.

## Contacto y escalamiento

- Incidentes activos: `#incidents` + on-call PagerDuty.
- Seguridad: `@security-lead` en `#incidents`.
- Dirección de Ingeniería: `engineering@santopegasus.com`.