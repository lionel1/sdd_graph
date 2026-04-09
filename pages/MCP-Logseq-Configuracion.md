tipo:: configuración-técnica
estado:: activo
version:: 1.0
capa:: nucleo

- # MCP Logseq — Configuración
- ## MCPs Disponibles y Comparativa
  - | MCP | Proveedor | Tipo | Ventajas | Desventajas |
    |-----|-----------|------|----------|-------------|
    | `@logseq/mcp-server` | Logseq oficial | stdio/npx | Oficial, mantención garantizada | Requiere Logseq con HTTP API activo |
    | `logseq-mcp` (community) | Comunidad | stdio | Más métodos disponibles | Sin soporte oficial |
    | HTTP API directo | Logseq | REST | Sin dependencias extra | Requiere curl/fetch manual |
  - **Decisión**: usar `@logseq/mcp-server` oficial + HTTP API directo como fallback.
- ## Configuración JSON (Claude Code)
  - El MCP se agrega a Claude Code con:
  - ```bash
    claude mcp add logseq \
      -e LOGSEQ_API_TOKEN=<token> \
      -e LOGSEQ_BASE_URL=http://localhost:12315 \
      -- npx -y @logseq/mcp-server
    ```
  - ### Configuración en `.mcp.json` (proyecto)
    - ```json
      {
        "mcpServers": {
          "logseq": {
            "command": "npx",
            "args": ["-y", "@logseq/mcp-server"],
            "env": {
              "LOGSEQ_API_TOKEN": "<token>",
              "LOGSEQ_BASE_URL": "http://localhost:12315"
            }
          }
        }
      }
      ```
  - ### Prerequisitos
    - Logseq desktop corriendo
    - Plugin "Logseq HTTP API server" activo en Logseq
    - Puerto 12315 disponible y no bloqueado por firewall
- ## Métodos de API Disponibles
  - | Método | Descripción |
    |--------|-------------|
    | `logseq.Editor.createPage` | Crea una página nueva |
    | `logseq.Editor.getPage` | Lee una página por nombre |
    | `logseq.Editor.insertBlock` | Inserta un bloque en una página |
    | `logseq.Editor.updateBlock` | Actualiza un bloque existente |
    | `logseq.Editor.getAllPages` | Lista todas las páginas |
    | `logseq.App.getCurrentGraph` | Info del grafo actual |
    | `logseq.DB.q` | Query Datalog al grafo |
- ## Impacto por Agente
  - | Agente | Operaciones MCP usadas |
    |--------|----------------------|
    | validador-grafo | `getAllPages`, `getPage`, `DB.q` |
    | validador-negocio | `getPage`, `DB.q` |
    | analizador-requerimientos | `createPage`, `insertBlock` |
    | desarrollador | `getPage` (lectura de spec) |
    | documentador | `createPage`, `updateBlock`, `insertBlock` |
    | orquestador | `getCurrentGraph` (verificación de estado) |
- ## Verificación de Conexión
  - ```bash
    # Test rápido de conexión
    curl -X POST http://localhost:12315/api \
      -H "Authorization: Bearer <token>" \
      -H "Content-Type: application/json" \
      --data-raw '{"method":"logseq.App.getCurrentGraph","args":[]}'
    ```
  - Respuesta esperada: `{"url":"logseq_local_...","name":"graphdev","path":"C:/Dev/graphdev"}`
- ## Referencias
  - [[Agentes-y-Skills]] — Qué agentes usan el MCP y cómo
  - [[Protocolo-Orquestador]] — El orquestador coordina el acceso al MCP
  - [[README-Metodologia]] — Índice principal
