tipo:: documento-funcional
estado:: activo
version:: 1.1
capa:: proyecto
fecha:: 2026-04-10

- # Alternativas de Mejora del Sistema
	- Análisis de opciones para superar las limitaciones identificadas en [[Evaluacion-Critica]]. Foco en los dos puntos más débiles: el MCP de Logseq (5/10) y la complejidad para el usuario final (4/10).
- ## Diagnóstico de Raíz
	- Antes de evaluar alternativas, hay que separar dos problemas que hoy se confunden:
	- | Problema | Origen | Nota actual |
	  |----------|--------|:-----------:|
	  | Logseq como **editor humano** | Excelente — outliner, links, queries visuales | ~8 |
	  | Logseq como **puente de agentes** (HTTP API) | Requiere app abierta, sin modo headless | 5 |
	- El `5/10` no es de Logseq el editor — es del `@logseq/mcp-server` que depende de que la app esté corriendo. Son problemas distintos con soluciones distintas.
- ## Alternativas Evaluadas
	- ### Opción A — MCP server sobre archivos `.md` directo
		- Reemplazar el MCP de Logseq por un servidor que lea/escriba los archivos directamente, sin depender de ninguna app corriendo.
		- ```
		  Agente → MCP server (Python/TS) → archivos .md → Git
		  ```
		- **Ventajas**
			- No requiere ninguna app corriendo — headless nativo
			- Logseq sigue siendo el editor humano (lee los mismos archivos)
			- Implementable en ~300 líneas de Python
			- Las operaciones que necesitan los agentes (`read_page`, `create_page`, `search`, `get_backlinks`) son viables sobre archivos `.md`
		- **Tradeoffs**
			- Se pierde Datalog en tiempo real — reemplazable con grep + frontmatter parsing para los casos de uso de los agentes
		- **Impacto proyectado**: MCP 5 → 8, sin cambios en el resto del sistema
		- **Esfuerzo**: bajo — todo el vault, agentes y pipeline quedan intactos
	- ### Opción B — Obsidian + REST API plugin
		- Usar Obsidian como editor humano en reemplazo de Logseq, con el plugin [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) para agentes.
		- **Ventajas sobre Logseq**
			- Ecosistema más maduro y activo
			- Dataview plugin — queries potentes con sintaxis SQL-like
			- Properties como YAML frontmatter estándar (más portable que EDN)
			- Comunidad de plugins más grande
		- **Tradeoffs**
			- Sigue requiriendo la app para el MCP — no resuelve el problema raíz
			- Migración de propiedades EDN a YAML frontmatter no trivial
			- Sin outliner nativo — cambio de paradigma de edición
		- **Impacto proyectado**: MCP 5 → 6, Logseq 6 → 7
		- **Esfuerzo**: alto — migración de formato + adaptación de agentes
	- ### Opción C — Markdown puro + tooling custom
		- Sin GUI. Solo archivos `.md` con frontmatter YAML, un MCP server custom y los scripts de validación ya existentes.
		- **Ventajas**
			- Máxima portabilidad — sin dependencia de ninguna app
			- Los agentes son el único consumidor de la estructura
			- Alineado con lo que hace GitHub Spec Kit (ver [[Comparativa-SpecKit]])
		- **Tradeoffs**
			- Se pierde la UI del grafo para el humano — sin visualización de links, sin queries interactivas
			- Curva alta para onboarding de nuevos usuarios
			- Se pierde el diferencial visual del grafo bidireccional
		- **Impacto proyectado**: MCP 5 → 9, Complejidad usuario 4 → 3
		- **Esfuerzo**: muy alto — abandona el paradigma actual
	- ### Opción E — SilverBullet como plataforma base
		- Reemplazar Logseq por [SilverBullet](https://github.com/silverbulletmd/silverbullet) — servidor Go con HTTP API nativa, storage en archivos `.md` y MCP comunitario disponible.
		- ```
		  Agente → silverbullet-mcp (Docker) → SilverBullet server (Go) → archivos .md
		  ```
		- **Diferencia arquitectónica clave con Logseq**
			- Logseq es una app desktop que expone un plugin HTTP. SilverBullet es un proceso servidor desde el inicio — puede correr en Docker, CI o un VPS sin GUI.
			- Esto resuelve el problema raíz del MCP sin necesidad de buildear un server custom.
		- **Ventajas**
			- HTTP API nativa y oficial — no depende de plugin ni de app desktop
			- Puede correr headless, en Docker, en CI
			- MCP comunitario ya funcional (`Ahmad-A0/silverbullet-mcp`, HTTP Streamable + stdio)
			- YAML frontmatter estándar en lugar de propiedades EDN
			- Storage en archivos `.md` planos — mismo diferencial que hoy
			- Links bidireccionales y backlinks nativos (`[[PageName]]`)
		- **Tradeoffs críticos**
			- **Sin block references UUID** — no existe el equivalente a `((uuid))` de Logseq. Las referencias son por anchor (`[[PAGE#header]]`) o posición de línea (`[[PAGE@L3]]`), que no son estables si el contenido se mueve. Requiere rediseñar R-003 (`check_pr_spec.py`) completo.
			- Query language SQL-like + Lua — menos potente que Datalog de Logseq para los casos de uso de los agentes
			- Ecosistema más pequeño — 5k stars vs ~35k de Logseq, menos documentación y ejemplos
			- Cambio de paradigma de edición — sin outliner nativo, distinto al flujo actual
		- **Impacto proyectado**: MCP 5 → 8, Logseq 6 → 7, pero requiere rediseño de trazabilidad spec↔código
		- **Esfuerzo**: alto — migración de vault + rediseño de R-003 + adaptación de agentes
		- **Veredicto**: viable como rediseño deliberado si la prioridad es headless y API robusta. No es un reemplazo directo — es una reescritura del contrato de trazabilidad del sistema.
	- ### Opción D — Hybrid: Logseq para humanos + MCP sobre archivos (recomendada)
		- Mantener Logseq como editor humano. Reemplazar solo el MCP de Logseq por un servidor que acceda a los mismos archivos directamente.
		- ```
		                     ┌─ Logseq (UI humana, editor, grafo visual)
		  archivos .md ──────┤
		                     └─ MCP file server (agentes, headless, CI)
		  ```
		- **Ventajas**
			- Resuelve el problema raíz sin tocar el vault ni los agentes
			- El humano sigue con la mejor UX para navegar el grafo
			- Los agentes no dependen de que Logseq esté abierto
			- Todo el trabajo existente (páginas, propiedades, system prompts, pipeline) queda intacto
		- **Tradeoffs**
			- Requiere mantener un servidor MCP custom en lugar de usar el paquete de la comunidad
		- **Impacto proyectado**: MCP 5 → 8, sin regresión en otras dimensiones
		- **Esfuerzo**: bajo-medio — ~300 líneas de código nuevo, sin migración
- ## Tabla Comparativa
	- | Opción | MCP | Logseq | Complejidad | Esfuerzo | Migración |
	  |--------|:---:|:------:|:-----------:|:--------:|:---------:|
	  | A — MCP sobre archivos | 8 | 6 | 4 | bajo | ninguna |
	  | B — Obsidian + REST API | 6 | 7 | 4 | alto | alta |
	  | C — Markdown puro | 9 | — | 3 | muy alto | total |
	  | D — Hybrid (recomendada) | 8 | 6 | 4 | bajo-medio | ninguna |
	  | E — SilverBullet | 8 | 7 | 4 | alto | alta |
	  | Baseline actual | 5 | 6 | 4 | — | — |
- ## Próximos Pasos Propuestos
	- LATER Diseñar la interfaz del MCP file server (operaciones mínimas que necesitan los agentes)
	- LATER Implementar prototipo de MCP server en Python sobre archivos `.md`
	- LATER Testear con los agentes existentes — validar paridad con `@logseq/mcp-server`
	- LATER Evaluar si Obsidian Dataview reemplaza con ventaja las queries Datalog de Logseq
- ## Referencias
	- [[Evaluacion-Critica]] — limitaciones que motivan este análisis
	- [[MCP-Logseq-Configuracion]] — implementación actual del MCP
	- [[Comparativa-SpecKit]] — comparativa con GitHub Spec Kit (Opción C)
	- [[Backlog-Fases]] — fases donde estas mejoras se incorporarán
