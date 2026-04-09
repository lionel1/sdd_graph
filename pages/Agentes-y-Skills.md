tipo:: configuración-agentes
estado:: activo
version:: 1.0
capa:: nucleo

- # Agentes y Skills
- ## Resumen de Roles
  - | Agente | Dominio | Trigger Principal |
    |--------|---------|-------------------|
    | orquestador | Coordinación general | Toda interacción del usuario |
    | validador-grafo | Integridad del grafo Logseq | Pre-merge, post-edición |
    | validador-negocio | Consistencia de specs | Nueva spec o cambio de req |
    | analizador-requerimientos | Extracción de reqs | Documento de entrada nuevo |
    | desarrollador | Generación de código | Spec aprobada |
    | documentador | Generación de docs | Merge a main exitoso |
- ## Agente: Orquestador
  - **Rol**: Punto de entrada único. Interpreta la intención del usuario y despacha al agente correcto.
  - **Responsabilidades**:
    - Parsear la solicitud del usuario
    - Determinar qué agente(s) activar según el [[Protocolo-Orquestador]]
    - Agregar resultados y presentarlos al usuario
    - Escalar decisiones de alto impacto al humano
  - **Triggers**:
    - Cualquier mensaje del usuario
    - Resultado de otro agente que requiere decisión
  - **Skills**: `despacho`, `agregación`, `escalamiento` — ver [[Skills-de-Agentes]]
- ## Agente: Validador-Grafo
  - **Rol**: Verifica la integridad estructural del grafo Logseq.
  - **Responsabilidades**:
    - Detectar vínculos `[[...]]` rotos
    - Verificar que todas las propiedades requeridas existan (`tipo::`, `estado::`, `version::`)
    - Confirmar que los `((block-uuid))` referenciados existan
    - Generar reporte de errores para el orquestador
  - **Triggers**:
    - Antes de cualquier merge (via [[Pipeline-Git]])
    - Al crear o modificar páginas del grafo
  - **Skills**: `validación-estructura`, `reporte-errores`, `lectura-MCP`, `query-Datalog` — ver [[Skills-de-Agentes]]
- ## Agente: Validador-Negocio
  - **Rol**: Verifica la consistencia semántica de las especificaciones.
  - **Responsabilidades**:
    - Detectar contradicciones entre specs
    - Verificar que los requerimientos sean implementables
    - Validar que las restricciones del [[Manifiesto-SDD-Agentes]] se cumplan
  - **Triggers**:
    - Al crear una nueva spec
    - Al modificar un requerimiento existente
  - **Skills**: `validación-specs`, `análisis-semántico`, `query-Datalog` — ver [[Skills-de-Agentes]]
- ## Agente: Analizador-Requerimientos
  - **Rol**: Extrae y estructura requerimientos desde documentos en lenguaje natural.
  - **Responsabilidades**:
    - Parsear documentos de entrada (emails, reuniones, prompts)
    - Generar bloques de requerimiento en formato Logseq
    - Clasificar reqs por tipo (funcional, no-funcional, restricción)
    - Asignar IDs únicos y propiedades
  - **Triggers**:
    - Documento de entrada nuevo proporcionado por el usuario
    - Solicitud explícita de análisis
  - **Skills**: `extracción-reqs`, `clasificación`, `formato-Logseq`, `escritura-MCP` — ver [[Skills-de-Agentes]]
- ## Agente: Desarrollador
  - **Rol**: Genera código basado en specs aprobadas del grafo.
  - **Responsabilidades**:
    - Leer la spec desde Logseq via MCP
    - Generar código que implementa la spec
    - Crear PR siguiendo el template de [[Estructura-Proyecto]]
    - Referenciar los bloques de spec en el PR
  - **Triggers**:
    - Spec con `estado:: aprobado` en el grafo
    - Solicitud explícita del orquestador
  - **Skills**: `generación-código`, `creación-PR`, `lectura-MCP` — ver [[Skills-de-Agentes]]
- ## Agente: Documentador
  - **Rol**: Genera y actualiza documentación tras cambios exitosos.
  - **Responsabilidades**:
    - Detectar cambios en código o specs
    - Actualizar páginas del grafo afectadas
    - Mantener el [[README-Metodologia]] actualizado
    - Usar las [[Plantillas-Logseq]] correctas
  - **Triggers**:
    - Merge exitoso a `main`
    - Cambio de `estado::` en una spec
  - **Skills**: `generación-docs`, `actualización-grafo`, `escritura-MCP` — ver [[Skills-de-Agentes]]
- ## Referencias
  - [[Skills-de-Agentes]] — Catálogo completo con anatomía, inputs y outputs de cada skill
  - [[Agregar-Agente-y-Skills]] — Guía y checklist para registrar un agente nuevo
  - [[Protocolo-Orquestador]] — Lógica de despacho entre agentes
  - [[MCP-Logseq-Configuracion]] — Herramienta principal de los agentes
  - [[README-Metodologia]] — Índice principal
