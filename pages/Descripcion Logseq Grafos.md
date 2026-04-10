tipo:: motivacion
estado:: activo
version:: 1.0
capa:: nucleo

-
- Logseq es un proyecto fascinante porque, a diferencia de otras herramientas, no usa una base de datos tradicional (como SQL) como fuente de la verdad, sino que su "base de datos" es **tu sistema de archivos**.
  
  Aquí te explico cómo funciona su sistema de persistencia y cómo logra esa magia de consultas rápidas sobre archivos planos:
- ### 1. La Fuente de la Verdad: Archivos Locales
  
  Logseq sigue una filosofía de **"Local-first"**. Cada vez que escribes algo, se guarda inmediatamente en archivos físicos:
- **Páginas y Diarios:** Se guardan como archivos `.md` (Markdown) o `.org` (Org-mode) en las carpetas `/pages` y `/journals`.
- **Pizarras (Whiteboards):** Se guardan como archivos `.edn` (Extensible Data Notation) en la carpeta `/whiteboards`. Este formato permite representar datos estructurados complejos que Markdown no maneja bien.
- **Tarjetas (Flashcards):** No son archivos separados; son bloques dentro de tus archivos Markdown marcados con la propiedad `#card`.
- ### 2. El "Cerebro": El Grafo y la Memoria Flash
  
  Para que Logseq pueda relacionar miles de archivos mediante hipervínculos `[[vínculo]]` sin volverse lento, utiliza una base de datos en memoria llamada **Datascript** (una implementación de Datalog para ClojureScript).
  
  Así es el proceso:
- **Indexación:** Cuando abres tu "Graph" (carpeta), Logseq escanea todos los archivos.
- **Parsing:** Lee el contenido de los Markdown y los convierte en un árbol de bloques. Cada párrafo, lista o tarea es un "bloque" con un ID único.
- **Carga en Memoria:** Toda esa estructura de relaciones (qué bloque menciona a qué página) se carga en la base de datos Datascript que vive en la RAM de tu computadora.
- ### 3. El Sistema de Consultas (Queries)
  
  Debido a que Logseq carga todo en Datascript, las consultas no buscan "texto" en los archivos cada vez que las ejecutas. En su lugar, consultan el índice en memoria.
- **Simple Queries:** Son una capa de abstracción fácil de usar.
- **Advanced Queries:** Usan directamente el lenguaje **Datalog**. Esto permite buscar relaciones complejas, como "dame todos los bloques creados hace 3 días que tengan el tag #proyecto y no estén terminados".
- ### 4. Sincronización y Persistencia (DB vs. Archivo)
  
  Aquí está el truco técnico: **Logseq mantiene una sincronización bidireccional**.
- Si escribes en la app, Logseq actualiza la base de datos en memoria y luego "serializa" ese cambio escribiendo en el archivo `.md`.
- Si editas el archivo `.md` con un editor externo (como Notepad++), Logseq detecta el cambio en el sistema de archivos (file watcher) y vuelve a indexar ese archivo específico para actualizar su grafo en memoria.
- ### 5. Metadatos y Configuración
  
  Todo lo que no es contenido puro (configuración de la UI, plugins instalados, etc.) se guarda en una carpeta oculta llamada `logseq/`. Allí encontrarás el archivo `config.edn`, que es el corazón de la personalización de ese grafo específico.
  
  **En resumen:** Logseq es un sistema de gestión de archivos Markdown que utiliza una base de datos de grafos en memoria (Datascript) como "caché inteligente" para permitir las relaciones y consultas rápidas. Tu trabajo siempre está seguro en archivos de texto plano, pero la experiencia de usuario es la de una base de datos relacional potente.