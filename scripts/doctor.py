#!/usr/bin/env python3
"""
scripts/doctor.py - Diagnóstico de Salud y Dependencias del Entorno braind
Inspecciona requisitos del sistema, configuración, rutas y herramientas para skills.
Uso manual: python3 scripts/doctor.py [--json]
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
from pathlib import Path

# Colores ANSI
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Importar configuración central
_script_dir = Path(__file__).resolve().parent
_project_root = _script_dir.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

try:
    from scripts.config import (
        WORKSPACE_ROOT,
        BRAIN_DIR,
        ARCHIVOS_GENERADOS_DIR,
        MATERIAL_ACADEMICO_DIR,
        HOMELAB_SERVER_IP,
    )
except ImportError:
    WORKSPACE_ROOT = _project_root
    BRAIN_DIR = WORKSPACE_ROOT / "brain"
    ARCHIVOS_GENERADOS_DIR = WORKSPACE_ROOT / "archivos-generados"
    MATERIAL_ACADEMICO_DIR = (WORKSPACE_ROOT / ".." / "material-academico").resolve()
    HOMELAB_SERVER_IP = "192.168.20.200"


def check_command(cmd: str) -> tuple[bool, str]:
    """Verifica si un comando está disponible en el PATH y devuelve su ruta."""
    path = shutil.which(cmd)
    return (path is not None, path or "")


def get_cmd_version(cmd: str, flag: str = "--version") -> str:
    """Intenta obtener la versión de un comando."""
    try:
        res = subprocess.run([cmd, flag], capture_output=True, text=True, timeout=2)
        out = (res.stdout or res.stderr).splitlines()
        return out[0].strip() if out else ""
    except Exception:
        return ""


def run_diagnostics() -> dict:
    diag = {
        "workspace": str(WORKSPACE_ROOT),
        "base": {},
        "paths": {},
        "tools": {},
        "hooks": {},
        "suggestions": [],
        "all_ok": True,
    }

    # 1. Base: Python y Git
    py_ok = sys.version_info >= (3, 10)
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    diag["base"]["python"] = {"ok": py_ok, "version": py_ver, "path": sys.executable}
    if not py_ok:
        diag["all_ok"] = False
        diag["suggestions"].append("Se requiere Python 3.10 o superior.")

    git_ok, git_path = check_command("git")
    git_ver = get_cmd_version("git") if git_ok else ""
    diag["base"]["git"] = {"ok": git_ok, "path": git_path, "version": git_ver}
    if not git_ok:
        diag["all_ok"] = False
        diag["suggestions"].append("Git no está instalado. Instálalo mediante el gestor de paquetes de tu distribución.")

    env_file = WORKSPACE_ROOT / ".env"
    diag["base"]["env_file"] = {"present": env_file.is_file(), "path": str(env_file)}

    # 2. Rutas y Bóvedas
    brain_ok = BRAIN_DIR.is_dir()
    index_ok = (BRAIN_DIR / "index.md").is_file() if brain_ok else False
    notes_count = len(list(BRAIN_DIR.rglob("*.md"))) if brain_ok else 0
    diag["paths"]["brain"] = {
        "ok": brain_ok,
        "path": str(BRAIN_DIR),
        "index_present": index_ok,
        "notes_count": notes_count,
    }
    if not brain_ok:
        diag["all_ok"] = False
        diag["suggestions"].append(f"Directorio de conocimiento 'brain/' no encontrado en {BRAIN_DIR}.")

    gen_ok = ARCHIVOS_GENERADOS_DIR.is_dir()
    diag["paths"]["archivos_generados"] = {"ok": gen_ok, "path": str(ARCHIVOS_GENERADOS_DIR)}

    mat_ok = MATERIAL_ACADEMICO_DIR.is_dir()
    mat_count = sum(len(files) for _, _, files in os.walk(MATERIAL_ACADEMICO_DIR)) if mat_ok else 0
    diag["paths"]["material_academico"] = {
        "ok": mat_ok,
        "path": str(MATERIAL_ACADEMICO_DIR),
        "files_count": mat_count,
    }
    if not mat_ok:
        diag["suggestions"].append(
            f"Carpeta de material académico no encontrada en '{MATERIAL_ACADEMICO_DIR}'. "
            "Crea un archivo .env configurando 'MATERIAL_ACADEMICO_PATH' o clona/crea la carpeta correspondiente."
        )

    # 3. Herramientas para Skills
    # 3.1. LaTeX (latex-compiler)
    pdflatex_ok, pdflatex_path = check_command("pdflatex")
    diag["tools"]["pdflatex"] = {
        "ok": pdflatex_ok,
        "path": pdflatex_path,
        "skill": "latex-compiler",
    }
    if not pdflatex_ok:
        diag["suggestions"].append(
            "Para habilitar la compilación de PDFs con la skill 'latex-compiler', instala TeX Live:\n"
            "       • Arch Linux:    sudo pacman -S texlive-basic texlive-latexextra\n"
            "       • Ubuntu/Debian: sudo apt install texlive-latex-base texlive-latex-extra\n"
            "       • Fedora:        sudo dnf install texlive-scheme-basic"
        )

    # 3.2. Poppler Utils (pdftotext, pdfinfo para ingest-materia)
    pdftotext_ok, pdftotext_path = check_command("pdftotext")
    pdfinfo_ok, pdfinfo_path = check_command("pdfinfo")
    poppler_ok = pdftotext_ok and pdfinfo_ok
    diag["tools"]["poppler"] = {
        "ok": poppler_ok,
        "pdftotext": pdftotext_path,
        "pdfinfo": pdfinfo_path,
        "skill": "ingest-materia (lectura de PDFs)",
    }
    if not poppler_ok:
        diag["suggestions"].append(
            "Para habilitar la extracción de texto de PDFs en 'ingest-materia', instala Poppler Utils:\n"
            "       • Arch Linux:    sudo pacman -S poppler\n"
            "       • Ubuntu/Debian: sudo apt install poppler-utils\n"
            "       • Fedora:        sudo dnf install poppler-utils"
        )

    # 4. Hooks y Seguridad
    hooks_json = WORKSPACE_ROOT / ".agents" / "hooks.json"
    hooks_ok = hooks_json.is_file()
    hooks_valid = False
    if hooks_ok:
        try:
            with open(hooks_json, "r", encoding="utf-8") as fh:
                json.load(fh)
            hooks_valid = True
        except Exception:
            hooks_valid = False
    diag["hooks"]["hooks_json"] = {"ok": hooks_ok and hooks_valid, "path": str(hooks_json)}

    protect_py = WORKSPACE_ROOT / ".agents" / "protect_readonly.py"
    diag["hooks"]["protect_readonly"] = {"ok": protect_py.is_file(), "path": str(protect_py)}

    fix_backticks_py = WORKSPACE_ROOT / ".agents" / "fix_backticks.py"
    diag["hooks"]["fix_backticks"] = {"ok": fix_backticks_py.is_file(), "path": str(fix_backticks_py)}

    return diag


def print_human_report(diag: dict):
    print(f"\n{BOLD}{CYAN}┌──────────────────────────────────────────────────────────┐{RESET}")
    print(f"{BOLD}{CYAN}│             BRAIND DOCTOR — DIAGNÓSTICO DE ENTORNO       │{RESET}")
    print(f"{BOLD}{CYAN}└──────────────────────────────────────────────────────────┘{RESET}")
    print(f"📁 Workspace: {BOLD}{diag['workspace']}{RESET}\n")

    # 1. Base
    print(f"{BOLD}[1] ENTORNO BASE{RESET}")
    py = diag["base"]["python"]
    if py["ok"]:
        print(f"  {GREEN}✔{RESET} Python {py['version']} ({BLUE}{py['path']}{RESET})")
    else:
        print(f"  {RED}❌{RESET} Python {py['version']} (Obsoleto, se requiere >= 3.10)")

    git = diag["base"]["git"]
    if git["ok"]:
        ver = f" - {git['version']}" if git["version"] else ""
        print(f"  {GREEN}✔{RESET} Git instalado ({BLUE}{git['path']}{RESET}{ver})")
    else:
        print(f"  {RED}❌{RESET} Git no encontrado en el PATH")

    env_f = diag["base"]["env_file"]
    if env_f["present"]:
        print(f"  {GREEN}✔{RESET} Archivo de entorno .env detectado y activo")
    else:
        print(f"  {YELLOW}ℹ{RESET} Archivo .env no presente (usando valores por defecto Zero-Config)")

    # 2. Rutas
    print(f"\n{BOLD}[2] RUTAS Y BÓVEDAS{RESET}")
    brain = diag["paths"]["brain"]
    if brain["ok"]:
        idx = "con index.md" if brain["index_present"] else "sin index.md"
        print(f"  {GREEN}✔{RESET} Bóveda de conocimiento: {BOLD}brain/{RESET} ({brain['notes_count']} notas, {idx})")
    else:
        print(f"  {RED}❌{RESET} Directorio brain/ no existe en {brain['path']}")

    gen = diag["paths"]["archivos_generados"]
    if gen["ok"]:
        print(f"  {GREEN}✔{RESET} Salida de artefactos: {BOLD}archivos-generados/{RESET} (Disponible)")
    else:
        print(f"  {YELLOW}⚠️{RESET} Carpeta archivos-generados/ no creada aún")

    mat = diag["paths"]["material_academico"]
    if mat["ok"]:
        print(f"  {GREEN}✔{RESET} Material académico: {BOLD}{mat['path']}{RESET} ({mat['files_count']} archivos)")
    else:
        print(f"  {YELLOW}⚠️{RESET} Material académico no encontrado en: {mat['path']}")

    # 3. Herramientas para Skills
    print(f"\n{BOLD}[3] HERRAMIENTAS PARA SKILLS{RESET}")
    poppler = diag["tools"]["poppler"]
    if poppler["ok"]:
        print(f"  {GREEN}✔{RESET} Poppler Utils (pdftotext, pdfinfo) → {CYAN}Habilita 'ingest-materia'{RESET}")
    else:
        print(f"  {YELLOW}⚠️{RESET} Poppler Utils no instalado           → {YELLOW}Limitación en lectura de PDFs{RESET}")

    latex = diag["tools"]["pdflatex"]
    if latex["ok"]:
        print(f"  {GREEN}✔{RESET} pdflatex (TeX Live)                → {CYAN}Habilita 'latex-compiler'{RESET}")
    else:
        print(f"  {YELLOW}⚠️{RESET} pdflatex NO encontrado             → {YELLOW}Skill 'latex-compiler' deshabilitada{RESET}")

    # 4. Hooks
    print(f"\n{BOLD}[4] HOOKS Y SEGURIDAD{RESET}")
    h_json = diag["hooks"]["hooks_json"]
    if h_json["ok"]:
        print(f"  {GREEN}✔{RESET} .agents/hooks.json presente y sintácticamente válido")
    else:
        print(f"  {RED}❌{RESET} .agents/hooks.json falta o contiene errores JSON")

    prot = diag["hooks"]["protect_readonly"]
    if prot["ok"]:
        print(f"  {GREEN}✔{RESET} protect_readonly.py disponible (Guardián de solo lectura)")
    else:
        print(f"  {RED}❌{RESET} protect_readonly.py no encontrado")

    fix = diag["hooks"]["fix_backticks"]
    if fix["ok"]:
        print(f"  {GREEN}✔{RESET} fix_backticks.py disponible (Autocorrector de wikilinks)")
    else:
        print(f"  {RED}❌{RESET} fix_backticks.py no encontrado")

    # Resumen y sugerencias
    print(f"\n{BOLD}{CYAN}────────────────────────────────────────────────────────────{RESET}")
    if not diag["suggestions"]:
        print(f"{GREEN}{BOLD}🎉 ESTADO GENERAL: ENTORNO 100% OPERATIVO PARA TODAS LAS SKILLS{RESET}\n")
    else:
        if diag["all_ok"]:
            print(f"{GREEN}{BOLD}✔ ENTORNO BASE OPERATIVO{RESET} {YELLOW}(con sugerencias para habilidades opcionales):{RESET}")
        else:
            print(f"{RED}{BOLD}❌ SE DETECTARON OBSERVACIONES CRÍTICAS EN EL ENTORNO:{RESET}")

        print(f"\n{BOLD}{YELLOW}💡 SUGERENCIAS DE INSTALACIÓN Y CONFIGURACIÓN:{RESET}")
        for idx, sug in enumerate(diag["suggestions"], start=1):
            print(f"  {idx}. {sug}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Diagnóstico de Entorno y Dependencias braind")
    parser.add_argument("--json", action="store_true", help="Salida estructurada en JSON")
    args = parser.parse_args()

    diag = run_diagnostics()

    if args.json:
        print(json.dumps(diag, indent=2, ensure_ascii=False))
    else:
        print_human_report(diag)

    # Retornar código de salida acorde
    if not diag["all_ok"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
