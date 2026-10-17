---
name: compilador-pdf
description: >-
  Usa este skill cuando el usuario pida generar, diseñar, redactar o compilar documentos
  académicos, guías de estudio, resúmenes, tratados técnicos o CVs en formato PDF usando
  Typst (motor moderno y ultra-rápido en Rust) o LaTeX (pdflatex).
---

# Compilador de Documentos y Tratados (Compilador PDF: Typst & LaTeX)

Procedimiento estandarizado para la redacción, maquetación y compilación de documentos profesionales en PDF mediante arquitectura multi-motor: **Typst** (motor principal de alto rendimiento en Rust) y **LaTeX** (motor de compatibilidad académica formal).

---

## 1. Reglas de Ubicación y Propósito
* **Carpeta Exclusiva de Salida:** Todo archivo fuente (`.typ` o `.tex`), archivo auxiliar y `.pdf` final debe generarse **única y exclusivamente** dentro de:
  `archivos-generados/<nombre-proyecto>/`
* **Prohibición:** Está terminantemente prohibido generar artefactos de compilación dentro de `brain/` o en las carpetas académicas de referencia (`material-academico/`).
* **Propósito y Exclusión de LINT:** `archivos-generados/` es exclusivamente una carpeta de salida y entrega de entregables para el usuario. No participa en la administración interna de `braind` ni forma parte del grafo de notas. **Está terminantemente prohibido ejecutar `brain-lint.py` o la skill `brain-audit` tras compilar o generar archivos en esta carpeta.**

---

## 2. Motores de Compilación Soportados

| Criterio | Motor Typst (Recomendado) | Motor LaTeX (Compatibilidad) |
| :--- | :--- | :--- |
| **Binario** | `typst` (Escrito en Rust) | `pdflatex` (TeX Live) |
| **Extensión** | `.typ` | `.tex` |
| **Tiempo de Compilación** | **15 – 80 ms** (1 pasada directa) | 3 – 10 segundos (2 pasadas consecutivas) |
| **Archivos Auxiliares** | **Cero** (compila directamente al PDF) | Genera `.aux`, `.log`, `.toc`, `.synctex.gz` |
| **Cuándo Usarlo** | **Por defecto** para apuntes, guías, resúmenes, cheat-sheets y CVs. | Cuando la cátedra o revista exija específicamente entrega de código fuente `.tex`. |

---

## 3. Protocolo Anti-Improvisación y Verificación Previa

Antes de escribir código o intentar compilar, el asistente debe comprobar la disponibilidad del motor elegido en el sistema:

* **Para compilar con Typst:** Comprobar `which typst`.
* **Para compilar con LaTeX:** Comprobar `which pdflatex`.

### Regla de Detención Inmediata y Transparencia:
Si el binario solicitado **NO** está disponible en el PATH:
1. **Prohibición Absoluta de Simulación:** Queda terminantemente prohibido improvisar scripts con bibliotecas alternativas (`reportlab`, `fpdf`), generar archivos vacíos o simular que se compiló el documento.
2. **Notificación al Usuario:** El asistente debe detener el flujo y notificar de forma transparente:
   * **Si falta Typst:**
     > *"⚠️ Typst no se encuentra instalado en el sistema.*  
     > *Para instalarlo rápidamente (pesa solo 45 MB):*  
     > *• Arch Linux: `sudo pacman -S typst`*  
     > *• Ubuntu / Debian: `sudo apt install typst` (o vía `cargo install typst-cli`)*  
     > *• Binario universal: Disponible en GitHub Releases (Typst).*  
     > 
     > *Opciones: 1. Instalar Typst y compilar, 2. Compilar con LaTeX (`pdflatex`) si está disponible, 3. Generar únicamente el archivo fuente `.typ`."*
   * **Si falta LaTeX:**
     > *"⚠️ pdflatex no se encuentra instalado en el sistema.*  
     > *Para instalar TeX Live:*  
     > *• Arch Linux: `sudo pacman -S texlive-basic texlive-latexextra`*  
     > *• Ubuntu / Debian: `sudo apt install texlive-latex-base texlive-latex-extra`*  
     > 
     > *Opciones: 1. Instalar TeX Live, 2. Compilar con Typst si está disponible, 3. Generar únicamente el archivo fuente `.tex`."*

