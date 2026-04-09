#!/usr/bin/env bash
# bootstrap.sh — Inicializa un nuevo vault Logseq desde el release nucleo de sdd-metodologia
# Uso: ./bootstrap.sh <nombre-proyecto> <directorio-destino>
# Ejemplo: ./bootstrap.sh mi-proyecto ~/proyectos

set -e

NOMBRE=${1:?"Error: falta el nombre del proyecto. Uso: ./bootstrap.sh <nombre> <destino>"}
DESTINO=${2:?"Error: falta el directorio destino. Uso: ./bootstrap.sh <nombre> <destino>"}
TARGET="$DESTINO/$NOMBRE"

if [ -d "$TARGET" ]; then
  echo "Error: '$TARGET' ya existe. Elegí otro nombre o destino."
  exit 1
fi

echo "Creando vault '$NOMBRE' en $TARGET..."

# Crear estructura de directorios
mkdir -p "$TARGET/pages" "$TARGET/logseq" "$TARGET/assets" "$TARGET/journals"

# Copiar páginas nucleo
for f in pages/*.md; do
  grep -q "^capa:: nucleo" "$f" && cp "$f" "$TARGET/pages/" || true
done

# Copiar configuración Logseq
cp logseq/config.edn "$TARGET/logseq/"
[ -f logseq/custom.css ] && cp logseq/custom.css "$TARGET/logseq/" || true

# Copiar assets
if [ "$(ls assets/ 2>/dev/null)" ]; then
  cp assets/* "$TARGET/assets/"
fi

# Generar README del proyecto
TODAY=$(date +%Y-%m-%d)
cat > "$TARGET/pages/README-$NOMBRE.md" << EOREADME
tipo:: índice
estado:: activo
version:: 1.0
capa:: proyecto
proyecto:: $NOMBRE

- # $NOMBRE
	- Descripción del proyecto.
- ## Índice del Proyecto
	- ### Este Proyecto
		- (agregar páginas específicas del proyecto aquí)
	- ### Metodología (nucleo)
		- [[Manifiesto-SDD-Agentes]] — principios y restricciones
		- [[Agentes-y-Skills]] — agentes disponibles
		- [[Protocolo-Orquestador]] — lógica de despacho
		- [[Plantillas-Logseq]] — plantillas para páginas nuevas
		- [[Capas-del-Sistema]] — separación nucleo / proyecto
- ## Estado
	- Inicio: $TODAY
	- Nucleo: $(cat ../VERSION 2>/dev/null || echo "desconocida")
EOREADME

# Copiar VERSION si existe
[ -f VERSION ] && cp VERSION "$TARGET/VERSION" || true

# Crear .gitignore
cat > "$TARGET/.gitignore" << 'EOGIT'
logseq/bak/
logseq/.recycle/
logseq/version-files/
.DS_Store
Thumbs.db
EOGIT

echo ""
echo "✓ Vault '$NOMBRE' creado en $TARGET"
echo ""
echo "Próximos pasos:"
echo "  1. Abrir Logseq → Add graph → $TARGET"
echo "  2. Editar pages/README-$NOMBRE.md con la descripción del proyecto"
echo "  3. Activar el plugin HTTP API en Logseq para usar el MCP"
echo ""
echo "Guía completa: ver página [[Crear-Nuevo-Proyecto]] en el vault"
