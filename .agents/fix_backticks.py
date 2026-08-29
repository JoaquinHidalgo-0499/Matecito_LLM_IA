import os
import re

brain_dir = "/home/joaquin/Compartido/braind/brain"
backticked_wikilink_re = re.compile(r"`\[\[([^\]`]+)\]\]`")

modified_files = {}

for root, dirs, files in os.walk(brain_dir):
    for f in files:
        if f.endswith(".md"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            
            new_content, count = backticked_wikilink_re.subn(r"[[\1]]", content)
            if count > 0:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(new_content)
                rel_path = os.path.relpath(path, brain_dir)
                modified_files[rel_path] = count

if modified_files:
    print(f"[Autofix] Total files corrected: {len(modified_files)}")
    for file, count in sorted(modified_files.items()):
        print(f" - {file}: {count} backticked wikilinks removed")
