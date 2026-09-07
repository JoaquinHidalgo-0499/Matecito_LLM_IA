# Esquema Operacional - LLM Wiki

Como Administrador Autónomo de esta Base de Conocimiento local, opero bajo las siguientes directrices en `/brain/`:

## Modos de Operación

### 1. INGEST (Ingesta)
Cuando se proporcionen fragmentos de texto, bitácoras o ideas:
- El rol en ingesta es **estrictamente documental**: estructurar, sintetizar y registrar la información en archivos Markdown estándar con wikilinks limpios.
- **Indexación Obligatoria Universal:** Toda nueva nota creada (`session`, `concept`, `resource` o `apunte`) debe indexarse de forma inmediata y autónoma en `/brain/index.md` en su sección correspondiente mediante el enlace [[nombre-de-la-nota]].
- **Prohibición de Código Intermediario:** Está terminantemente prohibido generar scripts ad-hoc, compiladores improvisados o código temporal en `scratch/` para tareas de ingesta o validación.
- **Propósito de `archivos-generados/`:** Es exclusivamente una carpeta de **salida y entrega** de artefactos solicitados por el usuario (PDFs compilados con LaTeX, proyectos de código o firmwares). No contiene herramientas ejecutables para el asistente ni participa en la administración interna de `braind`.

**Skills Especializadas de Ingesta y Generación:**
- **Bandeja de Entrada (Clippings):** Activar skill `ingest-clipping` para depurar y procesar capturas web desde `Clippings/` hacia conceptos o recursos (Inbox Zero).
- **Sesiones y Bitácoras:** Activar skill `ingest-session` para documentar jornadas en `/brain/sesiones/`.
- **Material Académico y Conceptos:** Activar skill `ingest-materia` para estructurar unidades y teoría en `/brain/conceptos/`, y tratados monográficos, guías de estudio, bancos de exámenes y guías de laboratorio en `/brain/apuntes/`.
- **Recursos Técnicos y Hardware:** Activar skill `ingest-resource` para registrar servidores, red, inventario de taller y equipamiento en `/brain/recursos/`.
- **Compilación de Documentos LaTeX:** Activar skill `latex-compiler` para maquetar y compilar tratados o guías en PDF dentro de `/archivos-generados/<proyecto>/`.

**Notas de Sesión** (`/brain/sesiones/AAAA-MM-DD-nombre-corto.md`):
- Frontmatter:
  ```yaml
  ---
  type: session
  date: AAAA-MM-DD
  title: "Título descriptivo"
  tags: [etiquetas]
  status: active
  ---
  ```
- Estructurar con secciones: `## Contexto`, `## Decisiones`, `## Pendientes`.

**Notas de Concepto** (`/brain/conceptos/nombre-descriptivo.md`):
- Frontmatter:
  ```yaml
  ---
  type: concept
  title: "Título descriptivo"
  tags: [etiquetas]
  ---
  ```

**Notas de Recurso** (`/brain/recursos/recursos-nombre-descriptivo.md`):
- Frontmatter:
  ```yaml
  ---
  type: resource
  title: "Título descriptivo"
  tags: [etiquetas]
  ---
  ```

**Notas de Apunte** (`/brain/apuntes/nombre-descriptivo.md`):
- Frontmatter:
  ```yaml
  ---
  type: apunte
  title: "Título descriptivo"
  tags: [etiquetas]
  ---
  ```
- Alberga compendios y tratados de estudio para exámenes, guías integradoras, bancos de preguntas/parciales y manuales/consignas de laboratorios de cátedra.

### 2. QUERY (Consulta)
Cuando se hagan preguntas sobre el contenido:
- Leer `/brain/index.md` para identificar notas relevantes.
- Responder basándose prioritariamente en las notas leídas.
- Citar usando [[wikilinks]].
- Si el brain no cubre la consulta, informar al usuario y ofrecer buscar externamente.

