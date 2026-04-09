tipo:: decision-log
estado:: activo
version:: 1.0
capa:: proyecto
id:: DEC-001

- # Comparativa: SDD-Agentes vs GitHub Spec Kit
  - **Decisión ID**: DEC-001
  - **Fecha**: 2026-04-09
  - **Estado**: aprobado
- ## Contexto
  - Durante el diseño de la metodología, se evaluó si adoptar GitHub Spec Kit como base para la gestión de especificaciones, o construir un sistema propio integrado con Logseq.
- ## Tabla Comparativa
  - | Criterio | SDD-Agentes (Logseq) | GitHub Spec Kit |
    |----------|---------------------|-----------------|
    | **Almacenamiento** | Grafo Logseq (local, privado) | GitHub (repositorio) |
    | **Formato de specs** | Markdown con propiedades Logseq | Markdown estándar |
    | **Vínculos entre specs** | `[[links]]` bidireccionales | Links unidireccionales |
    | **Validación automática** | Agente validador-grafo + CI | GitHub Actions básico |
    | **Búsqueda** | Datalog queries sobre el grafo | GitHub search |
    | **Privacidad** | 100% local | Depende de visibilidad del repo |
    | **Integración con agentes IA** | MCP nativo | Via API de GitHub |
    | **Curva de aprendizaje** | Alta (Logseq + EDN + MCP) | Media (solo GitHub) |
    | **Costo** | Solo tokens de API | Gratis (open source) |
    | **Mantenimiento** | Propio | Comunidad GitHub |
    | **Templates** | [[Plantillas-Logseq]] | Templates de GitHub |
- ## Ventajas de SDD-Agentes
  - El grafo bidireccional de Logseq permite trazabilidad que Spec Kit no tiene nativamente.
  - La integración MCP permite a los agentes leer y escribir specs directamente, sin pasar por la API de GitHub.
  - El sistema es 100% local — no requiere conectividad ni depende de la disponibilidad de GitHub.
  - Las queries Datalog son más expresivas que la búsqueda de GitHub para análisis de impacto.
- ## Desventajas de SDD-Agentes
  - Mayor complejidad inicial de configuración (Logseq + MCP + agentes).
  - Depende de que Logseq esté corriendo para que los agentes funcionen.
  - El grafo local no es colaborativo sin sincronización adicional.
  - Spec Kit tiene ecosistema de herramientas ya integrado con GitHub (PRs, Issues).
- ## Decisión
  - **Se adopta SDD-Agentes con Logseq** como sistema de gestión de specs.
  - **Razón principal**: La trazabilidad bidireccional y la integración nativa con agentes IA via MCP supera las ventajas de Spec Kit para el caso de uso actual (desarrollo individual con asistencia de IA).
  - **Revisión**: Evaluar migración parcial a Spec Kit si el proyecto escala a un equipo de más de 3 personas.
- ## Referencias
  - [[MCP-Logseq-Configuracion]] — Configuración del MCP que habilita esta decisión
  - [[Manifiesto-SDD-Agentes]] — DD-004 registra esta decisión
  - [[README-Metodologia]] — Índice principal
