#!/usr/bin/env python3
"""
brain-stats: Estadísticas y Métricas del Grafo de Conocimiento
"""

import os
import sys
import re
import json
import argparse
from collections import Counter

BRAIN_DIR = "/home/joaquin/Compartido/braind/brain"

# Colores ANSI
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
MAGENTA = "\033[1;35m"
BOLD = "\033[1m"
RESET = "\033[0m"

def draw_bar(value, max_value, width=20):
    if max_value == 0:
        return "░" * width
    filled = int((value / max_value) * width)
    return "█" * filled + "░" * (width - filled)

def extract_tags(content):
    tags = []
    lines = content.splitlines()
    if lines and lines[0].strip() == "---":
        in_tags = False
        for i in range(1, len(lines)):
            line = lines[i]
            if line.strip() == "---":
                break
            
            if line.startswith("tags:"):
                val = line.split("tags:", 1)[1].strip()
                if val.startswith("[") and val.endswith("]"):
                    t_list = val[1:-1].split(",")
                    tags.extend([t.strip() for t in t_list if t.strip()])
                elif val:
                    tags.extend([t.strip() for t in val.split(",") if t.strip()])
                else:
                    in_tags = True
                continue
            
            if in_tags:
                if line.strip().startswith("-"):
                    tags.append(line.strip()[1:].strip())
                elif not line.startswith(" ") and not line.startswith("\t"):
                    in_tags = False
    return [t.strip('"\'') for t in tags if t]

def count_words_and_lines(content, ignore_code_and_yaml=True):
    if not ignore_code_and_yaml:
        return len(content.split()), len(content.splitlines())

    lines = content.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                lines = lines[i+1:]
                break
    
    text_no_yaml = "\n".join(lines)
    text_no_code = re.sub(r'```.*?```', '', text_no_yaml, flags=re.DOTALL)
    
    l_count = len([l for l in text_no_code.splitlines() if l.strip()])
    w_count = len(text_no_code.split())
    return w_count, l_count

def get_stats():
    categories = Counter()
    tags_count = Counter()
    inbound_links = Counter()
    outbound_links_count = Counter()
    all_files = set()
    
    total_lines = 0
    total_words = 0
    total_bytes = 0
    file_count = 0
    session_count = 0

    for root, dirs, files in os.walk(BRAIN_DIR):
        for f in files:
            if f.endswith('.md'):
                file_count += 1
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, BRAIN_DIR)
                base_name = os.path.splitext(f)[0]
                all_files.add(base_name)
                
                cat = rel_path.split(os.sep)[0] if os.sep in rel_path else "raiz"
                categories[cat] += 1
                if cat == "sesiones":
                    session_count += 1

                stat = os.stat(full_path)
                total_bytes += stat.st_size

                try:
                    with open(full_path, "r", encoding="utf-8", errors="replace") as file:
                        content = file.read()
                        w, l = count_words_and_lines(content)
                        total_words += w
                        total_lines += l

                        for t in extract_tags(content):
                            tags_count[t] += 1

                        clean_content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
                        links = re.findall(r'\[\[([^\[\]]+?)\]\]', clean_content)
                        
                        valid_links = []
                        for link in links:
                            link_clean = link.strip()
                            if link_clean.startswith(('-', '$', '!', '<', '>')): continue
                            if re.search(r'\s(==|!=|-eq|-ne|-lt|-le|-gt|-ge|=~)\s', link_clean): continue
                            target = link_clean.split('|')[0].split('#')[0].strip()
                            if target:
                                inbound_links[target] += 1
                                valid_links.append(target)
                        
                        outbound_links_count[base_name] = len(valid_links)
                except Exception:
                    continue

    # Orphan nodes (no inbound, no outbound)
    orphans = [
        f for f in all_files 
        if inbound_links.get(f, 0) == 0 and outbound_links_count.get(f, 0) == 0 and f not in ['index', 'GEMINI']
    ]
    
    total_edges = sum(inbound_links.values())
    density = 0
    if file_count > 1:
        density = total_edges / (file_count * (file_count - 1))

    return {
        "file_count": file_count,
        "session_count": session_count,
        "total_lines": total_lines,
        "total_words": total_words,
        "total_bytes": total_bytes,
        "categories": categories,
        "tags_count": tags_count,
        "top_nodes": inbound_links.most_common(10),
        "orphans": orphans,
        "density": density,
        "total_edges": total_edges
    }

