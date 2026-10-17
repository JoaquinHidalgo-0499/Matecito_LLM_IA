// =========================================================================
// PLANTILLA MAESTRA: CURRÍCULUM VITAE EJECUTIVO COMPACTO (1 PÁGINA A4) - TYPST
// =========================================================================
// Características:
// - Formato 100% compatible con ATS (Applicant Tracking Systems) y flujo lineal.
// - Tipografía moderna Sans-Serif en escala real de 9pt.
// - Cero solapamientos: macro de sección determinista con línea horizontal nativa.
// - Presupuesto vertical riguroso: encaja exactamente en 1 sola página A4 sin desbordes.
// - Jerarquía cromática corporativa: Azul Marino Profundo (#0F2A5B) y Azul Tecnológico (#2563EB).
// =========================================================================

#set document(
  title: "Curriculum Vitae - [NOMBRE COMPLETO]",
  author: "[NOMBRE COMPLETO]",
)

#set page(
  paper: "a4",
  margin: (top: 0.7cm, bottom: 0.55cm, left: 1.15cm, right: 1.15cm),
  header: none,
  footer: none,
)

#set text(
  font: ("Liberation Sans", "Helvetica Neue", "Arial", "DejaVu Sans"),
  size: 9pt,
  fill: rgb("#1e293b"),
  lang: "es",
  region: "ar",
)

#set par(
  justify: true,
  leading: 0.35em,
  spacing: 0.45em,
)

#let primary = rgb("#0f2a5b")
#let secondary = rgb("#2563eb")
#let muted = rgb("#64748b")

#let cvsection(title) = {
  v(3pt)
  text(weight: "bold", size: 9.5pt, fill: primary)[#upper(title)]
  v(-3pt)
  line(length: 100%, stroke: 0.8pt + secondary)
  v(2pt)
}

#let cvitem(title: "", subtitle: "", date: "", loc: "", body) = {
  grid(
    columns: (1fr, auto),
    align: (left, right),
    [
      #text(weight: "bold", fill: rgb("#0f172a"))[#title]
      #if subtitle != "" [ --- #text(style: "italic", fill: rgb("#334155"))[#subtitle] ]
    ],
    [
      #text(size: 8pt, fill: muted)[#date #if loc != "" [| #loc]]
    ]
  )
  v(1pt)
  body
  v(2pt)
}

// ===============================================================================
// ENCABEZADO PRINCIPAL
// ===============================================================================

#align(center)[
  #text(size: 16pt, weight: "bold", fill: primary)[HUGO JOAQUÍN HIDALGO] \
  #v(1.5pt)
  #text(size: 8.5pt, weight: "bold", fill: rgb("#1e293b"))[LICENCIATURA EN SISTEMAS | ADMINISTRACIÓN DE INFRAESTRUCTURA Y DEVSECOPS] \
  #v(1.2pt)
  #text(size: 7.8pt, weight: "bold", fill: secondary)[LINUX / ARCH | DOCKER & CONTAINERS | PYTHON / AUTOMATIZACIÓN | REDES & HOMELAB] \
  #v(2.5pt)
  #text(size: 8pt)[
    San Salvador de Jujuy, Argentina (Remoto / Presencial) |
    #link("tel:+5493880000000")[(+54) 388-0000000] |
    #link("mailto:contacto@ejemplo.com")[contacto@ejemplo.com] \
    LinkedIn: #link("https://linkedin.com/in/joaquinhidalgo")[linkedin.com/in/joaquinhidalgo] |
    GitHub: #link("https://github.com/joaquinhidalgo")[github.com/joaquinhidalgo]
  ]
]

#v(-3pt)

// ===============================================================================
// PERFIL PROFESIONAL
// ===============================================================================

#cvsection("Perfil Profesional")
Estudiante avanzado de Licenciatura en Sistemas con sólida formación en arquitectura de computadoras, redes de datos, sistemas operativos POSIX y computación paralela. Especializado en gestión de homelabs, orquestación con Docker, desarrollo de agentes inteligentes en CLI y automatización de flujos de trabajo mediante scripts robustos en Bash y Python. Orientado a la resolución pragmática de problemas de infraestructura y confiabilidad.

// ===============================================================================
// EXPERIENCIA Y PROYECTOS DESTACADOS
// ===============================================================================

#cvsection("Proyectos de Ingeniería e Infraestructura")

#cvitem(
  title: "Bóveda de Conocimiento Técnico Distribuida (braind)",
  subtitle: "Arquitecto y Desarrollador",
  date: "2024 --- Presente",
  loc: "Jujuy, AR",
)[
  - Diseñó un sistema distribuido de notas técnicas y apuntes con sincronización multi-dispositivo vía Syncthing.
  - Implementó suite de automatización en Python (linters, extractores de tags, scripts de diagnóstico y compiladores de PDF duales Typst/LaTeX).
  - Integró agentes autónomos de codificación y modelos RAG locales con Ollama sobre red interna homelab.
]

#cvitem(
  title: "Homelab y Servidor Personal Autosustentable",
  subtitle: "SysAdmin & DevOps",
  date: "2023 --- Presente",
  loc: "Local",
)[
  - Despliegue y mantenimiento de +15 contenedores Docker (Nextcloud, Uptime Kuma, AdGuard Home, Vaultwarden, Ollama).
  - Segmentación de red con router OpenWrt (VLANs dedicadas para IoT, servidores y red hogareña confiable).
  - Configuración de backups automatizados cifrados y acceso remoto seguro mediante VPN WireGuard.
]

// ===============================================================================
// COMPETENCIAS TÉCNICAS
// ===============================================================================

#cvsection("Competencias Técnicas")
- *Sistemas Operativos & Kernel:* Linux (Arch Linux, Debian/Ubuntu Server, OpenWrt), Bash scripting avanzado, POSIX, SSH.
- *Virtualización & Contenedores:* Docker, Docker Compose, aislamiento de recursos, redes puente y overlay.
- *Lenguajes & Automatización:* Python (FastAPI, Typer, automatización CLI), C/C++ básico, Rust (nociones y Typst).
- *Redes & Protocolos:* TCP/IP, VLANs, DNS (AdGuard Home, Unbound), VPN (WireGuard), HTTP/S, reverse proxies (Caddy, Nginx).
- *Documentación & Herramientas:* Git, Typst, LaTeX, Markdown/Obsidian, Vim/Neovim, Make.

// ===============================================================================
// EDUCACIÓN
// ===============================================================================

#cvsection("Educación Formal")

#cvitem(
  title: "Licenciatura en Sistemas",
  subtitle: "Facultad de Ingeniería --- Universidad Nacional de Jujuy (UNJu)",
  date: "2021 --- En curso",
  loc: "Jujuy, AR",
)[
  - Promedio académico destacado. Materias clave: Arquitectura de Computadoras, Sistemas Operativos, Redes, ACP.
]
