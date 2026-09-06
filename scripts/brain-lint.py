#!/usr/bin/env python3
"""
brain-lint: Auditoría Integral y Validación de Salud de la Base de Conocimiento
Verifica: Enlaces rotos, notas no indexadas, sintaxis de wikilinks, frontmatter YAML y normalización de tags.
"""

import os
import sys
import re
import argparse
import json
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAIN_DIR = os.environ.get("BRAIN_DIR", os.path.join(WORKSPACE_ROOT, "brain"))

# Vocabulario Controlado de Tags
FORBIDDEN_TAGS = {
    "ingest": "ingesta",
    "clipping": "clippings"
}

# Colores ANSI
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
BOLD = "\033[1m"
RESET = "\033[0m"

def is_bash_condition(content):
    content = content.strip()
    if content.startswith(('$', '-', '!', '<', '>')): return True
    if re.search(r'\s(==|!=|-eq|-ne|-lt|-le|-gt|-ge|=~)\s', content): return True
    if ' ' in content and content.startswith(('-z', '-n', '-f', '-d', '-e', '-r', '-w', '-x')): return True
    return False

def strip_code_blocks(content):
    # Eliminar bloques de código cercados
    no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Eliminar código en línea
    no_code = re.sub(r'`.*?`', '', no_code)
    return no_code

def validate_frontmatter(content, filepath):
    errors = []
    lines = content.splitlines()
    if not lines:
        return ["Línea 1: Archivo vacío"]

    if lines[0].strip() != "---":
        return ["Línea 1: Falta Frontmatter YAML inicial (---)"]

    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx == -1:
        return ["Línea EOF: Frontmatter YAML mal cerrado, falta '---' final"]

    frontmatter = lines[1:end_idx]
    fields_found = {}

    for i, line in enumerate(frontmatter, start=2):
        line_s = line.strip()
        if not line_s or line_s.startswith('#'):
            continue
        if line.startswith(' ') or line.startswith('\t'):
            continue
        if ':' in line_s:
            key = line_s.split(':', 1)[0].strip()
            value = line_s.split(':', 1)[1].strip()
            if not key.startswith('-'):
                fields_found[key] = value

    # Campos mínimos universales para cualquier nota
    base_required = {'type', 'title', 'tags'}

    note_type = fields_found.get('type', '')
    if note_type == 'session':
        required_fields = base_required | {'date', 'status'}
    else:
        # conceptos, recursos, y cualquier otro tipo: solo base
        required_fields = base_required

    missing = required_fields - set(fields_found.keys())
    if missing:
        errors.append(f"Línea 2-{end_idx+1}: Faltan campos obligatorios para tipo '{note_type}': {', '.join(sorted(missing))}")

    # Validación de campos prohibidos en conceptos / recursos
    if note_type in ('concept', 'resource'):
        forbidden_in_concept = {'date', 'status'} & set(fields_found.keys())
        if forbidden_in_concept:
            errors.append(f"Línea 2-{end_idx+1}: Campos no permitidos para tipo '{note_type}': {', '.join(sorted(forbidden_in_concept))}")

    # Validación de correspondencia entre carpeta y type
    if filepath.startswith("conceptos/") and note_type != "concept":
        errors.append(f"Línea 2-{end_idx+1}: Nota en carpeta 'conceptos/' debe tener 'type: concept' (tiene '{note_type}')")
    elif filepath.startswith("recursos/") and note_type != "resource":
        errors.append(f"Línea 2-{end_idx+1}: Nota en carpeta 'recursos/' debe tener 'type: resource' (tiene '{note_type}')")
    elif filepath.startswith("sesiones/") and note_type != "session":
        errors.append(f"Línea 2-{end_idx+1}: Nota en carpeta 'sesiones/' debe tener 'type: session' (tiene '{note_type}')")

    # Validación de Vocabulario Controlado de Tags
    raw_tags = fields_found.get('tags', '')
    extracted_tags = re.findall(r'[\w\-]+', raw_tags)
    for tag in extracted_tags:
        tag_lower = tag.lower()
        if tag_lower in FORBIDDEN_TAGS:
            errors.append(f"Línea 2-{end_idx+1}: Tag no canónico '{tag}' (debe ser '{FORBIDDEN_TAGS[tag_lower]}')")

    # Validación de coherencia de fecha en sesiones (date vs. nombre de archivo)
    if note_type == 'session':
        date_val = fields_found.get('date', '').strip().strip('"').strip("'")
        if date_val:
            # Verificar formato ISO 8601
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_val):
                errors.append(f"Línea 2-{end_idx+1}: Campo 'date' no es ISO 8601 válido (tiene '{date_val}', esperado AAAA-MM-DD)")
            else:
                # Verificar coherencia con prefijo del nombre de archivo
                filename = os.path.basename(filepath)
                fn_match = re.match(r'^(\d{4}-\d{2}-\d{2})', filename)
                if fn_match and fn_match.group(1) != date_val:
                    errors.append(f"Línea 2-{end_idx+1}: Fecha incoherente: frontmatter 'date: {date_val}' ≠ prefijo archivo '{fn_match.group(1)}'")

    return errors


