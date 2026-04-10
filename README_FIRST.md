# SDD-Agentes — Vault Nucleo

Bienvenido al release del vault base de la metodología **SDD con Agentes Inteligentes**.

Este paquete contiene todo lo necesario para inicializar un nuevo proyecto usando el sistema.

---

## Contenido del paquete

```
sdd-nucleo-vX.Y.Z/
├── README_FIRST.md        ← este archivo
├── VERSION                ← versión del nucleo
├── bootstrap.sh           ← script de inicialización
├── pages/                 ← páginas de metodología (capa:: nucleo)
│   ├── Manifiesto-SDD-Agentes.md
│   ├── Agentes-y-Skills.md
│   ├── Plantillas-Logseq.md
│   ├── Plantilla-SPEC.md
│   ├── Protocolo-Orquestador.md
│   └── ... (17 páginas en total)
├── logseq/
│   └── config.edn         ← configuración de Logseq
└── assets/                ← recursos compartidos
```

---

## Inicio rápido (5 minutos)

### Requisitos previos

- [Logseq](https://logseq.com/) desktop instalado
- bash disponible (Git Bash en Windows, terminal en Mac/Linux)

### Paso 1 — Ejecutar el bootstrap

```bash
# dar permisos de ejecución (Mac/Linux)
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

Abrir la página `README-mi-app` generada por el bootstrap y:

1. Reemplazar la descripción placeholder con la descripción del proyecto
2. Agregar las primeras páginas específicas del proyecto

---

## Estructura del sistema

El sistema trabaja con dos capas:

| Capa | Descripción |
|------|-------------|
| `nucleo` | Metodología base — estas páginas, no se modifican |
| `proyecto` | Contenido específico del proyecto — se crea sobre el nucleo |

Las páginas nucleo incluidas son solo lectura de metodología. Las páginas propias del proyecto se crean con `capa:: proyecto`.

## Plantillas disponibles

Todas las páginas nuevas deben crearse usando una de estas plantillas (ver `Plantillas-Logseq`):

| Prefijo | Uso |
|---------|-----|
| `README-` | Índice o documentación principal de un módulo |
| `SPEC-` | Especificación de software (artefacto central del flujo SDD) |
| `REQ-` | Requerimiento funcional o no funcional |
| `DOC-` | Documentación técnica o funcional detallada |
| `TASK-` | Tarea del backlog |
| `DEC-` | Decision log de arquitectura o diseño |

## Agentes del sistema

El orquestador coordina estos agentes especializados:

| Agente | Responsabilidad |
|--------|----------------|
| `orquestador` | Punto de entrada — despacha al agente correcto |
| `analizador-requerimientos` | Extrae REQs desde texto libre |
| `validador-grafo` | Verifica integridad estructural del grafo |
| `validador-negocio` | Verifica consistencia semántica de specs |
| `desarrollador` | Genera código desde specs aprobadas |
| `documentador` | Actualiza el grafo tras merges exitosos |

---

## Próximos pasos

Una vez abierto el vault en Logseq:

1. Leer `Manifiesto-SDD-Agentes` — principios y restricciones del sistema
2. Leer `Crear-Nuevo-Proyecto` — guía detallada paso a paso
3. Configurar el MCP de Logseq para conectar agentes al vault (ver `MCP-Logseq-Configuracion`)
4. Crear la primera spec del proyecto usando la plantilla `SPEC-`

---

Versión del nucleo: ver archivo `VERSION`
Repositorio: https://github.com/lionel1/sdd_graph
