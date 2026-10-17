#!/usr/bin/env python3
"""
Módulo de Configuración Central y Resolución de Rutas Portables para braind.
Permite definir rutas mediante .env con fallback inteligente a rutas relativas,
garantizando portabilidad universal al clonar el repositorio en cualquier máquina.
"""

import os
import sys
from pathlib import Path

# Raíz del workspace calculada dinámicamente desde la ubicación de este script
# scripts/config.py -> scripts/ -> braind/ (WORKSPACE_ROOT)
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

# Rutas estándar internas del workspace
BRAIN_DIR = (WORKSPACE_ROOT / "brain").resolve()
ARCHIVOS_GENERADOS_DIR = (WORKSPACE_ROOT / "archivos-generados").resolve()
SCRIPTS_DIR = (WORKSPACE_ROOT / "scripts").resolve()
AGENTS_DIR = (WORKSPACE_ROOT / ".agents").resolve()

def _load_env_file(filepath: Path) -> dict:
    """Parsea un archivo .env simple sin requerir dependencias externas."""
    env_vars = {}
    if not filepath.is_file():
        return env_vars
    try:
        content = filepath.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            # Ignorar líneas vacías y comentarios
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                env_vars[key] = val
    except Exception as e:
        print(f"⚠️ [Config] Error leyendo {filepath}: {e}", file=sys.stderr)
    return env_vars

# Cargar .env si existe en la raíz
_ENV = _load_env_file(WORKSPACE_ROOT / ".env")

# 1. Resolución de la ruta del material académico de referencia
_raw_material_path = (
    os.environ.get("MATERIAL_ACADEMICO_PATH")
    or _ENV.get("MATERIAL_ACADEMICO_PATH")
    or "../material-academico"
)

# Resolver a Path absoluto expandiendo tildes de usuario y rutas relativas
_candidate_material = Path(_raw_material_path).expanduser()
if not _candidate_material.is_absolute():
    MATERIAL_ACADEMICO_DIR = (WORKSPACE_ROOT / _candidate_material).resolve()
else:
    MATERIAL_ACADEMICO_DIR = _candidate_material.resolve()

# 2. Configuración de Homelab (IP o hostname del servidor personal)
HOMELAB_SERVER_IP = (
    os.environ.get("HOMELAB_SERVER_IP")
    or _ENV.get("HOMELAB_SERVER_IP")
    or "192.168.20.200"
)

def get_status() -> dict:
    """Devuelve un resumen del estado de resolución de rutas para diagnóstico."""
    return {
        "workspace_root": str(WORKSPACE_ROOT),
        "brain_dir": str(BRAIN_DIR),
        "brain_exists": BRAIN_DIR.is_dir(),
        "material_academico_dir": str(MATERIAL_ACADEMICO_DIR),
        "material_academico_exists": MATERIAL_ACADEMICO_DIR.is_dir(),
        "homelab_server_ip": HOMELAB_SERVER_IP,
        "env_file_loaded": (WORKSPACE_ROOT / ".env").is_file()
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_status(), indent=2, ensure_ascii=False))
