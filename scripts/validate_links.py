#!/usr/bin/env python3
"""
validate_links.py — Verifica que todos los vínculos [[PageName]] apunten a páginas existentes.

Reglas implementadas:
  V-002 (crítico) — todo [[vínculo]] debe resolver a una página existente en el vault.

Convención de nombres (triple-lowbar):
  Slashes en títulos → triple underscore en nombre de archivo (Page/Sub → Page___Sub.md)
  Espacios → espacios en el nombre de archivo

Uso: python scripts/validate_links.py pages/
Salida: exit 0 si no hay errores críticos, exit 1 si los hay.
"""

import sys
import re
from pathlib import Path


def get_page_index(pages_dir):
    """Construye un set de nombres de página normalizados a partir de los archivos existentes."""
    index = set()
    for f in Path(pages_dir).glob("*.md"):
        # Nombre original del archivo sin extensión
        stem = f.stem
        # Revertir triple-lowbar para comparar con el título del vínculo
        title = stem.replace("___", "/")
        index.add(title.lower())
        index.add(stem.lower())  # también el nombre literal del archivo
    return index


# Patrones que indican un vínculo es un placeholder de plantilla o ejemplo
PLACEHOLDER_PATTERNS = re.compile(
    r'^(\.\.\.|XXX|nombre-proyecto|nodo\d*|agente propietario|skill-previo|'
    r'link[s]?|v[ií]nculo[s]?|P[áa]gina \d+|P[áa]gina-de-Spec|'
    r'README-Proyecto|REQ-(\d{3}|XXX)|SPEC-(\d{3}|XXX)|DEC-(\d{3}|XXX)|NombreDePagina)$',
    re.IGNORECASE
)

# Páginas internas de Logseq que no tienen archivo físico
LOGSEQ_BUILTIN = {"contents", "card", "query", "tags"}


def strip_code_blocks(content):
    """Elimina bloques de código y código inline para no procesar sus vínculos."""
    # Primero bloques cercados (``` ... ```) — orden importante: antes que inline
    content = re.sub(r'```[\s\S]*?```', '', content)
    # Luego código inline con backtick doble (``...``)
    content = re.sub(r'``[^`]+``', '', content)
    # Luego código inline con backtick simple (`...`)
    content = re.sub(r'`[^`\n]+`', '', content)
    return content


def extract_links(content):
    """Extrae [[PageName]] del contenido, ignorando código y placeholders."""
    content = strip_code_blocks(content)
    links = re.findall(r'\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]', content)
    result = []
    for l in links:
        l = l.strip()
        if not l:
            continue
        if PLACEHOLDER_PATTERNS.match(l):
            continue
        if l.lower() in LOGSEQ_BUILTIN:
            continue
        result.append(l)
    return result


def title_to_filename(title):
    """Convierte título de página a nombre de archivo esperado (triple-lowbar)."""
    return title.replace("/", "___")


def validate_links(pages_dir):
    """Valida todos los vínculos en todas las páginas. Retorna lista de errores."""
    page_index = get_page_index(pages_dir)
    issues = []

    for filepath in sorted(Path(pages_dir).glob("*.md")):
        content = filepath.read_text(encoding="utf-8")
        links = extract_links(content)
        name = filepath.stem

        for link in links:
            link_normalized = link.lower()
            filename_normalized = title_to_filename(link).lower()

            if (link_normalized not in page_index and
                    filename_normalized not in page_index):
                issues.append((
                    "critico", "V-002",
                    f"{name}: vinculo roto -> [[{link}]]"
                ))

    return issues


def main():
    if len(sys.argv) < 2:
        print("Uso: python validate_links.py <directorio-pages>")
        sys.exit(1)

    pages_dir = sys.argv[1]

    if not Path(pages_dir).exists():
        print(f"Directorio no encontrado: {pages_dir}")
        sys.exit(1)

    issues = validate_links(pages_dir)
    criticos = [i for i in issues if i[0] == "critico"]

    files = list(Path(pages_dir).glob("*.md"))
    print(f"Páginas analizadas: {len(files)}")
    print(f"Vínculos rotos:     {len(criticos)}")

    if criticos:
        print("\n-- ERRORES CRITICOS (V-002) --------------------------")
        for sev, code, msg in criticos:
            print(f"  [{code}] {msg}")
    else:
        print("OK: Sin vinculos rotos.")

    sys.exit(1 if criticos else 0)


if __name__ == "__main__":
    main()
