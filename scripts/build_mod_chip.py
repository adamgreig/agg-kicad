"""
build_mod_chip.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Create two-terminal chip packages.
"""
from __future__ import print_function, division

# Package Configuration =======================================================
# Top keys are package names.
# Format is SIZE[-SPECIAL]. Examples: 0402, 0603-LED
# Valid inner keys are:
#   * pad_shape: (width, height) of the pads
#   * pitch: spacing between pad centres
#   * chip_shape: (width, height) of the chip (for Fab layer)
#   * pin_shape: (width, height) of chip pins (for Fab layer).
#                Use negative widths for internal pins (e.g., chip resistors)
#   * silk: "internal", "external", "triangle",
#           "internal_pin1", "external_pin1", or None.
#           What sort of silk to draw. Default is "internal".
#   * courtyard_gap: minimum distance from footprint extreme to courtyard.
#                    If not specified, the default ctyd_gap set below is used.
#   * model: {"path": str,
#             "offset": (x,y,z),
#             "scale": (x,y,z),
#             "rotate":(x,y,z)}
#            Defines which 3D model to associate with the footprint.
#
# Except where otherwise noted, all packages are in IPC nominal environment.
# Chip drawings are nominal sizes rather than maximum sizes.
# All lengths are in millimetres.

# Model Constants
# Scale factor for models in mm
MM_TO_DIN = (0.3937, 0.3937, 0.3937)

