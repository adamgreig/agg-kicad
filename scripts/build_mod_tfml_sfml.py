"""
build_mod_tfml_sfml.py
Copyright 2016 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generate footprints for Samtec TFML and SFML connectors.
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
from kicad_mod import fp_line, fp_text, pad, draw_square


def tfml_pads(pins):
    pads = []
    x = -((pins - 1) / 2.0) * 1.27
    for pin in range(pins):
        pads.append(pad(pin*2 + 1, "smd", "rect", (x, 1.715), [0.74, 2.92],
                        ["F.Cu", "F.Mask", "F.Paste"]))
        pads.append(pad(pin*2 + 2, "smd", "rect", (x, -1.715), [0.74, 2.92],
                        ["F.Cu", "F.Mask", "F.Paste"]))
        x += 1.27
    return pads


def sfml_pads(pins):
    pads = []
    x = -((pins - 1) / 2.0) * 1.27
    for pin in range(pins):
        pads.append(pad(pin*2 + 1, "smd", "rect", (x, -1.365), [0.74, 2.22],
                        ["F.Cu", "F.Mask", "F.Paste"]))
        pads.append(pad(pin*2 + 2, "smd", "rect", (x, 1.365), [0.74, 2.22],
                        ["F.Cu", "F.Mask", "F.Paste"]))
        x += 1.27
    return pads


def locking_clip(pins):
    x = (pins * 1.27 + 1.91) / 2.0
    size = [1.2, 1.2]
    l = ["*.Mask"]
    pads = []
    pads.append(pad("", "np_thru_hole", "circle", (+x, 0), size, l, drill=1.2))
    pads.append(pad("", "np_thru_hole", "circle", (-x, 0), size, l, drill=1.2))
    return pads


def tfml_fab(pins):
    _, _, _, _, sq = draw_square(
        pins * 1.27 + 3.18, 5.72, (0, 0), "F.Fab", fab_width)
    return sq


def sfml_fab(pins):
    out = []
    l = "F.Fab"
    w = fab_width
    a_x = (3.94 - 0.38) / 2.0
    a_y = (3.05 - 1.52) / 2.0
    nw, ne, se, sw, _ = draw_square(
        pins * 1.27 + 0.38, 3.05, (0, 0), l, w)
    out.append(fp_line(nw, ne, l, w))
    out.append(fp_line(ne, (ne[0], ne[1]+a_y), l, w))
    out.append(fp_line((ne[0], ne[1]+a_y), (ne[0]+a_x, ne[1]+a_y), l, w))
    out.append(fp_line((ne[0]+a_x, ne[1]+a_y), (se[0]+a_x, se[1]-a_y), l, w))
    out.append(fp_line((se[0]+a_x, se[1]-a_y), (se[0], se[1]-a_y), l, w))
    out.append(fp_line((se[0], se[1]-a_y), se, l, w))
    out.append(fp_line(se, sw, l, w))
    out.append(fp_line(sw, (sw[0], sw[1]-a_y), l, w))
    out.append(fp_line((sw[0], sw[1]-a_y), (sw[0]-a_x, sw[1]-a_y), l, w))
    out.append(fp_line((sw[0]-a_x, sw[1]-a_y), (nw[0]-a_x, nw[1]+a_y), l, w))
    out.append(fp_line((nw[0]-a_x, nw[1]+a_y), (nw[0], nw[1]+a_y), l, w))
    out.append(fp_line((nw[0], nw[1]+a_y), nw, l, w))
    return out


def tfml_silk(pins):
    out = []
    l = "F.SilkS"
    w = silk_width
    nw, ne, se, sw, _ = draw_square(
        pins * 1.27 + 3.18 - w, 5.72 - w, (0, 0), l, w)
    out.append(fp_line((nw[0]+1.5, nw[1]), nw, l, w))
    out.append(fp_line(nw, sw, l, w))
    out.append(fp_line(sw, (sw[0]+1.5, sw[1]), l, w))
    out.append(fp_line((se[0]-1.5, se[1]), (se[0], se[1]-1.5), l, w))
    out.append(fp_line((se[0], se[1]-1.5), (ne[0], ne[1]+1.5), l, w))
    out.append(fp_line((ne[0], ne[1]+1.5), (ne[0]-1.5, ne[1]), l, w))
    return out


def sfml_silk(pins):
    out = []
    l = "F.SilkS"
    w = silk_width
    a_x = (3.94 - 0.38) / 2.0
    a_y = (3.05 - 1.52) / 2.0
    nw, ne, se, sw, _ = draw_square(
        pins * 1.27 + 0.38 - w, 3.05 - w, (0, 0), l, w)

    out.append(fp_line(ne, (ne[0], ne[1]+a_y), l, w))
    out.append(fp_line((ne[0], ne[1]+a_y), (ne[0]+a_x, ne[1]+a_y), l, w))
    out.append(fp_line((ne[0]+a_x, ne[1]+a_y), (se[0]+a_x, se[1]-a_y), l, w))
    out.append(fp_line((se[0]+a_x, se[1]-a_y), (se[0], se[1]-a_y), l, w))
    out.append(fp_line((se[0], se[1]-a_y), se, l, w))
    out.append(fp_line(se, (se[0]-0.3, se[1]), l, w))

    out.append(fp_line((sw[0]+0.3, sw[1]), sw, l, w))
    out.append(fp_line(sw, (sw[0], sw[1]-a_y), l, w))
    out.append(fp_line((sw[0], sw[1]-a_y), (sw[0]-a_x, sw[1]-a_y), l, w))
    out.append(fp_line((sw[0]-a_x, sw[1]-a_y), (nw[0]-a_x, nw[1]+a_y), l, w))
    out.append(fp_line((nw[0]-a_x, nw[1]+a_y), (nw[0], nw[1]+a_y), l, w))
    out.append(fp_line((nw[0], nw[1]+a_y), nw, l, w))
    return out


def ctyd(pins):
    w = pins * 1.27 + 3.94 + 2 * ctyd_gap
    h = 6.35 + 2 * ctyd_gap
    grid = 2 * ctyd_grid
    w = grid * int(math.ceil(w / grid))
    h = grid * int(math.ceil(h / grid))
    _, _, _, _, sq = draw_square(w, h, (0, 0), "F.CrtYd", ctyd_width)
    return sq


def refs(name):
    out = []
    ctyd_h = 6.35 + 2 * ctyd_gap
    y = ctyd_h / 2.0 + font_halfheight
    out.append(fp_text("reference", "REF**", (0, -y),
               "F.Fab", font_size, font_thickness))
    out.append(fp_text("value", name, (0, y),
               "F.Fab", font_size, font_thickness))
    return out


def tfml_base(name, pins):
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += tfml_pads(pins)
    sexp += tfml_fab(pins)
    sexp += ctyd(pins)
    sexp += tfml_silk(pins)
    sexp += refs(name)
    return sexp


def tfml(pins):
    name = "TFML-1{:02d}-02-L-D".format(pins)
    sexp = tfml_base(name, pins)
    return name, sexp_generate(sexp)


def tfml_lc(pins):
    name = "TFML-1{:02d}-02-L-D-LC".format(pins)
    sexp = tfml_base(name, pins)
    sexp += locking_clip(pins)
    return name, sexp_generate(sexp)


def sfml_base(name, pins):
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += sfml_pads(pins)
    sexp += sfml_fab(pins)
    sexp += ctyd(pins)
    sexp += sfml_silk(pins)
    sexp += refs(name)
    return sexp


def sfml(pins):
    name = "SFML-1{:02d}-02-L-D".format(pins)
    sexp = sfml_base(name, pins)
    return name, sexp_generate(sexp)


def sfml_lc(pins):
    name = "SFML-1{:02d}-02-L-D-LC".format(pins)
    sexp = sfml_base(name, pins)
    sexp += locking_clip(pins)
    return name, sexp_generate(sexp)


def main(prettypath, verify=False, verbose=False):
    for pins in (5, 7, 10, 15):
        for generator in (tfml, tfml_lc, sfml, sfml_lc):
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
