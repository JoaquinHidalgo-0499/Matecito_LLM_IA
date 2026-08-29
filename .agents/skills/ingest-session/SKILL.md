---
name: ingest-session
description: >-
  Usa este skill cuando el usuario pida registrar, documentar, resumir o ingestar
  una sesión de trabajo, bitácora técnica, avance de proyecto o jornada de desarrollo
  hacia la base de conocimiento en brain/sesiones/.
---

# Ingesta y Registro de Sesiones de Trabajo

Procedimiento maestro para documentar jornadas de trabajo, sesiones de desarrollo, mantenimiento de homelab o avances de proyectos en `/brain/sesiones/`.

---

## 1. Nomenclatura del Archivo
Cada archivo de sesión debe ubicarse en `/home/joaquin/Compartido/braind/brain/sesiones/` y seguir estrictamente el patrón:
```
/home/joaquin/Compartido/braind/brain/sesiones/AAAA-MM-DD-nombre-corto.md
```
* **Fecha:** Debe corresponder a la fecha local del sistema (ej: `2026-08-23`).
* **Nombre corto:** Identificador en minúsculas separado por guiones (kebab-case) que resuma el foco principal de la jornada.

---

## 2. Frontmatter YAML Estricto
El archivo debe comenzar obligatoriamente con el bloque Frontmatter para notas de sesión:

```yaml
---
type: session
date: AAAA-MM-DD
title: "Título descriptivo y técnico de la sesión"
tags: [tag1, tag2, ingesta]
status: active
---
```

### Reglas Críticas de Metadatos:
* **Campos obligatorios:** `type`, `date`, `title`, `tags`, `status`.
* **Vocabulario Controlado de Tags:** Usar siempre formas canónicas. Prohibido usar `ingest` (usar `ingesta`) o `clipping` (usar `clippings`).
* **Formato de Enlaces:** Prohibido envolver wikilinks en backticks (usar siempre `[[enlace]]`, NUNCA `` `[[enlace]]` ``).

---

## 3. Estructura Obligatoria del Contenido
Toda nota de sesión debe estructurarse con las siguientes 3 secciones de nivel 2:

```markdown
## Contexto
- Qué motivó la sesión, qué problema se abordó o qué requerimiento solicitó el usuario.
- Antecedentes técnicos o estado previo del sistema.

## Decisiones
- Registro técnico de las acciones tomadas, arquitectura diseñada, bugs corregidos o configuraciones aplicadas.
- Fragmentos de configuración clave, comandos ejecutados o archivos modificados.
- Enlaces con [[wikilinks]] a conceptos o recursos relacionados.

## Pendientes
- Tareas restantes, pruebas pendientes o siguientes pasos a seguir en futuras sesiones.
```

---

## 4. Indexación en `index.md`
Toda nota de sesión creada debe agregarse inmediatamente a `/home/joaquin/Compartido/braind/brain/index.md`:
1. Ubicar la sección correspondiente bajo `## Sesiones de Trabajo`.
2. Insertar una nueva línea en la lista cronológica con el formato:
   ```markdown
   * [[AAAA-MM-DD-nombre-corto]] — Descripción concisa de los hitos logrados en la sesión.
   ```
3. Realizar la edición mediante `replace_file_content` de forma precisa sin alterar el resto del archivo.

---

## 5. Validación Final de Salud
Al finalizar la creación e indexación de la sesión, ejecutar el auditor oficial para certificar la salud del grafo:
```bash
python3 /home/joaquin/Compartido/braind/scripts/brain-lint.py
```
* **Veredicto esperado:** Exit code `0` (Cerebro 100% saludable). Si arroja observaciones, corregirlas de inmediato.
