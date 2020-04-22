"""
set3d.py
Copyright 2020 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Assigns 3d footprints to passives on a PCB.
"""

import argparse

MODELS = {
    "R": {
        "agg:0402": "${KISYS3DMOD}/Resistor_SMD.3dshapes/R_0402_1005Metric.step",
        "agg:0603": "${KISYS3DMOD}/Resistor_SMD.3dshapes/R_0603_1608Metric.step",
        "agg:0805": "${KISYS3DMOD}/Resistor_SMD.3dshapes/R_0805_2012Metric.step",
    },
    "C": {
        "agg:0402": "${KISYS3DMOD}/Capacitor_SMD.3dshapes/C_0402_1005Metric.step",
        "agg:0603": "${KISYS3DMOD}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step",
        "agg:0805": "${KISYS3DMOD}/Capacitor_SMD.3dshapes/C_0805_2012Metric.step",
        "agg:1206": "${KISYS3DMOD}/Capacitor_SMD.3dshapes/C_1206_3216Metric.step",
    },
    "L": {
        "agg:0603": "${KISYS3DMOD}/Inductor_SMD.3dshapes/L_0603_1608Metric.step",
        "agg:0805": "${KISYS3DMOD}/Inductor_SMD.3dshapes/L_0805_2012Metric.step",
    },
    "D": {
        "agg:0603-LED":
            "${KISYS3DMOD}/LED_SMD.3dshapes/LED_0603_1608Metric_Castellated.step",
    },
}

ADD_MODEL_SPEC = """\
    (model {}
      (at (xyz 0 0 0))
      (scale (xyz 1 1 1))
      (rotate (xyz 0 0 0))
    )
  )
"""


def process_pcb(fname):
    print(f"Processing {fname}")
    with open(fname, "r") as f:
        lines = f.readlines()

    ref = None
    pkg = None
    changed = False

    for (idx, line) in enumerate(lines):
        if "(module" in line:
            ref = None
            pkg = line.split()[1]
        if "(fp_text reference" in line:
            ref = line.split()[2]
        if "(model" in line:
            if ref[0] in MODELS and pkg in MODELS[ref[0]]:
                current_model = line.split()[1].strip()
                new_model = MODELS[ref[0]][pkg]
                if current_model != new_model:
                    print(f"Replacing {ref} {pkg} with {new_model}")
                    lines[idx] = f"    (model {new_model}\n"
                    changed = True
                ref = None
        if ref is not None and line == "  )\n":
            if ref[0] in MODELS and pkg in MODELS[ref[0]]:
                new_model = MODELS[ref[0]][pkg]
                print(f"Adding new model {ref} {pkg} {new_model}")
                lines[idx] = ADD_MODEL_SPEC.format(new_model)
                changed = True

    if changed:
        with open(fname, "w") as f:
            f.write("".join(lines))
    else:
        print("No replacements made")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Assigns 3d models to passives in a .kicad_pcb file")
    parser.add_argument("kicad_pcb", help="Path to .kicad_pcb file")
    args = parser.parse_args()
    process_pcb(args.kicad_pcb)
