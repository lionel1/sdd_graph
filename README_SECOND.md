# SDD-Agentes — Guía de Proyectos Próximos

Este documento es la hoja de ruta operativa para construir sobre el núcleo existente.

- `README.md` → qué es el sistema y cómo usarlo hoy
- `README_FIRST.md` → cómo inicializar un vault nuevo desde el release
- **`README_SECOND.md` (este archivo)** → qué construir después, paso a paso

---

## Estado actual del sistema

| Fase | Descripción | Estado |
|------|-------------|:------:|
| 1 — Fundamentos del Grafo | Estructura base, config, pipeline de release | ✅ Completada |
| 2 — Configuración MCP | MCP de Logseq instalado y verificado | ✅ Completada |
| 3 — Definición de Agentes | 8 agentes con system prompts completos | ✅ Completada |
| 4 — Protocolo del Orquestador | Árbol de despacho, escalamiento, respuesta | ⏳ Pendiente |
| 5 — Pipeline Git | GitHub Actions + 3 scripts de validación | ✅ Completada |
| 6 — Validador de Grafo | UUID blocks, propiedades completas, CI | ⏳ Pendiente |
| 7 — Analizador de Requerimientos | Extracción desde texto libre + escritura al grafo | ⏳ Pendiente |
| 8 — Integración Multi-Agente | Flujo end-to-end operativo y medido | ⏳ Pendiente |
| 9 — Refinamiento Final | Docs actualizados, release notes, release v2.0 | ⏳ Pendiente |

**Proyecto transversal — MCP File Server (Opción D)**: reemplazar el MCP de Logseq por un server que acceda directamente a los archivos `.md`. Sin dependencia de app corriendo. Ver `pages/Alternativas-Mejora.md` para el análisis completo.

---

## Orden de ejecución recomendado

```
MCP File Server ──→ Fase 4 ──→ Fase 6 ──→ Fase 7 ──→ Fase 8 ──→ Fase 9
(transversal)     (despacho)  (validador) (analizar)  (e2e)     (release)
```

El MCP File Server habilita que los agentes funcionen sin Logseq corriendo — prerequisito práctico antes de cualquier trabajo serio con Fases 7 y 8. Fase 4 puede avanzar en paralelo porque no depende del MCP.

---

## Proyecto A — MCP File Server (Opción D Hybrid)

### Descripción funcional

Construir un servidor MCP custom en Python que lea y escriba los archivos `.md` del vault directamente, sin depender de que Logseq esté corriendo. Logseq sigue siendo el editor humano — el MCP file server es solo para los agentes.

```
archivos .md ──┬── Logseq (UI humana)
               └── MCP file server (agentes, headless, CI)
```

### Operaciones mínimas a implementar

| Operación | Descripción |
|-----------|-------------|
| `read_page(name)` | Lee el contenido de `pages/{name}.md` |
| `create_page(name, content)` | Crea o sobreescribe `pages/{name}.md` |
| `search(query)` | Búsqueda por texto en todos los archivos `.md` |
| `get_backlinks(name)` | Lista páginas que contienen `[[name]]` |
| `list_pages()` | Lista todas las páginas del vault con sus propiedades |
| `get_property(name, key)` | Lee una propiedad `key::` de una página |

### Archivos a crear

```
scripts/
└── mcp_file_server.py      ← servidor MCP principal (~300 líneas)

tests/
└── test_mcp_file_server.py ← tests de las 6 operaciones

.mcp.json                   ← actualizar transport a nuevo server
```

### Pasos de implementación

1. Definir el esquema de cada operación (inputs, outputs, errores esperados)
2. Implementar `read_page` y `list_pages` — sin efectos secundarios, fácil de validar
3. Implementar `search` con soporte de regex básico (usar `re` de stdlib)
4. Implementar `get_backlinks` — parsear `[[...]]` en todos los `.md`
5. Implementar `create_page` — crear archivo + sobreescribir si existe
6. Implementar `get_property` — parsear frontmatter `key:: value`
7. Testear con los agentes existentes verificando paridad con `@logseq/mcp-server`
8. Actualizar `.mcp.json` para apuntar al nuevo server
9. Documentar en `pages/MCP-Logseq-Configuracion.md`

### Criterio de aceptación

- [ ] Los 8 agentes pueden leer y escribir páginas sin Logseq corriendo
- [ ] `test_mcp_file_server.py` pasa en CI (GitHub Actions)
- [ ] `.mcp.json` apunta al nuevo server y funciona desde Claude Code
- [ ] Logseq sigue mostrando cambios correctamente (archivos compatibles)