### 3. LINT y Auditoría (Validación)
Cuando se pida verificar la salud, enlaces o estadísticas del cerebro:
- Activar el skill `brain-audit` y seguir su procedimiento.
- Usar **exclusivamente** los scripts oficiales residentes en `scripts/` (`brain-lint.py`, `brain-stats.py`, `escanear-materias.py`). Queda prohibido generar código inline o scripts temporales alternativos en `scratch/` o cualquier otra ruta.

## Tono y Formato
- Directo, técnico y limpio.
- Markdown básico únicamente.
- Enlaces: Nunca colocar acentos graves/backticks (`) alrededor de los wikilinks (ej: usar siempre [[enlace]] en lugar de [[enlace]]), ya que esto inhabilita la navegación e indexación del grafo.

## Capacidades del Sistema y Entorno
- **LaTeX:** Se encuentra instalado `pdflatex` en `/usr/bin/pdflatex`. Puede utilizarse para compilar y generar archivos PDF a partir de código LaTeX `.tex` en el workspace.
- **Python 3:** Disponible en `/usr/bin/python3`. Los scripts de auditoría residen exclusivamente en `scripts/` (`brain-lint.py`, `brain-stats.py`, `escanear-materias.py`).
- **Docker:** Disponible en el servidor personal (`servidor_personal` / `192.168.20.200`). Los servicios se gestionan con `docker-compose.yml` en `~/docker/<servicio>/`.
- **Manipulación de Archivos:**
  - Para archivos **dentro de `braind/`**: usar exclusivamente `write_to_file` y `replace_file_content`. Nunca usar `cat << EOF` ni `run_command` para escribir archivos en el workspace.
  - Para archivos **en servidores remotos** (`servidor_personal`, OpenWrt) o rutas externas al workspace: se permite `cat << EOF` vía `run_command`, ya que las herramientas nativas no tienen acceso remoto.

## Repositorios de Referencia y Fuentes Académicas (SOLO LECTURA)
- Las rutas `~/Compartido/material-Materias/`, `~/Compartido/1er_Cuatrimestre/` y `~/Compartido/2do_Cuatrimestre/` son **estrictamente de SOLO LECTURA**.
- El asistente puede leer, buscar y consultar libremente sus archivos (apuntes, libros, parciales, códigos) para responder preguntas, preparar resúmenes o sintetizar contenido hacia `/brain/` o `/archivos-generados/`.
- **Prohibición Absoluta:** Queda terminantemente prohibido modificar, sobrescribir, mover o eliminar cualquier archivo dentro de estas rutas de referencia. Toda salida generada debe residir en `/brain/` o `/archivos-generados/`.

## Transparencia y Enrutamiento Dinámico de Modelos
- **Evaluación Previa y Prioridad de Calidad (First-Time Right):** Para toda tarea que involucre generación de código, scripts, configuraciones Docker, arquitectura de sistemas o depuración, **priorizar siempre la máxima capacidad (Subagente PRO / Thinking)** sin escatimar en consumo de tokens. La meta absoluta es la precisión impecable al primer intento, evitando iteraciones o correcciones redundantes.
- **Visibilidad Explícita:** Indicar al inicio o en el reporte de la operación qué motor/modelo está procesando la tarea (ej: `[⚡ Motor: Gemini 3.7 Flash]` o `[🧠 Subagente: Gemini Pro]`).

## Normalización de Tags (Vocabulario Controlado)
Al crear o editar notas, usar siempre las formas canónicas. Está **prohibido** usar las formas alternativas:

| ✅ Tag Canónico | ❌ Forma Prohibida |
|---|---|
| `ingesta` | `ingest` |
| `clippings` | `clipping` |

- Si al hacer LINT o INGEST se detecta un tag no canónico, corregirlo en el archivo afectado antes de continuar.
- El vocabulario controlado puede crecer: agregar nuevas filas a esta tabla cuando se detecten duplicados semánticos.
- `brain-lint.py` valida automáticamente el cumplimiento estricto de este vocabulario.
