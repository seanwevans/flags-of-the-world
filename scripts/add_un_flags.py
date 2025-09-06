import base64
import re
import unicodedata
from pathlib import Path
import requests

# normalization helper

def normalize(name: str) -> str:
    name = name.lower()
    name = unicodedata.normalize('NFKD', name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r'[^a-z0-9]+', '-', name).strip('-')
    return name

# map names from API to existing filenames
NAME_MAP = {
    'czechia': 'czech-republic',
    'democratic-republic-of-the-congo': 'congo-drc',
    'dr-congo': 'congo-drc',
    'republic-of-the-congo': 'congo-republic',
    'united-states': 'usa',
    'united-states-of-america': 'usa',
}

resp = requests.get('https://restcountries.com/v3.1/all?fields=name,unMember,flags').json()

members = [r for r in resp if r.get('unMember')]
existing = {p.stem for p in Path('.').glob('*.css')}
new_flags = []
flag_data = []  # list of (filename, caption)

for r in members:
    common = r['name']['common']
    file_stem = NAME_MAP.get(normalize(common), normalize(common))
    caption = common
    if file_stem in existing:
        continue
    svg_url = r['flags']['svg']
    svg = requests.get(svg_url).text
    # parse width and height if available
    m = re.search(r'width="(\d+)"[^>]*height="(\d+)"', svg)
    if m:
        w, h = m.groups()
    else:
        vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg)
        if vb:
            w, h = vb.groups()
        else:
            w, h = '3', '2'
    ratio = f"{w}/{h}"
    data = base64.b64encode(svg.encode('utf-8')).decode('ascii')
    css = f"""/* reference: {svg_url} */\n\n#{file_stem} {{\n  height: 180px;\n  aspect-ratio: {ratio};\n  background-image: url('data:image/svg+xml;base64,{data}');\n  background-size: 100% 100%;\n}}\n"""
    Path(f"{file_stem}.css").write_text(css, encoding='utf-8')
    existing.add(file_stem)
    new_flags.append(file_stem)
    flag_data.append((file_stem, caption))

# update index.html by inserting link tags and figures
if new_flags:
    index_path = Path('index.html')
    lines = index_path.read_text().splitlines()
    head_idx = next(i for i, line in enumerate(lines) if '</head>' in line)
    section_idx = next(i for i, line in enumerate(lines) if '</section>' in line)
    link_lines = [f'  <link rel="stylesheet" href="{f}.css">' for f in new_flags]
    def format_caption(name: str) -> str:
        return ' '.join(word.capitalize() for word in name.split('-'))
    figure_lines = []
    for stem in new_flags:
        caption = format_caption(stem)
        figure_lines.extend([
            '  <figure class="flag-card">',
            f'    <div id="{stem}"></div>',
            f'    <figcaption>{caption}</figcaption>',
            '  </figure>',
            '',
        ])
    lines[head_idx:head_idx] = link_lines
    lines[section_idx:section_idx] = figure_lines
    index_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

# regenerate README using existing script
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
import generate_readme
generate_readme.main('README.md')

print(f"Added {len(new_flags)} new flags")
