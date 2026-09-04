---
name: ingest-clipping
description: Procesamiento de archivos de la bandeja de entrada Clippings/ hacia la base de conocimiento (Inbox Zero).
---

# Skill: ingest-clipping

## Propósito
Este skill define el protocolo estándar para procesar archivos Markdown ubicados en la carpeta `Clippings/` e integrarlos adecuadamente en el cerebro (`/brain/`). El objetivo es mantener la carpeta `Clippings/` vacía (Inbox Zero).

## Protocolo de Procesamiento

1. **Inspección del Clipping Crudo:** Leer el archivo original en `Clippings/` para entender su contenido y contexto.
2. **Depuración de Artefactos Web:** Limpiar el contenido eliminando elementos basura provenientes de la captura web, como:
   - Menús de navegación.
   - Pies de página.
   - Scripts o código incrustado irrelevante.
   - Números de plantilla o artefactos visuales.
3. **Decisión de Destino:** Determinar el tipo de nota adecuado según el contenido sintetizado:
   - Si es un concepto académico, idea o teoría: Mover a `brain/conceptos/` con `type: concept`.
   - Si es un recurso, curso, herramienta o material de referencia: Mover a `brain/recursos/recursos-*.md` con `type: resource`.
4. **Frontmatter YAML Canónico:** Aplicar el frontmatter obligatorio a la nueva nota.
   *Para notas de concepto:*
   ```yaml
   ---
   type: concept
   title: "Título descriptivo"
   tags: [etiquetas]
   ---
   ```
   *Para notas de recurso:*
   ```yaml
   ---
   type: resource
   title: "Título descriptivo"
   tags: [etiquetas]
   ---
   ```
5. **Indexación Obligatoria:** Agregar el enlace `[[nombre-de-la-nueva-nota]]` junto a su descripción en la sección correspondiente de `/brain/index.md` de forma inmediata.
6. **Inbox Zero (Eliminación):** Eliminar el archivo procesado de `Clippings/`. Si la carpeta queda vacía, asegurar que exista el archivo `.gitkeep` para mantenerla en el repositorio.
7. **Validación:** Ejecutar siempre el linter `python3 scripts/brain-lint.py` al finalizar para confirmar la salud del cerebro.

## Restricciones
- Respetar la normalización de tags canónicos: usar siempre `ingesta` (no `ingest`) y `clippings` (no `clipping`).
- No usar acentos graves (backticks) alrededor de los wikilinks (ej: usar `[[enlace]]` y no \`[[enlace]]\`).
- No usar `cat << EOF` para crear archivos en `braind/`. Usar siempre la herramienta `write_to_file`.
