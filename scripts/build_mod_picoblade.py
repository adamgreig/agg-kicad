"""
build_mod_picoblade.py
Copyright 2019 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generate foorprints for Molex Picoblade connectors.
"""

from __future__ import print_function, division

import os
import sys
import time
import math
import argparse

from sexp import parse as sexp_parse, generate as sexp_generate
from kicad_mod import fp_line, fp_text, pad, draw_square, model


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


def top_smd_refs(name):
    out = []
    ctyd_h = 3.0 + 0.6 + 1.3 + 2*ctyd_gap
    ctyd_y = ctyd_h/2 - 1.3/2 - ctyd_gap
    y = ctyd_h / 2.0 + font_halfheight
    out.append(fp_text("reference", "REF**", (0, -y+ctyd_y),
                       "F.Fab", font_size, font_thickness))
    out.append(fp_text("value", name, (0, y+ctyd_y),
                       "F.Fab", font_size, font_thickness))
    return out


def top_smd_pads(pins):
    x = -(pins-1)/2 * 1.25
    pads = []
    for pin in range(pins):
        pads.append(pad(pin+1, "smd", "rect", (x, 0), [0.8, 1.3],
                        ["F.Cu", "F.Mask", "F.Paste"]))
        x += 1.25
    return pads


def top_smd_mount(pins):
    x = -(pins-1)/2 * 1.25 - 3.6 + 2.1/2
    out = []
    for xx in (x, -x):
        out.append(pad("", "smd", "rect", (xx, 0.6+3.0/2+1.3/2), (2.1, 3.0),
                       ["F.Cu", "F.Mask", "F.Paste"]))
    return out


def top_smd_silk(pins):
    out = []
    w = silk_width
    lyr = "F.SilkS"
    box_w = (pins-1)*1.25 + 2*3.6 - 2*2.1 - silk_width
    box_h = 3.5  # XXX
    box_y = box_h/2 + 0.2
    nw, ne, se, sw, _ = draw_square(box_w, box_h, (0, box_y), lyr, w)
    out.append(fp_line((nw[0]+0.8, nw[1]), nw, lyr, w))
    out.append(fp_line(nw, sw, lyr, w))
    out.append(fp_line(sw, se, lyr, w))
    out.append(fp_line(se, ne, lyr, w))
    out.append(fp_line((ne[0]-0.8, ne[1]), ne, lyr, w))
    return out


def top_smd_fab(pins):
    out = []
    w = fab_width
    lyr = "F.Fab"
    # Outline box
    box_w = (pins-1)*1.25 + 2*3.6 - 2*2.1
    box_h = 3.5  # XXX
    box_y = box_h/2 + 0.2
    nw, ne, se, sw, sq = draw_square(box_w, box_h, (0, box_y), lyr, w)
    out += sq
    # Mounting pins
    _, _, _, _, sq = draw_square(1.8, 2.8, (nw[0]-1.8/2, sw[1]-2.8/2), lyr, w)
    out += sq
    _, _, _, _, sq = draw_square(1.8, 2.8, (ne[0]+1.8/2, sw[1]-2.8/2), lyr, w)
    out += sq
    # Connector pins
    x = -(pins-1)/2 * 1.25
    for pin in range(pins):
        _, _, _, _, sq = draw_square(0.32, 0.6, (x, 2.6), lyr, w)
        out += sq
        x += 1.25
    return out


def top_smd_ctyd(pins):
    w = 1.25*(pins-1) + 2*3.6 + 2*ctyd_gap
    h = 3.0 + 0.6 + 1.3 + 2*ctyd_gap
    grid = 2 * ctyd_grid
    w = grid * int(math.ceil(w / (2*ctyd_grid)))
    h = grid * int(math.ceil(h / (2*ctyd_grid)))
    y = h/2 - 1.3/2 - ctyd_gap
    centre = (0, y)
    _, _, _, _, sq = draw_square(w, h, centre, "F.CrtYd", ctyd_width)
    return sq


def top_smd_model(pins):
    return [
        model(
            "${KISYS3DMOD}/Connector_Molex.3dshapes/" +
            "Molex_PicoBlade_53398-{:02d}71_1x{:02d}".format(pins, pins) +
            "-1MP_P1.25mm_Vertical.step",
            (0, -1.3/25.4, 0),
            (1, 1, 1),
            (0, 0, 0))]


def top_smd_fp(pins):
    name = "MOLEX-PICOBLADE-53398-{:02d}71".format(pins)
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += top_smd_refs(name)
    sexp += top_smd_silk(pins)
    sexp += top_smd_fab(pins)
    sexp += top_smd_ctyd(pins)
    sexp += top_smd_mount(pins)
    sexp += top_smd_pads(pins)
    sexp += top_smd_model(pins)
    return name, sexp_generate(sexp)


def main(prettypath, verify=False, verbose=False):
    for pins in range(2, 15):
        for generator in (top_smd_fp,):
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
