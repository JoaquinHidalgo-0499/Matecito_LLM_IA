---
name: brain-audit
description: >-
  Usa este skill cuando el usuario pida validar, auditar o verificar la salud
  de su Base de Conocimiento (brain). Se activa con palabras clave como: lint,
  stats, auditoría, salud del cerebro, escanear materias, verificar notas.
  Ejecuta los scripts residentes en scripts/ y reporta resultados estructurados.
---

# Brain Audit — Auditoría Integral de la Base de Conocimiento

Procedimiento estandarizado para auditar la salud, integridad y métricas del
grafo de conocimiento personal en `/brain/`.

## Herramientas Disponibles

| Script | Ubicación | Propósito |
|---|---|---|
| `brain-lint.py` | `scripts/brain-lint.py` | Validación de enlaces, YAML, indexación, tags y wikilinks |
| `brain-stats.py` | `scripts/brain-stats.py` | Métricas del grafo: palabras, densidad, hubs, tags |
| `escanear-materias.py` | `scripts/escanear-materias.py` | Detección de archivos nuevos/modificados en materias académicas |
| `consolidar-pendientes.py` | `scripts/consolidar-pendientes.py` | Agrupación y consolidación cronológica de tareas pendientes desde las sesiones |

## Procedimiento

### 1. LINT (Validación de Salud)

Ejecutar siempre con el script residente. **Nunca generar código inline alternativo.**

```bash
python3 scripts/brain-lint.py
```

**Modos adicionales:**
- Diagnóstico con desglose por carpetas:
  ```bash
  python3 scripts/brain-lint.py -v
  ```
- Autocorrección masiva de tags no canónicos (plural español obligatorio):
  ```bash
  python3 scripts/brain-lint.py --fix-tags
  ```
- Salida estructurada (JSON) para integraciones:
  ```bash
  python3 scripts/brain-lint.py --json
  ```

**Interpretación de resultados:**
- `exit 0` → Cerebro 100% saludable. Reportar al usuario con resumen breve.
- `exit 1` → Se detectaron observaciones. Analizar la salida y corregir:
  - **Notas no indexadas:** Agregar los wikilinks faltantes a `brain/index.md` (o subíndice temático).
  - **Enlaces rotos:** Verificar si la nota destino fue renombrada o eliminada. Corregir el wikilink o crear la nota faltante.
  - **Wikilinks con backticks:** Eliminar los backticks del wikilink afectado (o dejar que el hook `fix_backticks.py` lo sanee al guardar).
  - **Errores de YAML:** Corregir el frontmatter del archivo afectado según las reglas de `GEMINI.md`.
  - **Tags no canónicos:** Ejecutar `python3 scripts/brain-lint.py --fix-tags` para normalizarlos automáticamente a su forma plural canónica.
  - **Sesiones incompletas (`session_warnings`):** Asegurar que las notas en `brain/sesiones/` contengan las 3 secciones obligatorias: `## Contexto`, `## Decisiones`, `## Pendientes`.

### 2. STATS (Métricas del Grafo)

```bash
python3 scripts/brain-stats.py
```

**Qué reportar al usuario:**
- Total de notas, palabras netas y tamaño en disco.
- Distribución por categorías (conceptos/sesiones/recursos/apuntes).
- Top hubs de conocimiento (nodos más referenciados).
- Top etiquetas temáticas — **verificar si hay tags duplicados semánticos** según la tabla de Normalización de Tags en `GEMINI.md`.
- Densidad del grafo.

Para salida JSON:
```bash
python3 scripts/brain-stats.py --json
```

### 3. ESCANEAR MATERIAS (Novedades Académicas)

```bash
python3 scripts/escanear-materias.py
```

**Interpretación:**
- Si hay archivos nuevos o modificados, reportar al usuario agrupados por materia.
- Si el usuario confirma, actualizar el manifiesto:
  ```bash
  python3 scripts/escanear-materias.py --update
  ```
- **Nunca modificar los archivos de materias.** La ruta `~/Compartido/material-academico/` es estrictamente de SOLO LECTURA.

### 4. CONSOLIDACIÓN DE PENDIENTES

Extrae y centraliza las tareas pendientes de las notas de sesiones:

```bash
python3 scripts/consolidar-pendientes.py
```

**Interpretación:**
- Genera el tablero `Tablero-Pendientes.md` con los ítems agrupados por fecha y referenciando a su nota origen.
- `Tablero-Pendientes.md` actúa como un subíndice válido reconocido automáticamente por `brain-lint.py`.
- Admite argumentos como `--output` para cambiar el destino y `--json` para uso programático.

### 5. AUDITORÍA COMPLETA

Cuando el usuario pida una auditoría completa o "revisión general", ejecutar en secuencia:

1. `brain-lint.py` → Salud estructural
2. `brain-stats.py` → Métricas y tendencias
3. `escanear-materias.py` → Novedades académicas pendientes
4. `consolidar-pendientes.py` → Consolidación de tareas

Presentar un reporte consolidado con las secciones.

## Reglas Críticas

- **Nunca generar scripts Python inline** para hacer lo que estos scripts ya hacen.
- **Nunca usar `cat << EOF`** para archivos dentro de `braind/`. Usar las herramientas nativas (`write_to_file`, `replace_file_content`).
- Si un script falla, **leer el error y corregir el script residente**, no improvisar un reemplazo temporal.
- Si se detectan tags no canónicos durante STATS o LINT, usar `python3 scripts/brain-lint.py --fix-tags`.
