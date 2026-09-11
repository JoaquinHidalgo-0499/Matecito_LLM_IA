---
name: ingest-materia
description: >-
  Usa este skill cuando el usuario pida procesar, escanear, resumir o ingestar material
  académico nuevo de una materia (PDFs, PPTs, código) hacia la base de conocimiento.
---

# Ingesta de Materia Académica

Procedimiento maestro para procesar archivos crudos de la facultad y convertirlos en notas de conocimiento estructuradas dentro del Brain.

## Procedimiento Paso a Paso

### 1. Escaneo y Clasificación (Modo Seguro)
- Accede al directorio indicado por el usuario, típicamente en `~/Compartido/material-Materias/<materia>/`, `1er_Cuatrimestre/` o `2do_Cuatrimestre/`.
- **REGLA ABSOLUTA:** Estas rutas son estrictamente de **SOLO LECTURA**. NUNCA debes modificar, mover, renombrar o borrar archivos originales allí.
- Identifica los archivos clave: PDFs (teoría), PPTX (presentaciones), Código (.py, .c, .java) y enunciados de parciales/TPs.

### 1.1. Consulta Previa al RAG (Grounded Generation)
- Para materias indexadas en el servidor MCP `rag-materias`:
  - Ejecutar `buscar_bibliografia` y `leer_pagina_completa` para recuperar la terminología oficial, analogías pedagógicas y taxonomías evaluadas por los docentes de la cátedra.
  - Citar de forma transparente en la respuesta al usuario los documentos y páginas recuperados por el RAG.
  - Si el RAG no estuviera accesible por red o falta de cobertura, continuar con el conocimiento local advirtiendo el fallback.

### 2. Creación de Notas Conceptuales
- Por cada unidad, módulo o tema principal procesado, crea un archivo en:
  `/home/joaquin/Compartido/braind/brain/conceptos/<siglamateria>-u<numero>-<tema-corto>.md`
- Aplica estrictamente el Frontmatter YAML para "Notas de Concepto" definido en `GEMINI.md`:
  ```yaml
  ---
  type: concept
  title: "Título descriptivo de la unidad"
  tags: [siglamateria, unju, concepto]
  ---
  ```
- **Nota:** No incluyas los campos `date` ni `status` en notas de concepto, el linter de la bóveda fallará si los pones o si omites los 3 campos obligatorios (`type`, `title`, `tags`).
- **Profundidad Académica:** Si el texto fuente contiene algoritmos, demostraciones matemáticas o código complejo, invoca un **Subagente PRO** (`invoke_subagent` con `Model: pro`) para que redacte el resumen con máxima precisión conceptual (First-Time Right).

### 3. Creación de Apuntes, Compendios y Bancos de Ejercicios
- Si el material contiene compendios de estudio para exámenes, tratados integrales, bancos de ejercicios/parciales, cuestionarios o guías de laboratorio de cátedra, créalos en:
  `/home/joaquin/Compartido/braind/brain/apuntes/<siglamateria>-<nombre-descriptivo>.md`
- Aplica estrictamente el Frontmatter YAML para "Notas de Apunte" definido en `GEMINI.md`:
  ```yaml
  ---
  type: apunte
  title: "Título descriptivo del apunte, tratado o banco de examen"
  tags: [siglamateria, unju, apunte]
  ---
  ```
- **Nota:** Al igual que en conceptos, no incluyas campos `date` ni `status`. El linter validará que tenga `type: apunte` por residir en `apuntes/`.

### 4. Indexación
- Todo archivo creado debe ser agregado al índice central.
- Edita `/home/joaquin/Compartido/braind/brain/index.md` insertando el wikilink `[[nombre-del-archivo-sin-md]]` en la categoría correspondiente a la materia.
- **Importante:** Nunca uses acentos graves (backticks) alrededor de los wikilinks. (Usa `[[nota]]`, NO `\`[[nota]]\``).

### 5. Validación Final de Tags
- Revisa las etiquetas asignadas en el YAML.
- Aplica el vocabulario controlado de `GEMINI.md` (ej: usa siempre `ingesta`, prohibido usar `ingest`).

### 6. Cierre
- Termina la operación ejecutando el LINT de la bóveda para garantizar que la nueva ingesta no rompió nada:
  `python3 /home/joaquin/Compartido/braind/scripts/brain-lint.py`
