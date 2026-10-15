---
name: editable-catalysis-mechanism-pptx
description: Generate offline, fully editable PowerPoint scientific diagrams for molecular ball-and-stick models, local catalyst/crystal structures, and catalytic reaction mechanisms. Use when a user needs native PowerPoint atoms, bonds, arrows, and text rather than flattened images. Accepts SMILES, SDF, MOL, XYZ, CIF, POSCAR, CONTCAR, and YAML mechanism descriptions.
license: MIT
compatibility: Python 3.12+ with the packages pinned in requirements.txt; LibreOffice is optional for external rendering checks. No API keys or network access are used at runtime.
allowed-tools: Read Write Edit Bash
metadata:
  version: "1.0.0"
  skill-author: zq project
---

# Editable Catalysis Mechanism PPTX

Create PowerPoint research figures whose scientific objects remain editable. Never place a rendered molecule, crystal, mechanism, screenshot, or full-slide PNG inside the PPTX. A preview PNG is a separate convenience artifact and is not embedded.

## Required outputs

Unless the user supplies another output directory, write:

- `outputs/editable_mechanism.pptx`
- `outputs/preview.png`
- `outputs/structure_report.md`
- `outputs/build_log.txt`

## Workflow

1. Read the requested input and identify whether it is a molecule, crystal, or mechanism YAML.
2. Work from the repository root. Create or reuse an isolated Python environment outside the project checkout and install `requirements.txt` with normal TLS and package verification.
3. Run `scripts/build_editable_pptx.py` with one of the modes below.
4. Run `scripts/validate_editability.py` on the resulting PPTX. Treat any picture shape, grouped shape, missing required native shape type, or count mismatch as a failure.
5. Inspect `structure_report.md`, `build_log.txt`, and `preview.png`. State that the preview is independently drawn and does not prove PowerPoint rendering fidelity.
6. Report assumptions such as inferred bonding, periodic cluster cutoff, projection direction, and mechanism step labels. Scientific interpretation still needs domain review.

## Commands

Set the Skill directory once:

```bash
SKILL=.agents/skills/editable-catalysis-mechanism-pptx
PYTHON=/path/to/isolated-venv/bin/python
```

SMILES:

```bash
$PYTHON "$SKILL/scripts/build_editable_pptx.py" molecule \
  --smiles 'CCC' --title Propane --output-dir outputs
```

SDF, MOL, or XYZ:

```bash
$PYTHON "$SKILL/scripts/build_editable_pptx.py" molecule \
  --input molecule.sdf --output-dir outputs
```

CIF, POSCAR, or CONTCAR:

```bash
$PYTHON "$SKILL/scripts/build_editable_pptx.py" crystal \
  --input structure.cif --center-element Zr --radius 3.2 --output-dir outputs
```

Mechanism YAML:

```bash
$PYTHON "$SKILL/scripts/build_editable_pptx.py" mechanism \
  --input mechanism.yaml --output-dir outputs
```

Validation:

```bash
$PYTHON "$SKILL/scripts/validate_editability.py" \
  outputs/editable_mechanism.pptx --expect-manifest outputs/shape_manifest.yaml
```

See [README_examples.md](README_examples.md) for complete examples and the YAML schema. Use paths relative to the YAML file for molecule and crystal inputs.

## Native-shape contract

- Each atom is one PowerPoint oval named `Atom_*`; its element label is a separate textbox named `Text_atom_*`.
- Each visible bond segment is one PowerPoint connector named `Bond_*`. Multiple-bond strokes are separate connectors.
- Each reaction arrow is one PowerPoint connector with an arrowhead named `Arrow_*`.
- Each title, species label, condition, annotation, and atom label is a separate textbox named `Text_*`.
- Catalyst support outlines use native freeform/polygon shapes named `Catalyst_*`.
- The PPTX must contain zero picture shapes and zero group shapes.

The builder also writes `shape_manifest.yaml`. Validation compares this build-time manifest with the presentation contents.

## Safety and limits

Runtime is offline and uses no API key. Input parsers process complex third-party file formats; use trusted files and reasonable size limits. The builder caps molecule atoms, crystal cluster atoms, mechanism species, and slides. It refuses to overwrite an existing output directory unless `--force` is explicitly supplied.

RDKit bond perception for XYZ and pymatgen neighbor selection are heuristic. A projected local structure is not a crystallographic refinement. Periodic-image atoms are copied as individual editable shapes and reported with image offsets. Mechanism arrows express the supplied YAML, not an independently validated elementary-step model.
