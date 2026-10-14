"""Offline smoke tests using synthetic inputs only; outputs stay in temporary storage."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1] / '.agents' / 'skills'
os.environ.setdefault('MPLBACKEND', 'Agg')
os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')

def load(skill, file):
    path = ROOT / skill / 'scripts' / file
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run(skill, file, *args):
    result = subprocess.run([sys.executable, str(ROOT / skill / 'scripts' / file), *map(str, args)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout

with tempfile.TemporaryDirectory(prefix='zq-skills-smoke-') as temp:
    temp = Path(temp)
    os.environ['MPLCONFIGDIR'] = str(temp / 'mpl')
    run('scientific-writing', 'scaffold_manuscript.py', '--output-dir', temp / 'manuscript', '--document-id', 'synthetic-demo', '--study-design', 'experimental')
    assert (temp / 'manuscript/manuscript.md').is_file()
    assert json.loads((temp / 'manuscript/manuscript_manifest.json').read_text())['document_id'] == 'synthetic-demo'
    print('PASS: offline manuscript scaffolding')
    run('scientific-visualization', 'figure_export.py', '--demo', temp / 'figure', '--manifest')
    assert (temp / 'figure.png').read_bytes().startswith(b'\x89PNG')
    assert (temp / 'figure.pdf').read_bytes().startswith(b'%PDF-')
    print('PASS: Matplotlib PNG/PDF export')
    randomization = load('experimental-design', 'randomization.py')
    a = randomization.block_randomization(24, seed=42)
    assert a.equals(randomization.block_randomization(24, seed=42))
    assert sorted(a['arm'].value_counts()) == [12, 12]
    design = load('experimental-design', 'doe_designs.py').full_factorial({'temperature': [20, 40, 60], 'catalyst': ['A', 'B']})
    assert len(design) == 6 and len(design[['temperature', 'catalyst']].drop_duplicates()) == 6
    print('PASS: reproducible balanced randomization and six-run factorial design')
    stats = load('statistical-analysis', 'assumption_checks.py')
    result = stats.check_normality([1, 2, 3, 4, 5, 6, float('nan')], plot=False)
    assert result['n'] == 6 and result['n_missing'] == 1 and 0 <= result['p_value'] <= 1
    try:
        stats.check_normality([1, 1, 1], plot=False)
    except ValueError:
        pass
    else:
        raise AssertionError('constant observations must be rejected')
    print('PASS: statistical missingness and invalid-input handling')
    review = temp / 'review.md'
    review.write_text('# Synthetic review\n\nOffline smoke test.\n')
    run('literature-review', 'generate_pdf.py', review, '--output', temp / 'review.pdf')
    assert (temp / 'review.pdf').read_bytes().startswith(b'%PDF-')
    print('PASS: Pandoc/XeLaTeX PDF rendering')
print('No network APIs, credentials, real experimental data, or paid generation used.')
