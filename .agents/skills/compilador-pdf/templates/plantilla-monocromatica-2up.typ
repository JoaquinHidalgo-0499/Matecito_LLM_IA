// =========================================================================
// PLANTILLA MAESTRA: COMPENDIO 2-UP MONOCROMÁTICO HORIZONTAL (TYPST)
// =========================================================================
// Formato: 2 Páginas Lógicas por Hoja Física (A4 Landscape / Modo Horizontal)
// Optimizado para: Impresión láser monocromática, doble faz y ahorro de tóner.
//
// Principios de Diseño:
// 1. Cero Sombreado: Sin rellenos grises que ensucien el papel o gasten tóner.
// 2. Línea Guía Central: Trazo punteado para plegado o guillotina.
// 3. Cajas Técnicas Modulares:
//    - #slidebox: Contenedor rectangular fino (0.4pt) para bloques temáticos.
//    - #examplebox: Bloque abierto con acento lateral delgado (1pt) sin marco grueso.
//    - #importantbox: Recuadro punteado/discontinuo con etiqueta corta y directa.
// 4. Footer Minimalista: Únicamente el número de hoja centrado.
// =========================================================================

#set document(
  title: "Compendio Técnico Monocromo 2-Up - [Asignatura]",
  author: "Hugo Joaquín Hidalgo",
  date: auto,
)

#set page(
  paper: "a4",
  flipped: true, // Modo horizontal (landscape)
  margin: (top: 8mm, bottom: 8mm, left: 10mm, right: 10mm),
  background: {
    // Guía central sutil para plegado o guillotinado
    place(
      top + center,
      line(
        start: (0pt, 0.6cm),
        end: (0pt, 21cm - 0.6cm),
        stroke: (paint: luma(170), dash: "densely-dashed", thickness: 0.5pt),
      ),
    )
  },
  header: none,
  footer: context align(center)[
    #text(size: 7.2pt, fill: black)[#here().page()]
  ],
)

#set text(
  font: ("Liberation Sans", "DejaVu Sans", "Adwaita Sans"),
  size: 7.5pt,
  fill: black,
  lang: "es",
)

#set par(
  justify: true,
  leading: 0.38em,
  spacing: 0.45em,
  first-line-indent: 0pt,
)

// Encabezados en alto contraste monocromático (sin sombreado ni barras gruesas)
#show heading: set text(fill: black)

#show heading.where(level: 1): it => block(
  width: 100%,
  stroke: (bottom: 1pt + black),
  inset: (bottom: 3.5pt),
  above: 1.1em,
  below: 0.65em,
  breakable: false,
  text(size: 9.5pt, weight: "black", fill: black)[#it.body]
)

#show heading.where(level: 2): it => block(
  width: 100%,
  above: 0.8em,
  below: 0.45em,
  breakable: false,
  [
    #text(size: 8.5pt, weight: "bold", fill: black)[#it.body]
    #v(-2.5pt)
    #line(length: 100%, stroke: 0.5pt + black)
  ]
)

#show heading.where(level: 3): it => block(
  above: 0.65em,
  below: 0.35em,
  breakable: false,
  text(size: 7.8pt, weight: "bold", fill: black)[#it.body]
)

// --- Cajas Modulares y de Diapositivas (100% Monocromáticas) ---

#let slidebox(title, slide_num: none, content) = block(
  width: 100%,
  stroke: 0.4pt + luma(130),
  radius: 1.5pt,
  inset: (x: 5pt, y: 4pt),
  fill: none,
  below: 0.55em,
  breakable: false,
  [
    #grid(
      columns: if slide_num != none { (1fr, auto) } else { (1fr,) },
      text(weight: "bold", size: 8pt, fill: black)[#title],
      if slide_num != none { text(size: 6.8pt, fill: luma(110))[Diap. #slide_num] }
    )
    #v(1.5pt)
    #line(length: 100%, stroke: 0.3pt + luma(180))
    #v(2.5pt)
    #content
  ]
)

#let examplebox(title, content) = block(
  width: 100%,
  stroke: (left: 1pt + luma(90)),
  inset: (left: 6pt, y: 2.5pt),
  fill: none,
  below: 0.45em,
  breakable: false,
  [
    #text(weight: "bold", size: 7.3pt, fill: black)[Ejemplo: #title]
    #v(1.5pt)
    #text(size: 7.3pt, fill: black)[#content]
  ]
)

#let importantbox(title, content) = block(
  width: 100%,
  stroke: (paint: black, thickness: 0.5pt, dash: "dashed"),
  radius: 1.5pt,
  inset: (x: 5pt, y: 3.5pt),
  fill: none,
  below: 0.45em,
  breakable: false,
  [
    #text(weight: "bold", size: 7.3pt, fill: black)[Importante: #title]
    #v(1.5pt)
    #text(size: 7.3pt, fill: black)[#content]
  ]
)

// Inicia el flujo en 2 columnas (2 páginas lógicas por cara física)
#show: columns.with(2, gutter: 1.2cm)

// =========================================================================
// CONTENIDO DE EJEMPLO
// =========================================================================

= UNIDAD 1: CONCEPTOS FUNDAMENTALES Y ARQUITECTURA

== 1.1 Principios Básicos y Taxonomía

#slidebox("Concepto Primario y Alcance", slide_num: "3-4", [
  Definición canónica de la doctrina de cátedra. Los conceptos se organizan en bloques modulares que evitan fracturas entre columnas.

  #examplebox("Caso Práctico en Entorno Real", [
    En un entorno hospitalario de emergencia, si las historias clínicas no responden aunque los datos estén íntegros, el fallo es estrictamente de *disponibilidad*.
  ])

  #importantbox("Aclaración Doctrinal Fundamental", [
    La redundancia de componentes no sustituye a las copias de seguridad de datos (backups). Cada mecanismo opera en capas de defensa distintas.
  ])
])

#slidebox("Comparativa Estructurada en Dos Columnas", slide_num: "5-6", [
  Para optimizar el espacio vertical y evitar desperdicio de líneas, los ítems paralelos se organizan en rejillas:

  #grid(
    columns: (1fr, 1fr),
    gutter: 8pt,
    [
      *Ventajas Operativas:*
      - Incrementa la disponibilidad.
      - Elimina puntos únicos de falla (SPOF).
      - Facilita el mantenimiento sin corte de servicio.
    ],
    [
      *Limitaciones / Desventajas:*
      - Mayor costo de equipamiento.
      - Complejidad adicional de administración.
      - Requiere sincronización estricta de estados.
    ]
  )
])

== 1.2 Tabla Comparativa Monocromática

#slidebox("Matriz de Decisión y Niveles de Protección", slide_num: "7", [
  #align(center)[
    #table(
      columns: (1fr, 1.2fr, 1fr),
      stroke: 0.4pt + black,
      fill: none,
      align: (left, left, left),
      [*Mecanismo*], [*Acción Principal*], [*Nivel de Protección*],
      [Redundancia], [Duplicación de componentes], [Básico / Continuidad],
      [Alta Disponibilidad], [Monitoreo y conmutación rápida], [Interrupción mínima],
      [Tolerancia a Fallos], [Operación continua sin degradación], [Cero tiempo de corte],
    )
  ]
])
