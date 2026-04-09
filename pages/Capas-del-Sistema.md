tipo:: referencia
estado:: activo
version:: 1.0
capa:: nucleo

- # Capas del Sistema
	- El vault está dividido en dos capas: `nucleo` y `proyecto`. Esta separación es lo que permite replicar la metodología en proyectos nuevos sin arrastrar contenido específico de un proyecto anterior.
	- ## capa:: nucleo
		- Páginas de metodología portable. Viajan con cada proyecto nuevo vía GitHub Release. No contienen información específica de ningún proyecto — solo reglas, definiciones, plantillas y fundamentos teóricos.
		- Son empaquetadas automáticamente por el GitHub Action cuando se detecta un cambio en `pages/` o `logseq/config.edn`. Ver [[Configuracion-GitHub-Actions]].
		- ### Páginas nucleo de este vault
			- [[Manifiesto-SDD-Agentes]] — principios, restricciones y decisiones de diseño
			- [[Agentes-y-Skills]] — definición de roles y responsabilidades
			- [[Skills-de-Agentes]] — catálogo completo con anatomía de cada skill
			- [[Agregar-Agente-y-Skills]] — guía para extender el sistema con nuevos agentes
			- [[Protocolo-Orquestador]] — lógica de despacho y reglas de prioridad
			- [[MCP-Logseq-Configuracion]] — configuración de la conexión MCP
			- [[Plantillas-Logseq]] — plantillas estándar del sistema
			- [[Glosario-Metodologia]] — términos clave
			- [[La-definicion-de-tareas]] — anatomía de un nodo de tarea
			- [[Plantilla-de-tareas]] — plantilla estándar para tareas
			- [[La-estructura-etiquetas]] — sistema de etiquetas para el MCP
			- [[Grafo-como-fuente-de-verdad-utilizando-Logseq]] — fundamento metodológico
			- [[Logseq-Calidad-del-Contexto-Humano]] — fundamento teórico
			- [[Capas-del-Sistema]] — este documento
			- [[Configuracion-GitHub-Actions]] — explicación del pipeline de release
			- [[Crear-Nuevo-Proyecto]] — guía de inicio para un proyecto nuevo
	- ## capa:: proyecto
		- Páginas específicas de este proyecto. No se incluyen en el release nucleo. Cada proyecto nuevo crea las suyas desde cero, usando las plantillas y guías del nucleo.
		- ### Páginas proyecto de este vault
			- [[README-Metodologia]] — índice principal de este proyecto específico
			- [[Backlog-Fases]] — backlog de fases del proyecto actual
			- [[Estimacion-Tokens-Costos]] — estimaciones específicas de este proyecto
			- [[Comparativa-SpecKit]] — decisión tomada en este proyecto
			- [[Estructura-Proyecto]] — estructura de carpetas de este proyecto
			- [[Pipeline-Git]] — configuración Git de este proyecto
	- ## Cómo el workflow identifica cada capa
		- El GitHub Action filtra por la propiedad `capa:: nucleo` usando `grep`. Solo esas páginas se incluyen en el zip del release. Ver [[Configuracion-GitHub-Actions]].
		- El MCP puede hacer la misma distinción vía query Datalog:
		- ```clojure
		  [:find ?nombre
		   :where
		   [?p :block/name ?nombre]
		   [?p :block/properties ?props]
		   [(get ?props :capa) ?capa]
		   [(= ?capa "nucleo")]]
		  ```
	- ## Regla para páginas nuevas
		- Toda página nueva debe declarar su capa explícitamente:
		- ¿Esta página sería útil en **cualquier** proyecto que use esta metodología? → `capa:: nucleo`
		- ¿Esta página tiene sentido solo en el contexto de **este** proyecto? → `capa:: proyecto`
		- La duda se resuelve con la pregunta: *¿le serviría esta página a alguien que acaba de descargar el release nucleo?* Si sí → nucleo. Si no → proyecto.
	- ## Ver también
		- [[Configuracion-GitHub-Actions]] — cómo se empaqueta el nucleo en un release
		- [[Crear-Nuevo-Proyecto]] — cómo usar un release para iniciar un proyecto
		- [[README-Metodologia]] — índice principal
