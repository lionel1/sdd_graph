# SDD-Agentes — Metodología de Desarrollo Orientado a Especificaciones

Vault base de Logseq con la metodología **SDD (Specification-Driven Development) con Agentes Inteligentes**.

El sistema usa un grafo de conocimiento en Logseq conectado a agentes de IA vía MCP como fuente de verdad. Los agentes automatizan la validación, el análisis de requerimientos, la generación de código y la documentación.

## Qué incluye este repositorio

Este repo contiene el **nucleo** del sistema: las páginas de metodología base que se distribuyen a todos los proyectos nuevos.

| Contenido | Descripción |
|-----------|-------------|
| `pages/` (capa:: nucleo) | Manifiesto, agentes, skills, protocolo, plantillas, system prompts, glosario |
| `logseq/config.edn` | Configuración de Logseq con queries, workflows y vistas |
| `scripts/bootstrap.sh` | Script para inicializar un vault nuevo desde el release |
| `scripts/validate_properties.py` | Valida propiedades requeridas en páginas del vault (V-001 a V-006) |
| `scripts/validate_links.py` | Valida vínculos `[[...]]` internos del vault (V-002) |
| `scripts/check_pr_spec.py` | Verifica que el PR referencia un bloque de spec `((uuid))` (R-003) |
| `.github/workflows/validate.yml` | Ejecuta los validadores automáticamente en cada PR |
| `.github/workflows/release-nucleo.yml` | Genera el release empaquetado al pushear a `main` |
| `.github/PULL_REQUEST_TEMPLATE.md` | Template de PR con checklist SDD |

## Crear un proyecto nuevo

### 1. Descargar el release

```bash
# con gh CLI
gh release download --repo lionel1/sdd_graph --pattern "*.zip"

# o descargar desde la página de releases de GitHub
```

### 2. Ejecutar el bootstrap

```bash
unzip sdd-nucleo-v1.1.0.zip -d sdd-nucleo
cd sdd-nucleo
chmod +x bootstrap.sh
./bootstrap.sh mi-proyecto ~/proyectos
```

El script crea la siguiente estructura:

```
mi-proyecto/
├── pages/
│   ├── Manifiesto-SDD-Agentes.md
│   ├── Agentes-y-Skills.md
│   ├── Plantillas-Logseq.md
│   ├── Referencia-Agentes.md       ← guía rápida de agentes
│   ├── SystemPrompt-*.md           ← system prompts de los 8 agentes
│   ├── ...                         ← resto del nucleo
│   └── README-mi-proyecto.md       ← índice del proyecto (generado)
├── logseq/
│   └── config.edn
├── journals/
├── assets/
└── .gitignore
```

### 3. Abrir en Logseq

1. Abrir Logseq
2. **Add graph** → seleccionar la carpeta `~/proyectos/mi-proyecto`
3. Editar `README-mi-proyecto.md` con la descripción del proyecto

Ver la guía completa en la página `[[Crear-Nuevo-Proyecto]]` dentro del vault.

## Conceptos clave

**Capas del sistema**
- `capa:: nucleo` — metodología base, distribuida con cada release (este repo)
- `capa:: proyecto` — contenido específico de cada proyecto, no se distribuye

**Flujo SDD (Spec-First)**
1. El usuario describe una funcionalidad
2. El **analizador-requerimientos** extrae y estructura los REQs en el grafo
3. El **validador-negocio** verifica consistencia de la spec
4. El **desarrollador** genera código referenciando la spec aprobada
5. El **tester** genera tests basados en los criterios de aceptación de los REQs
6. El **validador-grafo** verifica integridad del vault antes del merge
7. El **documentador** actualiza el grafo tras el merge exitoso

**Agentes del sistema**

| Agente | Responsabilidad |
|--------|----------------|
| `orquestador` | Punto de entrada — coordina todos los agentes |
| `consultor-metodologia` | Responde preguntas sobre el sistema leyendo el vault en tiempo real |
| `analizador-requerimientos` | Extrae REQs desde texto libre |
| `validador-negocio` | Verifica consistencia semántica de specs |
| `validador-grafo` | Verifica integridad estructural del vault |
| `desarrollador` | Genera código desde specs aprobadas |
| `tester` | Genera tests basados en criterios de aceptación de REQs |
| `documentador` | Actualiza el grafo tras merges exitosos |

**Plantillas disponibles**
`README` · `DOC` · `REQ` · `SPEC` · `TASK` · `RN` · `CONC` · `DEC`

## Pipeline de validación

Cada PR hacia `main` o `dev` ejecuta automáticamente tres validadores:

| Script | Qué verifica | Cuándo bloquea |
|--------|--------------|----------------|
| `validate_properties.py` | Propiedades `tipo::`, `estado::`, `version::`, `capa::` en páginas | Error crítico si página nucleo sin propiedades |
| `validate_links.py` | Vínculos `[[...]]` rotos en el vault | Siempre si hay vínculos rotos |
| `check_pr_spec.py` | Referencia `((uuid))` al bloque de spec en el PR | Siempre si el PR no referencia la spec |

**Ejecutar localmente antes de abrir un PR:**

```bash
python scripts/validate_properties.py pages/
python scripts/validate_links.py pages/
python scripts/check_pr_spec.py "Descripción del PR con ((uuid-de-la-spec))"
```

## Pipeline de release

El workflow `.github/workflows/release-nucleo.yml` se activa en cada push a `main`.

- Colecta todas las páginas con `capa:: nucleo`
- Empaqueta junto a `config.edn`, `assets/`, `bootstrap.sh` y `README_FIRST.md`
- Publica el zip como GitHub Release

Para generar una versión estable con tag semántico, disparar el workflow manualmente desde GitHub Actions → **Release Nucleo** → **Run workflow** → ingresar versión (ej: `v1.1.0`).

## Requisitos

- [Logseq](https://logseq.com/) desktop
- Plugin **Logseq HTTP API server** activo (para usar el MCP con agentes)
- Python 3.8+ (para los scripts de validación)
- bash (Git Bash en Windows, terminal en Mac/Linux)
