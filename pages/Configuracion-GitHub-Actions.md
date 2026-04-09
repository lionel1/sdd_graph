tipo:: referencia
estado:: activo
version:: 1.0
capa:: nucleo

- # Configuración GitHub Actions — Release Nucleo
	- El workflow `release-nucleo.yml` empaqueta automáticamente todas las páginas `capa:: nucleo` del vault y las publica como un GitHub Release descargable. Es el mecanismo que permite replicar la metodología en proyectos nuevos.
	- ## Cuándo se dispara
		- **Automáticamente** — cuando se hace push a `main` y hay cambios en `pages/` o `logseq/config.edn`. Genera o sobreescribe el release `latest`.
		- **Manualmente** — desde GitHub → Actions → Release Nucleo → Run workflow. Pedirá una versión semántica (ej: `v1.2.0`) y genera un release versionado permanente.
	- ## Qué incluye el release zip
		- ```
		  sdd-nucleo-v1.2.0.zip
		  ├── pages/           ← todas las páginas con capa:: nucleo
		  ├── logseq/
		  │   ├── config.edn   ← configuración del vault (workflows, queries, etc.)
		  │   └── custom.css
		  ├── assets/          ← imágenes referenciadas en páginas nucleo
		  └── bootstrap.sh     ← script de inicialización de proyecto nuevo
		  ```
	- ## Cómo crear un release versionado manualmente
		- 1. Ir a `https://github.com/TU-USUARIO/sdd-metodologia/actions`
		- 2. Seleccionar el workflow **Release Nucleo**
		- 3. Click en **Run workflow**
		- 4. Ingresar la versión en formato `vX.Y.Z` (ej: `v1.0.0`)
		- 5. Click en **Run workflow**
		- El release aparece en `https://github.com/TU-USUARIO/sdd-metodologia/releases`
	- ## Convención de versiones
		- `latest` — versión automática, sobreescrita en cada push a main. Para uso en desarrollo activo.
		- `vX.Y.Z` — versión semántica estable. Para distribuir o fijar en proyectos.
			- `X` — cambio de estructura o principios (rompe compatibilidad conceptual)
			- `Y` — páginas nucleo nuevas o reorganización significativa
			- `Z` — correcciones, mejoras de texto, links actualizados
	- ## Cómo funciona el filtrado de páginas
		- El workflow recorre todos los archivos `.md` en `pages/` y verifica si contienen la línea `capa:: nucleo`. Solo esos archivos se copian al zip. Las páginas `capa:: proyecto` se ignoran.
		- ```yaml
		  for f in pages/*.md; do
		    if grep -q "capa:: nucleo" "$f"; then
		      cp "$f" dist/pages/
		    fi
		  done
		  ```
		- Esto significa que agregar una página nueva al nucleo es tan simple como incluir `capa:: nucleo` en sus propiedades. El próximo release la recogerá automáticamente.
	- ## Actualizar el nucleo en un proyecto existente
		- Los proyectos existentes no se actualizan automáticamente — eso es intencional. Cada proyecto decide cuándo adoptar una nueva versión del nucleo.
		- Para actualizar manualmente:
		- ```bash
		  # descargar el release nuevo
		  curl -L https://github.com/TU-USUARIO/sdd-metodologia/releases/download/v1.2.0/sdd-nucleo-v1.2.0.zip \
		    -o sdd-nucleo-v1.2.0.zip
		  unzip sdd-nucleo-v1.2.0.zip -d sdd-nuevo
		  
		  # copiar páginas nucleo al proyecto (sobreescribe las existentes)
		  cp sdd-nuevo/pages/* /ruta/mi-proyecto/pages/
		  ```
		- Revisar el diff en git antes de commitear para detectar conflictos con customizaciones locales.
	- ## Troubleshooting
		- **El release está vacío** — verificar que las páginas tengan exactamente `capa:: nucleo` (sin espacios extra, sin mayúsculas).
		- **El workflow falla en "Crear release"** — verificar que el repo tenga `contents: write` en los permisos del workflow. Ir a Settings → Actions → General → Workflow permissions.
		- **El tag `latest` ya existe** — el workflow usa `softprops/action-gh-release@v2` que sobreescribe releases existentes con el mismo tag. Es el comportamiento esperado para `latest`.
	- ## Ver también
		- [[Capas-del-Sistema]] — qué páginas se incluyen en cada release
		- [[Crear-Nuevo-Proyecto]] — cómo usar el release para iniciar un proyecto
		- [[README-Metodologia]] — índice principal
