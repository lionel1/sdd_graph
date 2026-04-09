tipo:: referencia
estado:: activo
version:: 1.0
capa:: nucleo

- # La estructura de etiquetas
	- El MCP necesita ambas dimensiones de etiquetas: de contenido y de estado.
	- Solo con etiquetas de contenido puede encontrar nodos relevantes, pero no sabe cuáles son confiables o vigentes.
	- Solo con etiquetas de estado puede filtrar, pero no puede navegar semánticamente.
	- ## Sistema de etiquetas mínimo sugerido
		- ### Para tareas
			- `#tarea` — identifica el nodo como unidad de trabajo
			- `#activa` — tarea en curso
			- `#completada` — tarea cerrada
			- `#bloqueada` — tarea detenida por dependencia externa
		- ### Para conocimiento
			- `#principio` — regla o guía de comportamiento
			- `#decisión` — decisión tomada y su contexto
			- `#aprendizaje` — insight derivado de la experiencia
			- `#referencia` — fuente externa o concepto importado
		- ### Para el cruce entre ambas capas
			- `#evergreen` — conocimiento consolidado que no caduca
			- `#contextual` — conocimiento válido solo en un proyecto específico
			- `#deprecated` — conocimiento vinculado pero ya no vigente
	- ## La query tipo que esto habilita en el MCP
		- "Traé todos los principios `#evergreen` vinculados a tareas `#activa` del proyecto X"
		- Eso es exactamente el cruce entre memoria de largo plazo y contexto operativo que hace útil tener todo en el mismo grafo.
	- ## Ver también
		- [[La-definicion-de-tareas]] — Anatomía de tareas y uso de etiquetas
		- [[Plantilla-de-tareas]] — Plantilla con campos de estado
		- [[Grafo-como-fuente-de-verdad-utilizando-Logseq]] — Contexto general del enfoque
		- [[MCP-Logseq-Configuracion]] — Cómo el MCP ejecuta estas queries
