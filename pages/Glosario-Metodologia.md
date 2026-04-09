tipo:: glosario
estado:: activo
version:: 1.0
capa:: nucleo

- # Glosario de la Metodología
- ## Términos Clave
  - ### SDD — Specification-Driven Development
    - Metodología de desarrollo donde toda funcionalidad debe tener una especificación aprobada antes de que se escriba código. La spec es la fuente de verdad, no el código.
    - Ver: [[Manifiesto-SDD-Agentes]]
  - ### MCP — Model Context Protocol
    - Protocolo estándar de Anthropic que permite a modelos de lenguaje (como Claude) conectarse a herramientas y fuentes de datos externas. En esta metodología, se usa para conectar los agentes al grafo de Logseq.
    - Ver: [[MCP-Logseq-Configuracion]]
  - ### Orquestador
    - Agente principal que actúa como punto de entrada único para todas las interacciones del usuario. Analiza la solicitud, despacha al agente correcto y agrega los resultados. No tiene dominio técnico propio — solo coordina.
    - Ver: [[Protocolo-Orquestador]], [[Agentes-y-Skills]]
  - ### Validador-Grafo
    - Agente especializado en verificar la integridad estructural del grafo de Logseq: vínculos rotos, propiedades faltantes, block-refs inválidos. Se ejecuta antes de cualquier merge.
    - Ver: [[Agentes-y-Skills]], [[Pipeline-Git]]
  - ### Spec-Anchored
    - Característica de un PR o tarea que tiene una referencia explícita a un bloque de especificación en el grafo de Logseq. Todo cambio de código debe ser spec-anchored. Un PR sin spec-anchor no puede mergearse.
    - Ver: [[Pipeline-Git]], [[Estructura-Proyecto]]
  - ### Decision-Log
    - Registro formal de una decisión de arquitectura o diseño. Sigue la [[Plantillas-Logseq]] — Plantilla DEC y tiene un ID único (DEC-XXX).
    - Ver: [[Comparativa-SpecKit]] (DEC-001), [[Plantillas-Logseq]]
  - ### Prompt Caching
    - Técnica de la API de Anthropic que cachea partes estables del prompt (como el system prompt) para reducir el costo de tokens en sesiones con múltiples llamadas. Los agentes de esta metodología usan prompt caching en sus system prompts.
    - Ver: [[Estimacion-Tokens-Costos]], [[Manifiesto-SDD-Agentes]] P-007
  - ### Grafo
    - El vault de Logseq como estructura de datos. A diferencia de un árbol de archivos, el grafo permite relaciones bidireccionales entre páginas via enlaces `[[ ]]`, queries Datalog, y propiedades estructuradas. Es la base de datos del sistema SDD-Agentes.
    - Ver: [[MCP-Logseq-Configuracion]], [[README-Metodologia]]
  - ### Block-Ref
    - Referencia a un bloque específico dentro de una página de Logseq, usando la sintaxis `((uuid))`. Permite citar una parte específica de una spec en un PR o en otra página, creando trazabilidad a nivel de bloque.
    - Ver: [[Pipeline-Git]], [[Estructura-Proyecto]]
  - ### Fase
    - Unidad de trabajo del [[Backlog-Fases]]. Cada fase agrupa tareas relacionadas, es independiente y entregable por separado. Las fases se numeran F-01 a F-09.
    - Ver: [[Backlog-Fases]], [[Manifiesto-SDD-Agentes]] P-008
- ## Referencias
  - [[Manifiesto-SDD-Agentes]] — Define los principios que usan estos términos
  - [[README-Metodologia]] — Índice principal
