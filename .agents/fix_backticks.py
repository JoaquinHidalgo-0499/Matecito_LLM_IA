import os
import sys
import re
import json

# Derivar brain_dir desde la ubicación del script (portabilidad)
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)  # .agents/ -> raíz del proyecto
brain_dir = os.path.join(_project_root, "brain")
backticked_wikilink_re = re.compile(r"`\[\[([^\]`]+)\]\]`")


def fix_file(path):
    """Corrige wikilinks rodeados de backticks en un solo archivo."""
    if not os.path.isfile(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content, count = backticked_wikilink_re.subn(r"[[\1]]", content)
    if count > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        rel = os.path.relpath(path, brain_dir)
        print(f"[Autofix] {rel}: {count} backticked wikilinks removed", file=sys.stderr)
    return count


def main():
    target_file = None

    # 1. Leer payload desde stdin (estándar de Antigravity PostToolUse)
    try:
        raw_input = sys.stdin.read().strip()
        if raw_input:
            payload = json.loads(raw_input)
            tool_call = payload.get("toolCall") or payload.get("tool_call") or {}
            args = tool_call.get("args") or payload.get("args") or {}
            target_file = args.get("TargetFile") or args.get("target_file")
    except Exception:
        pass

    # 2. Fallback a variable de entorno si estuviera presente
    if not target_file:
        tool_args_raw = os.environ.get("ANTIGRAVITY_TOOL_ARGS", "")
        if tool_args_raw:
            try:
                args = json.loads(tool_args_raw)
                target_file = args.get("TargetFile", "")
            except Exception:
                pass

    # 3. Procesar archivo o fallback
    if target_file and target_file.startswith(brain_dir) and target_file.endswith(".md"):
        # Caso óptimo: procesar exclusivamente el archivo modificado
        fix_file(target_file)
    elif target_file:
        # Archivo fuera de brain/ o no es .md — no requiere acción
        pass
    else:
        # Fallback de seguridad: si no se pudo determinar el archivo, escaneo completo
        modified_files = {}
        for root, dirs, files in os.walk(brain_dir):
            for f in files:
                if f.endswith(".md"):
                    path = os.path.join(root, f)
                    count = fix_file(path)
                    if count > 0:
                        modified_files[os.path.relpath(path, brain_dir)] = count
        if modified_files:
            print(f"[Autofix] Fallback scan: {len(modified_files)} files corrected", file=sys.stderr)

    # PostToolUse espera {} en stdout
    print(json.dumps({}))


if __name__ == "__main__":
    main()
