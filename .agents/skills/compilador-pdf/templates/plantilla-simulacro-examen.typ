// =========================================================================
// PLANTILLA ESTÁNDAR: SIMULACRO DE EXAMEN Y BANCO INTERACTIVO BIDIRECCIONAL
// =========================================================================
// Formato: A4 Vertical con Navegación Hipertextual Bidireccional (Pregunta <-> Solución)
// Diseñado para: Simulacros de Parcial, Exámenes Finales y Cuestionarios de Práctica
// Motor: Typst (Recomendado >= 0.12)
// =========================================================================

#set document(
  title: "Simulacro de Examen / Banco de Práctica Interactivo",
  author: "Cátedra Universitaria",
  date: auto,
)

#set page(
  paper: "a4",
  margin: (top: 1.8cm, bottom: 1.8cm, left: 1.8cm, right: 1.8cm),
  header: context [
    #if counter(page).get().first() > 1 [
      #grid(
        columns: (1fr, auto),
        text(size: 7.5pt, fill: rgb("#475569"))[
          *SIMULACRO DE EXAMEN PARCIAL* · Banco de Preguntas y Respuestas Interactivo
        ],
        text(size: 7.5pt, fill: rgb("#475569"))[
          Cátedra Universitaria
        ]
      )
      #v(2pt)
      #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
    ]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
    #v(3pt)
    #grid(
      columns: (1fr, auto),
      text(size: 7.5pt, fill: rgb("#64748b"))[
        Material de Preparación y Autoevaluación · Navegación Bidireccional
      ],
      text(size: 8pt, weight: "bold", fill: rgb("#1e293b"))[
        Página #counter(page).display() de #counter(page).final().first()
      ]
    )
  ],
)

#set text(
  font: ("Liberation Sans", "DejaVu Sans", "Adwaita Sans"),
  size: 8.8pt,
  fill: rgb("#0f172a"),
  lang: "es",
  region: "ar",
)

#set par(
  justify: true,
  leading: 0.45em,
  spacing: 0.55em,
  first-line-indent: 0pt,
)

// --- Macros de Badges y Botones de Navegación ---
#let badge(texto, fill_col: rgb("#1e3a8a"), text_col: white) = [
  #box(fill: fill_col, inset: (x: 5pt, y: 2.2pt), radius: 3pt)[
    #text(fill: text_col, weight: "bold", size: 7pt)[#texto]
  ]
]

// Macro de Tarjeta de Pregunta con Salto a Solución
#let cardpregunta(numero, tipo, puntos, titulo, body) = [
  #v(6pt)
  #block(
    width: 100%,
    stroke: 0.6pt + rgb("#94a3b8"),
    radius: 4pt,
    fill: white,
    inset: 0pt,
    breakable: false,
    [
      #metadata("preg-" + str(numero)) #label("preg-" + str(numero))
      #block(
        width: 100%,
        fill: rgb("#f1f5f9"),
        inset: (x: 10pt, y: 6pt),
        radius: (top: 4pt),
        stroke: (bottom: 0.5pt + rgb("#cbd5e1")),
        [
          #grid(
            columns: (auto, auto, auto, 1fr, auto),
            gutter: 6pt,
            align: (horizon, horizon, horizon, horizon, right + horizon),
            badge("APARTADO " + str(numero), fill_col: rgb("#0f172a")),
            if tipo == "desarrollo" { badge("A DESARROLLAR", fill_col: rgb("#2563eb")) }
            else if tipo == "mc_multi" { badge("SELECCIÓN MÚLTIPLE (1 o más)", fill_col: rgb("#059669")) }
            else if tipo == "mc_negativo" { badge("MARQUE LAS QUE NO CORRESPONDEN", fill_col: rgb("#d97706")) }
            else { badge("CASO PRÁCTICO", fill_col: rgb("#7c3aed")) },
            badge(str(puntos) + " PUNTOS", fill_col: rgb("#334155")),
            text(size: 7.8pt, style: "italic", fill: rgb("#64748b"))[#titulo],
            link(label("sol-" + str(numero)))[
              #box(
                fill: rgb("#0284c7"),
                inset: (x: 5.5pt, y: 2.5pt),
                radius: 3pt,
              )[
                #text(fill: white, weight: "bold", size: 6.8pt)[Ver Solución ➜]
              ]
            ]
          )
        ]
      )
      #block(
        width: 100%,
        inset: (x: 12pt, y: 8pt),
        body
      )
    ]
  )
]

