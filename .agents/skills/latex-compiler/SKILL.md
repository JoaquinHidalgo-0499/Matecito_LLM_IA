---
name: latex-compiler
description: >-
  Usa este skill cuando el usuario pida generar, diseñar, redactar o compilar documentos
  académicos, guías de estudio, resúmenes o tratados técnicos en formato PDF usando LaTeX (pdflatex).
---

# Compilador de Documentos y Tratados Académicos (LaTeX)

Procedimiento estandarizado para la redacción, maquetación y compilación de documentos profesionales en PDF a partir de código fuente LaTeX (`.tex`).

---

## 1. Reglas de Ubicación y Propósito
* **Carpeta Exclusiva de Salida:** Todo archivo `.tex`, archivo auxiliar y `.pdf` compilado debe generarse **única y exclusivamente** dentro de:
  `/home/joaquin/Compartido/braind/archivos-generados/<nombre-proyecto>/`
* **Prohibición:** Está terminantemente prohibido generar artefactos LaTeX dentro de `/brain/` o en las carpetas académicas de sólo lectura (`material-Materias/`, `1er_Cuatrimestre/`, `2do_Cuatrimestre/`).
* **Propósito:** `archivos-generados/` es exclusivamente una carpeta de salida y entrega de entregables para el usuario. No participa en la administración interna de `braind`.

---

## 2. Entorno y Binarios del Sistema
* **Motor LaTeX:** `/usr/bin/pdflatex` (instalado y verificado en el sistema).
* **Flags recomendados:** `-interaction=nonstopmode -halt-on-error`

---

## 3. Plantillas y Estructuras Estándar Recomendadas

### Formato A: Tratado Académico Formal / Tesis / Monografía
Para documentos extensos, monografías, informes de investigación formales o tesis con portada institucional, resumen ejecutivo y tabla de contenidos:
* **Características:**
  - Tipografía clásica a `11pt` con clase `article` y microtipografía activa.
  - Márgenes estándar ISO de `2.5 cm` con `geometry`.
  - Portada formal con metadatos completos (`\maketitle`), bloque de resumen (`abstract`) y tabla de contenidos interactiva (`\tableofcontents`).
  - Tablas limpias con `booktabs` / `tabularx` y soporte matemático robusto (`amsmath`, `amssymb`).
  - **Plantilla base:** Ubicada en `.agents/skills/latex-compiler/templates/plantilla-tratado-formal.tex` y en `archivos-generados/plantillas/plantilla-tratado-formal.tex`.

---

### Formato B: Guía de Apuntes Técnicos Compactos (Estilo Pastel - Alto Contraste y Apto Impresión)
Formato de alta densidad de información para apuntes de estudio, guías de laboratorio, cheat-sheets y resúmenes técnicos operativos:
* **Características y Principios de Diseño:**
  - Márgenes reducidos (`1.25 cm`) con `geometry`.
  - Tipografía compacta (`\documentclass[9pt,a4paper]{extarticle}` + `\usepackage{lmodern}`).
  - **Sin encabezado superior** (`\pagestyle{plain}`), **sin portada separada** y **sin índice** (`\tableofcontents` omitido).
  - **Banner superior compacto:** Fondo blanco con borde sutil (`colback=white, colframe=gray!60`) y tabla en dos columnas con título y metadatos.
  - **Paleta pastel armónica de alto contraste (95-97% brillo):** Azul Claro (`#F0F7FF`), Verde Menta (`#F0FDF4`), Ámbar Claro (`#FFFBEB`), Rojo Suave (`#FEF2F2`), Teal (`#F0FDFA`), Púrpura (`#FAF5FF`).
  - **Regla Anti-Empaste de Títulos:** Queda estrictamente prohibido usar barras de título con fondos oscuros y texto saturado (que empastan y se imprimen en negro sólido). Los títulos de `bloqueheader` usan `attach title to upper`, fondo idéntico al bloque, acento lateral (`leftrule=4.5pt`) y tipografía en negro puro (`\color{black}`).
  - **Cajas explicativas (`conceptbox`):** Fondo blanco puro (`colback=white`) para ahorro crítico de tóner, marco fino (`boxrule=0.4pt`), línea lateral cromática (`leftrule=3.5pt`) y título en acento de color integrado.
  - **Tablas Limpias y Estructuradas:** Uso de `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) con `tabularx`. Queda prohibido usar rellenos oscuros en cabeceras de tabla; los títulos de columna van en negrita con texto negro puro.
  - **Cajas de código (`codebox`):** `tcolorbox` con `listings` y estilo `bashstyle`.
  - **Plantilla base:** Ubicada en `.agents/skills/latex-compiler/templates/plantilla-apuntes-pastel.tex` y en `archivos-generados/plantillas/plantilla-apuntes-pastel.tex`.

---

### Formato B2: Apuntes Técnicos Monocromática (1 Columna Sin Margen ni Encabezado)
Formato de alta legibilidad optimizado para impresión física en impresoras láser monocromo (HP LaserJet / tóner 600 DPI):
* **Características:**
  - Tipografía sobria y robusta: **Bitstream Charter** a `10pt` para el cuerpo, **TeX Gyre Heros** para títulos sans-serif y **Courier** para código.
  - **1 Columna Completa (`162 mm`):** Sin columna lateral exterior de notas (`marginparwidth = 0mm`), maximizando el espacio para tablas, fórmulas y definiciones.
  - **Sin Encabezado Superior:** Cero running headers (`\fancyhead{}` vacío, `headheight=0pt`, `\headrulewidth=0pt`), maximizando la altura útil de lectura.
  - **Compensación de Anillado Dúplex:** `bindingoffset = 6mm` para perforado mecánico seguro de 2 o 3 ganchos o espiral sin tocar el texto.
  - **Cajas Técnicas Anti-Solapamiento:** Cajas `definicion`, `alertaparcial` y `formulabox` en blanco y negro con títulos integrados en el flujo superior interno para evitar cruces con bordes.
  - **Plantilla base:** Ubicada en `.agents/skills/latex-compiler/templates/plantilla-apuntes-monocromatica.tex` y en `archivos-generados/plantillas/plantilla-apuntes-monocromatica.tex`.

---

### Formato C: Currículum Vitae Ejecutivo Sans-Serif (1 Columna ATS-Friendly)
Estructura lineal optimizada para roles de ingeniería, infraestructura, desarrollo y máxima compatibilidad con motores ATS:
* **Características:**
  - Tipografía moderna Sans-Serif (`\usepackage{helvet}` + `\renewcommand{\familydefault}{\sfdefault}`).
  - Paleta corporativa sobria: Azul Marino Profundo (`#143769` / `#0F2A5B`), Slate Blue (`#2B6CB0` / `#2563EB`) y Carbón (`#1E293B`).
  - **Macro Anti-Solapamiento:** Uso de `\cvsection` determinista con `\hrule` nativo en lugar del frágil `\titlerule` de `titlesec` para garantizar cero cruce de líneas sobre el contenido.
  - Enlaces interactivos clickeables (`tel:`, `mailto:`, LinkedIn, GitHub).
  - **Variante Estándar (1-2 Páginas a 10pt):** Márgenes `1.05 cm` a `1.25 cm`. Ubicada en `.agents/skills/latex-compiler/templates/plantilla-cv-ejecutivo-sans.tex`.
  - **Variante Compacta (1 Página A4 Estricta a 9pt):** Clase `extarticle` a 9pt, márgenes calibrados (`top=0.7cm`, `bottom=0.55cm`, `sides=1.15cm`). Ubicada en `.agents/skills/latex-compiler/templates/plantilla-cv-ejecutivo-compacto-1pagina.tex`.

