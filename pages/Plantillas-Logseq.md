tipo:: plantillas
estado:: activo
version:: 1.0
capa:: nucleo

- # Plantillas Logseq
  - Plantillas estándar del sistema SDD-Agentes. Todas las páginas nuevas deben usar una de estas plantillas.
- ## Plantilla README
  - **Uso**: Páginas de índice o documentación principal de un módulo.
  - ```
    tipo:: índice
    estado:: borrador
    version:: 1.0
    
    - # Título
      - Descripción del módulo o sección.
    - ## Contenido
      - [[Página 1]]
      - [[Página 2]]
    - ## Referencias
      - [[README-Metodologia]]
    ```
- ## Plantilla DOC
  - **Uso**: Documentación técnica o funcional detallada.
  - ```
    tipo:: documento-funcional
    estado:: borrador
    version:: 1.0
    
    - # Título del Documento
    - ## Contexto
      - Por qué existe este documento.
    - ## Contenido Principal
      - Desarrollo del tema.
    - ## Referencias
      - [[README-Metodologia]]
    ```
- ## Plantilla REQ
  - **Uso**: Requerimientos funcionales o no funcionales.
  - ```
    tipo:: requerimiento
    estado:: borrador
    version:: 1.0
    id:: REQ-XXX
    prioridad:: alta | media | baja
    
    - # REQ-XXX — Título del Requerimiento
    - ## Descripción
      - Qué debe hacer el sistema.
    - ## Criterios de Aceptación
      - [ ] Criterio 1
      - [ ] Criterio 2
    - ## Referencias
      - Spec origen: [[Página-de-Spec]]
    ```
- ## Plantilla RN
  - **Uso**: Release notes de una versión.
  - ```
    tipo:: release-notes
    estado:: borrador
    version:: X.Y.Z
    fecha:: YYYY-MM-DD
    
    - # Release Notes — vX.Y.Z
    - ## Novedades
      - feat: descripción
    - ## Correcciones
      - fix: descripción
    - ## Breaking Changes
      - Ninguno | descripción
    - ## Referencias
      - PR: [[Pipeline-Git]]
    ```
- ## Plantilla TASK
  - **Uso**: Tareas del backlog o trabajo en curso.
  - ```
    tipo:: tarea
    estado:: TODO
    version:: 1.0
    fase:: F-XX
    
    - # TASK-XXX — Título de la Tarea
    - ## Descripción
      - Qué hay que hacer.
    - ## Criterios de Done
      - [ ] Criterio 1
    - ## Spec de Referencia
      - [[Página-de-Spec]]
    ```
- ## Plantilla CONC
  - **Uso**: Conclusiones de análisis, retrospectivas o evaluaciones.
  - ```
    tipo:: conclusión
    estado:: borrador
    version:: 1.0
    fecha:: YYYY-MM-DD
    
    - # Conclusión — Título
    - ## Contexto
      - Qué se analizó o evaluó.
    - ## Hallazgos
      - Hallazgo 1
    - ## Decisión
      - Qué se decidió como resultado.
    - ## Referencias
      - [[Comparativa-SpecKit]]
    ```
- ## Plantilla DEC
  - **Uso**: Decision log para decisiones de arquitectura o diseño importantes.
  - ```
    tipo:: decision-log
    estado:: borrador
    version:: 1.0
    id:: DEC-XXX
    fecha:: YYYY-MM-DD
    
    - # DEC-XXX — Título de la Decisión
    - ## Contexto
      - Por qué se debió tomar esta decisión.
    - ## Opciones Evaluadas
      - Opción A
      - Opción B
    - ## Decisión
      - Se eligió X porque Y.
    - ## Consecuencias
      - Positivas: ...
      - Negativas: ...
    - ## Referencias
      - [[Manifiesto-SDD-Agentes]]
    ```
- ## Referencias
  - [[Manifiesto-SDD-Agentes]] — DD-006 establece el uso de plantillas
  - [[README-Metodologia]] — Índice principal
