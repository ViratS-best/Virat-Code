import os
import re
import shutil

root_dir = r"c:/Users/virat/OneDrive/Documents/Free Ai agent/virat-code-agent-main"
ignore_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env', '.mypy_cache', '.pytest_cache', 'build', 'dist', '.docusaurus'}

# Map of exact string replacements
replacements = [
    # Match specific technical identifiers first
    (r'virat_code_cli', r'virat_code_cli'),
    (r'virat_code_constants', r'virat_code_constants'),
    (r'virat_code_swe_env', r'virat_code_swe_env'),
    (r'VIRAT_CODE_HOME', r'VIRAT_CODE_HOME'),
    (r'\.virat-code', r'.virat-code'),
    (r'VIRAT_CODE_', r'VIRAT_CODE_'),
    
    # Fix the pyproject.toml issue with pip extras
    (r'Virat Code\[', r'virat-code['),
    
    # Replace the command 'virat_code' with 'Virat-Code'
    (r'\bvirat_code command\b', r'Virat-Code command'),
    (r'\bvirat_code setup\b', r'Virat-Code setup'),
    (r'\bvirat_code config\b', r'Virat-Code config'),
    (r'\bvirat_code gateway\b', r'Virat-Code gateway'),
    (r'\bvirat_code update\b', r'Virat-Code update'),
    (r'\bvirat_code whatsapp\b', r'Virat-Code whatsapp'),
    (r'"virat_code"', r'"Virat-Code"'),
    (r"'virat_code'", r"'Virat-Code'"),
    (r'`virat_code`', r'`Virat-Code`'),
    (r' virat_code ', r' Virat-Code '),
    
    # Catch any remaining Virat Code/virat_code terms
    (r'Virat Code', r'Virat Code'),
    (r'\bvirat_code\b', r'virat-code')
]

def process_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    old_content = content
    for pattern, repl in replacements:
        content = re.sub(pattern, repl, content)

    if content != old_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")
            return False
    return False

# First, process file contents
for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
    dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
    for filename in filenames:
        if filename in ('package-lock.json', 'uv.lock', 'rebrand_virat_code.py', 'replace_urls.py', 'replace_os.py'):
            continue
        # We process files with text extensions
        if filename.endswith(('.py', '.md', '.json', '.yaml', '.yml', '.txt', '.sh', '.ts', '.tsx', '.css', '.toml', '.ps1', '.cmd', '.html', '.js', '.jsx')):
            filepath = os.path.join(dirpath, filename)
            if process_file_content(filepath):
                print(f"Updated content in {filepath}")

# Second, rename directories and files
# We collect them first, sort them by depth descending and length so we rename deepest/longest first to avoid breaking paths
renames = []
for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
    # Only iterate through non-ignored paths
    if any(ign in dirpath for ign in ignore_dirs):
        continue

    for name in dirnames + filenames:
        if 'virat_code' in name:
            old_path = os.path.join(dirpath, name)
            new_name = name.replace('virat_code', 'virat_code')
            # Handle hyphenated cases too if they exist
            if 'virat_code-' in name:
                new_name = name.replace('virat_code-', 'virat-code-')
            new_path = os.path.join(dirpath, new_name)
            renames.append((old_path, new_path))

for old_path, new_path in renames:
    try:
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} -> {new_path}")
    except Exception as e:
        print(f"Error renaming {old_path}: {e}")