// Macro de Tarjeta de Solución con Retorno Bidireccional
#let solcard(numero, tipo, resp_corta, slide_ref, body) = [
  #v(5pt)
  #block(
    width: 100%,
    stroke: (left: 3.5pt + rgb("#0284c7"), rest: 0.5pt + rgb("#cbd5e1")),
    radius: (right: 3pt),
    fill: rgb("#f8fafc"),
    inset: (x: 10pt, y: 7pt),
    breakable: false,
    [
      #metadata("sol-" + str(numero)) #label("sol-" + str(numero))
      #grid(
        columns: (auto, auto, 1fr, auto),
        gutter: 6pt,
        align: (horizon, horizon, horizon, right + horizon),
        badge("SOLUCIÓN #" + str(numero), fill_col: rgb("#0284c7")),
        link(label("preg-" + str(numero)))[
          #box(
            fill: rgb("#334155"),
            inset: (x: 5pt, y: 2.2pt),
            radius: 3pt,
          )[
            #text(fill: white, weight: "bold", size: 6.6pt)[⬅ Volver a Pregunta]
          ]
        ],
        text(weight: "bold", size: 8.5pt, fill: rgb("#0369a1"))[#resp_corta],
        text(size: 7.2pt, style: "italic", fill: rgb("#64748b"))[📚 #slide_ref]
      )
      #v(3pt)
      #line(length: 100%, stroke: 0.4pt + rgb("#e2e8f0"))
      #v(3pt)
      #body
      #v(2pt)
      #align(right)[
        #link(label("preg-" + str(numero)))[
          #box(
            stroke: 0.5pt + rgb("#cbd5e1"),
            fill: rgb("#f1f5f9"),
            inset: (x: 5pt, y: 2pt),
            radius: 2pt,
          )[
            #text(fill: rgb("#0284c7"), weight: "bold", size: 6.6pt)[⬅ Volver al Apartado #numero]
          ]
        ]
      ]
    ]
  )
]

// =========================================================================
// ENCABEZADO INSTITUCIONAL
// =========================================================================
#align(center)[
  #text(size: 9.5pt, weight: "bold", fill: rgb("#475569"))[
    UNIVERSIDAD NACIONAL · FACULTAD DE INGENIERÍA
  ] \
  #text(size: 8.5pt, fill: rgb("#64748b"))[
    CÁTEDRA DE EJEMPLO — TITULAR: DOCENTE TITULAR
  ] \
  #v(5pt)
  #text(size: 14pt, weight: "black", fill: rgb("#0f172a"))[
    SIMULACRO DE EXAMEN PARCIAL / FINAL
  ] \
  #text(size: 10pt, weight: "bold", fill: rgb("#2563eb"))[
    UNIDADES TEMÁTICAS · GUÍA DE AUTOEVALUACIÓN BIDIRECCIONAL
  ]
]

#v(4pt)
#line(length: 100%, stroke: 1.2pt + rgb("#0f172a"))
#v(6pt)

#block(
  width: 100%,
  fill: rgb("#f8fafc"),
  stroke: 0.6pt + rgb("#cbd5e1"),
  inset: (x: 10pt, y: 8pt),
  radius: 3pt,
  [
    #text(weight: "bold", size: 8.5pt, fill: rgb("#1e293b"))[📌 Instrucciones del Examen:]
    1. *Navegación Interactiva:* Haga clic en el botón azul *[Ver Solución ➜]* de cada apartado para contrastar de inmediato su respuesta con el solucionario al final del documento.
    2. *Retorno Rápido:* En el solucionario, utilice el botón *[⬅ Volver a Pregunta]* para regresar exactamente al reactivo en resolución.
  ]
)

