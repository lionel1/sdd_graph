# SDD-Agentes — Metodología de Desarrollo Orientado a Especificaciones

Vault base de Logseq con la metodología **SDD (Specification-Driven Development) con Agentes Inteligentes**.

El sistema usa un grafo de conocimiento en Logseq conectado a agentes de IA vía MCP como fuente de verdad. Los agentes automatizan la validación, el análisis de requerimientos, la generación de código y la documentación.

## Qué incluye este repositorio

Este repo contiene el **nucleo** del sistema: las páginas de metodología base que se distribuyen a todos los proyectos nuevos.

| Contenido | Descripción |
|-----------|-------------|
| `pages/` (capa:: nucleo) | Manifiesto, agentes, skills, protocolo, plantillas, glosario |
| `logseq/config.edn` | Configuración de Logseq con queries, workflows y vistas |
| `scripts/bootstrap.sh` | Script para inicializar un vault nuevo desde el release |
| `.github/workflows/release-nucleo.yml` | Pipeline que genera el release empaquetado |

## Crear un proyecto nuevo

### 1. Descargar el release

```bash
# con gh CLI
gh release download --repo lionel1/sdd_graph --pattern "*.zip"

# o descargar desde la página de releases de GitHub
```

### 2. Ejecutar el bootstrap

```bash
unzip sdd-nucleo-v1.0.0.zip -d sdd-nucleo
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
│   ├── ...                          ← resto del nucleo
│   └── README-mi-proyecto.md        ← índice del proyecto (generado)
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
4. El **desarrollador** genera código referenciando la spec
5. El **validador-grafo** verifica integridad antes del merge
6. El **documentador** actualiza el grafo tras el merge exitoso

**Plantillas disponibles**
`README` · `DOC` · `REQ` · `SPEC` · `TASK` · `RN` · `CONC` · `DEC`

## Pipeline de release

El workflow `.github/workflows/release-nucleo.yml` se activa en cada push a `main`.

- Colecta todas las páginas con `capa:: nucleo`
- Empaqueta junto a `config.edn`, `assets/` y `bootstrap.sh`
- Publica el zip como GitHub Release

Para generar una versión estable con tag semántico:

```bash
# desde GitHub Actions → workflow_dispatch → ingresar versión: v1.0.0
# o via gh CLI:
gh workflow run release-nucleo.yml -f version=v1.0.0
```

## Requisitos

- [Logseq](https://logseq.com/) desktop
- Plugin **Logseq HTTP API server** activo (para usar el MCP con agentes)
- bash (Git Bash en Windows, terminal en Mac/Linux)
