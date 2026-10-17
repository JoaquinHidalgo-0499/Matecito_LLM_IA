// =========================================================================
// PLANTILLA MAESTRA: TRATADO ACADÉMICO FORMAL / TESIS / MONOGRAFÍA (TYPST)
// =========================================================================
// Optimizada para monografías formales, informes de investigación, tesis
// de grado y publicaciones académicas tradicionales.
//
// Características Editoriales:
// 1. Portada formal institucional con metadatos.
// 2. Resumen ejecutivo estructurado (Abstract) y palabras clave.
// 3. Tabla de contenidos interactiva con numeración jerárquica.
// 4. Geometría estándar ISO A4 con márgenes de 2.5 cm.
// 5. Tipografía serif clara a 11pt con justificación y microinterlineado.
// 6. Tablas limpias, ecuaciones numeradas y referencias cruzadas nativas.
// =========================================================================

#set document(
  title: "Tratado Académico Formal",
  author: "Hugo Joaquín Hidalgo",
  date: auto,
)

#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
  header: locate(loc => {
    // Encabezado activo únicamente a partir del cuerpo principal (pág > 2)
    if loc.page() > 2 [
      #grid(
        columns: (1fr, 1fr),
        align: (left, right),
        text(size: 8.5pt, fill: rgb("#64748b"), font: "DejaVu Sans")[Tratado Académico Formal],
        text(size: 8.5pt, fill: rgb("#64748b"), font: "DejaVu Sans")[Universidad Nacional de Jujuy],
      )
      #v(-3pt)
      #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
    ]
  }),
  footer: locate(loc => {
    // Pie de página con numeración
    if loc.page() > 1 [
      #align(center)[
        #text(size: 9pt, fill: rgb("#475569"))[— #loc.page() —]
      ]
    ]
  }),
)

#set text(
  font: ("Linux Libertine", "Times New Roman", "DejaVu Serif", "PT Serif"),
  size: 11pt,
  lang: "es",
  region: "ar",
  spacing: 120%,
)

#set par(
  justify: true,
  leading: 0.65em,
  first-line-indent: 1.5em,
)

// Numeración de encabezados
#set heading(numbering: "1.1")
#show heading: it => [
  #set text(fill: rgb("#0f172a"), font: ("DejaVu Sans", "Liberation Sans", "Helvetica Neue"))
  #v(1em)
  #it
  #v(0.5em)
]

#show heading.where(level: 1): it => [
  #set text(size: 14pt, weight: "bold")
  #v(1.5em)
  #it
  #v(0.8em)
]

#show link: it => text(fill: rgb("#1d4ed8"), it)

// =========================================================================
// PORTADA FORMAL
// =========================================================================

#align(center)[
  #v(2cm)
  #text(size: 22pt, weight: "bold", fill: rgb("#0f172a"))[Tratado Académico Formal] \
  #v(0.6em)
  #text(size: 13pt, fill: rgb("#475569"))[Subtítulo Descriptivo o Alcance Técnico de la Investigación]
  
  #v(2.5cm)
  
  #text(size: 12pt, weight: "bold")[Hugo Joaquín Hidalgo] \
  #v(0.3em)
  #text(size: 10pt, fill: rgb("#334155"))[
    Facultad de Ingeniería --- Universidad Nacional de Jujuy \
    #link("mailto:contacto@ejemplo.com")[contacto@ejemplo.com]
  ]
  
  #v(3cm)
  
  #text(size: 10pt, fill: rgb("#64748b"))[
    #datetime.today().display("[day] de [month repr:long] de [year]")
  ]
]

#pagebreak()

// =========================================================================
// RESUMEN Y TABLA DE CONTENIDOS
// =========================================================================

#block(
  fill: rgb("#f8fafc"),
  stroke: (left: 3pt + rgb("#2563eb")),
  inset: (x: 1.2em, y: 1em),
  radius: (right: 4pt),
)[
  #text(weight: "bold", size: 10.5pt, fill: rgb("#1e293b"))[Resumen Ejecutivo] \
  #v(0.4em)
  #text(size: 9.5pt, style: "italic")[
    Este documento ejemplifica la estructura formal requerida para monografías académicas, informes técnicos de investigación y proyectos finales de grado. Se presenta un resumen ejecutivo conciso del contexto problemático, los objetivos metodológicos, los resultados analíticos cuantitativos y las conclusiones principales alcanzadas, permitiendo al evaluador una rápida comprensión de la contribución técnica.
  ]
  
  #v(0.6em)
  #text(size: 9pt)[*Palabras clave:* Computación de Alto Rendimiento, Redes de Interconexión, Latencia, Arquitectura de Sistemas, Typst.]
]

#v(1.5em)
#outline(
  title: [Índice General],
  indent: 1.5em,
  depth: 3,
)

#pagebreak()

// =========================================================================
// CUERPO DEL DOCUMENTO
// =========================================================================

= Introducción

La creciente demanda de procesamiento en sistemas de cómputo modernos exige arquitecturas capaces de mitigar el cuello de botella de la memoria mediante topologías de comunicación escalables y jerarquías de almacenamiento optimizadas.

== Motivación y Contexto

El modelado analítico de redes de interconexión en multiprocesadores de chip (CMP) permite predecir el comportamiento del sistema ante saturación de tráfico, optimizando la asignación de buffers y el consumo energético de los enrutadores.

== Objetivos del Trabajo

- Formalizar el modelo matemático de latencia de red en topologías de malla 2D y torus.
- Evaluar el impacto de la contención de buffers mediante análisis estocástico.
- Sintetizar recomendaciones directas de diseño para implementaciones en silicio.

= Marco Teórico y Fundamentos Matemáticos

La latencia base de transporte $T_("base")$ de un paquete de $L$ flits en una red con $H$ saltos promedio se modela formalmente como:

$ T_("base") = H dot t_("router") + frac(L, b) + t_("wire") dot H $

Donde:
- $H$: Distancia promedio en saltos de conmutación.
- $t_("router")$: Latencia interna de procesamiento en el switch (ciclos de reloj).
- $L$: Tamaño total del paquete expresado en unidades mínimas de flujo (flits).
- $b$: Ancho de banda de canal por ciclo.
- $t_("wire")$: Retardo físico de propagación en el enlace de interconexión.

== Tabla Comparativa de Rendimiento

#align(center)[
  #table(
    columns: (auto, auto, auto, auto),
    fill: (x, y) => if y == 0 { rgb("#e2e8f0") } else if calc.even(y) { rgb("#f8fafc") } else { white },
    stroke: 0.5pt + rgb("#cbd5e1"),
    align: (col, row) => if col == 0 { left } else { center },
    [*Topología*], [*Diámetro*], [*Bisección*], [*Escalabilidad*],
    [Malla 2D $k times k$], [$2(k - 1)$], [$k$], [Media],
    [Torus 2D $k times k$], [$k$], [$2k$], [Alta],
    [Hipercubo $n$-dim], [$n$], [$2^(n-1)$], [Exponencial],
  )
]

= Conclusiones y Trabajo Futuro

Los modelos analíticos y las simulaciones demuestran que Typst ofrece una velocidad de procesamiento órdenes de magnitud superior sin perder la rigurosidad tipográfica requerida en documentos formales.
