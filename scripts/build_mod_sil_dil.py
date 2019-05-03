"""
build_mod_sil_dil.py
Copyright 2016 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generate footprints for standard 0.1" SIL and DIL headers.
"""

from __future__ import print_function, division

# Settings ====================================================================

# Courtyard clearance
# Use 0.25 for IPC nominal and 0.10 for IPC least
ctyd_gap = 0.25

# Courtyard grid
ctyd_grid = 0.05

# Courtyard line width
ctyd_width = 0.01

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


# End Settings ================================================================


import os
import sys
import time
import math
import argparse

from sexp import parse as sexp_parse, generate as sexp_generate
from kicad_mod import fp_line, fp_text, pad, draw_square, model


def sil_pads(pins):
    pads = []
    x = -((pins - 1) / 2) * 2.54
    for pin in range(pins):
        shape = "rect" if pin == 0 else "circle"
        pads.append(pad(pin + 1, "thru_hole", shape, (x, 0), [1.9, 1.9],
                        ["*.Cu", "F.SilkS", "F.Mask", "B.Mask"], drill=[1.0]))
        x += 2.54
    return pads


def dil_pads(pins):
    pads = []
    x = -((pins - 1) / 2) * 2.54
    for pin in range(pins):
        shape = "rect" if 2*pin+1 == 1 else "circle"
        pads.append(pad(2*pin + 1, "thru_hole", shape, (x, 1.27), [1.9, 1.9],
                        ["*.Cu", "F.SilkS", "F.Mask", "B.Mask"], drill=[1.0]))
        pads.append(pad(2*pin + 2, "thru_hole", "circle", (x, -1.27),
                        [1.9, 1.9], ["*.Cu", "F.SilkS", "F.Mask", "B.Mask"],
                        drill=[1.0]))
        x += 2.54
    return pads


def fab(pins, h):
    _, _, _, _, sq = draw_square(
        pins * 2.54, h, (0, 0), "F.Fab", fab_width)
    return sq


def kk_fab(pins):
    w = fab_width
    nw, ne, se, sw, sq = draw_square(pins * 2.54, 6.35, (0, 0), "F.Fab", w)
    sq.append(fp_line((nw[0], nw[1]+2.0), (ne[0], ne[1]+2.0), "F.Fab", w))
    return sq


def sil_silk(pins):
    _, _, _, _, sq = draw_square(
        pins * 2.54, 2.54, (0, 0), "F.SilkS", silk_width)
    return sq


def dil_silk(pins):
    nw, ne, se, sw, _ = draw_square(
        pins * 2.54, 2*2.54, (0, 0), "F.SilkS", silk_width)
    layer = "F.SilkS"
    w = silk_width
    out = []
    out.append(fp_line(nw, ne, layer, w))
    out.append(fp_line(ne, se, layer, w))
    out.append(fp_line(se, (1.27, se[1]), layer, w))
    out.append(fp_line((-1.27, sw[1]), sw, layer, w))
    out.append(fp_line(sw, nw, layer, w))
    return out


def kk_silk(pins):
    w = silk_width
    nw, ne, se, sw, sq = draw_square(pins * 2.54, 6.35, (0, 0), "F.SilkS", w)
    sq.append(fp_line((nw[0], nw[1]+2.0), (ne[0], ne[1]+2.0), "F.SilkS", w))
    return sq


def ctyd(pins, h):
    w = pins * 2.54 + 2 * ctyd_gap
    h = h + 2 * ctyd_gap
    grid = 2 * ctyd_grid
    w = grid * int(math.ceil(w / grid))
    h = grid * int(math.ceil(h / grid))
    _, _, _, _, sq = draw_square(w, h, (0, 0), "F.CrtYd", ctyd_width)
    return sq


def refs(name, h):
    out = []
    ctyd_h = h + 2 * ctyd_gap
    y = ctyd_h / 2.0 + font_halfheight
    out.append(fp_text("reference", "REF**", (0, -y),
               "F.Fab", font_size, font_thickness))
    out.append(fp_text("value", name, (0, y),
               "F.Fab", font_size, font_thickness))
    return out


def sil_model(pins):
    if pins <= 20:
        return [model("${KISYS3DMOD}/Pin_Headers.3dshapes/" +
                      "PinHeader_1x{:02d}_P2.54mm_Vertical.step".format(pins),
                      (0, 0, 0),
                      (1, 1, 1),
                      (0, 0, 0))]
    else:
        return []


def dil_model(pins):
    if pins <= 40:
        return [model("${KISYS3DMOD}/Connector_PinHeader_2.54mm.3dshapes/" +
                      "PinHeader_2x{:02d}_P2.54mm_Vertical.step".format(pins),
                      (0, 0, 0),
                      (1, 1, 1),
                      (0, 0, 0))]
    else:
        return []


def kk_model(pins):
    if pins <= 16:
        return [model("${KISYS3DMOD}/Connector_Molex.3dshapes/" +
                      "Molex_KK-254_AE-6410-" +
                      "{:02d}A_1x{:02d}".format(pins, pins) +
                      "_P2.54mm_Vertical.step",
                      (0, 0, 0),
                      (1, 1, 1),
                      (0, 0, 0))]


def sil(pins):
    name = "SIL-254P-{:02d}".format(pins)
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += sil_pads(pins)
    sexp += fab(pins, 2.54)
    sexp += sil_silk(pins)
    sexp += ctyd(pins, 2.54)
    sexp += refs(name, 2.54)
    sexp += sil_model(pins)
    return name, sexp_generate(sexp)


def dil(pins):
    name = "DIL-254P-{:02d}".format(2*pins)
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += dil_pads(pins)
    sexp += fab(pins, 2*2.54)
    sexp += dil_silk(pins)
    sexp += ctyd(pins, 2*2.54)
    sexp += refs(name, 2*2.54)
    sexp += dil_model(pins)
    return name, sexp_generate(sexp)


def kk(pins):
    name = "MOLEX-KK-254P-{:02d}".format(pins)
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += sil_pads(pins)
    sexp += kk_fab(pins)
    sexp += kk_silk(pins)
    sexp += ctyd(pins, 6.35)
    sexp += refs(name, 6.35)
    sexp += kk_model(pins)
    return name, sexp_generate(sexp)


def main(prettypath, verify=False, verbose=False):
    for pins in range(1, 21):
        for generator in (sil, dil, kk):
            if generator == kk and (pins == 1 or pins > 16):
                continue

            # Generate footprint
            name, fp = generator(pins)
            path = os.path.join(prettypath, name + ".kicad_mod")

            if verify and verbose:
                print("Verifying", path)

            # Check if the file already exists and isn't changed
            if os.path.isfile(path):
                with open(path) as f:
                    old = f.read()
                old = [n for n in sexp_parse(old) if n[0] != "tedit"]
                new = [n for n in sexp_parse(fp) if n[0] != "tedit"]
                if new == old:
                    continue

            # If it needs changing, either verification failed or we rewrite
            if verify:
                return False
            else:
                with open(path, "w") as f:
                    f.write(fp)

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
