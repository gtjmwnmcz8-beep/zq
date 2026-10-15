#!/usr/bin/env python3
"""Run all three documented examples in temporary directories and validate them."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from rdkit import Chem
from rdkit.Chem import AllChem
from pymatgen.core import Structure


HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
EXAMPLES = SKILL / "examples"


def command(*args: str) -> tuple[str, dict]:
    env = dict(os.environ)
    env.setdefault("XDG_CACHE_HOME", "/tmp/editable-pptx-cache")
    env.setdefault("MPLCONFIGDIR", "/tmp/editable-pptx-mpl")
    env.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    result = subprocess.run([sys.executable, str(HERE / "build_editable_pptx.py"), *args],
                            text=True, capture_output=True, env=env)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    output = Path(args[args.index("--output-dir") + 1])
    check = subprocess.run([sys.executable, str(HERE / "validate_editability.py"),
                            str(output / "editable_mechanism.pptx"), "--expect-manifest",
                            str(output / "shape_manifest.yaml"), "--json"], text=True, capture_output=True, env=env)
    if check.returncode:
        raise RuntimeError(check.stdout + check.stderr)
    return result.stdout, json.loads(check.stdout)


def main() -> int:
    results = {}
    with tempfile.TemporaryDirectory(prefix="editable-pptx-test-") as temp:
        root = Path(temp)
        cases = {
            "propane_propylene": ("mechanism", "--input", str(EXAMPLES / "propane_propylene.yaml")),
            "monoclinic_zro2": ("mechanism", "--input", str(EXAMPLES / "zro2_local.yaml")),
            "v_zro2_pdh": ("mechanism", "--input", str(EXAMPLES / "v_zro2_pdh.yaml")),
        }
        for name, args in cases.items():
            out = root / name
            _, result = command(*args, "--output-dir", str(out))
            required = {"editable_mechanism.pptx", "preview.png", "structure_report.md", "build_log.txt", "shape_manifest.yaml"}
            missing = required - {p.name for p in out.iterdir()}
            if missing: raise AssertionError(f"{name} missing {sorted(missing)}")
            if (out / "preview.png").read_bytes()[:8] != b"\x89PNG\r\n\x1a\n": raise AssertionError("bad PNG")
            if not (out / "editable_mechanism.pptx").read_bytes().startswith(b"PK"): raise AssertionError("bad PPTX")
            results[name] = result
            print(f"PASS {name}: {result['native_shapes']}")
        formats = root / "formats"; formats.mkdir()
        mol = Chem.AddHs(Chem.MolFromSmiles("CCC"))
        params = AllChem.ETKDGv3(); params.randomSeed = 42
        assert AllChem.EmbedMolecule(mol, params) == 0
        Chem.MolToMolFile(mol, str(formats / "propane.mol"))
        writer = Chem.SDWriter(str(formats / "propane.sdf")); writer.write(mol); writer.close()
        Chem.MolToXYZFile(mol, str(formats / "propane.xyz"))
        structure = Structure.from_file(EXAMPLES / "monoclinic_zro2.cif")
        structure.to(filename=formats / "POSCAR", fmt="poscar")
        structure.to(filename=formats / "CONTCAR", fmt="poscar")
        for filename in ("propane.mol", "propane.sdf", "propane.xyz"):
            out = root / f"format-{filename.replace('.', '-')}"
            _, result = command("molecule", "--input", str(formats / filename), "--output-dir", str(out))
            results[filename] = result
            print(f"PASS format {filename}")
        for filename in ("POSCAR", "CONTCAR"):
            out = root / f"format-{filename.lower()}"
            _, result = command("crystal", "--input", str(formats / filename), "--output-dir", str(out))
            results[filename] = result
            print(f"PASS format {filename}")
    print(json.dumps({"status": "PASS", "cases": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