---

## Proyecto B — Fase 4: Protocolo del Orquestador

### Descripción funcional

Implementar la lógica de despacho del orquestador: cómo decide a qué agente delegar, bajo qué condiciones escala al humano, y qué formato devuelve cada agente. Hoy el system prompt existe (`pages/SystemPrompt-Orquestador.md`) pero el árbol de decisión no está codificado ni testeado.

### Archivos a modificar / crear

```
pages/
├── SystemPrompt-Orquestador.md   ← agregar árbol de decisión explícito
├── Protocolo-Orquestador.md      ← documentar condiciones de escalamiento
└── SPEC-orquestador-dispatch.md  ← spec formal del flujo (nueva)

scripts/
└── test_orquestador_flow.py      ← caso de uso simple end-to-end
```

### Pasos de implementación

1. **Definir el árbol de despacho** en `Protocolo-Orquestador.md`:
   - Input del usuario → ¿es una pregunta de metodología? → `consultor-metodologia`
   - Input con descripción de funcionalidad → `analizador-requerimientos`
   - Spec existente aprobada → `desarrollador`
   - Código generado sin tests → `tester`
   - Pre-merge → `validador-grafo`
   - Post-merge → `documentador`

2. **Definir condiciones de escalamiento al humano**:
   - Ambigüedad irresolvible en la spec
   - Conflicto entre REQs existentes
   - Error en 3+ intentos consecutivos

3. **Definir formato de respuesta de agentes** (contrato JSON):
   ```json
   {
     "status": "ok | error | escalate",
     "agent": "nombre-del-agente",
     "output": "...",
     "artifacts": ["[[Pagina]]", "((uuid))"],
     "next_suggested": "nombre-agente-siguiente | null"
   }
   ```

4. **Actualizar `SystemPrompt-Orquestador.md`** con el árbol y el contrato de respuesta

5. **Escribir y ejecutar `test_orquestador_flow.py`** con un caso simple:
   - Input: "Necesito una función que valide emails"
   - Expected: orquestador invoca `analizador-requerimientos`
   - Expected: se crea una página `REQ-validacion-email.md` en el vault

6. Documentar lecciones aprendidas en `Protocolo-Orquestador.md`

### Criterio de aceptación

- [ ] El árbol de despacho está documentado con cada condición y su agente destino
- [ ] Las condiciones de escalamiento al humano están definidas explícitamente
- [ ] El formato JSON de respuesta de agentes está en `Protocolo-Orquestador.md`
- [ ] El flujo simple (input → analizador → REQ en grafo) funciona de extremo a extremo

---

## Proyecto C — Fase 6: Validador de Grafo (extensión)

### Descripción funcional

Extender los scripts de validación existentes (Fase 5) con la verificación de block UUIDs y mejorar la cobertura de propiedades. Los scripts actuales verifican vínculos `[[...]]` y propiedades básicas — falta verificar que los `((uuid))` referenciados realmente existen en algún bloque del vault.

### Archivos a modificar / crear

```
scripts/
├── validate_properties.py      ← EXTENDER: agregar verificación de capa:: proyecto
├── validate_links.py           ← EXTENDER: agregar detección de páginas huérfanas
└── validate_block_refs.py      ← NUEVO: verificar que ((uuid)) existen en el vault

.github/workflows/validate.yml  ← agregar validate_block_refs.py al pipeline
pages/Pipeline-Git.md           ← documentar el nuevo validador
```

### Pasos de implementación

1. **`validate_block_refs.py`** — nuevo script:
   - Extraer todos los `((uuid))` referenciados en todos los archivos del vault
   - Verificar que cada UUID existe como block ID en alguna página
   - Salir con error y lista de UUIDs rotos si encuentra faltantes

2. **Extender `validate_properties.py`**:
   - Agregar verificación de páginas `capa:: proyecto` con `proyecto::` faltante
   - Mejorar mensajes de error para indicar qué propiedad específica falta

3. **Extender `validate_links.py`**:
   - Detectar páginas que no tienen ningún vínculo entrante ni saliente (huérfanas)
   - Reportar como warning (no como error bloqueante)

4. **Agregar `validate_block_refs.py` al workflow** en `.github/workflows/validate.yml`

5. **Testear con casos de error intencionales**: crear una página con `((uuid-inexistente))` y verificar que el pipeline lo detecta

6. Actualizar `pages/Pipeline-Git.md` con el nuevo validador