---

### Formato D: Currículum Vitae Moderno Visual (2 Columnas con Foto y QR)
Estructura visual asimétrica de alto impacto para perfiles donde la presentación personal, diseño o consultoría comercial son prioritarios:
* **Características:**
  - Dos columnas balanceadas mediante el entorno `paracol` (`5.6 cm` lateral / `12.2 cm` principal).
  - Columna lateral con fotografía de esquinas redondeadas en TikZ y código QR vectorizado.
  - Íconos vectoriales y banderas de idiomas programados nativamente en TikZ (sin dependencias externas).
  - Cajas de perfil profesional en `tcolorbox` con borde lateral sutil.
  - **Plantilla base:** Ubicada en `.agents/skills/latex-compiler/templates/plantilla-cv-moderno-dos-columnas.tex`.

---

### Formato E: Transcripción de Diapositivas y Texto Ultra-Denso (2 Columnas Continuas)
Formato de compresión de superficie diseñado para vaciar presentaciones de PowerPoint (PPT de 30-80 filminas), guías infladas o apuntes largos sin resumir:
* **Características:**
  - Formato a 2 columnas continuas (`twocolumn`) con regla divisoria sutil (`0.3pt`) para empaquetar viñetas breves a longitud de línea ergonómica (55–65 caracteres).
  - Geometría extrema de `1.0 cm` en todos los bordes (92% de superficie útil aprovechada).
  - Cero páginas de portada ni banners iniciales: cabecera mínima de 1 renglón e inicio inmediato en página 1.
  - Macro `\filmina{N}{Título}`: Marcador inline sin salto de página que permite conservar la referencia de la diapositiva original en lectura corrida continua.
  - Tipografía Bitstream Charter a `9pt` monocromo 600 DPI, ultra económica en tóner y de alta nitidez en papel.
  - Pie de página compacto con contador dinámico (`Pág. X de Y`).
  - **Plantilla base:** Ubicada en `.agents/skills/latex-compiler/templates/plantilla-transcripcion-diapositivas.tex` y en `archivos-generados/plantillas/plantilla-transcripcion-diapositivas.tex`.

---

## 4. Flujo de Compilación Paso a Paso

### Paso 1: Escritura del Código Fuente `.tex`
Escribir el código fuente completo en `/home/joaquin/Compartido/braind/archivos-generados/<proyecto>/documento.tex` usando la herramienta nativa `write_to_file`.

### Paso 2: Compilación con `pdflatex` (Doble Pasada)
Ejecutar la compilación en dos pasadas consecutivas para resolver correctamente la tabla de contenidos (`\tableofcontents`), referencias cruzadas y numeración de páginas:

```bash
cd /home/joaquin/Compartido/braind/archivos-generados/<proyecto> && pdflatex -interaction=nonstopmode documento.tex && pdflatex -interaction=nonstopmode documento.tex
```

### Paso 3: Limpieza de Archivos Auxiliares (Opcional pero Recomendado)
Eliminar los archivos temporales de compilación para mantener el directorio limpio, conservando el `.tex` y el `.pdf`:

```bash
cd /home/joaquin/Compartido/braind/archivos-generados/<proyecto> && rm -f *.aux *.log *.out *.toc *.synctex.gz
```

---

## 5. Reporte y Entrega
Al finalizar exitosamente:
1. Notificar al usuario la ruta absoluta del PDF generado:
   `file:///home/joaquin/Compartido/braind/archivos-generados/<proyecto>/documento.pdf`
2. Resumir la estructura de secciones, páginas y contenido del documento entregado.
