tipo:: plantilla
estado:: activo
version:: 1.0
capa:: nucleo

- # Agregar Agente y Skills
	- Guía y plantillas para registrar un nuevo agente en el sistema. Seguir este proceso garantiza que el agente quede correctamente integrado en el grafo, visible al orquestador y con sus skills trazables.
	- Un **agente** es una unidad de responsabilidad con dominio único. Un **skill** es la capacidad mínima que ese agente puede ejecutar. Ambos deben declararse explícitamente — el orquestador razona sobre lo que está declarado, no sobre lo que existe implícitamente.
	- ## Paso 1 — Definir el agente en `Agentes-y-Skills`
		- Agregar una sección nueva al final de [[Agentes-y-Skills]], usando esta plantilla:
		- ```
		  ## Agente: <nombre-agente>
		    - **Rol**: Una línea que describe qué problema resuelve este agente y desde qué ángulo.
		    - **Responsabilidades**:
		      - Responsabilidad concreta 1
		      - Responsabilidad concreta 2
		    - **Triggers**:
		      - Condición que activa este agente (evento, estado en el grafo, solicitud explícita)
		    - **Skills**: `skill-1`, `skill-2` — ver [[Skills-de-Agentes]]
		  ```
		- ### Reglas para completar la plantilla
			- **Rol** — debe poder leerse como "Este agente existe para X". Si no se puede formular así, el dominio no está bien delimitado.
			- **Responsabilidades** — acciones concretas, no intenciones. "Detectar vínculos rotos" es una responsabilidad; "asegurar calidad" no lo es.
			- **Triggers** — deben ser condiciones observables: un `estado::` en el grafo, un evento del pipeline, una solicitud del orquestador. Evitar triggers ambiguos como "cuando sea necesario".
			- **Skills** — solo listar los skills que se definirán en el Paso 2. No inventar skills no definidos.
		- ### Actualizar la tabla de resumen
			- Agregar una fila en la tabla "Resumen de Roles" al inicio de [[Agentes-y-Skills]]:
			- ```
			  | <nombre-agente> | <dominio-en-dos-palabras> | <trigger-principal> |
			  ```
	- ## Paso 2 — Definir los skills en `Skills-de-Agentes`
		- Para cada skill del agente, agregar un bloque en la sección del tipo que corresponde dentro de [[Skills-de-Agentes]]. Usar esta plantilla:
		- ```
		  **`<nombre-skill>`**
		    - agente:: <nombre-agente>
		    - input:: qué recibe exactamente (formato o tipo de dato)
		    - output:: qué produce exactamente (artefacto, reporte, bloque Logseq)
		    - depende-de:: `skill-previo` (omitir si no hay dependencia)
		    - descripción:: Una oración que explique qué hace y por qué existe separado de otros skills.
		  ```
		- ### Tipos de skill disponibles
			- | Tipo | Cuándo usarlo |
			  |---|---|
			  | `coordinación` | El skill dirige flujo o toma decisiones de despacho |
			  | `lectura-MCP` | El skill recupera datos del grafo vía MCP |
			  | `escritura-MCP` | El skill crea o modifica nodos en el grafo vía MCP |
			  | `validación` | El skill verifica integridad o consistencia |
			  | `análisis` | El skill procesa input no estructurado para extraer estructura |
			  | `generación` | El skill produce un artefacto nuevo (código, docs, bloques) |
		- ### Si el skill reutiliza uno existente
			- Verificar primero si el comportamiento ya existe en el catálogo de [[Skills-de-Agentes]].
			- Si es idéntico, agregar el nuevo agente al campo `agentes::` del skill existente en lugar de duplicarlo.
			- Si hay diferencia en input/output, crear un skill nuevo con nombre distinto.
	- ## Paso 3 — Registrar las operaciones MCP en `MCP-Logseq-Configuracion`
		- Si el agente usa el MCP, agregar una fila en la tabla "Impacto por Agente" de [[MCP-Logseq-Configuracion]]:
		- ```
		  | <nombre-agente> | `operacion1`, `operacion2` |
		  ```
		- Las operaciones disponibles están documentadas en la sección "Métodos de API Disponibles" de [[MCP-Logseq-Configuracion]].
		- Si el agente no usa el MCP directamente, omitir este paso.
	- ## Paso 4 — Evaluar si el `Protocolo-Orquestador` necesita actualizarse
		- El árbol de decisión del [[Protocolo-Orquestador]] debe actualizarse solo si el nuevo agente introduce un **nuevo tipo de trigger** que el orquestador no sabe resolver hoy.
		- Preguntas para decidir:
			- ¿El trigger del nuevo agente ya está cubierto por alguna rama del árbol? → No actualizar.
			- ¿El agente puede ser invocado desde una rama existente como sub-despacho? → No actualizar el árbol, sí agregar una nota en la rama correspondiente.
			- ¿El trigger es genuinamente nuevo y requiere una rama propia? → Agregar la rama al árbol de decisión.
	- ## Paso 5 — Actualizar el flujo de composición en `Skills-de-Agentes`
		- Si los skills del nuevo agente se insertan en un flujo existente (como el flujo spec→código→PR), actualizar el diagrama "Composición de skills en un flujo típico" de [[Skills-de-Agentes]] para mostrar dónde se integran.
		- Si los skills forman un flujo propio, agregar un nuevo diagrama en esa misma sección.
	- ## Checklist de registro completo
		- ```
		  [ ] Agente definido en Agentes-y-Skills (sección + fila en tabla resumen)
		  [ ] Skills definidos en Skills-de-Agentes (uno por skill, en la sección de tipo correcta)
		  [ ] Skills reutilizados: campo agentes:: actualizado en Skills-de-Agentes
		  [ ] Operaciones MCP registradas en MCP-Logseq-Configuracion (si aplica)
		  [ ] Árbol de despacho evaluado en Protocolo-Orquestador (actualizar solo si hay rama nueva)
		  [ ] Flujo de composición actualizado en Skills-de-Agentes (si el agente se inserta en flujo existente)
		  ```
	- ## Relaciones que se crean al registrar un agente
		- ```
		  [nuevo-agente]
		      │
		      ├─ declarado en ──────────→ [[Agentes-y-Skills]]
		      │                                │
		      │                                └─ tabla resumen + sección propia
		      │
		      ├─ skills definidos en ──→ [[Skills-de-Agentes]]
		      │                                │
		      │                                └─ sección por tipo + flujo de composición
		      │
		      ├─ operaciones MCP en ───→ [[MCP-Logseq-Configuracion]]
		      │                                │
		      │                                └─ tabla "Impacto por Agente"
		      │
		      └─ visible al ────────────→ [[Protocolo-Orquestador]]
		                                       │
		                                       └─ árbol de decisión (si trigger es nuevo)
		  ```
	- ## Ver también
		- [[Agentes-y-Skills]] — Definición actual de todos los agentes
		- [[Skills-de-Agentes]] — Catálogo actual de todos los skills
		- [[Protocolo-Orquestador]] — Lógica de despacho que consume los agentes registrados
		- [[MCP-Logseq-Configuracion]] — Infraestructura compartida entre agentes
		- [[Plantillas-Logseq]] — Plantillas de páginas usadas por los skills de generación
		- [[README-Metodologia]] — Índice principal