#v(8pt)
#align(center)[
  #text(size: 11pt, weight: "black", fill: rgb("#0f172a"))[
    PARTE 1: SIMULACRO DE EXAMEN (PREGUNTAS)
  ]
]
#v(4pt)

// --- EJEMPLOS DE USO DE CARDPREGUNTA ---

#cardpregunta(1, "desarrollo", 10, "Tema 1 · Pregunta de Desarrollo")[
  *Enuncie y desarrolle el concepto fundamental solicitado:*
  - Indique las características principales y su ámbito de aplicación.
  - Justifique técnicamente el impacto operativo y las ventajas de su implementación.
]

#cardpregunta(2, "mc_multi", 10, "Tema 2 · Selección Múltiple (1 o más)")[
  *Marque la/las opción/es correcta/s:*
  - [ ] *1.* Opción de ejemplo número uno.
  - [ ] *2.* Opción de ejemplo número dos (correcta).
  - [ ] *3.* Opción de ejemplo número tres (correcta).
  - [ ] *4.* Opción de ejemplo número cuatro.
]

#cardpregunta(3, "mc_negativo", 10, "Tema 3 · Marque las que NO corresponden")[
  *Las características que NO CORRESPONDEN al concepto bajo análisis son:*
  - [ ] *1.* Característica verídica del concepto.
  - [ ] *2.* Afirmación errónea que NO corresponde (Marcar).
  - [ ] *3.* Característica verídica del concepto.
  - [ ] *4.* Afirmación errónea que NO corresponde (Marcar).
]

#pagebreak()

// =========================================================================
// PARTE 2: SOLUCIONARIO Y JUSTIFICACIONES
// =========================================================================
#align(center)[
  #text(size: 13pt, weight: "black", fill: rgb("#0f172a"))[
    PARTE 2: SOLUCIONARIO COMPLETO Y JUSTIFICACIONES
  ] \
  #text(size: 8.5pt, fill: rgb("#475569"))[
    Respuestas correctas, fuentes bibliográficas y justificación punto por punto
  ]
]

#v(8pt)
#line(length: 100%, stroke: 1.2pt + rgb("#0284c7"))
#v(8pt)

// --- EJEMPLOS DE USO DE SOLCARD ---

#solcard(1, "desarrollo", "Resumen Ejecutivo de la Respuesta", "Apunte de Cátedra / Slide Oficial")[
  - *Desarrollo Conceptual:* Explicación exhaustiva del concepto con los términos clave requeridos por la cátedra para la máxima puntuación.
  - *Criterio de Evaluación:* El docente evalúa que se mencionen taxativamente los elementos distintivos y las justificaciones teóricas del marco normativo.
]

#solcard(2, "mc_multi", "Opciones Correctas: 2 y 3", "Presentación Oficial")[
  - *Opción 1: FALSA.* Justificación de por qué es incorrecta.
  - *Opción 2: VERDADERA.* Justificación y cita de la fuente.
  - *Opción 3: VERDADERA.* Justificación y cita de la fuente.
  - *Opción 4: FALSA.* Justificación de por qué es incorrecta.
]

#solcard(3, "mc_negativo", "NO Corresponden: 2 y 4 (Las Falsas en la teoría)", "Presentación Oficial")[
  - *Opción 1: Corresponde.* Afirmación verídica del tema.
  - *Opción 2: NO CORRESPONDE (Marcar).* Explicación del error conceptual.
  - *Opción 3: Corresponde.* Afirmación verídica del tema.
  - *Opción 4: NO CORRESPONDE (Marcar).* Explicación del error conceptual.
]