def validate_session_sections(content, filepath):
    """Valida que las sesiones contengan las 3 secciones obligatorias: Contexto, Decisiones, Pendientes."""
    warnings = []
    required_prefixes = ['contexto', 'decisiones', 'pendientes']
    headings = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
    headings_lower = [h.strip().lower() for h in headings]

    labels = {'contexto': 'Contexto', 'decisiones': 'Decisiones', 'pendientes': 'Pendientes'}
    for prefix in required_prefixes:
        if not any(h.startswith(prefix) for h in headings_lower):
            warnings.append(f"Sección obligatoria faltante: '## {labels[prefix]}'")

    return warnings

def audit_brain(verbose=False, brain_dir=None):
    target_dir = os.path.abspath(brain_dir) if brain_dir else BRAIN_DIR
    if not os.path.exists(target_dir):
        print(f"{RED}❌ Error: No se encontró el directorio {target_dir}{RESET}")
        sys.exit(1)

    all_md_files = {}
    for root, dirs, files in os.walk(target_dir):
        for f in files:
            if f.endswith('.md'):
                rel_path = os.path.relpath(os.path.join(root, f), target_dir)
                base_name = os.path.splitext(f)[0]
                all_md_files[base_name] = rel_path

    index_wikilinks = set()
    indexes_to_process = ["index"]
    processed_indexes = set()

    while indexes_to_process:
        current_index = indexes_to_process.pop(0)
        if current_index in processed_indexes:
            continue
        processed_indexes.add(current_index)
        
        idx_rel_path = all_md_files.get(current_index)
        if not idx_rel_path and current_index == "index":
            idx_rel_path = "index.md"
        elif not idx_rel_path:
            continue
            
        index_path = os.path.join(target_dir, idx_rel_path)
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8", errors="replace") as f:
                index_content = f.read()
            raw_index_links = re.findall(r'\[\[(.*?)\]\]', strip_code_blocks(index_content))
            for l in raw_index_links:
                if not is_bash_condition(l):
                    clean = l.split('|')[0].split('#')[0].strip()
                    if clean:
                        index_wikilinks.add(clean)
                        if clean.startswith("index-") or clean == "Tablero-Pendientes":
                            indexes_to_process.append(clean)

    # 1. Archivos no indexados
    unindexed = [
        name for name in all_md_files 
        if name not in index_wikilinks and not (name == 'index' or name == 'GEMINI' or name.startswith('index-') or name == 'Tablero-Pendientes')
    ]

    # 2. Enlaces rotos y backticks
    broken_links = {}
    backtick_links = {}
    yaml_errors = {}
    session_warnings = {}
    total_wikilinks = 0

    for name, rel_path in all_md_files.items():
        if name == 'GEMINI':
            continue
        full_path = os.path.join(target_dir, rel_path)
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            yaml_errors[rel_path] = [f"Error de lectura: {e}"]
            continue

        if not (name == 'index' or name == 'GEMINI' or name.startswith('index-') or name == 'Tablero-Pendientes'):
            y_errs = validate_frontmatter(content, rel_path)
            if y_errs:
                yaml_errors[rel_path] = y_errs

        # Validar secciones obligatorias en sesiones
        if rel_path.startswith("sesiones/"):
            s_warns = validate_session_sections(content, rel_path)
            if s_warns:
                session_warnings[rel_path] = s_warns

        # Detectar backticks alrededor de wikilinks (ej: `[[link]]` o [[`link`]])
        bad_backticks = re.findall(r'`\[\[.*?\]\]`|\[\[`.*?`\]\]|\[\[.*?`.*?\]\]', content)
        if bad_backticks:
            backtick_links[rel_path] = bad_backticks

        # Buscar enlaces rotos fuera de bloques de código
        clean_content = strip_code_blocks(content)
        links = re.findall(r'\[\[([^\[\]]+?)\]\]', clean_content)
        
        for l in links:
            if is_bash_condition(l):
                continue
            total_wikilinks += 1
            target = l.split('|')[0].split('#')[0].strip()
            if target and target not in all_md_files:
                broken_links.setdefault(rel_path, []).append(l.strip())

    return {
        "target_dir": target_dir,
        "total_files": len(all_md_files),
        "total_wikilinks": total_wikilinks,
        "unindexed": unindexed,
        "broken_links": broken_links,
        "backtick_links": backtick_links,
        "yaml_errors": yaml_errors,
        "session_warnings": session_warnings,
        "all_files": all_md_files
    }

