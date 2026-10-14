# zq

## Editable catalysis PowerPoint Skill

The project-local Skill at `.agents/skills/editable-catalysis-mechanism-pptx/` creates offline, genuinely editable PowerPoint diagrams for molecules, local crystal/catalyst structures, and catalytic mechanisms. It accepts SMILES/SDF/MOL/XYZ, CIF/POSCAR/CONTCAR, and YAML mechanism descriptions. Atoms, bond segments, arrows, and text are separate native PowerPoint objects; preview PNG files are never embedded in the presentation.

Start a new Codex session in this repository and request `$editable-catalysis-mechanism-pptx`, or follow [the example commands](.agents/skills/editable-catalysis-mechanism-pptx/README_examples.md). The Skill requires no API key and makes no runtime API calls.