config = {
    # 0201 from IPC-7351B: CAPC0603X33N
    "0201": {
        "pad_shape": (0.46, 0.42),
        "pitch": 0.66,
        "chip_shape": (0.6, 0.3),
        "pin_shape": (-0.15, 0.3),
        "silk": None,
        "model": {"path": "${KISYS3DMOD}/Resistors_SMD.3dshapes/R_0201.wrl",
                  "offset": (0, 0, 0),
                  "scale": (1, 1, 1),
                  "rotate": (0, 0, 0)},
    },

    # 0201-L from IPC-7351B: CAPC0603X33L
    "0201-L": {
        "pad_shape": (0.36, 0.32),
        "pitch": 0.56,
        "chip_shape": (0.6, 0.3),
        "pin_shape": (-0.15, 0.3),
        "silk": None,
        "courtyard_gap": 0.10,
        "model": {"path": "${KISYS3DMOD}/Resistors_SMD.3dshapes/R_0201.wrl",
                  "offset": (0, 0, 0),
                  "scale": (1, 1, 1),
                  "rotate": (0, 0, 0)},
    },

    # 0402 from IPC-7351B: CAPC1005X55N
    "0402": {
        "pad_shape": (0.62, 0.62),
        "pitch": 0.90,
        "chip_shape": (1.00, 0.50),
        "pin_shape": (-0.30, 0.50),
        "silk": None,
        "model": {"path": "${KISYS3DMOD}/Resistors_SMD.3dshapes/R_0402.wrl",
                  "offset": (0, 0, 0),
                  "scale": (1, 1, 1),
                  "rotate": (0, 0, 0)},
    },

    # 0402-L from IPC-7351B: CAPC1005X55L
    # This is a LEAST environment
    "0402-L": {
        "pad_shape": (0.52, 0.52),
        "pitch": 0.80,
        "chip_shape": (1.00, 0.50),
        "pin_shape": (-0.30, 0.50),
        "silk": None,
        "courtyard_gap": 0.10,
        "model": {"path": "${KISYS3DMOD}/Resistors_SMD.3dshapes/R_0402.wrl",
                  "offset": (0, 0, 0),
                  "scale": (1, 1, 1),
                  "rotate": (0, 0, 0)},
    },

    # 0603 from IPC-7351B: CAPC1608X90N
    "0603": {
        "pad_shape": (0.95, 1.00),
        "pitch": 1.60,
        "chip_shape": (1.60, 0.80),
        "pin_shape": (-0.35, 0.80),
        "model": {"path": "${KISYS3DMOD}/Resistors_SMD.3dshapes/R_0603.wrl",
                  "offset": (0, 0, 0),
                  "scale": (1, 1, 1),
                  "rotate": (0, 0, 0)},
    },

    # 0603-L from IPC-7351B: CAPC1608X90L
    # This is a LEAST environment
    "0603-L": {
        "pad_shape": (0.75, 0.90),
        "pitch": 1.40,
        "chip_shape": (1.60, 0.80),
        "pin_shape": (-0.35, 0.80),
        "courtyard_gap": 0.10,
        "model": {"path": "${KISYS3DMOD}/Resistors_SMD.3dshapes/R_0603.wrl",
                  "offset": (0, 0, 0),
                  "scale": (1, 1, 1),
                  "rotate": (0, 0, 0)},
    },

    # 0603-LED from IPC-7351B: CAPC1608X90N
    # Modified silkscreen to indicate LED polarity.
    "0603-LED": {
        "pad_shape": (0.95, 1.00),
        "pitch": 1.60,
        "chip_shape": (1.60, 0.80),
        "pin_shape": (-0.25, 0.80),
        "silk": "triangle",
        "model": {"path": "${KISYS3DMOD}/LEDs.3dshapes/LED_0603.wrl",
                  "offset": (0, 0, 0),
                  "scale": (1, 1, 1),
                  "rotate": (0, 0, 180)},
    },

    # 0805 from IPC-7351B: CAPC2013X100N
    "0805": {
        "pad_shape": (1.15, 1.45),
        "pitch": 1.80,
        "chip_shape": (2.00, 1.25),
        "pin_shape": (-0.50, 1.25),
        "model": {"path": "${KISYS3DMOD}/Resistors_SMD.3dshapes/R_0805.wrl",
                  "offset": (0, 0, 0),
                  "scale": (1, 1, 1),
                  "rotate": (0, 0, 0)},
    },

    # 0805-LED from IPC-7351B: CAPC2013X100N
    # Modified silkscreen to indicate LED polarity.
    "0805-LED": {
        "pad_shape": (1.15, 1.45),
        "pitch": 1.80,
        "chip_shape": (2.00, 1.25),
        "pin_shape": (-0.50, 1.25),
        "silk": "triangle",
        "model": {"path": "${KISYS3DMOD}/LEDs.3dshapes/LED_0805.wrl",
                  "offset": (-0.006, 0, 0),
                  "scale": (1, 1, 1),
                  "rotate": (0, 0, 0)},
    },

    # 1206 from IPC-7351B: CAPC3216X130N
    "1206": {
        "pad_shape": (1.15, 1.80),
        "pitch": 3.00,
        "chip_shape": (3.20, 1.60),
        "pin_shape": (-0.60, 1.60),
        "model": {"path": "${KISYS3DMOD}/Resistors_SMD.3dshapes/R_1206.wrl",
                  "offset": (0, 0, 0),
                  "scale": (1, 1, 1),
                  "rotate": (0, 0, 0)},
    },

    # 1210 from IPC-7351B: CAPC3225X230N
    "1210": {
        "pad_shape": (1.15, 2.70),
        "pitch": 3.0,
        "chip_shape": (3.20, 2.50),
        "pin_shape": (-0.60, 2.30),
        "model": {"path": "${KISYS3DMOD}/Resistors_SMD.3dshapes/R_1210.wrl",
                  "offset": (0, 0, 0),
                  "scale": (1, 1, 1),
                  "rotate": (0, 0, 0)},
    },

    # 2512 from IPC-7351A: RESC4532X110N
    "1812": {
        "pad_shape": (1.40, 3.4),
        "pitch": 4.1,
        "chip_shape": (4.8, 3.4),
        "pin_shape": (-.9, 3.4),
    },

    # 2512 from IPC-7351A: RESC6432X70N
    "2512": {
        "pad_shape": (1.25, 3.4),
        "pitch": 6.1,
        "chip_shape": (6.6, 3.4),
        "pin_shape": (-.8, 3.4),
        "model": {"path": "${KISYS3DMOD}/Resistors_SMD.3dshapes/R_2512.wrl",
                  "offset": (0, 0, 0),
                  "scale": (1, 1, 1),
                  "rotate": (0, 0, 0)},
    },
    
    # WE 7443330220 Inductor
    "WE-HCC-1090": {
        "pad_shape": (2.3, 3.6),
        "pitch": 9.2,
        "chip_shape": (10.9, 10),
        "pin_shape": (-1.6, 3),
    },    

    # Coil Craft WA8514-AE Inductor
    "WA8514-AE": {
        "pad_shape": (0.838, 2.413),
        "pitch": 3.988,
        "chip_shape": (4.34, 1.98),
        "pin_shape": (-0.33, 1.65),
    }, 

    # SOD-323 from IPC-7351B: SOD2513X100L
    "SOD-323": {
        "pad_shape": (0.90, 0.50),
        "pitch": 2.60,
        "chip_shape": (1.80, 1.35),
        "pin_shape": (0.45, 0.40),
        "silk": "internal_pin1",
    },

    # SOD-123 from IPC-7351B: SOD3716X135N
    "SOD-123": {
        "pad_shape": (1.0, 0.8),
        "pitch": 3.6,
        "chip_shape": (2.8, 1.8),
        "pin_shape": (.5, .7),
        "silk": "internal_pin1",
    },

    # 5.0 x 3.2 mm 2-pin crystal
    "XTAL-50x32": {
        "pad_shape": (1.9, 2.4),
        "pitch": 4.1,
        "chip_shape": (5.0, 3.2),
        "pin_shape": (-1.3, 2.0),
    },

    # Panasonic ELL-VGG Inductor
    "ELLVGG": {
        "pad_shape": (1.4, 3.2),
        "pitch": 2.0,
        "chip_shape": (3, 3),
        "pin_shape": (-1.1, 3),
    },

    # Laird TYS5040 Inductor
    "TYS5040": {
        "pad_shape": (1.4, 4.2),
        "pitch": 3.7,
        "chip_shape": (5.0, 5.0),
        "pin_shape": (-1.25, 4.0),
    },

    # Bourns SRP5030T Inductor
    "SRP5030T": {
        "pad_shape": (1.8, 2.0),
        "pitch": 4.5,
        "chip_shape": (5.2, 5.2),
        "pin_shape": (0.25, 1.5),
    },

    # TDK VLS-201610HBX-1 series Inductor
    "VLS201610HBX-1": {
        "pad_shape": (0.5, 1.6),
        "pitch": 1.5,
        "chip_shape": (2, 1.6),
        "pin_shape": (-0.5, 1.6),
    },

    # Coilcraft XFL4020 series Inductors
    "XFL4020": {
        "pad_shape": (0.98, 3.4),
        "pitch": 2.37,
        "chip_shape": (4, 4),
        "pin_shape": (-1.5, 4),
    },

    # Coilcraft MSS1210 series inductors
    "MSS1210": {
        "pad_shape": (3.0, 5.5),
        "pitch": 9.5,
        "chip_shape": (12.3, 12.3),
        "pin_shape": (-2.5, 5.0),
    },

    # Coilcraft LPS4018 series inductors
    "LPS4018": {
        "pad_shape": (1.45, 3.89),
        "pitch": 2.95,
        "chip_shape": (3.9, 3.9),
        "pin_shape": (-1.1, 3.9),
    },

    # DO-214AC (SMA) from Diodes Inc.
    "DO-214AC-SMA": {
        "pad_shape": (2.5, 1.7),
        "pitch": 4.0,
        "chip_shape": (4.6, 2.92),
        "pin_shape": (0.5, 1.63),
        "silk": "triangle",
        "model": {"path": "${KISYS3DMOD}/Diodes_SMD.3dshapes/SMA_Standard.wrl",
                  "offset": (0, 0, 0),
                  "scale": MM_TO_DIN,
                  "rotate": (0, 0, 180)},
    },

    # DO-214AA (SMB) from Diodes Inc.
    "DO-214AA-SMB": {
        "pad_shape": (2.5, 2.3),
        "pitch": 4.3,
        "chip_shape": (4.6, 3.94),
        "pin_shape": (0.5, 2.21),
        "silk": "triangle",
        "model": {"path": "${KISYS3DMOD}/Diodes_SMD.3dshapes/SMB_Standard.wrl",
                  "offset": (0, 0, 0),
                  "scale": MM_TO_DIN,
                  "rotate": (0, 0, 180)},
    },

    # DO-214AB (SMC) from Diodes Inc.
    "DO-214AB-SMC": {
        "pad_shape": (2.5, 3.3),
        "pitch": 6.9,
        "chip_shape": (7.11, 6.22),
        "pin_shape": (0.51, 3.18),
        "silk": "triangle",
        "model": {"path": "${KISYS3DMOD}/Diodes_SMD.3dshapes/SMC_Standard.wrl",
                  "offset": (0, 0, 0),
                  "scale": MM_TO_DIN,
                  "rotate": (0, 0, 180)},
    },

    # KSR232G tactile switch
    "KSR232G": {
        "pad_shape": (1.0, 1.4),
        "pitch": 7.0,
        "chip_shape": (6.0, 3.8),
        "pin_shape": (0.6, 1.0),
    },
}

