tipo:: referencia
estado:: activo
version:: 1.0
capa:: nucleo

- # La definición de tareas
	- Cada tarea vive en un nodo con una anatomía consistente.
	- ## Anatomía de un nodo de tarea
		- ```
		  tipo:: tarea
		  proyecto:: [[nombre-proyecto]]
		  estado:: activa | pausada | completada
		  conocimiento-relacionado:: [[nodo1]] [[nodo2]]
		  aprendizaje::
		  ```
		- El campo `conocimiento-relacionado` es el vínculo explícito hacia la memoria de largo plazo.
		- El agente puede recorrerlo en ambas direcciones: desde la tarea hacia el conocimiento, y desde cualquier nodo de conocimiento hacia todas las tareas donde fue relevante.
	- ## Etiquetas: de contenido vs. de estado
		- Las etiquetas que realmente importan para el MCP son las que permiten queries útiles, no las que describen contenido.
		- **Etiquetas de contenido** — `#gestión-riesgo`, `#arquitectura`, `#decisión` — describen de qué trata el nodo.
		- **Etiquetas de estado y rol** — `#activo`, `#consolidado`, `#pendiente-revisión`, `#semilla` — describen en qué estado está el conocimiento.
		- El MCP necesita ambas para funcionar con precisión.
	- ## Ver también
		- [[Plantilla-de-tareas]] — Plantilla lista para usar
		- [[La-estructura-etiquetas]] — Sistema completo de etiquetas
		- [[Grafo-como-fuente-de-verdad-utilizando-Logseq]] — Contexto general del enfoque
		- [[Plantillas-Logseq]] — Otras plantillas del sistema
