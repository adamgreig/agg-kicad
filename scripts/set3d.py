"""
set3d.py
Copyright 2020-2022 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Assigns 3d footprints to passives on a PCB.
"""

import argparse
import pcbnew

MODELS = {
    "R": {
        "agg:0402": "${KICAD8_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0402_1005Metric.step",
        "agg:0603": "${KICAD8_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step",
        "agg:0805": "${KICAD8_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0805_2012Metric.step",
    },
    "C": {
        "agg:0402": "${KICAD8_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0402_1005Metric.step",
        "agg:0603": "${KICAD8_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step",
        "agg:0805": "${KICAD8_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0805_2012Metric.step",
        "agg:1206": "${KICAD8_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_1206_3216Metric.step",
        "agg:1210": "${KICAD8_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_1210_3225Metric.step",
    },
    "L": {
        "agg:0603": "${KICAD8_3DMODEL_DIR}/Inductor_SMD.3dshapes/L_0603_1608Metric.step",
        "agg:0805": "${KICAD8_3DMODEL_DIR}/Inductor_SMD.3dshapes/L_0805_2012Metric.step",
    },
    "D": {
        "agg:0402": "${KICAD8_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0402_1005Metric.step",
        "agg:0603": "${KICAD8_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0603_1608Metric.step",
        "agg:0603-LED":
            "${KICAD8_3DMODEL_DIR}/LED_SMD.3dshapes/LED_0603_1608Metric_Castellated.step",
    },
}


def process_pcb(fname):
    print(f"Processing {fname}")
    board = pcbnew.LoadBoard(fname)
    for fp in board.GetFootprints():
        ref = fp.Reference().GetText()
        pkg = fp.Footprint().GetText()
        if ref[0] in MODELS and pkg in MODELS[ref[0]]:
            if fp.Models().size() > 0:
                if fp.Models()[0].m_Filename == MODELS[ref[0]][pkg]:
                    continue
            print(f"Setting {ref} to {MODELS[ref[0]][pkg]}")
            fp.Models().clear()
            model = pcbnew.FP_3DMODEL()
            model.m_Filename = MODELS[ref[0]][pkg]
            fp.Add3DModel(model)
    board.Save(fname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Assigns 3d models to passives in a .kicad_pcb file")
    parser.add_argument("kicad_pcb", help="Path to .kicad_pcb file")
    args = parser.parse_args()
    process_pcb(args.kicad_pcb)