# Other constants =============================================================

# Courtyard clearance
# Use 0.25 for IPC nominal and 0.10 for IPC least.
ctyd_gap = 0.25

# Courtyard grid
ctyd_grid = 0.05

# Courtyard line width
ctyd_width = 0.01

# Internal silk clearance from pads
silk_pad_igap = 0.2

# External silk clearance from pads
silk_pad_egap = 0.2

# Silk line width
silk_width = 0.15

# Fab layer line width
fab_width = 0.01

# Ref/Val font size (width x height)
font_size = (1.0, 1.0)

# Ref/Val font thickness
font_thickness = 0.15

# Ref/Val font spacing from centre to top/bottom edge
font_halfheight = 0.7

# End constants ===============================================================

import os
import sys
import time
import math
import argparse

from sexp import parse as sexp_parse, generate as sexp_generate
from kicad_mod import fp_line, fp_text, pad, draw_square, model


def refs(conf):
    """Generate val and ref labels."""
    out = []
    x = conf['pitch']/2 + conf['pad_shape'][0]/2 + ctyd_gap + font_halfheight
    out.append(fp_text("reference", "REF**", (-x, 0, 90), "F.Fab",
                       font_size, font_thickness))
    out.append(fp_text("value", conf['name'], (x, 0, 90), "F.Fab",
                       font_size, font_thickness))
    return out