def main():
    parser = argparse.ArgumentParser(description="Auditor de Salud del Cerebro (brain-lint)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Modo detallado")
    parser.add_argument("-j", "--json", action="store_true", help="Salida en JSON")
    parser.add_argument("--brain-dir", default=BRAIN_DIR, help="Ruta al directorio brain (por defecto: entorno local)")
    args = parser.parse_args()

    res = audit_brain(verbose=args.verbose, brain_dir=args.brain_dir)

    if args.json:
        out = {
            "target_dir": res["target_dir"],
            "total_files": res["total_files"],
            "total_wikilinks": res["total_wikilinks"],
            "unindexed_count": len(res["unindexed"]),
            "broken_count": sum(len(v) for v in res["broken_links"].values()),
            "session_warnings_count": sum(len(v) for v in res["session_warnings"].values()),
            "unindexed": res["unindexed"],
            "broken_links": res["broken_links"],
            "backtick_links": res["backtick_links"],
            "yaml_errors": res["yaml_errors"],
            "session_warnings": res["session_warnings"]
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        sys.exit(0 if (len(res["unindexed"]) == 0 and len(res["broken_links"]) == 0 and len(res["yaml_errors"]) == 0 and len(res["backtick_links"]) == 0) else 1)

    print(f"\n{BOLD}{CYAN}┌──────────────────────────────────────────────────────────┐{RESET}")
    print(f"{BOLD}{CYAN}│          AUDITOR DE SALUD DEL CEREBRO (BRAIN-LINT)       │{RESET}")
    print(f"{BOLD}{CYAN}└──────────────────────────────────────────────────────────┘{RESET}")
    print(f"📁 Ruta: {BOLD}{res['target_dir']}{RESET}")
    print(f"📊 Total de notas evaluadas: {BOLD}{res['total_files']}{RESET}")
    print(f"🔗 Total de wikilinks activos: {BOLD}{res['total_wikilinks']}{RESET}\n")

    has_errors = False

    # 1. Reporte de no indexados
    if res["unindexed"]:
        has_errors = True
        print(f"{YELLOW}⚠️  Notas NO indexadas en [[index]] ({len(res['unindexed'])}):{RESET}")
        for u in res["unindexed"]:
            print(f"   • {BOLD}{u}{RESET} ({res['all_files'][u]})")
        print()
    else:
        print(f"{GREEN}✔ Todas las notas están 100% indexadas en [[index]]{RESET}")

    # 2. Reporte de enlaces rotos
    if res["broken_links"]:
        has_errors = True
        print(f"{RED}❌ Enlaces rotos (Wikilinks 404):{RESET}")
        for src, targets in res["broken_links"].items():
            for t in targets:
                print(f"   • En {BOLD}{src}{RESET}: [[{t}]]")
        print()
    else:
        print(f"{GREEN}✔ Cero enlaces rotos detectados en el grafo{RESET}")

    # 3. Reporte de backticks
    if res["backtick_links"]:
        has_errors = True
        print(f"{YELLOW}⚠️  Wikilinks con acentos graves prohibidos (`[[...]]`):{RESET}")
        for src, bts in res["backtick_links"].items():
            for bt in bts:
                print(f"   • En {BOLD}{src}{RESET}: {bt}")
        print()

    # 4. Reporte de YAML y Tags
    if res["yaml_errors"]:
        has_errors = True
        print(f"{RED}❌ Errores de Frontmatter YAML y Vocabulario Controlado:{RESET}")
        for src, errs in res["yaml_errors"].items():
            for err in errs:
                print(f"   • En {BOLD}{src}{RESET}: {err}")
        print()
    else:
        print(f"{GREEN}✔ 100% de Frontmatters YAML válidos y tags canónicos{RESET}")

    # 5. Reporte de secciones faltantes en sesiones (advertencia, no bloquea)
    if res["session_warnings"]:
        total_sw = sum(len(v) for v in res["session_warnings"].values())
        print(f"{YELLOW}📝 Sesiones con secciones faltantes ({total_sw} advertencias en {len(res['session_warnings'])} notas):{RESET}")
        for src, warns in res["session_warnings"].items():
            for w in warns:
                print(f"   • En {BOLD}{src}{RESET}: {w}")
        print()
    else:
        print(f"{GREEN}✔ Todas las sesiones tienen secciones Contexto/Decisiones/Pendientes{RESET}")

    print(f"\n{BOLD}────────────────────────────────────────────────────────────{RESET}")
    if not has_errors:
        print(f"{GREEN}{BOLD}🎉 ESTADO GENERAL: CEREBRO 100% SALUDABLE Y COHERENTE{RESET}\n")
        sys.exit(0)
    else:
        print(f"{RED}{BOLD}⚠️  SE DETECTARON OBSERVACIONES QUE REQUIEREN ATENCIÓN{RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
