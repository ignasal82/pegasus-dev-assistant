# Guía oficial de ingeniería front-end

**Empresa:** Santo Pegasus Soluciones — Chapter Front-end  
**Versión:** 1.0.0 (Octubre 2025)  
**Fuente completa:** `guia-ingenieria-frontend.pdf`

## Propósito

Estándares obligatorios para proyectos nuevos (desde oct. 2025) y refactorizaciones mayores al 30 % del código. Alineada con la Guía de Ingeniería Back-end v2.4.0.

## Filosofía

- **UX como métrica técnica:** Web Vitals son criterio de aceptación.
- **Componentes como contratos:** props predecibles, reutilizables y testeables.
- **Seguridad en presentación:** validar y sanear todo input; nunca confiar ciegamente en datos del servidor.

## Stack mínimo obligatorio

| Categoría | Tecnología | Versión mínima |
|-----------|------------|----------------|
| Lenguaje | TypeScript | 5.0+ |
| UI | React | 18+ |
| Meta-framework | Next.js (si aplica SSR/SSG) | 14+ |
| Bundler (SPA) | Vite | 5+ |
| Estado servidor | TanStack Query | 5+ |
| Estado global | Zustand | 4+ |
| Formularios | React Hook Form | 7+ |
| Validación | Zod | 3+ |
| HTTP | Axios | 1.6+ |
| Estilos | Tailwind CSS | 3+ |

## Estructura de carpetas

```
src/
├── components/
│   ├── ui/          # Design System (reutilizable)
│   └── features/    # Componentes por dominio
├── hooks/           # Hooks compartidos
├── services/        # Clientes API
├── stores/          # Zustand stores
└── utils/
```

## Principios de código

### SOLID en componentes

- **SRP:** separar fetch de datos (hooks), presentación (`ProductCard`) y contenedores.
- **DRY:** buscar en `src/components/ui/` y `src/hooks/` antes de crear código nuevo.
- **KISS:** preferir soluciones legibles en < 5 minutos de lectura.
- **YAGNI:** no abstraer para casos hipotéticos.

### Ejemplo correcto (separación de responsabilidades)

```tsx
// hooks/useProduct.ts
export const useProduct = (id: string) =>
  useQuery({ queryKey: ['product', id], queryFn: () => fetchProduct(id) });

// components/ProductCard.tsx — solo presentación
export const ProductCard = ({ product }: { product: Product }) => (
  <div>{product.name}</div>
);
```

## Consumo de APIs

1. Definir funciones en `src/services/` con Axios configurado (interceptores JWT, errores).
2. Usar TanStack Query para cache, revalidación y estados loading/error.
3. No hacer `fetch` directo dentro de componentes de UI.

## Formularios

1. Schema Zod para validación tipada.
2. React Hook Form para performance.
3. Mensajes de error accesibles y en español/portugués según producto.

## Pruebas mínimas

| Tipo | Herramienta | Cobertura esperada |
|------|-------------|-------------------|
| Unitarias | Vitest + Testing Library | Componentes y hooks críticos |
| E2E | Playwright | Flujos principales de usuario |
| Visual | Storybook (opcional) | Componentes del Design System |

Ejecutar antes de PR: `npm run test` y `npm run build`.

## Code review

- Todo PR requiere al menos **1 aprobación** de un Senior del Chapter.
- Checklist: tipado estricto, sin `any` innecesarios, accesibilidad básica, pruebas incluidas.
- Propuestas de cambio a la guía: PR al repo `eng-guidelines`, aprobación de 2 Senior + Tech Lead.

## Performance (Web Vitals objetivo)

| Métrica | Objetivo |
|---------|----------|
| LCP | < 2.5 s |
| INP | < 200 ms |
| CLS | < 0.1 |

## Seguridad front-end

- No almacenar tokens en `localStorage` sin evaluación de riesgo; preferir cookies httpOnly cuando el back-end lo soporte.
- Sanitizar HTML dinámico; evitar `dangerouslySetInnerHTML` sin DOMPurify.
- No exponer secretos en variables `VITE_*` o `.env` commiteados.

## CI/CD front-end

Pipeline GitHub Actions típico:

1. `npm ci`
2. `npm run lint`
3. `npm run test`
4. `npm run build`
5. Deploy a ambiente según branch (`develop` → staging, `main` → producción).

## Contacto

- Chapter Front-end: `#front-end` en Slack.
- Tech Lead Front-end: solicitar vía People o `#people-hr` si no está asignado.