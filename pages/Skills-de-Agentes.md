tipo:: referencia
estado:: activo
version:: 1.0
capa:: nucleo

- # Skills de Agentes
	- Un **skill** es la unidad mínima de capacidad de un agente: una acción nombrada, con input y output definidos, que el agente puede invocar de forma autónoma o en respuesta a un trigger del [[Protocolo-Orquestador]].
	- Los skills no son funciones de código — son capacidades declaradas que describen qué puede hacer cada agente, con qué consume y qué produce. Esta declaración permite al orquestador razonar sobre qué agente invocar y en qué orden.
	- ## Anatomía de un skill
		- Cada skill se puede describir con esta estructura:
		- ```
		  nombre::          identificador único del skill
		  agente::          [[agente propietario]]
		  tipo::            lectura-MCP | escritura-MCP | validación | análisis | generación | coordinación
		  input::           qué recibe (tipo de dato o nodo del grafo)
		  output::          qué produce (artefacto, reporte, bloque Logseq, código)
		  depende-de::      [[skill-previo]] (si aplica)
		  ```
	- ## Catálogo de Skills por Tipo
		- ### Coordinación — orquestador
			- **`despacho`**
				- input:: intención del usuario (texto libre)
				- output:: nombre del agente destino + parámetros de invocación
				- descripción:: analiza la solicitud, aplica el árbol de decisión del [[Protocolo-Orquestador]] y selecciona el agente correcto.
			- **`agregación`**
				- input:: outputs de uno o más agentes
				- output:: respuesta consolidada para el usuario
				- descripción:: reúne resultados de múltiples agentes en una respuesta coherente y sin redundancia.
			- **`escalamiento`**
				- input:: condición de alto impacto detectada por cualquier agente
				- output:: pausa del flujo + notificación al humano con contexto suficiente
				- descripción:: implementa P-005 del [[Manifiesto-SDD-Agentes]]. Se activa ante operaciones irreversibles o conflictos entre specs aprobadas.
		- ### Consulta — consultor-metodologia
			- **`consulta-vault`**
				- agente:: consultor-metodologia
				- tipo:: lectura-MCP
				- input:: pregunta en lenguaje natural sobre la metodología, una convención, un agente o una plantilla
				- output:: respuesta fundamentada en el contenido actual del vault (páginas leídas vía MCP)
				- depende-de:: `lectura-MCP`, `query-Datalog`
				- descripción:: skill central del consultor. Lee las páginas nucleo relevantes (Manifiesto, Agentes-y-Skills, Plantillas-Logseq, etc.) para responder con el estado actual del sistema — no con el estado al momento de escribir el system prompt. Garantiza que la respuesta sea siempre consistente con el vault real.
		- ### Lectura-MCP — agentes de consulta
			- **`lectura-MCP`**
				- agentes:: consultor-metodologia, validador-grafo, validador-negocio, desarrollador
				- input:: nombre de página o UUID de bloque
				- output:: contenido del nodo con sus propiedades y vínculos
				- depende-de:: [[MCP-Logseq-Configuracion]]
				- descripción:: recupera páginas y bloques del grafo vía `logseq.Editor.getPage` o `getBlock`. Base de casi todo flujo de consulta.
			- **`query-Datalog`**
				- agentes:: consultor-metodologia, validador-grafo, validador-negocio
				- input:: query en sintaxis Datalog (string)
				- output:: conjunto de bloques que satisfacen la query
				- depende-de:: `lectura-MCP`
				- descripción:: ejecuta `logseq.DB.q` para traversal semántico. Permite queries del tipo "todos los nodos `#decisión` vinculados a tareas `#activa`". Ver [[La-estructura-etiquetas]].
		- ### Escritura-MCP — agentes de producción
			- **`escritura-MCP`**
				- agentes:: analizador-requerimientos, documentador
				- input:: título de página + contenido en formato Logseq Markdown
				- output:: página o bloque creado/actualizado en el grafo
				- depende-de:: [[MCP-Logseq-Configuracion]]
				- descripción:: crea páginas vía `createPage` e inserta bloques vía `insertBlock`. Toda escritura pasa por este skill; ningún agente modifica el grafo directamente.
			- **`actualización-grafo`**
				- agente:: documentador
				- input:: lista de páginas afectadas + cambios a aplicar
				- output:: bloques actualizados con nuevo `estado::` o contenido
				- depende-de:: `lectura-MCP`, `escritura-MCP`
				- descripción:: combina lectura y escritura para mantener el grafo sincronizado con el estado real del proyecto.
		- ### Validación — agentes verificadores
			- **`validación-estructura`**
				- agente:: validador-grafo
				- input:: lista de páginas del grafo (vía `getAllPages`)
				- output:: reporte de errores estructurales (vínculos rotos, propiedades faltantes, UUIDs inexistentes)
				- descripción:: verifica las invariantes formales del grafo: que todo `[[vínculo]]` apunte a una página real, que toda página tenga `tipo::`, `estado::` y `version::`, y que todo `((uuid))` referenciado exista.
			- **`reporte-errores`**
				- agente:: validador-grafo
				- input:: lista de errores detectados por `validación-estructura`
				- output:: JSON estructurado compatible con el formato de respuesta del [[Protocolo-Orquestador]]
				- descripción:: formatea errores para que el orquestador pueda decidir si escalar, corregir o bloquear el flujo.
			- **`validación-specs`**
				- agente:: validador-negocio
				- input:: spec nueva o modificada + specs existentes relacionadas
				- output:: resultado de validación (ok | conflicto | ambigüedad) + detalle
				- depende-de:: `lectura-MCP`, `query-Datalog`
				- descripción:: verifica que la nueva spec no contradiga specs aprobadas y que sus requerimientos sean implementables.
			- **`análisis-semántico`**
				- agente:: validador-negocio
				- input:: texto de spec o requerimiento
				- output:: lista de ambigüedades, contradicciones o restricciones del [[Manifiesto-SDD-Agentes]] violadas
				- descripción:: complementa `validación-specs` con razonamiento sobre el significado, no solo la estructura formal.
		- ### Análisis — analizador-requerimientos
			- **`extracción-reqs`**
				- agente:: analizador-requerimientos
				- input:: documento en lenguaje natural (email, minuta, prompt)
				- output:: lista estructurada de requerimientos con tipo (funcional | no-funcional | restricción) y prioridad preliminar
				- descripción:: primer skill del pipeline de análisis. Convierte texto ambiguo en requerimientos discretos y clasificables.
			- **`clasificación`**
				- agente:: analizador-requerimientos
				- input:: lista de reqs extraídos por `extracción-reqs`
				- output:: reqs con tipo, prioridad y ID asignados
				- depende-de:: `extracción-reqs`
				- descripción:: asigna `tipo::`, `prioridad::` e `id::` a cada requerimiento. Prepara los datos para `formato-Logseq`.
		- ### Generación — desarrollador y documentador
			- **`formato-Logseq`**
				- agente:: analizador-requerimientos
				- input:: reqs clasificados por `clasificación`
				- output:: bloques Logseq en formato de plantilla REQ (ver [[Plantillas-Logseq]])
				- depende-de:: `clasificación`
				- descripción:: último skill del pipeline de análisis. Produce los bloques listos para `escritura-MCP`.
			- **`generación-código`**
				- agente:: desarrollador
				- input:: spec con `estado:: aprobado` recuperada vía `lectura-MCP`
				- output:: código fuente que implementa la spec
				- depende-de:: `lectura-MCP`
				- descripción:: implementa P-001 (Spec-First) del [[Manifiesto-SDD-Agentes]]. El desarrollador no genera código sin spec aprobada en el grafo.
			- **`creación-PR`**
				- agente:: desarrollador
				- input:: código generado + referencias a bloques de spec (UUIDs)
				- output:: Pull Request siguiendo el template de [[Estructura-Proyecto]] con referencias `((uuid))` al grafo
				- depende-de:: `generación-código`
				- descripción:: cierra el ciclo spec → código → PR. Garantiza la trazabilidad exigida por P-003.
			- **`generación-docs`**
				- agente:: documentador
				- input:: diff de código o cambio de `estado::` en una spec
				- output:: páginas o bloques Logseq actualizados con la documentación del cambio
				- depende-de:: `lectura-MCP`, `escritura-MCP`
				- descripción:: se activa post-merge. Mantiene el grafo sincronizado con el código real. Usa las plantillas de [[Plantillas-Logseq]].
	- ## Composición de skills en un flujo típico
		- ```
		  FLUJO: spec nueva → validación → código → PR
		  
		  0. consulta-vault         (consultor, si el orquestador necesita confirmar convención)
		  1. extracción-reqs        (analizador)
		  2. clasificación           (analizador)
		  3. formato-Logseq          (analizador)
		  4. escritura-MCP           (analizador → grafo)
		  5. validación-specs        (validador-negocio)
		  6. análisis-semántico      (validador-negocio)
		  7. generación-código       (desarrollador)
		  8. creación-PR             (desarrollador)
		  9. validación-estructura   (validador-grafo, pre-merge)
		  10. generación-docs        (documentador, post-merge)
		  11. actualización-grafo    (documentador)
		  ```
		- Cada paso es orquestado por `despacho`. Si cualquier validación falla, se activa `reporte-errores` o `escalamiento` según la severidad.
	- ## Ver también
		- [[Agentes-y-Skills]] — Definición de cada agente y sus responsabilidades
		- [[Agregar-Agente-y-Skills]] — Guía paso a paso para registrar un agente y sus skills
		- [[Protocolo-Orquestador]] — Cómo el orquestador selecciona y encadena skills
		- [[MCP-Logseq-Configuracion]] — Infraestructura que habilita los skills de lectura/escritura MCP
		- [[La-estructura-etiquetas]] — Las etiquetas que potencian los skills de query-Datalog
		- [[Plantillas-Logseq]] — Las plantillas que usan los skills de generación
		- [[Manifiesto-SDD-Agentes]] — Los principios que los skills implementan
		- [[README-Metodologia]] — Índice principal
