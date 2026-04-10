tipo:: referencia
estado:: activo
version:: 1.0
capa:: nucleo

- # Referencia de Agentes — Guía Rápida
	- Guía de consulta rápida para entender qué hace cada agente, cuándo usarlo y qué esperar de él. Para la definición completa de cada agente ver [[Agentes-y-Skills]]. Para los system prompts ver las páginas `SystemPrompt-*`.
- ## Mapa del Sistema
	- ```
	  USUARIO
	    │
	    ▼
	  orquestador ─────────────────────────────────────────────────┐
	    │                                                           │
	    ├── consultor-metodologia   (preguntas sobre el sistema)   │
	    │                                                           │
	    ├── analizador-requerimientos → [vault: REQs]              │
	    │                                                           │
	    ├── validador-negocio        (verifica specs)              │
	    │                                                           │
	    ├── validador-grafo          (verifica grafo)              │
	    │                                                           │
	    ├── desarrollador           → [git: PR + código]           │
	    │                                                           │
	    ├── tester                  → [git: tests en el PR]        │
	    │                                                           │
	    └── documentador            → [vault: DOC/DEC/updates] ───┘
	  ```
- ## Tabla de Roles
	- | Agente | Dominio | Trigger principal | Produce |
	  |--------|---------|-------------------|---------|
	  | orquestador | Coordinación | Toda interacción del usuario | Respuesta consolidada al usuario |
	  | consultor-metodologia | Consulta del vault | Pregunta sobre el sistema | Respuesta fundamentada en el vault |
	  | validador-grafo | Integridad estructural | Pre-merge / post-edición | Reporte de errores V-001 a V-008 |
	  | validador-negocio | Consistencia semántica | Nueva spec / cambio de req | Reporte de errores N-001 a N-009 |
	  | analizador-requerimientos | Extracción de reqs | Documento en lenguaje natural | Páginas REQ en el vault |
	  | desarrollador | Generación de código | Spec con estado:: aprobado | Rama feat/ + PR con código |
	  | tester | Generación de tests | PR del desarrollador listo | Tests en el branch del PR |
	  | documentador | Actualización del vault | Merge exitoso / cambio de estado | Páginas DOC/DEC actualizadas |
- ## Qué Lee y Qué Escribe Cada Agente
	- | Agente | Lee | Escribe |
	  |--------|-----|---------|
	  | orquestador | — | — (solo coordina) |
	  | consultor-metodologia | Vault (páginas nucleo) | — |
	  | validador-grafo | Vault (todas las páginas) | — |
	  | validador-negocio | Vault (specs y REQs) | — |
	  | analizador-requerimientos | Documento de entrada + vault | Vault (páginas REQ) |
	  | desarrollador | Vault (spec + REQs) | Git (rama + PR) |
	  | tester | Vault (REQs) + Git (código del PR) | Git (tests en el PR) |
	  | documentador | Vault + Git (diff del merge) | Vault (DOC/DEC/updates) |
- ## Skills por Agente
	- | Agente | Skills |
	  |--------|--------|
	  | orquestador | `despacho` · `agregación` · `escalamiento` |
	  | consultor-metodologia | `consulta-vault` · `lectura-MCP` · `query-Datalog` |
	  | validador-grafo | `validación-estructura` · `reporte-errores` · `lectura-MCP` · `query-Datalog` |
	  | validador-negocio | `validación-specs` · `análisis-semántico` · `lectura-MCP` · `query-Datalog` |
	  | analizador-requerimientos | `extracción-reqs` · `clasificación` · `formato-Logseq` · `escritura-MCP` |
	  | desarrollador | `generación-código` · `creación-PR` · `lectura-MCP` |
	  | tester | `generación-tests` · `validación-cobertura` · `lectura-MCP` |
	  | documentador | `generación-docs` · `actualización-grafo` · `lectura-MCP` · `escritura-MCP` |
- ## Páginas Cacheadas por Agente
	- | Agente | Páginas en caché |
	  |--------|-----------------|
	  | orquestador | Manifiesto · Agentes-y-Skills · Skills-de-Agentes · Protocolo-Orquestador · Estimacion-Tokens-Costos |
	  | consultor-metodologia | Manifiesto · Agentes-y-Skills · Skills-de-Agentes · Plantillas-Logseq · La-estructura-etiquetas · Capas-del-Sistema |
	  | validador-grafo | Manifiesto · La-estructura-etiquetas · La-definicion-de-tareas · Plantillas-Logseq |
	  | validador-negocio | Manifiesto · Agentes-y-Skills · Plantillas-Logseq · Glosario-Metodologia |
	  | analizador-requerimientos | Plantillas-Logseq · Manifiesto · La-estructura-etiquetas · Glosario-Metodologia |
	  | desarrollador | Manifiesto · Estructura-Proyecto · Pipeline-Git |
	  | tester | Plantillas-Logseq · Manifiesto · La-estructura-etiquetas |
	  | documentador | Plantillas-Logseq · Manifiesto · La-estructura-etiquetas · Agentes-y-Skills |
