# Guía paso a paso — Challenge: Documentación para tu agente inteligente

Esta guía te ayuda a completar el **Paso 01** del Challenge de Alura: crear la documentación que alimentará a tu agente de IA para responder preguntas de usuarios reales.

---

## ¿Qué vas a construir?

Un conjunto de documentos (políticas, FAQs, guías, etc.) que tu agente usará como **base de conocimiento**. Cuando un usuario pregunte algo como *"¿Cuánto tarda el envío?"* o *"¿Puedo devolver un producto?"*, el agente buscará la respuesta en estos archivos.

**Formatos aceptados:** Markdown (`.md`), PDF (`.pdf`), CSV (`.csv`) u otros que tu herramienta de IA pueda leer.

---

## Paso 1 — Elige el contexto de tu negocio

Define **qué problema resuelve** tu agente. Elige un escenario que te resulte natural o que quieras practicar:

| # | Contexto | Documentos sugeridos |
|---|----------|----------------------|
| 1 | **Tienda Online / E-commerce** | Política de privacidad, reembolsos y devoluciones, FAQ, guía de envíos, términos y condiciones |
| 2 | **SaaS / Plataforma Digital** | Base de conocimiento del producto, FAQ de soporte, privacidad, planes y precios, términos de uso |
| 3 | **Logística / Envíos** | Política de envíos, rastreo de pedidos, reembolsos y siniestros, FAQ, reclamos |
| 4 | **Clínica / Consultorio** | Privacidad del paciente, FAQ de turnos, cancelaciones, convenios, instrucciones pre/post consulta |
| 5 | **Plataforma Educativa** | Reglamento del estudiante, reembolso de matrículas, FAQ de cursos, guía de la plataforma, becas |
| 6 | **Fintech / Banco Digital** | Privacidad, términos de uso, FAQ de transacciones, seguridad y fraudes, tarifas |

> **Recomendación:** No estás obligado a usar estas opciones. Puedes inventar tu propio negocio (restaurante, gimnasio, inmobiliaria, etc.) siempre que los documentos permitan responder preguntas útiles.

**Acción:** Anota en una línea el nombre de tu negocio ficticio y el contexto elegido.

```
Ejemplo: "TechStore — Tienda online de accesorios tecnológicos"
```

---

## Paso 2 — Define el nombre y la personalidad del agente

Antes de escribir documentos, piensa en **quién** responderá las preguntas:

- **Nombre del agente:** ej. *Asistente TechStore*, *Soporte LogiExpress*
- **Tono:** formal, cercano, técnico
- **Qué SÍ puede hacer:** consultar políticas, explicar procesos, orientar al usuario
- **Qué NO debe hacer:** dar consejos médicos/legales reales, inventar datos que no estén en los documentos

**Acción:** Escribe 3–5 frases describiendo a tu agente. Guárdalas; las usarás más adelante en el prompt del sistema.

---

## Paso 3 — Organiza la estructura de carpetas

Crea esta estructura dentro de `doc/` (puedes adaptarla):

```
doc/
├── INSTRUCCIONES-PASO-A-PASO.md    ← esta guía
├── conocimiento/                    ← documentos para el agente
│   ├── faq.md
│   ├── politica-privacidad.md
│   ├── politica-reembolsos.md
│   ├── guia-envios.md
│   └── terminos-condiciones.md
└── metadatos/
    └── agente.md                    ← nombre, tono y reglas del agente
```

**Acción:** Crea la carpeta `doc/conocimiento/` y `doc/metadatos/`.

---

## Paso 4 — Lista los documentos que necesitas

Marca al menos **3 documentos** (idealmente 4–5) según tu contexto:

### Si elegiste E-commerce (ejemplo)

- [ ] `faq.md` — Preguntas frecuentes
- [ ] `politica-privacidad.md`
- [ ] `politica-reembolsos.md`
- [ ] `guia-envios.md`
- [ ] `terminos-condiciones.md`

### Si elegiste otro contexto

Usa la tabla del Paso 1 y convierte cada ítem sugerido en un archivo `.md` o `.pdf`.

**Acción:** Completa tu checklist personal antes de escribir.

---

## Paso 5 — Redacta cada documento

Sigue estas reglas para que el agente responda bien:

### 5.1 Estructura clara

Usa títulos (`##`), listas y párrafos cortos. Evita bloques enormes de texto.

### 5.2 Información concreta

Incluye datos que un usuario preguntaría de verdad:

- Plazos (ej. *"El envío estándar tarda 3–5 días hábiles"*)
- Montos (ej. *"Devolución gratuita dentro de los 30 días"*)
- Pasos numerados (ej. *"1. Ingresá a Mi cuenta → 2. Pedidos → 3. Solicitar devolución"*)
- Contacto (email, teléfono, horario de atención)

### 5.3 No contradecir otros documentos

Si en `guia-envios.md` decís 5 días y en `faq.md` decís 7, el agente dará respuestas inconsistentes. Revisá coherencia entre archivos.

### 5.4 Plantilla mínima para un FAQ

