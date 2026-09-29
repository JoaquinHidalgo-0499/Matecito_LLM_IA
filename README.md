# LLM Wiki Engine & Copiloto Técnico (`braind`)

Infraestructura integral y modular para la administración autónoma de una Base de Conocimiento personal (LLM Wiki / Second Brain), compilación de artefactos de ingeniería y orquestación con Google Antigravity y Homelab.

---

## 📁 Arquitectura del Workspace

El repositorio implementa una separación estricta entre motor ejecutable, base de conocimiento viva, entregables finales y repositorios de solo lectura:

### 1. Núcleo Documental y Grafo de Conocimiento (`brain/`)
Bóveda de notas interconectadas en Markdown estándar con hipervínculos bidireccionales `[[wikilinks]]`:
* **`conceptos/`**: Unidades teóricas atómicas y compendios temáticos de ingeniería.
* **`recursos/`**: Fichas de infraestructura, inventario de hardware/taller, servidores MCP y guías operativas.
* **`sesiones/`**: Bitácoras cronológicas de jornadas de desarrollo con secciones obligatorias (`## Contexto`, `## Decisiones`, `## Pendientes`).
* **`apuntes/`**: Tratados académicos, guías maestras de estudio y compendios por materia universitaria.
* **`adjuntos/`**: Activos multimedia y esquemas referenciados por las notas.
* **Índices y Tableros:**
  * `index.md`: Índice maestro y punto de entrada al grafo de conocimiento.
  * `index-sesiones.md`: Archivo histórico completo de sesiones de trabajo.
  * `index-csyt.md` / `index-oeymn.md`: Subíndices temáticos por asignatura académica.
  * `Tablero-Pendientes.md` / `Tablero-Pendientes-Archivo.md`: Sistema de gestión y seguimiento de tareas consolidadas.

### 2. Salida y Entrega de Artefactos (`archivos-generados/`)
Directorio exclusivo para alojar entregables solicitados por el usuario. Mantiene una jerarquía plana por proyecto (`<proyecto>/`):
* Documentos técnicos y guías de estudio compiladas en LaTeX (`.tex` y `.pdf`).
* Entregables de código final y firmwares para microcontroladores (CircuitPython/KMK).
* No contiene herramientas de soporte ni scripts temporales del asistente.

### 3. Bandeja de Entrada (`Clippings/`)
Receptor de capturas web, artículos o notas móviles para su posterior catalogación y síntesis hacia `brain/` mediante la skill `ingest-clipping` bajo la directriz de **Inbox Zero**.

### 4. Habilidades Agénticas y Seguridad (`.agents/`)
* **Skills Especializadas (`.agents/skills/`):**
  * `brain-audit`: Auditoría de integridad, detección de enlaces rotos y cálculo de métricas del grafo.
  * `ingest-materia`: Ingesta y estructuración de contenido académico universitario.
  * `ingest-resource`: Registro técnico de infraestructura, hardware, servidores y fichas de equipamiento.
  * `ingest-session`: Documentación estructurada de jornadas de desarrollo y bitácoras técnicas.
  * `ingest-clipping`: Procesamiento y vaciado de notas en bandeja de entrada hacia la base de conocimiento.
  * `latex-compiler`: Maquetación y compilación de documentos profesionales en PDF mediante `pdflatex`.
* **Hooks de Ciclo de Vida (`hooks.json`):**
  * `protect_readonly.py` (`PreToolUse`): Bloqueo activo de comandos destructivos y escrituras sobre `~/Compartido/material-academico/`.
  * `fix_backticks.py` (`PostToolUse`): Saneamiento automático de wikilinks con comillas invertidas preservando bloques de código.

### 5. Herramientas Operativas Residentes (`scripts/`)
Utilidades centralizadas en Python para administración y validación del workspace:
* `brain-lint.py`: Validador estricto de Frontmatter YAML, vocabulario controlado de tags, enlaces rotos e indexación.
* `brain-stats.py`: Analizador de métricas de red, densidad del grafo, volumen léxico y topología de hubs.
* `escanear-materias.py`: Escáner de novedades y control de cambios en repositorios académicos de referencia.
* `consolidar-pendientes.py`: Agrupador y consolidador cronológico de tareas pendientes desde las sesiones de trabajo.

### 6. Esquema Operacional (`GEMINI.md`)
Reglas rectoras del asistente, principio de honestidad radical y anti-complacencia, directrices de manipulación de archivos y criterios RAG-First con el servidor Homelab.

---

## 🔄 Modelo de Sincronización y Persistencia Híbrida

* **Control de Versiones (Git):** Resguarda y versiona el motor de ejecución, directrices del copiloto, hooks, skills y scripts operativos (`.agents/`, `scripts/`, `GEMINI.md`, `README.md`).
* **Sincronización en Tiempo Real (Syncthing):** Las carpetas de datos dinámicos (`brain/`, `archivos-generados/`, `Clippings/`) se replican de forma continua y bidireccional entre la estación local y el servidor personal (`192.168.20.200`).
