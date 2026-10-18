// =========================================================================
// PLANTILLA MAESTRA: APUNTES TÉCNICOS COMPACTOS (ESTILO PASTEL) - TYPST
// =========================================================================
// Características:
// - Márgenes reducidos (1.25 cm) y tipografía compacta (9pt).
// - Sin encabezado superior, sin portada separada y sin índice (formato continuo).
// - Banner superior estilizado, blanco y de borde fino en la página inicial.
// - Paleta de colores pastel de alto contraste (fondos 95-97% brillo).
// - Cajas modulares de concepto con borde de acento cromático (azul, verde, ámbar, rojo, teal, púrpura).
// - Tablas compactas estructuradas y bloques de comandos legibles.
// - 100% amigable para lectura en pantalla y ahorro de tinta/tóner en impresión.
// =========================================================================

#set document(
  title: "Apuntes Técnicos - [Materia]",
  author: "Hugo Joaquín Hidalgo",
  date: auto,
)

#set page(
  paper: "a4",
  margin: (top: 1.2cm, bottom: 1.3cm, left: 1.25cm, right: 1.25cm),
  header: none,
  footer: context [
    #align(center)[
      #text(size: 8pt, fill: rgb("#64748b"))[— Página #counter(page).display() —]
    ]
  ],
)

#set text(
  font: ("Liberation Sans", "DejaVu Sans", "Adwaita Sans"),
  size: 9pt,
  lang: "es",
  region: "ar",
)

#set par(
  justify: true,
  leading: 0.45em,
  spacing: 0.6em,
  first-line-indent: 0pt,
)

// --- Paleta Pastel y de Acento ---
#let temas = (
  azul: (bg: rgb("#f0f7ff"), border: rgb("#2563eb"), title: rgb("#1e3a8a")),
  verde: (bg: rgb("#f0fdf4"), border: rgb("#16a34a"), title: rgb("#14532d")),
  ambar: (bg: rgb("#fffbeb"), border: rgb("#d97706"), title: rgb("#78350f")),
  rojo: (bg: rgb("#fef2f2"), border: rgb("#dc2626"), title: rgb("#7f1d1d")),
  teal: (bg: rgb("#f0fdfa"), border: rgb("#0d9488"), title: rgb("#134e4a")),
  purpura: (bg: rgb("#faf5ff"), border: rgb("#9333ea"), title: rgb("#581c87")),
)

// --- Funciones para Cajas de Concepto ---
#let conceptbox(title: "", tema: "azul", body) = {
  let c = temas.at(tema, default: temas.azul)
  block(
    width: 100%,
    fill: c.bg,
    stroke: (left: 3.5pt + c.border, rest: 0.5pt + rgb("#e2e8f0")),
    radius: (right: 4pt),
    inset: (x: 10pt, y: 8pt),
    spacing: 8pt,
    [
      #if title != "" [
        #text(weight: "bold", size: 9.5pt, fill: c.title)[#title]
        #v(3pt)
      ]
      #text(size: 8.8pt, fill: rgb("#0f172a"))[#body]
    ]
  )
}

// --- Formato de Secciones ---
#show heading: it => [
  #v(0.6em)
  #text(fill: rgb("#0f172a"), weight: "bold")[#it.body]
  #v(0.2em)
]

#show heading.where(level: 1): it => [
  #v(0.8em)
  #block(
    width: 100%,
    stroke: (bottom: 1.5pt + rgb("#2563eb")),
    inset: (bottom: 4pt),
    [
      #text(size: 11pt, weight: "bold", fill: rgb("#1e293b"))[#it.body]
    ]
  )
  #v(0.4em)
]

#show heading.where(level: 2): it => [
  #text(size: 9.8pt, weight: "bold", fill: rgb("#2563eb"))[▶ #it.body]
]

