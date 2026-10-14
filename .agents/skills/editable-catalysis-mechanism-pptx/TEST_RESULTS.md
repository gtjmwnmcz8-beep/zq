# Test results

Tested on 2026-10-14 with Python 3.12.14 in an isolated environment using the exact versions in `requirements.txt`. The test runner used synthetic example inputs and temporary output directories. It made no API calls, used no API keys, and deleted generated outputs after completion.

Command:

```bash
XDG_CACHE_HOME=/tmp/editable-pptx-cache \
MPLCONFIGDIR=/tmp/editable-pptx-mpl \
PYTHONDONTWRITEBYTECODE=1 \
/workspace/skill-environments/editable-catalysis-pptx/bin/python \
  .agents/skills/editable-catalysis-mechanism-pptx/scripts/run_examples.py
```

Results:

| Case | Atoms | Bond segments | Arrows | Text boxes | Pictures | Groups | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| propane / propylene | 20 | 19 | 1 | 25 | 0 | 0 | PASS |
| monoclinic ZrO2 local cluster | 8 | 7 | 0 | 10 | 0 | 0 | PASS |
| propane dehydrogenation over V/ZrO2 | 39 | 29 | 3 | 49 | 0 | 0 | PASS |
| MOL input | 11 | 10 | 0 | 13 | 0 | 0 | PASS |
| SDF input | 11 | 10 | 0 | 13 | 0 | 0 | PASS |
| XYZ input | 11 | 10 | 0 | 13 | 0 | 0 | PASS |
| POSCAR input | 8 | 7 | 0 | 10 | 0 | 0 | PASS |
| CONTCAR input | 8 | 7 | 0 | 10 | 0 | 0 | PASS |

Every case produced `editable_mechanism.pptx`, `preview.png`, `structure_report.md`, `build_log.txt`, and `shape_manifest.yaml`. Validation compared native object counts against the build manifest and inspected the PPTX ZIP package for picture XML and media files.

The example CIF emits a pymatgen warning because it intentionally omits publication metadata and formula keys. The structure parses successfully and is only a software-test fixture, not an authoritative crystallographic record.

The V/ZrO2 mechanism PPTX was also opened headlessly by LibreOffice and exported to a one-page PDF. The export completed successfully. Visual inspection confirmed right-pointing reaction arrows, readable independent labels, molecular models, and catalyst-site shapes. This compatibility check does not replace testing in the user's exact Microsoft PowerPoint version.
