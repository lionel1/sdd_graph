#!/usr/bin/env python3
"""
validate_properties.py — Verifica propiedades requeridas en páginas del vault.

Reglas implementadas:
  V-001 (crítico)     — páginas capa:: nucleo deben tener: tipo::, estado::, version::, capa::
  V-004 (advertencia) — páginas capa:: proyecto deben tener: tipo::, estado::, version::
  V-005 (advertencia) — toda página debe declarar capa::
  V-006 (advertencia) — estado:: debe ser un valor reconocido

Uso: python scripts/validate_properties.py pages/
Salida: exit 0 si no hay errores críticos, exit 1 si los hay.
"""

import sys
import os
import re
from pathlib import Path

REQUIRED_NUCLEO = {"tipo", "estado", "version", "capa"}
REQUIRED_PROYECTO = {"tipo", "estado", "version"}
VALID_ESTADOS = {
    "borrador", "activo", "activa", "completada", "pausada",
    "aprobado", "implementado", "deprecated", "en-progreso", "todo"
}

def parse_properties(filepath):
    """Extrae propiedades key:: value del inicio del archivo."""
    props = {}
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            # Propiedades de página: al inicio, sin sangría o con sangría mínima
            m = re.match(r'^[\t ]{0,2}(\w[\w/-]*):: *(.*)', line)
            if m:
                props[m.group(1).lower()] = m.group(2).strip()
            # Detener al llegar al primer bloque de contenido
            elif line.startswith("- ") or line.startswith("\t- "):
                break
    return props


def validate_file(filepath):
    """Valida las propiedades de un archivo. Retorna lista de (severidad, código, detalle)."""
    issues = []
    props = parse_properties(filepath)
    name = Path(filepath).stem

    capa = props.get("capa", "").lower()

    # V-005 — capa:: ausente
    if not capa:
        issues.append(("advertencia", "V-005", f"{name}: propiedad capa:: ausente"))
        # Sin capa no podemos aplicar V-001 ni V-004 con certeza
        reqs = REQUIRED_PROYECTO
    elif capa == "nucleo":
        reqs = REQUIRED_NUCLEO
    else:
        reqs = REQUIRED_PROYECTO

    # V-001 / V-004 — propiedades requeridas faltantes
    missing = reqs - set(props.keys())
    if missing:
        sev = "critico" if capa == "nucleo" else "advertencia"
        code = "V-001" if capa == "nucleo" else "V-004"
        issues.append((sev, code, f"{name}: faltan propiedades {sorted(missing)}"))

    # V-006 — valor de estado:: no reconocido
    estado = props.get("estado", "").lower()
    if estado and estado not in VALID_ESTADOS:
        issues.append(("advertencia", "V-006",
                        f"{name}: estado:: '{estado}' no reconocido. "
                        f"Valores válidos: {sorted(VALID_ESTADOS)}"))

    return issues


def main():
    if len(sys.argv) < 2:
        print("Uso: python validate_properties.py <directorio-pages>")
        sys.exit(1)

    pages_dir = sys.argv[1]
    # Páginas auto-generadas por Logseq — no tienen propiedades SDD
    LOGSEQ_BUILTIN = {"contents", "proyecto"}

    files = [f for f in sorted(Path(pages_dir).glob("*.md"))
             if f.stem.lower() not in LOGSEQ_BUILTIN]

    if not files:
        print(f"No se encontraron archivos .md en {pages_dir}")
        sys.exit(1)

    all_issues = []
    for f in files:
        all_issues.extend(validate_file(f))

    criticos    = [i for i in all_issues if i[0] == "critico"]
    advertencias = [i for i in all_issues if i[0] == "advertencia"]

    print(f"Páginas analizadas: {len(files)}")
    print(f"Errores críticos:   {len(criticos)}")
    print(f"Advertencias:       {len(advertencias)}")

    if criticos:
        print("\n-- ERRORES CRITICOS ----------------------------------")
        for sev, code, msg in criticos:
            print(f"  [{code}] {msg}")

    if advertencias:
        print("\n-- ADVERTENCIAS -------------------------------------")
        for sev, code, msg in advertencias:
            print(f"  [{code}] {msg}")

    if not all_issues:
        print("OK: Sin errores de propiedades.")

    sys.exit(1 if criticos else 0)


if __name__ == "__main__":
    main()