def fab(conf):
    """Generate a drawing of the chip on the Fab layer."""
    out = []
    cw, ch = conf['chip_shape']
    pw, ph = conf['pin_shape']
    w = fab_width

    # Chip body
    _, _, _, _, sq = draw_square(cw, ch, (0, 0), "F.Fab", w)
    out += sq

    # Pin 1 indicator
    if conf.get('silk') in ("triangle", "internal_pin1", "external_pin1"):
        out.append(fp_line(
            (-cw/4, -ch/2), (-cw/4, ch/2), "F.Fab", w))

    # Left pin
    out.append(fp_line((-cw/2 - pw, -ph/2), (-cw/2 - pw, ph/2), "F.Fab", w))
    if ph != ch:
        out.append(fp_line((-cw/2 - pw, -ph/2), (-cw/2, -ph/2), "F.Fab", w))
        out.append(fp_line((-cw/2 - pw, ph/2), (-cw/2, ph/2), "F.Fab", w))

    # Right pin
    out.append(fp_line((cw/2 + pw, -ph/2), (cw/2 + pw, ph/2), "F.Fab", w))
    if ph != ch:
        out.append(fp_line((cw/2 + pw, -ph/2), (cw/2, -ph/2), "F.Fab", w))
        out.append(fp_line((cw/2 + pw, ph/2), (cw/2, ph/2), "F.Fab", w))

    return out


def internal_silk(conf):
    """Draw internal silkscreen."""
    w = conf['pitch'] - conf['pad_shape'][0] - 2*silk_pad_igap
    h = conf['chip_shape'][1] - silk_width
    _, _, _, _, sq = draw_square(w, h, (0, 0), "F.SilkS", silk_width)
    return sq


def external_silk(conf):
    """Draw external silkscreen."""
    out = []
    return out


