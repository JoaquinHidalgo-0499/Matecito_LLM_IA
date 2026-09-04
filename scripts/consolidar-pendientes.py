#!/usr/bin/env python3
import os
import re
import yaml
import argparse
import json
import logging
from datetime import datetime
from collections import defaultdict
from pathlib import Path

def parse_frontmatter(content):
    """Extrae el frontmatter YAML de un string."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return {}
    return {}

def extract_pendientes(content):
    """Extrae la lista de tareas pendientes de la sección ## Pendientes."""
    lines = content.split('\n')
    in_pendientes = False
    pendientes = []
    
    for line in lines:
        if re.match(r'^#{2,3}\s+Pendientes', line, re.IGNORECASE):
            in_pendientes = True
            continue
        elif in_pendientes and re.match(r'^#+', line):
            in_pendientes = False
            continue
            
        if in_pendientes:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Match list items: -, *, - [ ], * [ ]
            match = re.match(r'^[-*]\s+(?:\[\s*\]\s+)?(.*)', stripped)
            if match:
                # If there's an explicit [x] or [X] check, ignore it.
                if re.match(r'^[-*]\s+\[[xX]\]', stripped):
                    continue
                    
                task = match.group(1).strip()
                task_lower = task.lower()
                if not task or task_lower.startswith(('ninguno', 'ninguna', 'nada', 'sin pendientes')):
                    continue
                pendientes.append(task)
    return pendientes

def main():
    parser = argparse.ArgumentParser(description="Consolidar pendientes de sesiones de braind.")
    parser.add_argument('--output', default='brain/Tablero-Pendientes.md', help='Archivo de salida Markdown (relativo a braind_dir si no es absoluto).')
    parser.add_argument('--json', action='store_true', help='Generar salida en formato JSON en lugar de Markdown (hacia stdout).')
    parser.add_argument('-v', '--verbose', action='store_true', help='Habilitar logs detallados.')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format='%(levelname)s: %(message)s')

    braind_dir = Path('/home/joaquin/Compartido/braind')
    sesiones_dir = braind_dir / 'brain' / 'sesiones'
    
    if not sesiones_dir.exists():
        logging.error(f"Directorio de sesiones no encontrado: {sesiones_dir}")
        return

    tareas_por_mes = defaultdict(list)
    total_sesiones = 0
    total_pendientes = 0

    for file_path in sesiones_dir.glob('*.md'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Error leyendo {file_path}: {e}")
            continue
            
        total_sesiones += 1
        frontmatter = parse_frontmatter(content)
        date_str = frontmatter.get('date', '') if isinstance(frontmatter, dict) else ''
        
        if not date_str:
            # Try to infer from filename
            match = re.match(r'^(\d{4}-\d{2}-\d{2})', file_path.name)
            if match:
                date_str = match.group(1)
            else:
                date_str = '1970-01-01' # Default fallback
                
        try:
            date_obj = datetime.strptime(str(date_str), '%Y-%m-%d')
            mes_key = date_obj.strftime('%Y-%m')
        except ValueError:
            mes_key = 'Desconocido'
            
        pendientes = extract_pendientes(content)
        
        session_name = file_path.stem
        
        for p in pendientes:
            tareas_por_mes[mes_key].append({
                'tarea': p,
                'sesion': session_name,
                'fecha': str(date_str)
            })
            total_pendientes += 1

    # Sort months descending
    meses_ordenados = sorted(tareas_por_mes.keys(), reverse=True)

    if args.json:
        out_data = {
            'total_sesiones': total_sesiones,
            'total_pendientes': total_pendientes,
            'pendientes_por_mes': {mes: tareas_por_mes[mes] for mes in meses_ordenados}
        }
        print(json.dumps(out_data, indent=2, ensure_ascii=False))
        return

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = braind_dir / output_path
        
    # Create parent dirs if necessary
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("type: board\n")
        f.write("title: Tablero de Pendientes\n")
        f.write("tags: [gestion, pendientes]\n")
        f.write("---\n\n")
        f.write("# Tablero de Pendientes\n\n")
        
        f.write(f"**Última actualización:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Navegación:** [[index]] | [[index-sesiones]]\n\n")
        
        f.write(f"**Métricas:**\n")
        f.write(f"- Sesiones analizadas: {total_sesiones}\n")
        f.write(f"- Pendientes activos: {total_pendientes}\n\n")
        
        for mes in meses_ordenados:
            f.write(f"## {mes}\n\n")
            # sort tasks by date descending within month
            tareas = sorted(tareas_por_mes[mes], key=lambda x: x['fecha'], reverse=True)
            for t in tareas:
                f.write(f"- [ ] {t['tarea']} (en [[{t['sesion']}]])\n")
            f.write("\n")
            
    logging.info(f"Tablero generado en {output_path}")

if __name__ == '__main__':
    main()