Copia y adapta esto en `doc/conocimiento/faq.md`:

```markdown
# Preguntas frecuentes — [Nombre del negocio]

## Envíos
**¿Cuánto tarda en llegar mi pedido?**
El envío estándar demora entre 3 y 5 días hábiles. El express llega en 24–48 horas.

**¿Hacen envíos internacionales?**
Sí, a [países]. El plazo es de 10 a 15 días hábiles.

## Devoluciones
**¿Puedo devolver un producto?**
Sí, dentro de los 30 días desde la recepción, sin uso y con empaque original.

## Pagos
**¿Qué métodos de pago aceptan?**
Tarjeta de crédito/débito, transferencia y [otros].
```

### 5.5 Usa IA para acelerar (opcional)

Puedes pedirle a Cursor u otra IA:

> *"Genera una política de reembolsos para una tienda online de electrónica llamada TechStore. Incluye plazos, condiciones y pasos. Formato Markdown."*

Luego **revisa y personaliza** el contenido. No publiques texto genérico sin adaptarlo a tu negocio.

**Acción:** Crea y completa cada archivo de tu checklist.

---

## Paso 6 — Crea el archivo de metadatos del agente

En `doc/metadatos/agente.md` documenta cómo debe comportarse el agente:

```markdown
# Configuración del agente

## Nombre
Asistente [NombreNegocio]

## Rol
Asistente virtual de atención al cliente. Responde consultas sobre productos, envíos, devoluciones y políticas usando únicamente la documentación en `doc/conocimiento/`.

## Reglas
1. Responder siempre en español.
2. Si la información no está en los documentos, decirlo con claridad y ofrecer contacto humano.
3. No inventar precios, plazos ni políticas.
4. Ser breve y amable.

## Fuentes de conocimiento
- doc/conocimiento/faq.md
- doc/conocimiento/politica-privacidad.md
- (lista el resto de archivos)
```

**Acción:** Guarda `doc/metadatos/agente.md` con tu configuración real.

---

## Paso 7 — Valida la documentación con preguntas de prueba

Antes de conectar el agente, probá manualmente si tus documentos responden bien. Escribe 10 preguntas y busca la respuesta en tus archivos:

| Pregunta de prueba | ¿Está respondida en algún doc? |
|--------------------|--------------------------------|
| ¿Cuánto tarda el envío? | |
| ¿Cómo pido un reembolso? | |
| ¿Qué datos personales guardan? | |
| ¿Cuál es el horario de atención? | |
| … (agrega 6 más) | |

Si alguna pregunta no tiene respuesta, **agrega o amplía** el documento correspondiente.

**Acción:** Completa la tabla. Corrige huecos antes de seguir.

---

## Paso 8 — (Opcional) Exporta a PDF o CSV

Si tu herramienta de agente exige PDF o CSV:

- **PDF:** Exporta desde VS Code/Cursor con una extensión, o desde Word/Google Docs.
- **CSV:** Útil para FAQs tabulares:

```csv
categoria,pregunta,respuesta
envios,"¿Cuánto tarda el envío?","3 a 5 días hábiles en envío estándar."
devoluciones,"¿Puedo devolver un producto?","Sí, dentro de 30 días con empaque original."
```

Guarda exports en `doc/conocimiento/` si los necesitas.

---

## Paso 9 — Checklist final del Paso 01

Antes de pasar al siguiente paso del Challenge, verifica:

- [ ] Elegiste un contexto de negocio claro
- [ ] Creaste al menos 3 documentos de conocimiento
- [ ] Los documentos tienen información concreta (plazos, pasos, contacto)
- [ ] No hay contradicciones entre documentos
- [ ] Existe `doc/metadatos/agente.md` con reglas del agente
- [ ] Probaste al menos 10 preguntas y todas tienen respuesta en la documentación
- [ ] Los archivos están en formato legible (`.md`, `.pdf` o `.csv`)

---

## Paso 10 — Próximos pasos del Challenge

Cuando termines este paso, normalmente seguirás con:

1. **Integrar la documentación** al agente (RAG, archivos adjuntos, vector store, etc.)
2. **Configurar el prompt** usando `doc/metadatos/agente.md`
3. **Probar el agente** con las mismas preguntas del Paso 7
4. **Iterar:** si el agente falla, mejora el documento fuente, no solo el prompt

---

## Consejos finales

- **Menos es más al inicio:** 4 documentos bien escritos valen más que 10 vacíos.
- **Piensa como usuario:** ¿Qué preguntarías en el chat de soporte?
- **Coherencia:** mismos plazos, mismos montos, mismo email en todos los archivos.
- **Proyecto personal:** adapta nombres, productos y políticas a algo que te represente.

---

## Referencia rápida — Comandos para crear carpetas

Desde la raíz del proyecto (`proyecto_challenger`):

```powershell
New-Item -ItemType Directory -Force -Path doc\conocimiento
New-Item -ItemType Directory -Force -Path doc\metadatos
```

¡Listo! Con esta guía puedes completar el Paso 01 y tener una base sólida para tu agente inteligente.
