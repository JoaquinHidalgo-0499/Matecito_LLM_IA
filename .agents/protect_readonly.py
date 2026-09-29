import sys
import json
import re

PROTECTED_PATTERNS = [
    "material-academico",
]

DANGEROUS_CMD_REGEX = re.compile(
    r"\b(rm|mv|cp|touch|chmod|chown|sed\s+-i|truncate|dd|tee|rsync|unlink|shred)\b|>{1,2}",
    re.IGNORECASE
)


def is_protected_path(path: str) -> bool:
    if not path:
        return False
    return any(p in path for p in PROTECTED_PATTERNS)


def check_pre_tool_use(payload: dict) -> dict:
    tool_call = payload.get("toolCall") or payload.get("tool_call") or {}
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args", {})

    # 1. Herramientas nativas de edición/escritura de archivos
    if tool_name in ("write_to_file", "replace_file_content", "multi_replace_file_content"):
        target_file = args.get("TargetFile", "")
        if is_protected_path(target_file):
            return {
                "decision": "deny",
                "reason": f"Acceso denegado por política de seguridad: La ruta '{target_file}' pertenece a un repositorio de SOLO LECTURA."
            }

    # 2. Comandos de consola mediante run_command
    elif tool_name == "run_command":
        cmd = args.get("CommandLine", "")
        cwd = args.get("Cwd", "")
        if is_protected_path(cmd) or is_protected_path(cwd):
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
    except Exception:
        # En caso de error inesperado, permitir para no bloquear el agente de forma errónea
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
