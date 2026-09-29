#!/usr/bin/env python3
"""
Escáner Inteligente de Novedades Académicas
Detecta archivos nuevos, modificados o eliminados en las carpetas de materias.
Ubicación canónica: scripts/escanear-materias.py
"""

import os
import sys
import json
import argparse
import datetime

_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)
MANIFEST_PATH = os.path.join(_project_root, ".manifest-materias.json")
_compartido_dir = os.path.dirname(_project_root)

SCAN_DIRS = [
    os.path.join(_compartido_dir, "material-academico")
]

IGNORED_PATTERNS = [
    ".directory", ".stfolder", ".syncthing", ".git", ".swp", ".tmp",
    "__pycache__", ".DS_Store"
]

# Colores ANSI
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
BOLD = "\033[1m"
RESET = "\033[0m"

def is_ignored(name):
    for pat in IGNORED_PATTERNS:
        if pat in name:
            return True
    return False

def scan_current_state():
    state = {}
    for base_dir in SCAN_DIRS:
        if not os.path.exists(base_dir):
            continue
        base_name = os.path.basename(base_dir)
        for root, dirs, files in os.walk(base_dir):
            # Filtrar carpetas ignoradas
            dirs[:] = [d for d in dirs if not is_ignored(d)]
            for f in files:
                if is_ignored(f):
                    continue
                full_path = os.path.join(root, f)
                try:
                    stat = os.stat(full_path)
                    rel_path = os.path.relpath(full_path, _compartido_dir)
                    parts = rel_path.split(os.sep)
                    group = parts[1] if len(parts) > 1 else parts[0]
                    subject = parts[2] if len(parts) > 2 else "General"
                    state[rel_path] = {
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "full_path": full_path,
                        "group": group,
                        "subject": subject,
                        "file": f
                    }
                except OSError:
                    continue
    return state

def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_manifest(state):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def main():
    parser = argparse.ArgumentParser(description="Escáner Inteligente de Novedades Académicas")
    parser.add_argument("--update", "-u", action="store_true", help="Actualiza el manifiesto con el estado actual")
    parser.add_argument("--json", "-j", action="store_true", help="Salida en formato JSON")
    args = parser.parse_args()

    current_state = scan_current_state()
    manifest = load_manifest()

    if args.update:
        if not current_state and manifest:
            print(f"{RED}⚠️ Advertencia: No se detectaron archivos en el material académico. El directorio podría estar desmontado. Manifiesto NO modificado.{RESET}", file=sys.stderr)
            sys.exit(1)
        save_manifest(current_state)
        if args.json:
            print(json.dumps({"status": "updated", "total_files": len(current_state)}))
        else:
            print(f"{GREEN}✔ Manifiesto actualizado exitosamente.{RESET}")
            print(f"📊 Total de archivos registrados: {BOLD}{len(current_state)}{RESET}")
        return

    if not manifest:
        if args.json:
            print(json.dumps({"status": "no_manifest", "message": "Manifiesto no encontrado. Ejecutar con --update para crearlo."}))
        else:
            print(f"{YELLOW}⚠️ No se encontró manifiesto previo ({MANIFEST_FILE}).{RESET}")
            print(f"Para inicializar el manifiesto por primera vez, ejecuta: {BOLD}python3 scripts/escanear-materias.py --update{RESET}")
        return

    # Comparar estados
    new_files = {}
    modified_files = {}
    deleted_files = []

    for rel_path, info in current_state.items():
        if rel_path not in manifest:
            subj = f"{info['group']}/{info['subject']}"
            new_files.setdefault(subj, []).append(info)
        else:
            prev_info = manifest[rel_path]
            prev_mtime = prev_info.get('mtime', 0.0)
            prev_size = prev_info.get('size', -1)
            if abs(info['mtime'] - prev_mtime) > 1.0 or info['size'] != prev_size:
                subj = f"{info['group']}/{info['subject']}"
                modified_files.setdefault(subj, []).append(info)

    for rel_path in manifest:
        if rel_path not in current_state:
            deleted_files.append(rel_path)

    if args.json:
        out = {
            "total_current": len(current_state),
            "new_count": sum(len(v) for v in new_files.values()),
            "modified_count": sum(len(v) for v in modified_files.values()),
            "deleted_count": len(deleted_files),
            "new_files": new_files,
            "modified_files": modified_files,
            "deleted_files": deleted_files
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    # Salida visual amigable
    total_new = sum(len(v) for v in new_files.values())
    total_mod = sum(len(v) for v in modified_files.values())

    print(f"\n{BOLD}{CYAN}┌──────────────────────────────────────────────────────────┐{RESET}")
    print(f"{BOLD}{CYAN}│        ESCÁNER DE NOVEDADES ACADÉMICAS - BRAIN           │{RESET}")
    print(f"{BOLD}{CYAN}└──────────────────────────────────────────────────────────┘{RESET}")
    print(f"📁 Monitoreando: {BOLD}material-academico{RESET}")
    print(f"📊 Total de archivos en disco: {BOLD}{len(current_state)}{RESET}\n")

    if total_new == 0 and total_mod == 0 and len(deleted_files) == 0:
        print(f"{GREEN}✔ Todo se encuentra al día. No hay archivos nuevos ni cambios.{RESET}\n")
        return

    if total_new > 0:
        print(f"{YELLOW}⚡ Se detectaron {BOLD}{total_new}{RESET}{YELLOW} archivo(s) NUEVO(S):{RESET}")
        for subj, files in sorted(new_files.items()):
            print(f"\n  📚 {BOLD}{subj}{RESET}:")
            for f in files:
                sz = format_size(f['size'])
                print(f"     ➕ {f['file']} {BLUE}({sz}){RESET}")

    if total_mod > 0:
        print(f"\n{YELLOW}📝 Se detectaron {BOLD}{total_mod}{RESET}{YELLOW} archivo(s) MODIFICADO(S):{RESET}")
        for subj, files in sorted(modified_files.items()):
            print(f"\n  📚 {BOLD}{subj}{RESET}:")
            for f in files:
                sz = format_size(f['size'])
                print(f"     🔄 {f['file']} {BLUE}({sz}){RESET}")

    if deleted_files:
        print(f"\n{RED}🗑️ Archivos eliminados del disco ({len(deleted_files)}):{RESET}")
        for df in deleted_files[:5]:
            print(f"     ❌ {df}")
        if len(deleted_files) > 5:
            print(f"     ... y {len(deleted_files)-5} más")

    print(f"\n{CYAN}💡 Para aceptar estos cambios y sincronizar el manifiesto:{RESET}")
    print(f"   {BOLD}python3 scripts/escanear-materias.py --update{RESET}\n")

if __name__ == "__main__":
    main()
