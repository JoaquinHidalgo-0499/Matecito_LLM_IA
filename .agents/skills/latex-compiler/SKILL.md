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

### Formato A: Tratado Académico Formal / Tesis
Para documentos extensos, monografías o informes formales con portada, resumen y tabla de contenidos:

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[spanish,es-tabla]{babel}
\usepackage{geometry}
\geometry{top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{microtype}
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=blue!80!black,
    urlcolor=blue!80!black,
    citecolor=blue!80!black
}

\title{\textbf{Título del Documento}}
\author{Hugo Joaquín Hidalgo}
\date{\today}

\begin{document}
\maketitle

\begin{abstract}
Resumen ejecutivo del documento o guía técnica.
\end{abstract}

\tableofcontents
\newpage

\section{Introducción}
Contenido del documento...

\end{document}
```

---

### Formato B: Guía de Apuntes Técnicos Compactos (Estilo Pastel)
Formato de alta densidad de información para apuntes de estudio, guías de laboratorio, cheat-sheets y resúmenes técnicos operativos:
* **Características:**
  - Márgenes chicos (`1.25 cm`) con `geometry`.
  - Tipografía compacta (`\documentclass[9pt,a4paper]{extarticle}` + `\usepackage{lmodern}`).
  - **Sin encabezado superior** (`\pagestyle{plain}`), **sin portada separada** y **sin índice** (`\tableofcontents` omitido).
  - **Banner superior compacto** en la primera página con título, subtítulo e institución.
  - **Paleta pastel armónica por bloques/módulos:** Azul Pastel (`#EBF4FA` / `#2B6CB0`), Verde Pastel (`#EAF7ED` / `#2F855A`), Ámbar Pastel (`#FEF3E9` / `#C05621`), Púrpura Pastel (`#F6EEFB` / `#6B46C1`).
  - **Cajas explicativas:** `conceptbox` / `whybox` con fondo pastel y barra lateral para fundamentaciones ("Por qué").
  - **Cajas de código:** `codebox` (`tcolorbox` con `listings` y estilo `bashstyle`).
  - **Plantilla base:** Ubicada en `.agents/skills/latex-compiler/templates/plantilla-apuntes-compactos-pastel.tex`.

---

### Formato C: Currículum Vitae Ejecutivo Sans-Serif (1 Columna ATS-Friendly)
Estructura lineal optimizada para roles de ingeniería, infraestructura, desarrollo y máxima compatibilidad con motores ATS:
* **Características:**
  - Tipografía moderna Sans-Serif (`\usepackage{helvet}` + `\renewcommand{\familydefault}{\sfdefault}`).
  - Tamaño base de `10pt` con márgenes equilibrados (`1.05 cm` a `1.25 cm`).
  - Paleta corporativa sobria: Azul Marino Profundo (`#143769`), Slate Blue (`#2B6CB0`) y Carbón (`#1E293B`).
  - Separación clara entre viñetas y títulos con línea divisoria fina (`titlerule`).
  - Enlaces interactivos clickeables (`tel:`, `mailto:`, LinkedIn, GitHub).
  - **Plantilla base:** Ubicada en `.agents/skills/latex-compiler/templates/plantilla-cv-ejecutivo-sans.tex`.

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
