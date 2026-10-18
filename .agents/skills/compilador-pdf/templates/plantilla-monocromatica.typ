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
  footer: context {
    grid(
      columns: (1fr, auto),
      align: (left, right),
      text(size: 7.5pt, fill: rgb("#475569"), font: "DejaVu Sans")[
        [Materia / Asignatura] · Compendio Técnico Monocromo
      ],
      text(size: 8.5pt, weight: "bold", fill: black, font: "DejaVu Sans")[
        #counter(page).display()
      ]
    )
    v(-3pt)
    line(length: 100%, stroke: 0.3pt + rgb("#94a3b8"))
  },
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

// --- Cajas Técnicas Monocromáticas ---
#let definicion(title: "", body) = {
  block(
    width: 100%,
    fill: white,
    stroke: (left: 2.5pt + black, rest: 0.4pt + rgb("#cbd5e1")),
    inset: (x: 10pt, y: 7pt),
    spacing: 7pt,
    radius: (right: 2pt),
    [
      #if title != "" [
        #text(weight: "bold", size: 9.5pt, font: "DejaVu Sans", fill: black)[Definición: #title]
        #v(3pt)
        #line(length: 100%, stroke: 0.3pt + rgb("#e2e8f0"))
        #v(3pt)
      ]
      #text(size: 9.2pt)[#body]
    ]
  )
}

#let alertaparcial(title: "", body) = {
  block(
    width: 100%,
    fill: white,
    stroke: 0.8pt + black,
    inset: (x: 10pt, y: 8pt),
    spacing: 8pt,
    radius: 2pt,
    [
      #text(weight: "bold", size: 9.2pt, font: "DejaVu Sans", fill: black)[▶ Punto Crítico / Criterio de Examen: #title]
      #v(3pt)
      #line(length: 100%, stroke: 0.4pt + black)
      #v(4pt)
      #text(size: 9.2pt)[#body]
    ]
  )
}

#let formulabox(body) = {
  block(
    width: 100%,
    fill: white,
    stroke: 0.5pt + rgb("#475569"),
    inset: (x: 9pt, y: 7pt),
    spacing: 6pt,
    radius: 2pt,
    [
      #text(size: 9.2pt)[#body]
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
