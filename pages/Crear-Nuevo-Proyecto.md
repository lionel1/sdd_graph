tipo:: referencia
estado:: activo
version:: 1.0
capa:: nucleo

- # Crear un Nuevo Proyecto
	- Guía paso a paso para inicializar un nuevo vault Logseq a partir del release nucleo de `sdd-metodologia`. El proceso toma menos de 5 minutos.
	- ## Prerequisitos
		- Logseq desktop instalado
		- Git Bash (Windows) o terminal con bash (Mac/Linux)
		- Acceso a `https://github.com/TU-USUARIO/sdd-metodologia/releases`
	- ## Paso 1 — Descargar el release nucleo
		- Ir a la página de releases del repo y descargar el zip de la versión deseada:
		- ```bash
		  # opción A: desde el navegador
		  # https://github.com/TU-USUARIO/sdd-metodologia/releases
		  # descargar sdd-nucleo-v1.0.0.zip
		  
		  # opción B: desde terminal con gh CLI
		  gh release download v1.0.0 --repo TU-USUARIO/sdd-metodologia
		  ```
		- **¿Qué versión usar?**
			- `latest` — metodología actualizada, puede tener cambios recientes
			- `vX.Y.Z` — versión estable, recomendada para proyectos en producción
	- ## Paso 2 — Ejecutar el bootstrap
		- ```bash
		  # descomprimir
		  unzip sdd-nucleo-v1.0.0.zip -d sdd-nucleo
		  cd sdd-nucleo
		  chmod +x bootstrap.sh
		  
		  # crear el vault del nuevo proyecto
		  # uso: ./bootstrap.sh <nombre-proyecto> <directorio-destino>
		  ./bootstrap.sh mi-proyecto ~/proyectos
		  ```
		- El script crea la siguiente estructura en `~/proyectos/mi-proyecto/`:
		- ```
		  mi-proyecto/
		  ├── pages/
		  │   ├── Manifiesto-SDD-Agentes.md    ← nucleo
		  │   ├── Agentes-y-Skills.md           ← nucleo
		  │   ├── ...                           ← resto del nucleo
		  │   └── README-mi-proyecto.md         ← índice del proyecto (generado)
		  ├── logseq/
		  │   └── config.edn
		  ├── assets/
		  ├── journals/
		  └── .gitignore
		  ```
	- ## Paso 3 — Abrir en Logseq
		- 1. Abrir Logseq
		- 2. Click en **Add graph** (o el ícono de grafo → agregar)
		- 3. Seleccionar la carpeta `~/proyectos/mi-proyecto`
		- 4. Logseq indexa el vault — tarda unos segundos
		- 5. Verificar que las páginas nucleo aparecen en el grafo
	- ## Paso 4 — Configurar el proyecto
		- Abrir `README-mi-proyecto.md` (generado por bootstrap) y:
		- 1. Reemplazar la descripción placeholder
		- 2. Agregar las primeras páginas específicas del proyecto en el índice
		- 3. Opcionalmente, agregar `proyecto:: mi-proyecto` como propiedad en las páginas nuevas
	- ## Paso 5 — Inicializar git (opcional pero recomendado)
		- ```bash
		  cd ~/proyectos/mi-proyecto
		  git init
		  git add .
		  git commit -m "init: vault desde sdd-nucleo v1.0.0"
		  
		  # crear repo en GitHub
		  gh repo create mi-proyecto --private --source=. --push
		  ```
	- ## Verificación rápida post-setup
		- ```
		  [ ] Las páginas nucleo aparecen en Logseq sin errores
		  [ ] El grafo muestra vínculos entre páginas (no todo aislado)
		  [ ] MCP conectado: Logseq corriendo + plugin HTTP API activo (ver [[MCP-Logseq-Configuracion]])
		  [ ] README-mi-proyecto.md existe y tiene el nombre correcto
		  [ ] .gitignore excluye logseq/bak/ y logseq/.recycle/
		  ```
	- ## Qué hacer después
		- Con el vault listo, los primeros pasos en cualquier proyecto nuevo son:
		- 1. Definir el dominio del proyecto en el README
		- 2. Crear las primeras páginas `capa:: proyecto` usando las [[Plantillas-Logseq]]
		- 3. Si el proyecto requiere agentes adicionales, usar [[Agregar-Agente-y-Skills]]
		- 4. Activar el MCP de Logseq para habilitar el acceso del agente al grafo
	- ## Troubleshooting
		- **`bootstrap.sh: permission denied`** — ejecutar `chmod +x bootstrap.sh` primero
		- **Logseq no encuentra páginas** — verificar que el grafo apunta a la carpeta raíz del proyecto, no a `pages/`
		- **Vínculos rotos en nucleo** — asegurarse de no haber editado los nombres de archivo de páginas nucleo
		- **El MCP no conecta** — revisar [[MCP-Logseq-Configuracion]], especialmente que el plugin HTTP API esté activo en Logseq
	- ## Ver también
		- [[Capas-del-Sistema]] — qué contiene el nucleo y qué es proyecto
		- [[Configuracion-GitHub-Actions]] — cómo se genera el release
		- [[MCP-Logseq-Configuracion]] — siguiente paso: conectar el agente al vault
		- [[Agregar-Agente-y-Skills]] — extender el sistema con agentes propios