---

## 4. Plantillas Estándar Disponibles (`templates/`)

Ubicadas en `.agents/skills/compilador-pdf/templates/`:

### Formato A: Tratado Académico Formal / Monografía
* **Versión Typst:** `plantilla-tratado-formal.typ`
  - Tipografía `Linux Libertine` o `Charter` a `10.5pt`, márgenes ISO `2.5cm`.
  - Portada con metadatos completos, resumen y tabla de contenidos generada con `#outline()`.
* **Versión LaTeX:** `plantilla-tratado-formal.tex`
  - Clase `article` a `11pt`, márgenes `geometry`, `\maketitle`, `abstract` y `\tableofcontents`.

### Formato B: Plantilla Pastel (Apuntes Técnicos con Acento Cromático)
* **Versión Typst:** `plantilla-pastel.typ`
  - Márgenes reducidos (`1.25cm`), tipografía sans-serif compacta a `9pt`.
  - Banner superior en dos columnas con metadatos, sin portada separada.
  - Cajas de concepto (`#conceptbox(...)`) con fondo blanco puro y línea lateral pastel para ahorro de tinta/tóner.
* **Versión LaTeX:** `plantilla-pastel.tex`
  - Clase `extarticle` a `9pt`, `geometry`, cajas `tcolorbox` con acento lateral y fondo blanco.

### Formato C: Plantilla Monocromática (Impresión Láser / Alto Rendimiento)
* **Versión Typst:** `plantilla-monocromatica.typ`
  - Formato a 1 columna continua con ancho completo y compensación para anillado/perforado.
  - Tipografía serif de alto contraste (`10pt`), sin distracciones visuales ni encabezados superiores.
  - Cajas modulares (`#definicion`, `#alertaparcial`, `#formulabox`) 100% negro puro sobre blanco.
* **Versión LaTeX:** `plantilla-monocromatica.tex`
  - Clase `extarticle` a `10pt` con fuente Charter, geometría de 1 columna (162 mm útil), reglas de 0.8pt y ahorro total de tóner.

### Formato D: CV Ejecutivo ATS (1 Página A4)
* **Versión Typst:** `plantilla-cv-ejecutivo.typ`
  - Tipografía compacta a `9pt`, presupuesto vertical calibrado a exactamente 1 página sin desbordes.
* **Versión LaTeX:** `plantilla-cv-ejecutivo-compacto-1pagina.tex`
  - Clase `extarticle` a `9pt`, secciones con `\cvsection` y macros anti-solapamiento.

---

## 5. Flujos de Compilación Paso a Paso

### Flujo 1: Compilación con Typst (Recomendado)

```bash
# Paso 1: Escritura del fuente en archivos-generados/<proyecto>/documento.typ
# Paso 2: Compilación directa (una sola pasada instantánea)
typst compile archivos-generados/<proyecto>/documento.typ archivos-generados/<proyecto>/documento.pdf
```
*No requiere limpieza de archivos auxiliares.*

### Flujo 2: Compilación con LaTeX

```bash
# Paso 1: Escritura del fuente en archivos-generados/<proyecto>/documento.tex
# Paso 2: Compilación con doble pasada para referencias cruzadas
pdflatex -interaction=nonstopmode -output-directory=archivos-generados/<proyecto> archivos-generados/<proyecto>/documento.tex && pdflatex -interaction=nonstopmode -output-directory=archivos-generados/<proyecto> archivos-generados/<proyecto>/documento.tex

# Paso 3: Limpieza de auxiliares temporales
rm -f archivos-generados/<proyecto>/*.aux archivos-generados/<proyecto>/*.log archivos-generados/<proyecto>/*.out archivos-generados/<proyecto>/*.toc archivos-generados/<proyecto>/*.synctex.gz
```

---

## 6. Reporte y Entrega
Al concluir la compilación exitosa:
1. Notificar al usuario el enlace al archivo PDF generado:
   `[Documento PDF](file:///ruta/absoluta/archivos-generados/<proyecto>/documento.pdf)`
2. Resumir la cantidad de páginas, motor utilizado (Typst o LaTeX) y estructura del documento entregado.
