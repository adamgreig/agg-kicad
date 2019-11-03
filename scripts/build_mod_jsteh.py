"""
build_mod_jsteh.py
Copyright 2016 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generate footprints for JST-EH connectors.
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


def side_pth_refs(name):
    out = []
    ctyd_h = 8.2 + 2*ctyd_gap
    y = ctyd_h / 2.0 + font_halfheight
    out.append(fp_text("reference", "REF**", (0, -y-2.6),
               "F.Fab", font_size, font_thickness))
    out.append(fp_text("value", name, (0, y-2.6),
               "F.Fab", font_size, font_thickness))
    return out


def pth_pads(pins):
    x = (pins - 1)*1.25
    pads = []
    for pin in range(pins):
        pads.append(pad(pin+1, "thru_hole", "circle", (x, 0), [1.8, 1.8],
                        ["*.Cu", "*.Mask"], drill=1.0))
        x -= 2.5
    return pads


def side_pth_silk(pins):
    out = []
    w = silk_width
    centre = (0, -2.6)
    nw, ne, se, sw, _ = draw_square(2.5*(pins-1)+5, 8.2, centre, "F.SilkS", w)
    out.append(fp_line(nw, ne, "F.SilkS", w))
    out.append(fp_line(ne, se, "F.SilkS", w))
    out.append(fp_line(se, (se[0]-1, se[1]), "F.SilkS", w))
    out.append(fp_line((se[0]-1, se[1]), (se[0]-1, se[1]-2.2), "F.SilkS", w))
    out.append(fp_line(nw, sw, "F.SilkS", w))
    out.append(fp_line(sw, (sw[0]+1, sw[1]), "F.SilkS", w))
    out.append(fp_line((sw[0]+1, sw[1]), (sw[0]+1, sw[1]-2.2), "F.SilkS", w))
    return out


def side_pth_fab(pins):
    out = []
    w = fab_width
    centre = (0, -2.6)

    # Draw outline
    nw, ne, se, sw, _ = draw_square(2.5*(pins-1)+5, 8.2, centre, "F.Fab", w)
    out.append(fp_line(nw, ne, "F.Fab", w))
    out.append(fp_line(ne, se, "F.Fab", w))
    out.append(fp_line(se, (se[0]-1, se[1]), "F.Fab", w))
    out.append(fp_line((se[0]-1, se[1]), (se[0]-1, se[1]-2.2), "F.Fab", w))
    out.append(fp_line((se[0]-1, se[1]-2.2), (sw[0]+1, sw[1]-2.2), "F.Fab", w))
    out.append(fp_line(nw, sw, "F.Fab", w))
    out.append(fp_line(sw, (sw[0]+1, sw[1]), "F.Fab", w))
    out.append(fp_line((sw[0]+1, sw[1]), (sw[0]+1, sw[1]-2.2), "F.Fab", w))

    # Draw the pins
    x = 1.25*(pins - 1)
    for pin in range(pins):
        sq = draw_square(0.5, 0.75, (x, -0.125), "F.Fab", fab_width)
        out += sq[4]
        out.append(fp_line((x-.25, -.25), (x+.25, -.25), "F.Fab", fab_width))
        x -= 2.5
    return out


def side_pth_ctyd(pins):
    w = 2.5*(pins-1)+5 + 2*ctyd_gap
    h = 8.2 + 2*ctyd_gap
    grid = 2*ctyd_grid
    w = grid * int(math.ceil(w / (2*ctyd_grid)))
    h = grid * int(math.ceil(h / (2*ctyd_grid)))
    centre = (0, -2.6)
    _, _, _, _, sq = draw_square(w, h, centre, "F.CrtYd", ctyd_width)
    return sq


def side_pth_fp(pins):
    name = "S{:d}B-EH".format(pins)
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += side_pth_refs(name)
    sexp += side_pth_silk(pins)
    sexp += side_pth_fab(pins)
    sexp += side_pth_ctyd(pins)
    sexp += pth_pads(pins)
    return name, sexp_generate(sexp)



def main(prettypath, verify=False, verbose=False):
    for pins in range(2, 9):
        for generator in (side_pth_fp,):
            # Generate the footprint
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

            # If not, either verification failed or we should output the new fp
            if verify:
                return False
            else:
                with open(path, "w") as f:
                    f.write(fp)

    # If we finished and didn't return yet, verification has succeeded
    if verify:
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prettypath", type=str,
                        help="Path to footprints to process")
    parser.add_argument("--verify", action="store_true",
                        help="Verify libraries are up to date")
    parser.add_argument("--verbose", action="store_true",
                        help="Print out every library verified")
    args = vars(parser.parse_args())
    result = main(**args)
    if args['verify']:
        if result:
            print("OK: all footprints up-to-date.")
            sys.exit(0)
        else:
            print("Error: footprints not up-to-date.", file=sys.stderr)
            sys.exit(1)
