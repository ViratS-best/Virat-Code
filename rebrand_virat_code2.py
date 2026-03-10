import os
import re

root_dir = r"c:/Users/virat/OneDrive/Documents/Free Ai agent/hermes-agent-main"
ignore_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env', '.mypy_cache', '.pytest_cache', 'build', 'dist', '.docusaurus'}

replacements = [
    # Explicit camelCase mappings
    ('hermesCmd', 'viratCodeCmd'),
    ('HermesHome', 'ViratCodeHome'),
    ('currentHermesHome', 'currentViratCodeHome'),
    ('hermesBin', 'viratCodeBin'),
    
    # Common function names
    ('hermes_home', 'virat_code_home'),
    ('get_hermes_home', 'get_virat_code_home'),
    
    # Catch any remaining occurrences without regex boundaries
    ('hermes', 'virat_code'),
    ('Hermes', 'Virat Code'),
    ('HERMES', 'VIRAT_CODE'),
    
    # Just in case there are double strings like virat_code-agent, we can fix them later if needed,
    # but since hermes is being straight up replaced by virat_code,
    # hermes-agent -> virat_code-agent -> we already replaced hermes-agent before!
]

def process_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    old_content = content
    for old_str, new_str in replacements:
        content = content.replace(old_str, new_str)

    # Some manual cleanup because of the crude string replacement above:
    content = content.replace('Virat Code_HOME', 'VIRAT_CODE_HOME') # if HERMES_HOME was partially matched
    content = content.replace('Virat_Code', 'Virat Code')
    content = content.replace('virat_code-agent', 'virat-code-agent')
    content = content.replace('.virat_code', '.virat-code')
    content = content.replace('\\virat_code\\', '\\virat-code\\')
    content = content.replace('/virat_code/', '/virat-code/')

    if content != old_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False
    return False

# Also let's rename any files or folders that STILL have "hermes" in them
renames = []
for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
    if any(ign in dirpath for ign in ignore_dirs):
        continue

    for name in dirnames + filenames:
        if 'hermes' in name.lower():
            old_path = os.path.join(dirpath, name)
            # Case preserving rename for filenames
            new_name = name.replace('hermes', 'virat_code').replace('Hermes', 'ViratCode').replace('HERMES', 'VIRAT_CODE')
            new_path = os.path.join(dirpath, new_name)
            renames.append((old_path, new_path))

for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
    dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
    for filename in filenames:
        if filename in ('package-lock.json', 'uv.lock', 'rebrand_hermes.py', 'rebrand_hermes2.py', 'replace_urls.py', 'replace_os.py'):
            continue
        filepath = os.path.join(dirpath, filename)
        if process_file_content(filepath):
            print(f"Updated content in {filepath}")

for old_path, new_path in renames:
    try:
        os.rename(old_path, new_path)
        print(f"Renamed {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
    except Exception as e:
        pass
