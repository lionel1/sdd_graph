tipo:: referencia
estado:: activo
version:: 1.0
capa:: proyecto

- # Estimación de Tokens y Costos
- ## Supuestos del Modelo
  - Modelo base: Claude Sonnet 4.6 (`claude-sonnet-4-6`)
  - Precios (aproximados, verificar en console.anthropic.com):
    - Input: $3 / MTok
    - Output: $15 / MTok
    - Cache write: $3.75 / MTok
    - Cache read: $0.30 / MTok
- ## Tabla Comparativa de Escenarios
  - | Escenario | Input tokens | Output tokens | Cache hit | Costo por sesión |
    |-----------|-------------|---------------|-----------|-----------------|
    | **Sin cache, sesión corta** | 10k | 2k | 0% | ~$0.060 |
    | **Sin cache, sesión larga** | 50k | 10k | 0% | ~$0.300 |
    | **Con cache, sesión corta** | 10k | 2k | 80% | ~$0.018 |
    | **Con cache, sesión larga** | 50k | 10k | 80% | ~$0.090 |
    | **Multi-agente, sin cache** | 100k | 20k | 0% | ~$0.600 |
    | **Multi-agente, con cache** | 100k | 20k | 80% | ~$0.180 |
  - *Cache hit estimado del 80% cuando el system prompt es estable entre sesiones.*
- ## Impacto del Prompt Caching
  - El system prompt del orquestador (~5k tokens) se cachea tras la primera llamada.
  - Ahorro estimado: **70% del costo de input** en sesiones con múltiples turnos.
  - Condición: el system prompt no debe cambiar entre llamadas (ver [[Protocolo-Orquestador]]).
- ## Proyección Anual
  - | Uso estimado | Sesiones/día | Costo/día | Costo/mes | Costo/año |
    |-------------|-------------|-----------|-----------|-----------|
    | Uso ligero | 2 | ~$0.04 | ~$1.20 | ~$14 |
    | Uso moderado | 5 | ~$0.20 | ~$6.00 | ~$72 |
    | Uso intensivo | 15 | ~$0.80 | ~$24.00 | ~$288 |
  - *Todos los escenarios asumen prompt caching activo.*
- ## Umbral de Alerta
  - El orquestador debe escalar al humano si el costo proyectado de la sesión supera **$2.00**.
  - Este umbral corresponde a una sesión de ~330k tokens de input sin cache.
  - Ver condición de escalamiento en [[Protocolo-Orquestador]].
- ## Optimizaciones Implementadas
  - **Prompt caching**: System prompts estables en todos los agentes (ver [[Manifiesto-SDD-Agentes]] P-007)
  - **Agentes especializados**: Cada agente recibe solo el contexto relevante a su dominio, reduciendo tokens de input
  - **Lectura MCP en lugar de contexto**: Los agentes leen specs del grafo via MCP en lugar de incluirlas todas en el prompt
- ## Referencias
  - [[Protocolo-Orquestador]] — Condición de escalamiento por costo
  - [[Agentes-y-Skills]] — Consumo por agente
  - [[README-Metodologia]] — Índice principal
