# Editable catalysis mechanism PPTX examples

This Skill runs locally and does not use an API key. It draws every atom, bond, reaction arrow, and label as a separate native PowerPoint object. `preview.png` is independently drawn with Matplotlib and is never embedded in the presentation.

## Setup

From the project root:

```bash
export UV_CACHE_DIR=/tmp/editable-pptx-uv-cache
uv venv --python 3.12 /workspace/skill-environments/editable-catalysis-pptx
uv pip install --python /workspace/skill-environments/editable-catalysis-pptx/bin/python \
  --only-binary :all: \
  -r .agents/skills/editable-catalysis-mechanism-pptx/requirements.txt
```

The `/workspace/...` location is suitable for this cloud environment. On another machine, use any writable virtual-environment directory outside the Git checkout.

## 1. Propane / propylene molecules

```bash
PY=/workspace/skill-environments/editable-catalysis-pptx/bin/python
SKILL=.agents/skills/editable-catalysis-mechanism-pptx
$PY "$SKILL/scripts/build_editable_pptx.py" mechanism \
  --input "$SKILL/examples/propane_propylene.yaml" \
  --output-dir outputs/propane-propylene
$PY "$SKILL/scripts/validate_editability.py" \
  outputs/propane-propylene/editable_mechanism.pptx \
  --expect-manifest outputs/propane-propylene/shape_manifest.yaml
```

The two `.smi` inputs demonstrate local SMILES-file support. Direct `--smiles 'CCC'`, SDF, MOL, and XYZ inputs are accepted by molecule mode. XYZ bond perception assumes total charge 0 and must be reviewed.

## 2. Monoclinic ZrO2 local structure

```bash
$PY "$SKILL/scripts/build_editable_pptx.py" mechanism \
  --input "$SKILL/examples/zro2_local.yaml" \
  --output-dir outputs/zro2-local
```

The example CIF is a compact, synthetic literature-style monoclinic ZrO2 cell for software testing, not an authoritative crystallographic reference. CIF, POSCAR, and CONTCAR parsing use `pymatgen.Structure.from_file`. A center atom and periodic cutoff select the local cluster; bonds are inferred from covalent radii.

## 3. Propane dehydrogenation over V/ZrO2

```bash
$PY "$SKILL/scripts/build_editable_pptx.py" mechanism \
  --input "$SKILL/examples/v_zro2_pdh.yaml" \
  --output-dir outputs/v-zro2-pdh
```

This is explicitly a proposed schematic. The editable catalyst support, V/O/Zr site circles, molecule shapes, step arrows, and labels do not assert a uniquely established elementary mechanism.

## Mechanism YAML schema

Top-level fields:

- `schema_version`: must be `1`.
- `title`: report and preview title.
- `theme`: optional `background`, `foreground`, `accent`, and `catalyst` hex colors.
- `slides`: one to twelve slide mappings.

Each slide can contain:

- `title`: independent title textbox.
- `species`: up to twelve molecule mappings. Each needs a unique `id`, `x`, `y`, `width`, and `height`, plus either `smiles` or `input`. Relative input paths resolve from the YAML directory.
- `arrows`: mappings with `from` and `to` species IDs and optional `label`.
- `catalyst`: native support rectangle with optional native atom `sites`.
- `crystal`: local structure mapping with `input`, `center_element`, `radius`, and bounding box.
- `texts`: independent annotation textboxes with position, size, and optional font size.

Start from [templates/mechanism_template.yaml](templates/mechanism_template.yaml).

## Full self-test

```bash
$PY "$SKILL/scripts/run_examples.py"
```

The runner uses temporary output directories, validates every PPTX against its build manifest, checks required artifacts, and deletes generated files when complete. No experimental data or network service is used.
