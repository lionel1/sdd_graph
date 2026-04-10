# SDD-Agentes — Vault Nucleo

Bienvenido al release del vault base de la metodología **SDD con Agentes Inteligentes**.

Este paquete contiene todo lo necesario para inicializar un nuevo proyecto usando el sistema.

---

## Contenido del paquete

```
sdd-nucleo-vX.Y.Z/
├── README_FIRST.md           <- este archivo
├── VERSION                   <- version del nucleo
├── bootstrap.sh              <- script de inicializacion
├── scripts/
│   ├── validate_properties.py  <- valida propiedades de paginas (V-001 a V-006)
│   ├── validate_links.py       <- valida vinculos [[...]] internos (V-002)
│   └── check_pr_spec.py        <- verifica referencia a spec en PRs (R-003)
├── pages/                    <- paginas de metodologia (capa:: nucleo)
│   ├── Manifiesto-SDD-Agentes.md
│   ├── Agentes-y-Skills.md
│   ├── Referencia-Agentes.md      <- guia rapida comparativa de agentes
│   ├── Plantillas-Logseq.md
│   ├── Plantilla-SPEC.md
│   ├── Protocolo-Orquestador.md
│   ├── SystemPrompt-Orquestador.md
│   ├── SystemPrompt-Consultor-Metodologia.md
│   ├── SystemPrompt-Validador-Grafo.md
│   ├── SystemPrompt-Validador-Negocio.md
│   ├── SystemPrompt-Analizador-Requerimientos.md
│   ├── SystemPrompt-Desarrollador.md
│   ├── SystemPrompt-Tester.md
│   ├── SystemPrompt-Documentador.md
│   └── ... (resto del nucleo)
├── logseq/
│   └── config.edn            <- configuracion de Logseq
└── assets/                   <- recursos compartidos
```

---

## Inicio rapido (5 minutos)

### Requisitos previos

- [Logseq](https://logseq.com/) desktop instalado
- Python 3.8+ (para los scripts de validacion)
- bash disponible (Git Bash en Windows, terminal en Mac/Linux)

### Paso 1 — Ejecutar el bootstrap

```bash
# dar permisos de ejecucion (Mac/Linux)
chmod +x bootstrap.sh

# crear el vault del proyecto
./bootstrap.sh <nombre-proyecto> <directorio-destino>

# ejemplo:
./bootstrap.sh mi-app ~/proyectos
```

El script crea la estructura del vault en `~/proyectos/mi-app/`.

### Paso 2 — Abrir en Logseq

1. Abrir Logseq
2. Click en **Add graph**
3. Seleccionar la carpeta `~/proyectos/mi-app`
4. Esperar que Logseq indexe el vault (unos segundos)

### Paso 3 — Configurar el proyecto

Abrir la pagina `README-mi-app` generada por el bootstrap y:

1. Reemplazar la descripcion placeholder con la descripcion del proyecto
2. Agregar las primeras paginas especificas del proyecto

---

## Estructura del sistema

El sistema trabaja con dos capas:

| Capa | Descripcion |
|------|-------------|
| `nucleo` | Metodologia base — estas paginas, no se modifican |
| `proyecto` | Contenido especifico del proyecto — se crea sobre el nucleo |

Las paginas nucleo son solo lectura de metodologia. Las paginas propias del proyecto se crean con `capa:: proyecto`.

## Plantillas disponibles

Todas las paginas nuevas deben crearse usando una de estas plantillas (ver `Plantillas-Logseq`):

| Prefijo | Uso |
|---------|-----|
| `README-` | Indice o documentacion principal de un modulo |
| `SPEC-` | Especificacion de software (artefacto central del flujo SDD) |
| `REQ-` | Requerimiento funcional o no funcional |
| `DOC-` | Documentacion tecnica o funcional detallada |
| `TASK-` | Tarea del backlog |
| `DEC-` | Decision log de arquitectura o diseno |

## Agentes del sistema

El orquestador coordina estos 8 agentes especializados:

| Agente | Responsabilidad |
|--------|----------------|
| `orquestador` | Punto de entrada — coordina todos los agentes |
| `consultor-metodologia` | Responde preguntas sobre el sistema leyendo el vault en tiempo real |
| `analizador-requerimientos` | Extrae REQs desde texto libre |
| `validador-negocio` | Verifica consistencia semantica de specs |
| `validador-grafo` | Verifica integridad estructural del vault |
| `desarrollador` | Genera codigo desde specs aprobadas |
| `tester` | Genera tests basados en criterios de aceptacion de REQs |
| `documentador` | Actualiza el grafo tras merges exitosos |

Ver `Referencia-Agentes` en el vault para la guia comparativa completa.

## Pipeline de validacion de PRs

El paquete incluye tres scripts de validacion que se ejecutan automaticamente en cada PR (via GitHub Actions) y pueden correrse localmente antes de hacer commit:

| Script | Que verifica | Sale con error si... |
|--------|--------------|----------------------|
| `validate_properties.py` | `tipo::`, `estado::`, `version::`, `capa::` en cada pagina | Pagina `nucleo` sin propiedades requeridas |
| `validate_links.py` | Todos los `[[vinculos]]` internos del vault | Algun vinculo apunta a pagina inexistente |
| `check_pr_spec.py` | Cuerpo del PR tiene referencia `((uuid))` a spec | PR sin referencia a bloque del grafo |

### Correr validaciones localmente

```bash
# desde la raiz del vault del proyecto
python scripts/validate_properties.py pages/
python scripts/validate_links.py pages/
python scripts/check_pr_spec.py "Descripcion del PR ((uuid-de-la-spec))"
```

Todos deben terminar con exit 0 antes de abrir el PR.

### Como configurar GitHub Actions en tu proyecto

Copiar `.github/workflows/validate.yml` a tu repositorio. Se activa automaticamente en cada PR hacia `main` o `dev`.

---

## Proximos pasos

Una vez abierto el vault en Logseq:

1. Leer `Manifiesto-SDD-Agentes` — principios y restricciones del sistema
2. Leer `Referencia-Agentes` — guia rapida de los 8 agentes
3. Leer `Crear-Nuevo-Proyecto` — guia detallada paso a paso
4. Configurar el MCP de Logseq para conectar agentes al vault (ver `MCP-Logseq-Configuracion`)
5. Crear la primera spec del proyecto usando la plantilla `SPEC-`

---

Version del nucleo: ver archivo `VERSION`
Repositorio: https://github.com/lionel1/sdd_graph
