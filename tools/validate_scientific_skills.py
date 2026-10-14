"""Verify the six vendored skills without executing upstream code or using data."""
import ast
import hashlib
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1] / '.agents' / 'skills'
manifest = json.loads((ROOT / 'UPSTREAM.json').read_text())
assert {p.name for p in ROOT.iterdir() if p.is_dir()} == set(manifest['skills'])
assert hashlib.sha256((ROOT / 'UPSTREAM-LICENSE.md').read_bytes()).hexdigest() == manifest['license_sha256']
actual = set()
links = 0
for name in manifest['skills']:
    directory = ROOT / name
    text = (directory / 'SKILL.md').read_text()
    assert text.startswith('---\n'), name
    meta = yaml.safe_load(text.split('---', 2)[1])
    assert meta['name'] == name
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name)
    assert isinstance(meta['description'], str) and 0 < len(meta['description']) <= 1024
    for file in directory.rglob('*'):
        assert not file.is_symlink(), file
        if not file.is_file():
            continue
        key = str(file.relative_to(ROOT))
        actual.add(key)
        assert hashlib.sha256(file.read_bytes()).hexdigest() == manifest['files'][key], key
        if file.suffix == '.py':
            ast.parse(file.read_text(), filename=str(file))
        if file.suffix == '.md':
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', file.read_text()):
                target = target.split('#')[0]
                if not target or re.match(r'[a-z]+:|/', target):
                    continue
                assert (file.parent / target).is_file(), (file, target)
                links += 1
assert actual == set(manifest['files'])
print(f'PASS: {len(manifest["skills"])} skills, {len(actual)} matching upstream files, {links} local Markdown links; Python syntax valid')
print('Optional scientific-schematics command is outside this six-skill installation.')
