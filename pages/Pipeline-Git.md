tipo:: documento-funcional
estado:: activo
version:: 1.0
capa:: proyecto

- # Pipeline Git
- ## Flujo de PR y Validación Automática
  - ```
    Developer / Agente-Desarrollador
    │
    ├─ 1. Crea rama: feat/<nombre> desde dev
    ├─ 2. Implementa cambio referenciando spec del grafo
    ├─ 3. Abre PR contra dev (usa template de [[Estructura-Proyecto]])
    │
    GitHub Actions (trigger: PR abierto)
    │
    ├─ 4. Checkout del repositorio
    ├─ 5. Validador-grafo verifica integridad del grafo
    │   ├─ OK → continúa
    │   └─ ERROR → bloquea merge, notifica
    ├─ 6. Valida que el PR tiene block-ref de spec
    │   ├─ OK → marca checks como passed
    │   └─ FALTA → bloquea merge
    │
    Revisión Humana (opcional según impacto)
    │
    ├─ 7. Merge a dev
    ├─ 8. Al cerrar fase: PR de dev → main
    └─ 9. Documentador se activa post-merge
    ```
- ## Workflow GitHub Actions
  - ```yaml
    # .github/workflows/validate.yml
    name: Validate SDD Graph
    
    on:
      pull_request:
        branches: [main, dev]
    
    jobs:
      validate-graph:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout
            uses: actions/checkout@v4
    
          - name: Validate page properties
            run: |
              # Verificar que todas las páginas tengan tipo::, estado::, version::
              python scripts/validate_properties.py pages/
    
          - name: Validate internal links
            run: |
              # Verificar que todos los [[links]] apunten a páginas existentes
              python scripts/validate_links.py pages/
    
          - name: Check PR has spec reference
            run: |
              # Verificar que el PR description tiene referencia a spec
              python scripts/check_pr_spec.py "${{ github.event.pull_request.body }}"
    
          - name: Report results
            if: always()
            run: |
              echo "Validación completada. Ver logs para detalles."
    ```
- ## Condiciones de Merge
  - ### Para merge a `dev`
    - Todos los checks de GitHub Actions pasan (verde)
    - El PR tiene al menos una referencia a un bloque de spec
    - El validador-grafo no reporta errores críticos
  - ### Para merge a `main`
    - Todo lo anterior, más:
    - La fase del [[Backlog-Fases]] está marcada como completada
    - El validador-negocio aprobó los cambios de specs (si aplica)
    - Aprobación humana explícita (en casos de alto impacto, según [[Protocolo-Orquestador]])
- ## Scripts de Validación
  - Los scripts en `scripts/` son invocados por GitHub Actions y también pueden ejecutarse localmente.
  - | Script | Propósito |
    |--------|-----------|
    | `validate_properties.py` | Verifica `tipo::`, `estado::`, `version::` en cada página |
    | `validate_links.py` | Detecta vínculos `[[...]]` rotos |
    | `check_pr_spec.py` | Verifica que el PR referencie una spec del grafo |
- ## Referencias
  - [[Estructura-Proyecto]] — Estructura de ramas y PR template
  - [[Agentes-y-Skills]] — Agentes que interactúan con el pipeline
  - [[README-Metodologia]] — Índice principal
