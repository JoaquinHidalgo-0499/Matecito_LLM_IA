// =========================================================================
// PLANTILLA MAESTRA: APUNTES TÉCNICOS MONOCROMO (TYPST)
// =========================================================================
// Optimizada para impresión física láser monocromática y ahorro de tóner.
//
// Principios de Diseño Editorial:
// 1. Formato a 1 Columna Continua: Ancho útil completo con compensación para anillado.
// 2. Sin Encabezado Superior: Cero distracciones para maximizar la superficie útil.
// 3. Tipografía de Alto Rendimiento: Tipografía serif para lectura cómoda en papel.
// 4. Alto Contraste Monocromo: 100% negro puro (#000000) y grises limpios sobre blanco.
// 5. Cajas modulares sin degradados: Definiciones, alertas de examen y fórmulas.
// =========================================================================

#set document(
  title: "Compendio Técnico Monocromo - [Materia]",
  author: "Hugo Joaquín Hidalgo",
  date: auto,
)

#set page(
  paper: "a4",
  margin: (top: 1.8cm, bottom: 1.8cm, left: 2.2cm, right: 1.8cm),
  header: none,
  footer: context align(center)[
    #text(size: 8.5pt, fill: black, font: "DejaVu Sans")[#counter(page).display()]
  ],
)

#set text(
  font: ("Libertinus Serif", "Liberation Serif", "DejaVu Serif"),
  size: 10pt,
  fill: black,
  lang: "es",
  region: "ar",
  spacing: 115%,
)

#set par(
  justify: true,
  leading: 0.55em,
  spacing: 0.65em,
  first-line-indent: 0pt,
)

// --- Títulos y Encabezados Sans-Serif Monocromo ---
#show heading: it => [
  #set text(fill: black, font: ("DejaVu Sans", "Liberation Sans"))
  #v(0.8em)
  #it
  #v(0.3em)
]

#show heading.where(level: 1): it => [
  #v(1.1em)
  #text(size: 13pt, weight: "bold")[#it.body]
  #v(2pt)
  #line(length: 100%, stroke: 0.8pt + black)
  #v(0.4em)
]

#show heading.where(level: 2): it => [
  #text(size: 10.5pt, weight: "bold", fill: rgb("#1e293b"))[#it.body]
]

// --- Cajas Técnicas Monocromáticas (Sin sombreado, sin bordes gruesos) ---
#let slidebox(title, slide_num: none, content) = block(
  width: 100%,
  stroke: 0.4pt + luma(130),
  radius: 1.5pt,
  inset: (x: 8pt, y: 6pt),
  fill: none,
  below: 0.6em,
  breakable: false,
  [
    #grid(
      columns: if slide_num != none { (1fr, auto) } else { (1fr,) },
      text(weight: "bold", size: 9pt, font: "DejaVu Sans", fill: black)[#title],
      if slide_num != none { text(size: 7.5pt, fill: luma(100))[Diap. #slide_num] }
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
  inset: (left: 7pt, y: 3pt),
  fill: none,
  below: 0.5em,
  breakable: false,
  [
    #text(weight: "bold", size: 8.5pt, font: "DejaVu Sans", fill: black)[Ejemplo: #title]
    #v(1.5pt)
    #text(size: 8.8pt)[#content]
  ]
)

#let importantbox(title, content) = block(
  width: 100%,
  stroke: (paint: black, thickness: 0.5pt, dash: "dashed"),
  radius: 1.5pt,
  inset: (x: 7pt, y: 5pt),
  fill: none,
  below: 0.5em,
  breakable: false,
  [
    #text(weight: "bold", size: 8.5pt, font: "DejaVu Sans", fill: black)[Importante: #title]
    #v(1.5pt)
    #text(size: 8.8pt)[#content]
  ]
)

#let definicion(title: "", body) = {
  block(
    width: 100%,
    fill: none,
    stroke: (left: 1.2pt + black, rest: 0.3pt + luma(180)),
    inset: (x: 8pt, y: 6pt),
    spacing: 7pt,
    radius: (right: 1.5pt),
    [
      #if title != "" [
        #text(weight: "bold", size: 9pt, font: "DejaVu Sans", fill: black)[Definición: #title]
        #v(2pt)
        #line(length: 100%, stroke: 0.3pt + luma(200))
        #v(2.5pt)
      ]
      #text(size: 9pt)[#body]
    ]
  )
}

#let alertaparcial(title: "", body) = {
  block(
    width: 100%,
    fill: none,
    stroke: (paint: black, thickness: 0.5pt, dash: "dashed"),
    inset: (x: 8pt, y: 6pt),
    spacing: 7pt,
    radius: 1.5pt,
    [
      #text(weight: "bold", size: 8.8pt, font: "DejaVu Sans", fill: black)[Importante / Examen: #title]
      #v(2pt)
      #line(length: 100%, stroke: 0.3pt + luma(180))
      #v(3pt)
      #text(size: 9pt)[#body]
    ]
  )
}

