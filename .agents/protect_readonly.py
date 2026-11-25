import sys
import os
import json
import re

_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

try:
    from scripts.config import MATERIAL_ACADEMICO_DIR
    PROTECTED_DIRS = [str(MATERIAL_ACADEMICO_DIR)]
except Exception:
    PROTECTED_DIRS = [
        os.path.realpath(os.path.join(_project_root, "..", "material-academico")),
    ]

DANGEROUS_CMD_REGEX = re.compile(
    r"\b(rm|mv|cp|touch|mkdir|rmdir|ln|install|chmod|chown|sed\s+-i|truncate|dd|tee|rsync|unlink|shred|python[0-9.]*\s+.*-c)\b|>{1,2}",
    re.IGNORECASE
)

_base_folder_name = os.path.basename(PROTECTED_DIRS[0])
CMD_TARGETS_REGEX = re.compile(
    rf"(?:^|[\s\"'/])(?:[^\s\"']*/)?{re.escape(_base_folder_name)}(?:/|[\s\"']|$)",
    re.IGNORECASE
)


def is_protected_file(path: str, base_cwd: str = "") -> bool:
    if not path:
        return False
    try:
        expanded = os.path.expanduser(path)
        if not os.path.isabs(expanded):
            expanded = os.path.join(base_cwd or _project_root, expanded)
        real = os.path.realpath(expanded)
        for pdir in PROTECTED_DIRS:
            real_pdir = os.path.realpath(pdir)
            if real == real_pdir or real.startswith(real_pdir + os.sep):
                return True
    except Exception:
        pass
    return False


def is_protected_command(cmd: str, cwd: str) -> bool:
    if is_protected_file(cwd):
        return True
    if CMD_TARGETS_REGEX.search(cmd):
        return True
    return False


def check_pre_tool_use(payload: dict) -> dict:
    tool_call = payload.get("toolCall") or payload.get("tool_call") or {}
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args", {})
    payload_cwd = payload.get("cwd", "")

    # 1. Herramientas nativas de edición/escritura de archivos
    if tool_name in (
        "write_file",
        "edit_file",
        "write_to_file",
        "replace_file_content",
        "multi_replace_file_content",
    ):
        target_file = (
            args.get("Path")
            or args.get("path")
            or args.get("TargetFile")
            or args.get("target_file")
            or ""
        )
        if is_protected_file(target_file, payload_cwd):
            return {
                "decision": "deny",
                "reason": f"Acceso denegado por política de seguridad: La ruta '{target_file}' pertenece a un repositorio de SOLO LECTURA."
            }

    # 2. Comandos de consola mediante run_command
    elif tool_name == "run_command":
        cmd = args.get("CommandLine", "")
        cwd = args.get("Cwd") or payload_cwd
        if is_protected_command(cmd, cwd):
            if DANGEROUS_CMD_REGEX.search(cmd):
                return {
                    "decision": "deny",
                    "reason": "Acceso denegado por política de seguridad: El comando intenta modificar un repositorio de SOLO LECTURA."
                }

    return {"decision": "allow"}


def main():
    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input:
            print(json.dumps({"decision": "allow"}))
            return
        payload = json.loads(raw_input)
        result = check_pre_tool_use(payload)
        print(json.dumps(result))
    except Exception as exc:
        # Ante fallo de parseo, solicitar confirmación explícita en lugar de permitir silenciosamente
        print(json.dumps({
            "decision": "ask",
            "reason": f"No se pudo validar el payload en protect_readonly.py ({exc}); se requiere confirmación."
        }))


if __name__ == "__main__":
    main()