def main():
    parser = argparse.ArgumentParser(description="Estadísticas de la Base de Conocimiento (brain-stats)")
    parser.add_argument("-j", "--json", action="store_true", help="Salida en JSON")
    args = parser.parse_args()

    s = get_stats()

    if args.json:
        print(json.dumps(s, indent=2, ensure_ascii=False))
        return

    mb_size = s["total_bytes"] / (1024 * 1024)

    print(f"\n{BOLD}{CYAN}┌──────────────────────────────────────────────────────────┐{RESET}")
    print(f"{BOLD}{CYAN}│        ESTADÍSTICAS DEL GRAFO DE CONOCIMIENTO (BRAIN)    │{RESET}")
    print(f"{BOLD}{CYAN}└──────────────────────────────────────────────────────────┘{RESET}")
    print(f"📊 {BOLD}Métricas Generales:{RESET}")
    print(f"   • Total de notas Markdown:    {BOLD}{GREEN}{s['file_count']}{RESET}")
    print(f"   • Total de palabras útiles:   {BOLD}{YELLOW}{s['total_words']:,}{RESET} (ignora YAML/código)")
    print(f"   • Total de líneas de texto:   {BOLD}{BLUE}{s['total_lines']:,}{RESET}")
    print(f"   • Tamaño total en disco:      {BOLD}{MAGENTA}{mb_size:.2f} MB{RESET}")
    print(f"   • Conexiones totales (edges): {BOLD}{CYAN}{s['total_edges']}{RESET}")
    print(f"   • Densidad del Grafo:         {BOLD}{s['density']:.4f}{RESET}\n")

    print(f"📁 {BOLD}Distribución por Categorías:{RESET}")
    max_cat = max(s["categories"].values()) if s["categories"] else 1
    for cat, count in s["categories"].most_common():
        pct = (count / s["file_count"]) * 100
        bar = draw_bar(count, max_cat)
        print(f"   • {BOLD}{cat.capitalize():<15}{RESET}: {count:>3} notas | {CYAN}{bar}{RESET} {pct:>5.1f}%")

    print(f"\n🔗 {BOLD}Top Hubs de Conocimiento (Más referenciados):{RESET}")
    max_hub = s["top_nodes"][0][1] if s["top_nodes"] else 1
    for node, count in s["top_nodes"]:
        if node not in ['index', 'GEMINI']:
            bar = draw_bar(count, max_hub, width=15)
            print(f"   • [[{BOLD}{node}{RESET}]] {MAGENTA}{bar}{RESET} {count} refs")

    print(f"\n🏷️  {BOLD}Top Etiquetas Temáticas:{RESET}")
    max_tag = s["tags_count"].most_common(1)[0][1] if s["tags_count"] else 1
    for tag, count in s["tags_count"].most_common(8):
        bar = draw_bar(count, max_tag, width=15)
        print(f"   • #{BOLD}{tag:<12}{RESET} {YELLOW}{bar}{RESET} {count}")
        
    if s["orphans"]:
        print(f"\n👻 {BOLD}Notas Huérfanas ({len(s['orphans'])}):{RESET} (Sin enlaces entrantes ni salientes)")
        for o in s["orphans"][:10]:
            print(f"   • {o}")
        if len(s["orphans"]) > 10:
            print(f"   • ... y {len(s['orphans']) - 10} más.")
    
    print()

if __name__ == "__main__":
    main()