- ## Qué Bloquea Cada Agente
	- | Agente | Condición de bloqueo | Bloquea qué |
	  |--------|---------------------|-------------|
	  | validador-grafo | Errores V-001, V-002, V-003 | Merge a main / dev |
	  | validador-negocio | Errores N-001, N-002, N-003, N-004 | Aprobación de la spec |
	  | tester | Criterio de aceptación sin cobertura de test | Merge a main / dev |
	  | analizador-requerimientos | >20 REQs potenciales en un documento | Escalamiento por costo |
	  | desarrollador | Spec sin estado:: aprobado | No genera código |
	  | documentador | Sin contexto de merge | No escribe al vault |
- ## Códigos de Error por Agente
	- ### validador-grafo (estructura)
		- | Código | Descripción | Severidad |
		  |--------|-------------|-----------|
		  | V-001 | Propiedades requeridas faltantes en página nucleo | Crítico |
		  | V-002 | Vínculo `[[...]]` roto | Crítico |
		  | V-003 | Referencia `((uuid))` inexistente | Crítico |
		  | V-004 | Propiedades faltantes en página proyecto | Advertencia |
		  | V-005 | Propiedad `capa::` ausente | Advertencia |
		  | V-006 | Valor de `estado::` no reconocido | Advertencia |
		  | V-007 | Página sin vínculos salientes | Info |
		  | V-008 | Página sin vínculos entrantes | Info |
	- ### validador-negocio (semántica)
		- | Código | Descripción | Severidad |
		  |--------|-------------|-----------|
		  | N-001 | Contradicción directa entre specs | Crítico |
		  | N-002 | Requerimiento no implementable | Crítico |
		  | N-003 | SPEC sin al menos un REQ referenciado | Crítico |
		  | N-004 | Modificación de spec aprobada sin escalamiento | Escalamiento |
		  | N-005 | Ambigüedad no resuelta en criterio | Advertencia |
		  | N-006 | REQ huérfano sin spec que lo referencie | Advertencia |
		  | N-007 | Solapamiento entre specs del mismo dominio | Advertencia |
		  | N-008 | Vocabulario inconsistente con el glosario | Advertencia |
		  | N-009 | Criterio de aceptación sin métrica verificable | Info |
- ## Flujo Completo del Sistema
	- ```
	  0.  consulta-vault         → consultor     (verificación de convención)
	  1.  extracción-reqs        → analizador    (texto → REQs borrador)
	  2.  clasificación           → analizador    (tipo + prioridad + ID)
	  3.  formato-Logseq          → analizador    (plantilla REQ)
	  4.  escritura-MCP           → analizador    (REQs al vault)
	  5.  validación-specs        → val-negocio   (consistencia semántica)
	  6.  análisis-semántico      → val-negocio   (ambigüedades + contradicciones)
	  7.  generación-código       → desarrollador (código desde spec aprobada)
	  8.  creación-PR             → desarrollador (rama feat/ + PR)
	  9.  generación-tests        → tester        (tests por criterio de aceptación)
	  10. validación-cobertura    → tester        (todos los criterios cubiertos)
	  11. validación-estructura   → val-grafo     (integridad pre-merge)
	  12. generación-docs         → documentador  (post-merge)
	  13. actualización-grafo     → documentador  (estado:: implementado + versiones)
	  ```
- ## Cuándo Usar Cada Agente — Guía de Decisión Rápida
	- **"No sé cómo se llama la propiedad / plantilla / agente"** → consultor-metodologia
	- **"Tengo un email/reunión con requerimientos"** → analizador-requerimientos
	- **"Quiero saber si el vault está íntegro"** → validador-grafo
	- **"Quiero aprobar esta spec"** → validador-negocio primero
	- **"La spec está aprobada, quiero el código"** → desarrollador
	- **"El PR está listo, quiero verificar que pasan los criterios"** → tester
	- **"Mergeamos, hay que actualizar la documentación"** → documentador
- ## Ver También
	- [[Agentes-y-Skills]] — Definición completa con responsabilidades y triggers
	- [[Skills-de-Agentes]] — Catálogo de skills con inputs, outputs y dependencias
	- [[Protocolo-Orquestador]] — Árbol de decisión y reglas de prioridad
	- [[Manifiesto-SDD-Agentes]] — Principios y restricciones que gobiernan los agentes
	- [[MCP-Logseq-Configuracion]] — Operaciones MCP que usan los agentes