def triangle_silk(conf):
    """Draw a triangle silkscreen pointing to pin 1."""
    out = []
    w = conf['pitch'] - conf['pad_shape'][0] - 2*silk_pad_igap
    h = conf['chip_shape'][1] - silk_width
    out.append(fp_line((-w/2, 0), (w/2, -h/2), "F.SilkS", silk_width))
    out.append(fp_line((-w/2, 0), (w/2, +h/2), "F.SilkS", silk_width))
    out.append(fp_line((w/2, -h/2), (w/2, +h/2), "F.SilkS", silk_width))
    return out


def pin1_silk(conf):
    """Draw a small pin1 indicator on the silkscreen."""
    w = conf['pitch'] - conf['pad_shape'][0] - 2*silk_pad_igap
    h = conf['chip_shape'][1] - silk_width
    return [fp_line((-w/4, -h/2), (-w/4, h/2), "F.SilkS", silk_width)]


def silk(conf):
    s = conf.get('silk', 'internal')
    if s == "internal":
        return internal_silk(conf)
    elif s == "external":
        return external_silk(conf)
    elif s == "triangle":
        return triangle_silk(conf)
    elif s == "internal_pin1":
        return internal_silk(conf) + pin1_silk(conf)
    elif s == "external_pin1":
        return external_silk(conf) + pin1_silk(conf)
    else:
        return []


def ctyd(conf):
    """Draw a courtyard around the part."""
    gap = conf.get('courtyard_gap', ctyd_gap)

    # Compute width and height of courtyard
    width = max(conf['pad_shape'][0] + conf['pitch'], conf['chip_shape'][0])
    height = max(conf['pad_shape'][1], conf['chip_shape'][1])

    width += 2 * gap
    height += 2 * gap

    # Ensure courtyard lies on a specified grid
    # (double the grid since we halve the width/height)
    grid = 2*ctyd_grid
    width = grid * int(math.ceil(width / (2*ctyd_grid)))
    height = grid * int(math.ceil(height / (2*ctyd_grid)))

    # Render courtyard
    _, _, _, _, sq = draw_square(width, height, (0, 0), "F.CrtYd", ctyd_width)
    return sq


def pads(conf):
    """Place the part pads."""
    out = []
    x = conf['pitch'] / 2.0
    layers = ["F.Cu", "F.Mask", "F.Paste"]
    out.append(pad(1, "smd", "rect", (-x, 0), conf['pad_shape'], layers))
    out.append(pad(2, "smd", "rect", (+x, 0), conf['pad_shape'], layers))
    return out


def _3d(conf):
    """Add 3d model."""
    if "model" in conf:
        return [model(**conf['model'])]
    else:
        return []


def footprint(conf):
    tedit = format(int(time.time()), 'X')
    sexp = ["module", conf['name'], ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += refs(conf)
    sexp += fab(conf)
    sexp += silk(conf)
    sexp += ctyd(conf)
    sexp += pads(conf)
    sexp += _3d(conf)
    return sexp_generate(sexp)


def main(prettypath, verify=False, verbose=False):
    for name, conf in config.items():
        # Generate footprint
        conf['name'] = name
        fp = footprint(conf)
        path = os.path.join(prettypath, name+".kicad_mod")

        if verify and verbose:
            print("Verifying", path)

        # Check if an identical part already exists
        if os.path.isfile(path):
            with open(path) as f:
                old = f.read()
            old = [n for n in sexp_parse(old) if n[0] != "tedit"]
            new = [n for n in sexp_parse(fp) if n[0] != "tedit"]
            if new == old:
                continue

        # If not, either verification failed or we should output the new fp
        if verify:
            return False
        else:
            with open(path, "w") as f:
                f.write(fp)

    # If we finished and didn't return yet, verification has succeeded.
    if verify:
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prettypath", type=str, help=
                        "Path to footprints to process")
    parser.add_argument("--verify", action="store_true", help=
                        "Verify libraries are up to date")
    parser.add_argument("--verbose", action="store_true", help=
                        "Print out every library verified")
    args = vars(parser.parse_args())
    result = main(**args)
    if args['verify']:
        if result:
            print("OK: all footprints up-to-date.")
            sys.exit(0)
        else:
            print("Error: footprints not up-to-date.", file=sys.stderr)
            sys.exit(1)
