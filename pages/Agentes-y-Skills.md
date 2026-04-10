tipo:: configuración-agentes
estado:: activo
version:: 1.0
capa:: nucleo

- # Agentes y Skills
- ## Resumen de Roles
  - | Agente | Dominio | Trigger Principal |
    |--------|---------|-------------------|
    | orquestador | Coordinación general | Toda interacción del usuario |
    | consultor-metodologia | Consulta viva del vault y la metodología | Pregunta sobre el sistema o convención |
    | validador-grafo | Integridad del grafo Logseq | Pre-merge, post-edición |
    | validador-negocio | Consistencia de specs | Nueva spec o cambio de req |
    | analizador-requerimientos | Extracción de reqs | Documento de entrada nuevo |
    | desarrollador | Generación de código | Spec aprobada |
    | documentador | Generación de docs | Merge a main exitoso |
- ## Agente: Consultor-Metodologia
  - **Rol**: Fuente de consulta viva sobre la metodología SDD y el estado del vault. Responde preguntas sobre cómo funciona el sistema leyendo directamente el grafo.
  - **Responsabilidades**:
    - Resolver preguntas sobre la metodología (principios, flujos, restricciones)
    - Indicar qué plantilla, etiqueta o convención usar ante una situación concreta
    - Listar agentes, skills y plantillas disponibles en el estado actual del vault
    - Verificar que una página o propiedad cumple las convenciones del sistema
  - **Por qué es crítico**:
    - Los demás agentes conocen la metodología por su system prompt (estático). Este agente la consulta en tiempo real — si el vault evoluciona, la respuesta es siempre la actual.
    - Desacopla al orquestador de tener que conocer la metodología completa.
  - **Triggers**:
    - Pregunta del usuario sobre cómo usar el sistema
    - Orquestador necesita confirmar una convención antes de despachar
    - Cualquier agente necesita verificar una regla del [[Manifiesto-SDD-Agentes]]
  - **Skills**: `consulta-vault`, `lectura-MCP`, `query-Datalog` — ver [[Skills-de-Agentes]]
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
