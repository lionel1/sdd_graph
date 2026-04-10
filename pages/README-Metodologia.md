filters:: {"comparativa-speckit" true}
tipo:: índice
estado:: activo
version:: 1.0
capa:: proyecto

- # Metodología SDD con Agentes Inteligentes
	- Sistema de desarrollo orientado a especificaciones, potenciado por agentes de IA especializados que automatizan la validación, documentación y flujo de trabajo.
	- Utiliza Grafo de Logseq conectado al LLM por MCP como fuente de datos y utiliza características del modelo mismo pudiendo interrogar el grafo, recorrer vínculos, buscar por etiquetas, traer nodos relacionados y escribir de vuelta.
- ## Índice de Páginas
	- ### Motivación
		- [[Grafo-como-fuente-de-verdad-utilizando-Logseq]] — Por qué Logseq como fuente de verdad y el rol del MCP
		- [[Logseq-Calidad-del-Contexto-Humano]] — Fundamento teórico desde psicología cognitiva, aprendizaje y lingüística computacional
		- [[Descripcion Logseq Grafos]]  — Descripción del sistema de persistencia
	- ### Fundamentos
		- [[Manifiesto-SDD-Agentes]] — Principios, restricciones y decisiones de diseño
		- [[Glosario-Metodologia]] — Términos clave del sistema
	- ### Arquitectura y Agentes
		- [[Agentes-y-Skills]] — Roles, responsabilidades y triggers de cada agente
		- [[Skills-de-Agentes]] — Catálogo de skills: anatomía, inputs, outputs y composición en flujos
		- [[Agregar-Agente-y-Skills]] — Guía y checklist para registrar un agente nuevo con sus skills
		- [[Protocolo-Orquestador]] — Lógica de despacho y reglas de prioridad
	- ### Estructura Técnica
		- [[Estructura-Proyecto]] — Carpetas, ramas Git y PR template
		- [[Pipeline-Git]] — Flujo de PR, GitHub Actions y condiciones de merge
		- [[MCP-Logseq-Configuracion]] — Configuración de MCPs y comparativa
	- ### Decisiones y Referencias
		- [[Comparativa-SpecKit]] — Comparativa con GitHub Spec Kit (DEC-001)
		- [[Estimacion-Tokens-Costos]] — Proyección de costos por escenario
		- [[Plantillas-Logseq]] — Plantillas estándar del sistema
		- [[Tareas]] — Tareas activas del proyecto con anatomía completa (tipo, estado, conocimiento)
		- [[Backlog-Fases]] — Fases 1–9 con todas las subtareas
	- ### Estructura del Grafo
		- [[La-definicion-de-tareas]] — Anatomía de un nodo de tarea y sistema de etiquetas
		- [[Plantilla-de-tareas]] — Plantilla estándar para nodos de tarea
		- [[La-estructura-etiquetas]] — Sistema completo de etiquetas para tareas y conocimiento
- ## Estado del Proyecto
	- estado:: activo
	- Fase actual: [[Backlog-Fases]]
- ## Vínculos Rápidos
	- Configuración: [[MCP-Logseq-Configuracion]]
	- Decisiones: [[Comparativa-SpecKit]]
	- Tareas: [[Backlog-Fases]]
-