### Criterio de aceptación

- [ ] `validate_block_refs.py` detecta UUIDs rotos y falla el pipeline
- [ ] Los tres scripts tienen tests de casos de error documentados
- [ ] El pipeline de CI ejecuta los cuatro scripts en cada PR
- [ ] `pages/Pipeline-Git.md` describe los cuatro validadores

---

## Proyecto D — Fase 7: Analizador de Requerimientos

### Descripción funcional

Hacer operativo el agente `analizador-requerimientos`: que pueda recibir texto libre (descripción de una funcionalidad), extraer requerimientos estructurados y escribirlos al vault como páginas `REQ-*` usando el MCP. Este es el primer agente que produce artefactos reales en el grafo.

### Prerequisito

El MCP File Server (Proyecto A) debe estar operativo antes de implementar este proyecto.

### Archivos a modificar / crear

```
pages/
├── SystemPrompt-Analizador-Requerimientos.md  ← revisar y ajustar con formato de salida
├── Plantilla-SPEC.md                           ← verificar que cubre REQ completo
├── REQ-ejemplo-validacion-email.md             ← REQ de prueba generado por el agente

scripts/
└── test_analizador.py    ← script de prueba del flujo completo
```

### Formato de salida del agente (REQ)

Cada página generada debe seguir esta estructura:

```markdown
tipo:: requerimiento
estado:: borrador
capa:: proyecto
proyecto:: [[README-mi-proyecto]]
clasificacion:: funcional | no-funcional | restriccion

- # REQ — [Nombre corto]
  - ## Descripción
    - [Qué debe hacer el sistema]
  - ## Criterios de aceptación
    - [ ] [Condición verificable 1]
    - [ ] [Condición verificable 2]
  - ## Contexto
    - Extraído de: [fuente del texto original]
```

### Pasos de implementación

1. **Definir el formato de entrada** del analizador:
   - Texto libre del usuario vía prompt
   - Contexto del proyecto (nombre, dominio, páginas relacionadas)

2. **Actualizar `SystemPrompt-Analizador-Requerimientos.md`** con:
   - Instrucciones explícitas para clasificar (funcional / no-funcional / restricción)
   - El template exacto de la página REQ que debe generar
   - Instrucción de usar `create_page` del MCP para escribir al vault

3. **Testear con un caso simple**: proveer el texto "Necesito que la app valide que el email tiene formato correcto antes de guardar el usuario"
   - Expected: agente crea `REQ-validacion-formato-email.md` con al menos 2 criterios de aceptación
   - Expected: página tiene todas las propiedades requeridas

4. **Testear clasificación múltiple**: texto con un REQ funcional y uno no-funcional en el mismo párrafo — verificar que el agente genera dos páginas separadas

5. Documentar el flujo en `pages/README-Metodologia.md`

### Criterio de aceptación

- [ ] El agente genera páginas REQ válidas (pasan `validate_properties.py`)
- [ ] Las páginas creadas tienen vínculos correctos al proyecto (`proyecto::`)
- [ ] El agente clasifica correctamente funcional vs. no-funcional
- [ ] Los criterios de aceptación son verificables (no ambiguos)

---

## Proyecto E — Fase 8: Integración Multi-Agente

### Descripción funcional

Testear el flujo completo de extremo a extremo: desde que el usuario describe una funcionalidad hasta que el código está mergeado y el grafo actualizado. Este proyecto no agrega nuevas capacidades — valida que todo lo construido funciona en conjunto y mide los costos reales.

### Prerequisito

Fases 4, 6 y 7 deben estar completadas.

### Flujo a testear

```
Usuario describe funcionalidad
       ↓
analizador-requerimientos → crea REQ en grafo
       ↓
validador-negocio → verifica consistencia semántica
       ↓
desarrollador → genera código referenciando la SPEC
       ↓
tester → genera tests basados en criterios de aceptación
       ↓
validador-grafo → verifica integridad pre-merge (CI)
       ↓
merge a main
       ↓
documentador → actualiza grafo post-merge
```

### Archivos a crear

```
pages/
└── DOC-integracion-multiagente-resultados.md  ← resultados del test, costos reales

scripts/
└── test_flujo_completo.py   ← script de orquestación del test e2e
```

### Pasos de implementación

1. **Elegir un caso de uso real pero pequeño** — no trivial, no enorme. Ejemplo: "Función que valide y normalice un número de teléfono argentino".

