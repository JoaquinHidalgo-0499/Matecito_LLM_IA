---
name: ingest-resource
description: >-
  Usa este skill cuando el usuario pida registrar, documentar, catalogar o ingestar
  recursos técnicos, inventario de hardware/taller, infraestructura de red, servidores homelab,
  fichas de equipamiento o guías operativas hacia la base de conocimiento en brain/recursos/.
---

# Ingesta y Registro de Recursos Técnicos

Procedimiento maestro para documentar infraestructura, inventario de hardware/taller, servidores homelab, fichas de equipamiento o manuales operativos en `/brain/recursos/`.

---

## 1. Ubicación y Nomenclatura del Archivo

Cada archivo de recurso debe ubicarse en `/home/joaquin/Compartido/braind/brain/recursos/` y seguir estrictamente la convención de nomenclatura:

```
/home/joaquin/Compartido/braind/brain/recursos/recursos-<identificador-kebab-case>.md
```
o en subcarpetas temáticas ya estructuradas (ej: `/brain/recursos/<materia>/recursos-...md` o `/brain/recursos/<materia>/<nombre>.md`).

* **Identificador:** Cadena en minúsculas separada por guiones (`kebab-case`) que describa unívocamente el equipo, servidor, componente, proyecto o recurso documentado.

---

## 2. Frontmatter YAML Estricto

El archivo debe comenzar obligatoriamente con el bloque Frontmatter para notas de recurso:

```yaml
---
type: resource
title: "Título descriptivo y técnico del recurso o equipamiento"
tags: [recursos, categoria, tag-especifico]
---
```

### Reglas Críticas de Metadatos:
* **Campos obligatorios:** `type`, `title`, `tags`.
* **Valor de Type:** Debe ser estrictamente `type: resource`.
* **Campos Prohibidos:** Está terminantemente **prohibido** incluir los campos `date` o `status` en notas de tipo recurso (el linter `brain-lint.py` arrojará error si están presentes).
* **Vocabulario Controlado de Tags:** Usar siempre formas canónicas de `GEMINI.md`. Prohibido usar `ingest` (usar `ingesta`) o `clipping` (usar `clippings`).
* **Formato de Enlaces:** Prohibido envolver wikilinks en backticks (usar siempre `[[enlace]]`, NUNCA `` `[[enlace]]` ``).

---

## 3. Estructura Recomendada del Contenido

Toda nota de recurso debe estar bien organizada y documentada según su tipología técnica:

```markdown
# [Título del Recurso / Ficha Técnica]

Resumen técnico del recurso, propósito dentro del ecosistema/homelab/taller y contexto de uso.

---

## 1. Especificaciones Técnicas / Topología / Inventario
- Características de hardware, especificaciones de componentes, esquemas de red o inventario de piezas.
- Se recomienda el uso de diagramas Mermaid (`mermaid`) para topologías de red o arquitectura de servidores.
- Tablas comparativas o de inventario en Markdown estándar cuando aplique.

## 2. Configuración y Operación
- Fragmentos de configuración clave (`docker-compose.yml`, scripts de despliegue, firmware o parámetros de configuración).
- Rutas locales, direcciones IP, puertos de red o credenciales genéricas del servicio.

## 3. Referencias y Enlaces Vinculados
- Enlaces mediante [[wikilinks]] a conceptos teóricos, notas de sesiones de mantenimiento o cátedras relacionadas.
```

---

## 4. Indexación en `index.md`

Toda nota de recurso creada debe indexarse de forma inmediata en `/home/joaquin/Compartido/braind/brain/index.md`:
1. Ubicar la sección correspondiente:
   - `## Planificación y Cronogramas` (para recursos de homelab, taller, hardware o servicios).
   - O bajo la sección de la cátedra específica si el recurso es de ámbito académico (ej: `ACP`, `CSyT`, etc.).
2. Insertar una nueva línea en la lista con el formato:
   ```markdown
   * [[recursos-nombre-del-archivo]] — **Título o Resumen en Negrita** (Breve descripción técnica).
   ```
3. Realizar la edición mediante la herramienta nativa `replace_file_content` sin alterar el resto del documento.

---

## 5. Validación Final de Salud

Al finalizar la creación e indexación del recurso, certificar la integridad del grafo ejecutando el linter oficial:

```bash
python3 /home/joaquin/Compartido/braind/scripts/brain-lint.py
```

* **Veredicto esperado:** Exit code `0` (Cerebro 100% saludable). Si se detectan observaciones o enlaces rotos, corregirlos inmediatamente.
