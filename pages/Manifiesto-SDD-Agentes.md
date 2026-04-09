tipo:: manifiesto
estado:: activo
version:: 1.0
capa:: nucleo

- # Manifiesto SDD con Agentes Inteligentes
- ## Principios
  - **P-001 — Spec-First**: Toda funcionalidad debe tener una especificación aprobada antes de que se escriba código.
  - **P-002 — Validación Automática**: El grafo de Logseq es la fuente de verdad; los agentes validan contra él.
  - **P-003 — Trazabilidad Total**: Cada decisión, requerimiento y tarea debe ser trazable en el grafo.
  - **P-004 — Agentes Especializados**: Cada agente tiene un único dominio de responsabilidad y no opera fuera de él.
  - **P-005 — Revisión Humana en Puntos Críticos**: El orquestador eleva decisiones de alto impacto al humano antes de ejecutar.
  - **P-006 — Documentación como Código**: La documentación se genera, versiona y valida igual que el código.
  - **P-007 — Prompt Caching**: Las instrucciones del sistema de cada agente se cachean para reducir costos.
  - **P-008 — Iteración Incremental**: Las fases del backlog son independientes y entregables por separado.
- ## Restricciones
  - **R-001**: Ningún agente puede modificar una spec aprobada sin aprobación explícita del orquestador.
  - **R-002**: El validador-grafo debe ejecutarse antes de cualquier merge a `main`.
  - **R-003**: Todo PR debe referenciar al menos un bloque de spec del grafo (`((uuid))`).
  - **R-004**: Los agentes no tienen acceso de escritura directa al repositorio Git — solo proponen cambios.
  - **R-005**: El token de API de Logseq no puede estar hardcodeado en ningún archivo de código.
  - **R-006**: El costo por sesión no puede superar el umbral definido en [[Estimacion-Tokens-Costos]].
  - **R-007**: Las plantillas definidas en [[Plantillas-Logseq]] son las únicas plantillas válidas del sistema.
- ## Decisiones de Diseño
  - **DD-001 — Logseq como grafo central**: Se eligió Logseq por su modelo de datos en grafo, soporte de propiedades y MCP disponible. Ver [[MCP-Logseq-Configuracion]].
  - **DD-002 — Orquestador como único punto de entrada**: Simplifica el flujo y centraliza la lógica de despacho. Ver [[Protocolo-Orquestador]].
  - **DD-003 — GitHub Actions para CI/CD**: Automatiza la validación del pipeline sin herramientas externas. Ver [[Pipeline-Git]].
  - **DD-004 — No usar GitHub Spec Kit**: Se evaluó y descartó. Ver [[Comparativa-SpecKit]] (DEC-001).
  - **DD-005 — Prompt Caching en System Prompts**: Reduce costos de tokens en sesiones largas. Ver [[Estimacion-Tokens-Costos]].
  - **DD-006 — Plantillas tipadas en Logseq**: Estandariza la creación de páginas y reduce errores de formato. Ver [[Plantillas-Logseq]].
- ## Referencias
  - [[README-Metodologia]] — Índice principal
  - [[Agentes-y-Skills]] — Implementación de los principios de agentes especializados
