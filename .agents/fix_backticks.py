import os
import re
import json

brain_dir = "/home/joaquin/Compartido/braind/brain"
backticked_wikilink_re = re.compile(r"`\[\[([^\]`]+)\]\]`")


def fix_file(path):
    """Corrige wikilinks rodeados de backticks en un solo archivo."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content, count = backticked_wikilink_re.subn(r"[[\1]]", content)
    if count > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        rel = os.path.relpath(path, brain_dir)
        print(f"[Autofix] {rel}: {count} backticked wikilinks removed")
    return count


# --- Determinar qué archivo procesar ---
# Intentar obtener el archivo modificado desde los args del hook de Antigravity.
# Si no está disponible, fallback a escaneo completo (compatibilidad retroactiva).
target_file = None
tool_args_raw = os.environ.get("ANTIGRAVITY_TOOL_ARGS", "")
if tool_args_raw:
    try:
        args = json.loads(tool_args_raw)
        target_file = args.get("TargetFile", "")
    except (json.JSONDecodeError, TypeError):
        pass

if target_file and target_file.startswith(brain_dir) and target_file.endswith(".md"):
    # Caso óptimo: procesar solo el archivo tocado por write_to_file / replace_file_content
    if os.path.isfile(target_file):
        fix_file(target_file)
elif target_file:
    # Archivo fuera de brain/ o no es .md — no aplica, salir silenciosamente
    pass
else:
    # Fallback: escaneo completo (cuando no se detecta ANTIGRAVITY_TOOL_ARGS)
    modified_files = {}
    for root, dirs, files in os.walk(brain_dir):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                count = fix_file(path)
                if count > 0:
                    modified_files[os.path.relpath(path, brain_dir)] = count
    if modified_files:
        print(f"[Autofix] Fallback scan: {len(modified_files)} files corrected")
