tipo:: documento-funcional
estado:: activo
version:: 1.0
capa:: proyecto

- # Estructura del Proyecto
- ## Estructura de Carpetas del Repositorio
  - ```
    graphdev/                  ← Raíz del repositorio / vault Logseq
    ├── pages/                 ← Páginas del grafo (specs, decisiones, docs)
    │   ├── README-Metodologia.md
    │   ├── Manifiesto-SDD-Agentes.md
    │   ├── Agentes-y-Skills.md
    │   └── ...
    ├── journals/              ← Entradas de diario diario (auto-generadas)
    ├── logseq/
    │   ├── config.edn         ← Configuración del vault
    │   └── custom.css         ← Estilos personalizados
    ├── .github/
    │   ├── workflows/
    │   │   └── validate.yml   ← GitHub Actions para validación
    │   └── PULL_REQUEST_TEMPLATE.md
    ├── CLAUDE.md              ← Instrucciones para Claude Code
    └── prompt.txt             ← Prompts de sesión (no versionado)
    ```
- ## Estrategia de Ramas Git
  - **`main`** — Rama estable. Solo recibe PRs validados por el agente validador-grafo.
  - **`dev`** — Rama de integración. Se mergea a `main` al cerrar una fase del [[Backlog-Fases]].
  - **`feat/<nombre>`** — Ramas de features individuales. Nombradas según la tarea del backlog.
  - **`fix/<nombre>`** — Ramas de correcciones. Requieren referencia a un bloque del grafo.
  - **`docs/<nombre>`** — Ramas exclusivas para documentación. No requieren validación de código.
  - ### Reglas
    - Nunca hacer push directo a `main`
    - Todo merge a `main` requiere aprobación del validador-grafo (ver [[Pipeline-Git]])
    - Las ramas `feat/` se eliminan tras el merge
- ## PR Template
  - ```markdown
    ## Descripción
    <!-- Qué hace este PR y por qué -->
    
    ## Spec de referencia
    <!-- Bloque Logseq que especifica esta funcionalidad -->
    - Página: [[...]]
    - Block ref: ((...))
    
    ## Tipo de cambio
    - [ ] feat — nueva funcionalidad
    - [ ] fix — corrección de bug
    - [ ] docs — solo documentación
    - [ ] refactor — sin cambio de comportamiento
    
    ## Checklist
    - [ ] El validador-grafo aprobó este cambio
    - [ ] La spec referenciada está aprobada en el grafo
    - [ ] Las plantillas usadas corresponden a [[Plantillas-Logseq]]
    - [ ] No hay vínculos rotos en las páginas modificadas
    
    ## Agente que generó el cambio
    <!-- Nombre del agente o "humano" -->
    ```
- ## Referencias
  - [[Pipeline-Git]] — Flujo completo de CI/CD
  - [[Agentes-y-Skills]] — Quién genera los PRs
  - [[README-Metodologia]] — Índice principal
