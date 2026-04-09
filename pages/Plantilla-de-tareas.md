tipo:: plantilla
estado:: activo
version:: 1.0
capa:: nucleo

- # Plantilla de tareas
	- Plantilla estándar para la creación de nodos de tarea en el grafo.
	- ## Plantilla
		- ```
		  tipo:: tarea
		  proyecto:: [[nombre-proyecto]]
		  estado:: activa | pausada | completada
		  conocimiento-relacionado:: [[nodo1]] [[nodo2]]
		  aprendizaje::
		  ```
	- ## Instrucciones de uso
		- `tipo:: tarea` — identificador fijo, permite queries MCP del tipo "traé todas las tareas".
		- `proyecto::` — vincula la tarea al nodo del proyecto activo.
		- `estado::` — eliminar los valores que no aplican, dejar solo el estado actual.
		- `conocimiento-relacionado::` — vínculos explícitos a nodos de conocimiento relevantes. Es el campo más importante para el traversal del agente.
		- `aprendizaje::` — completar al cerrar la tarea con lo que se aprendió. Alimenta la memoria de largo plazo.
	- ## Ver también
		- [[La-definicion-de-tareas]] — Explicación completa de la anatomía de tareas
		- [[La-estructura-etiquetas]] — Etiquetas que complementan esta plantilla
		- [[Plantillas-Logseq]] — Otras plantillas del sistema
