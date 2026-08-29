# LLM Wiki Engine: Skills, Scripts & System Prompt

Infraestructura modular para la administración autónoma de una Base de Conocimiento personal (LLM Wiki / Second Brain) basada en Markdown, Wikilinks y Antigravity.

---

## 📁 Estructura del Repositorio

* **`GEMINI.md`**: Reglas de operación, modos de trabajo (Ingest, Query, Lint), directrices de calidad y vocabulario controlado de tags.
* **`.agents/skills/`**: Skills especializadas del asistente:
  * `brain-audit`: Auditoría de integridad, detección de enlaces rotos y cálculo de métricas del grafo.
  * `ingest-materia`: Ingesta y estructuración de contenido académico universitario.
  * `ingest-resource`: Registro técnico de infraestructura, hardware, servidores y fichas de equipamiento.
  * `ingest-session`: Documentación estructurada de jornadas de desarrollo y bitácoras técnicas.
  * `latex-compiler`: Maquetación y compilación de documentos profesionales y guías compactas en PDF mediante LaTeX (`pdflatex`).
* **`scripts/`**: Herramientas nativas en Python para mantenimiento y auditoría:
  * `brain-lint.py`: Validador estricto de Frontmatter YAML, normalización de tags y resolución de wikilinks.
  * `brain-stats.py`: Generador de estadísticas, densidad del grafo y topología de hubs.
  * `escanear-materias.py`: Escáner en modo sólo lectura para sincronización de repositorios académicos.
