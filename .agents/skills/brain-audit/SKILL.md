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
| `brain-lint.py` | `/home/joaquin/Compartido/braind/scripts/brain-lint.py` | Validación de enlaces, YAML, indexación y wikilinks |
| `brain-stats.py` | `/home/joaquin/Compartido/braind/scripts/brain-stats.py` | Métricas del grafo: palabras, densidad, hubs, tags |
| `escanear-materias.py` | `/home/joaquin/Compartido/braind/scripts/escanear-materias.py` | Detección de archivos nuevos/modificados en materias académicas |

## Procedimiento

### 1. LINT (Validación de Salud)

Ejecutar siempre con el script residente. **Nunca generar código inline alternativo.**

```bash
python3 /home/joaquin/Compartido/braind/scripts/brain-lint.py
```

**Interpretación de resultados:**
- `exit 0` → Cerebro 100% saludable. Reportar al usuario con resumen breve.
- `exit 1` → Se detectaron observaciones. Analizar la salida y:
  - **Notas no indexadas:** Agregar los wikilinks faltantes a `brain/index.md`.
  - **Enlaces rotos:** Verificar si la nota destino fue renombrada o eliminada. Corregir el wikilink o crear la nota faltante.
  - **Wikilinks con backticks:** Eliminar los backticks del wikilink afectado.
  - **Errores de YAML:** Corregir el frontmatter del archivo afectado según las reglas de `GEMINI.md`.

Para salida estructurada (JSON) usable por integraciones:
```bash
python3 /home/joaquin/Compartido/braind/scripts/brain-lint.py --json
```

### 2. STATS (Métricas del Grafo)

```bash
python3 /home/joaquin/Compartido/braind/scripts/brain-stats.py
```

**Qué reportar al usuario:**
- Total de notas, palabras netas y tamaño en disco.
- Distribución por categorías (conceptos/sesiones/recursos).
- Top hubs de conocimiento (nodos más referenciados).
- Top etiquetas temáticas — **verificar si hay tags duplicados semánticos** según la tabla de Normalización de Tags en `GEMINI.md`.
- Densidad del grafo.

Para salida JSON:
```bash
python3 /home/joaquin/Compartido/braind/scripts/brain-stats.py --json
```

### 3. ESCANEAR MATERIAS (Novedades Académicas)

```bash
python3 /home/joaquin/Compartido/braind/scripts/escanear-materias.py
```

**Interpretación:**
- Si hay archivos nuevos o modificados, reportar al usuario agrupados por materia.
- Si el usuario confirma, actualizar el manifiesto:
  ```bash
  python3 /home/joaquin/Compartido/braind/scripts/escanear-materias.py --update
  ```
- **Nunca modificar los archivos de materias.** Las rutas `~/Compartido/material-Materias/`, `~/Compartido/1er_Cuatrimestre/` y `~/Compartido/2do_Cuatrimestre/` son estrictamente de SOLO LECTURA.

### 4. AUDITORÍA COMPLETA

Cuando el usuario pida una auditoría completa o "revisión general", ejecutar los tres en secuencia:

1. `brain-lint.py` → Salud estructural
2. `brain-stats.py` → Métricas y tendencias
3. `escanear-materias` → Novedades académicas pendientes

Presentar un reporte consolidado con las tres secciones.

## Reglas Críticas

- **Nunca generar scripts Python inline** para hacer lo que estos scripts ya hacen.
- **Nunca usar `cat << EOF`** para archivos dentro de `braind/`. Usar las herramientas nativas (`write_to_file`, `replace_file_content`).
- Si un script falla, **leer el error y corregir el script residente**, no improvisar un reemplazo temporal.
- Si se detectan tags no canónicos durante STATS, corregirlos según la tabla de Normalización en `GEMINI.md`.