2. **Ejecutar el flujo completo a mano** la primera vez, registrando en detalle:
   - Qué prompt exacto se le da a cada agente
   - Qué devuelve cada agente
   - Cuántos tokens consume (input + output + cache hit)
   - Qué artefactos quedan en el grafo

3. **Verificar prompt caching activo** en cada agente (buscar `cache_read_input_tokens` en las respuestas de la API)

4. **Medir costos reales** y comparar con `pages/Estimacion-Tokens-Costos.md`

5. **Ejecutar `validate_properties.py`** sobre todos los artefactos generados — deben pasar sin errores

6. **Documentar en `DOC-integracion-multiagente-resultados.md`**:
   - Flujo real ejecutado
   - Costos medidos vs. estimados
   - Ajustes de umbrales si es necesario
   - Lecciones aprendidas

7. Ajustar `pages/Estimacion-Tokens-Costos.md` con los datos reales

### Criterio de aceptación

- [ ] El flujo completo se ejecuta sin intervención manual (excepto el input inicial)
- [ ] Los artefactos generados pasan todas las validaciones del pipeline
- [ ] Los costos reales están documentados y son comparables a la estimación
- [ ] El grafo queda en estado consistente después del merge

---

## Proyecto F — Fase 9: Refinamiento y Release v2.0

### Descripción funcional

Con las fases 4–8 operativas, este proyecto cierra el ciclo: actualiza toda la documentación del grafo para reflejar el estado real del sistema, verifica integridad, genera release notes y publica el núcleo v2.0.

### Pasos de implementación

1. **Ejecutar los tres validadores** sobre el vault completo:
   ```bash
   python scripts/validate_properties.py pages/
   python scripts/validate_links.py pages/
   python scripts/validate_block_refs.py pages/
   ```
   Corregir cualquier error antes de continuar.

2. **Actualizar `pages/README-Metodologia.md`** con:
   - Estado final de todas las fases
   - Notas de evaluación actualizadas (comparar con `pages/Evaluacion-Critica.md`)

3. **Actualizar `pages/Evaluacion-Critica.md`** con nueva evaluación post-Fase 8:
   - MCP (5 → esperado 8 con el file server)
   - Metodología SDD (8 → esperado 9 con el flujo operativo)
   - Mantenimiento de especificación (6 → esperado 8 con el documentador activo)

4. **Generar release notes** usando la plantilla `RN` de `pages/Plantillas-Logseq.md`:
   - Crear `pages/RN-v2.0.0.md`
   - Documentar cada fase completada con su impacto funcional

5. **Disparar release v2.0.0** desde GitHub Actions:
   ```bash
   # manualmente desde GitHub Actions → Release Nucleo → Run workflow → v2.0.0
   ```

6. **Verificar el zip generado** con un bootstrap en un directorio limpio:
   ```bash
   ./bootstrap.sh test-v2 /tmp/proyectos
   ```

### Criterio de aceptación

- [ ] Los tres validadores pasan con 0 errores en el vault completo
- [ ] `pages/Evaluacion-Critica.md` tiene evaluación actualizada post-Fase 8
- [ ] Release `v2.0.0` publicado en GitHub Releases
- [ ] Bootstrap `v2.0.0` verificado en directorio limpio

---

## Referencia rápida — archivos clave por proyecto

| Proyecto | Archivos principales |
|----------|---------------------|
| A — MCP File Server | `scripts/mcp_file_server.py`, `.mcp.json` |
| B — Fase 4 Orquestador | `pages/Protocolo-Orquestador.md`, `pages/SystemPrompt-Orquestador.md` |
| C — Fase 6 Validador | `scripts/validate_block_refs.py`, `.github/workflows/validate.yml` |
| D — Fase 7 Analizador | `pages/SystemPrompt-Analizador-Requerimientos.md` |
| E — Fase 8 Integración | `scripts/test_flujo_completo.py`, `pages/DOC-integracion-multiagente-resultados.md` |
| F — Fase 9 Release | `pages/RN-v2.0.0.md`, `pages/Evaluacion-Critica.md` |

## Ver también

- `pages/Backlog-Fases.md` — vista de tareas por fase con estado actual
- `pages/Alternativas-Mejora.md` — análisis del MCP File Server (Opción D)
- `pages/Evaluacion-Critica.md` — línea base de evaluación antes de estas fases
- `pages/Estimacion-Tokens-Costos.md` — referencia de costos para la Fase 8
- `README_FIRST.md` — guía de inicialización de vault nuevo (independiente de este doc)