// --- Resaltado de Código ---
#show raw.where(block: true): it => [
  #block(
    fill: rgb("#f8fafc"),
    stroke: 0.5pt + rgb("#cbd5e1"),
    inset: 7pt,
    radius: 3pt,
    width: 100%,
    text(size: 8pt, font: "DejaVu Sans Mono", it)
  )
]

// =========================================================================
// BANNER SUPERIOR DE CABECERA
// =========================================================================

#block(
  width: 100%,
  stroke: 0.8pt + rgb("#64748b"),
  inset: (x: 12pt, y: 8pt),
  radius: 3pt,
  fill: white,
  [
    #grid(
      columns: (1fr, auto),
      align: (left + horizon, right + horizon),
      [
        #text(size: 13pt, weight: "bold", fill: rgb("#0f172a"))[ARQUITECTURAS Y COMPUTACIÓN PARALELA] \
        #text(size: 9pt, weight: "bold", fill: rgb("#2563eb"))[Unidad V: Computación Distribuida, Clusters, Grids y Clouds]
      ],
      [
        #text(size: 8pt, fill: rgb("#475569"))[
          *Autor:* Hugo Joaquín Hidalgo \
          *Carrera:* Lic. en Sistemas --- UNJu \
          *Compilación:* Typst (Rust Engine)
        ]
      ]
    )
  ]
)

#v(0.5em)

// =========================================================================
// CONTENIDO MODULAR
// =========================================================================

= 1. Taxonomía de Sistemas Distribuidos y Acoplamiento

#conceptbox(title: "Principio de Acoplamiento y Modelo de Comunicación", tema: "azul")[
  A diferencia de los multiprocesadores de memoria compartida (SMP/NUMA), los sistemas multicomputador se basan en *nodos autónomos desacoplados* conectados mediante una red de datos. La comunicación se realiza exclusivamente a través de paso de mensajes explícito (*Message Passing Interface*).
]

== Clusters de Cómputo (Beowulf)

#conceptbox(title: "Arquitectura Beowulf Estándar", tema: "verde")[
  - *Hardware:* Nodos comerciales COTS (Commodity Off-The-Shelf) de bajo costo.
  - *Red Privada:* Red dedicada de baja latencia aislada del tráfico de campus (Gigabit / InfiniBand).
  - *Nodo Maestro:* Ejecuta servicios de gestión, scheduler de jobs (SLURM, PBS) y gateway SSH.
  - *Nodos de Cómputo (Esclavos):* Procesan tareas concurrentes sin pantalla ni interacción directa.
]

== Grids de Cómputo

#conceptbox(title: "Infraestructura Grid y Heterogeneidad", tema: "ambar")[
  Redes geográficamente distribuidas y acopladas mediante middleware (Globus Toolkit). Soportan organizaciones virtuales (VO), heterogeneidad extrema de arquitecturas y recursos dinámicos.
]

== Modelos de Servicio Cloud (NIST SP 800-145)

#conceptbox(title: "Jerarquía de Responsabilidad Compartida", tema: "teal")[
  #table(
    columns: (1fr, 1.5fr, 1.5fr),
    fill: (x, y) => if y == 0 { rgb("#e0f2fe") } else { none },
    stroke: 0.5pt + rgb("#cbd5e1"),
    align: (left, left, left),
    [*Modelo*], [*El Usuario Administra*], [*El Proveedor Administra*],
    [IaaS (EC2, Droplets)], [SO, Runtime, Datos, Apps], [Virtualización, Servidores, Red],
    [PaaS (Heroku, Lambda)], [Código de App y Datos], [SO, Middleware, Runtimes, HW],
    [SaaS (Nextcloud, M365)], [Configuración y Usuarios], [Infraestructura Completa y Código],
  )
]

== Diagnóstico y Monitoreo de Procesos en Slurm

```bash
# Inspección de cola de trabajos y estado de nodos en cluster
squeue -u $USER --format="%.18i %.9P %.8j %.8u %.2t %.10M %.6D %R"
sinfo -N -l
```
