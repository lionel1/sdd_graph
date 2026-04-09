tipo:: protocolo
estado:: activo
version:: 1.0
capa:: nucleo

- # Protocolo del Orquestador
- ## Lógica de Despacho
  - El orquestador analiza cada solicitud y aplica este árbol de decisión:
  - ```
    INPUT del usuario
    │
    ├─ ¿Es un documento/texto para analizar?
    │   └─ → Despachar: analizador-requerimientos
    │
    ├─ ¿Es una consulta sobre el grafo?
    │   └─ → Despachar: validador-grafo (modo lectura)
    │
    ├─ ¿Es una spec aprobada lista para implementar?
    │   └─ → Despachar: desarrollador
    │
    ├─ ¿Es un cambio a una spec existente?
    │   ├─ → Despachar: validador-negocio (primero)
    │   └─ → Si aprueba: despachar documentador
    │
    ├─ ¿Es post-merge a main?
    │   └─ → Despachar: documentador
    │
    └─ ¿Impacto alto / decisión irreversible?
        └─ → ESCALAR AL HUMANO antes de continuar
    ```
- ## Reglas de Prioridad
  - **P1 — Escalamiento humano**: Siempre tiene prioridad máxima. El orquestador detiene todo flujo hasta recibir aprobación.
  - **P2 — Validación antes de acción**: El validador-grafo se ejecuta antes que el desarrollador o documentador.
  - **P3 — Negocio antes que técnico**: El validador-negocio se ejecuta antes que el desarrollador.
  - **P4 — Documentación al final**: El documentador siempre es el último en ejecutarse.
  - **P5 — Un agente a la vez por dominio**: No se despachan dos instancias del mismo agente en paralelo.
- ## Condiciones de Escalamiento al Humano
  - Eliminar o modificar una spec con `estado:: aprobado`
  - Merge a `main` con errores no críticos del validador-grafo
  - Conflicto entre dos specs aprobadas
  - Costo proyectado de la sesión supera el umbral (ver [[Estimacion-Tokens-Costos]])
  - Cualquier operación irreversible sobre el grafo o el repositorio
- ## Formato de Respuesta Esperado
  - Cada agente devuelve al orquestador una respuesta con esta estructura:
  - ```json
    {
      "agente": "nombre-del-agente",
      "estado": "ok | error | escalamiento",
      "resultado": "descripción breve del resultado",
      "artefactos": ["lista de archivos o bloques creados/modificados"],
      "errores": ["lista de errores si los hay"],
      "proximos_pasos": ["sugerencias para el orquestador"]
    }
    ```
  - ### Estados posibles
    - `ok` — El agente completó su tarea sin errores.
    - `error` — El agente encontró un error que impide continuar. Requiere intervención.
    - `escalamiento` — El agente detectó una condición que requiere decisión humana.
- ## Contexto del Sistema (System Prompt)
  - El orquestador usa prompt caching en su system prompt para reducir costos. Ver [[Estimacion-Tokens-Costos]].
  - El system prompt incluye:
    - Referencia al [[Manifiesto-SDD-Agentes]] (principios y restricciones)
    - Lista de agentes disponibles de [[Agentes-y-Skills]]
    - Catálogo de skills invocables de [[Skills-de-Agentes]]
    - Acceso al MCP de Logseq (ver [[MCP-Logseq-Configuracion]])
- ## Referencias
  - [[Agentes-y-Skills]] — Definición de cada agente
  - [[Skills-de-Agentes]] — Catálogo de skills con inputs, outputs y dependencias
  - [[Pipeline-Git]] — Flujo de validación pre-merge
  - [[README-Metodologia]] — Índice principal
