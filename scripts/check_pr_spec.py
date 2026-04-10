#!/usr/bin/env python3
"""
check_pr_spec.py — Verifica que el PR referencie al menos un bloque de spec.

Regla implementada:
  R-003 (crítico) — todo PR debe referenciar al menos un bloque de spec
                    del grafo mediante una referencia ((uuid)).

Uso: python scripts/check_pr_spec.py "$PR_BODY"
     python scripts/check_pr_spec.py --file pr_body.txt

Salida: exit 0 si hay al menos una referencia, exit 1 si no la hay.
"""

import sys
import re


UUID_PATTERN = re.compile(
    r'\(\([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\)\)',
    re.IGNORECASE
)

SPEC_SECTION_PATTERN = re.compile(
    r'##\s*(?:spec|especificaci[oó]n|block.?ref)',
    re.IGNORECASE
)


def check_pr_body(body):
    """
    Verifica que el cuerpo del PR contenga:
    1. Al menos una referencia ((uuid)) de bloque Logseq.
    2. Preferentemente en la sección 'Spec de referencia'.

    Retorna (ok: bool, detalle: str)
    """
    uuids = UUID_PATTERN.findall(body)

    if not uuids:
        return False, (
            "El PR no contiene ninguna referencia a bloque de spec ((uuid)).\n"
            "Todo PR debe referenciar al menos un bloque del grafo (R-003).\n"
            "Ejemplo: ((69d97c12-76ad-4dd5-afa5-7fd90fc3f915))"
        )

    has_spec_section = bool(SPEC_SECTION_PATTERN.search(body))

    if not has_spec_section:
        return True, (
            f"OK: {len(uuids)} referencia(s) de bloque encontrada(s).\n"
            f"  Sugerencia: agregar sección '## Spec de referencia' para mayor claridad."
        )

    return True, f"OK: {len(uuids)} referencia(s) de bloque en sección de spec."


def main():
    if len(sys.argv) < 2:
        print("Uso: python check_pr_spec.py <pr_body>")
        print("     python check_pr_spec.py --file <archivo>")
        sys.exit(1)

    if sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print("Error: falta el nombre del archivo.")
            sys.exit(1)
        with open(sys.argv[2], encoding="utf-8") as f:
            body = f.read()
    else:
        body = " ".join(sys.argv[1:])

    ok, detalle = check_pr_body(body)

    if ok:
        print(detalle)
        sys.exit(0)
    else:
        print(f"ERROR [R-003] {detalle}")
        sys.exit(1)


if __name__ == "__main__":
    main()