#let formulabox(body) = {
  block(
    width: 100%,
    fill: none,
    stroke: 0.4pt + luma(120),
    inset: (x: 8pt, y: 6pt),
    spacing: 6pt,
    radius: 1.5pt,
    [
      #text(size: 9pt)[#body]
    ]
  )
}

// --- Bloques de Código ---
#show raw.where(block: true): it => [
  #block(
    fill: white,
    stroke: 0.5pt + rgb("#475569"),
    inset: 8pt,
    radius: 2pt,
    width: 100%,
    text(size: 8.5pt, font: "DejaVu Sans Mono", it)
  )
]

// =========================================================================
// ENCABEZADO SUPERIOR COMPACTO (PÁGINA INICIAL)
// =========================================================================

#text(size: 15pt, weight: "bold", font: "DejaVu Sans", fill: black)[[TÍTULO PRINCIPAL DE LA ASIGNATURA]] \
#v(1pt)
#text(size: 10pt, fill: rgb("#334155"), font: "DejaVu Sans")[[Subtítulo o Módulo Temático --- Compendio Integral de Cátedra]] \
#v(1pt)
#text(size: 8pt, fill: rgb("#64748b"))[
  Facultad de Ingeniería · Universidad Nacional de Jujuy (UNJu) · Edición Monocromo Láser (Typst)
]
#v(2pt)
#line(length: 100%, stroke: 0.8pt + black)
#v(0.6em)

// =========================================================================
// CONTENIDO DE EJEMPLO
// =========================================================================

= 1. Introducción y Conceptos Fundamentales

== 1.1. Marco Teórico Principal

Texto introductorio del tema desarrollado. El formato a 1 columna continua garantiza una densidad de lectura óptima en papel, permitiendo que el texto fluya con total naturalidad sin recortes laterales ni distracciones visuales.

#definicion(title: "Concepto Primario")[
  Explicación formal y canónica del concepto según la doctrina de la cátedra universitaria:
  - *Elemento A:* Descripción técnica detallada del primer componente.
  - *Elemento B:* Descripción técnica del segundo componente.
  - *Elemento C:* Justificación e impacto dentro del sistema integral.
]

== 1.2. Tabla Comparativa de Rendimiento

#align(center)[
  #table(
    columns: (1.2fr, 2fr, 2fr),
    fill: (x, y) => if y == 0 { rgb("#f1f5f9") } else { white },
    stroke: 0.5pt + black,
    align: (left, left, left),
    [*Criterio Evaluado*], [*Enfoque Convencional*], [*Enfoque Avanzado / Cátedra*],
    [*Objetivo Primario*], [Mecanismo base y limitaciones operativas.], [Alta disponibilidad y tolerancia a fallos.],
    [*Tiempo de Respuesta*], [Latencia dependiente de conmutación electromecánica.], [Conmutación instantánea ($0 upright("ms")$).],
    [*Resiliencia*], [Intervención manual ante caídas de enlace.], [Recuperación automatizada con redundancia activa.],
  )
]

#alertaparcial(title: "Advertencia de Evaluación Parcial")[
  Recordar que en exámenes teóricos la cátedra suele evaluar la distinción precisa entre mecanismos preventivos y correctivos, haciendo énfasis en que las medidas activas reducen la probabilidad del siniestro, mientras que las pasivas mitigan el impacto residual.
]

== 1.3. Expresiones Matemáticas y Métricas

#formulabox[
  *Cálculo de Pérdida Anual Esperada (ALE):*
  $ upright("ALE") = upright("SLE") times upright("ARO") $
  Donde $upright("SLE")$ representa la pérdida ante un evento individual ($upright("SLE") = upright("AV") times upright("EF")$) y $upright("ARO")$ es la frecuencia anual estimada del incidente.
]

== 1.4. Bloques de Comandos y Código Técnico

```bash
# Verificación de integridad y permisos en Linux
chmod 600 /etc/security/audit.conf
chown root:root /etc/security/audit.conf
auditctl -l -a always,exit -F arch=b64 -S open,openat -F success=0
```

== 1.5. Cajas Modulares y de Diapositivas (Diseño Monocromo Limpio)

#slidebox("Concepto Modular de Diapositiva", slide_num: "12-14", [
  Estructura modular ideal para transcripciones de presentaciones oficiales o compendios canónicos. No posee sombreado ni rellenos grises que ensucien la impresión láser o consuman tóner innecesario.
  
  #examplebox("Caso Práctico en Producción", [
    Los médicos acceden a las historias clínicas digitales. Si el sistema cae, el problema radica en la *disponibilidad*, no en la confidencialidad.
  ])
  
  #importantbox("Aclaración Doctrinal Crítica", [
    Un mecanismo redundante no reemplaza las copias de seguridad de datos. Protege contra averías de hardware, pero no ante ransomware o borrado accidental.
  ])
])
