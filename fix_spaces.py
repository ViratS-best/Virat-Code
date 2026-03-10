import os
import re

root_dir = r"c:/Users/virat/OneDrive/Documents/Free Ai agent/hermes-agent-main"
ignore_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env', '.mypy_cache', '.pytest_cache', 'build', 'dist', '.docusaurus'}

def fix_content(content):
    # If "Virat Code" is touching a word character or $ on the left, e.g., $Virat Code or currentVirat Code
    content = re.sub(r'([a-zA-Z0-9_$])Virat Code', r'\1ViratCode', content)
    # If "Virat Code" is touching a word character on the right, e.g., Virat CodeHome
    content = re.sub(r'Virat Code([a-zA-Z0-9_])', r'ViratCode\1', content)
    
    # Also fix some known broken things:
    # "Virat Code CLI" might be fine, but let's check what broke.
    content = content.replace('Virat CodeCommand', 'ViratCodeCommand')
    content = content.replace('Virat CodeDir', 'ViratCodeDir')
    return content

for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
    dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
    for filename in filenames:
        if filename in ('package-lock.json', 'uv.lock', 'rebrand_hermes.py', 'rebrand_hermes2.py', 'fix_spaces.py'):
            continue
        filepath = os.path.join(dirpath, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = fix_content(content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed spaces in {filepath}")
        except Exception:
            pass
