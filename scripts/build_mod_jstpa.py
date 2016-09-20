"""
build_mod_jstpa.py
Copyright 2016 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generate footprints for JST-PA connectors.
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


def top_pth_refs(name):
    out = []
    ctyd_h = 5.3 + 2*ctyd_gap
    y = ctyd_h / 2.0 + font_halfheight
    out.append(fp_text("reference", "REF**", (0, -y),
               "F.Fab", font_size, font_thickness))
    out.append(fp_text("value", name, (0, y),
               "F.Fab", font_size, font_thickness))
    return out


def side_pth_refs(name):
    out = []
    ctyd_h = 11.7 + 2*ctyd_gap
    y = ctyd_h / 2.0 + font_halfheight
    out.append(fp_text("reference", "REF**", (0, -y-2.35),
               "F.Fab", font_size, font_thickness))
    out.append(fp_text("value", name, (0, y-2.35),
               "F.Fab", font_size, font_thickness))
    return out


def top_smd_refs(name):
    out = []
    ctyd_h = 3.0 + 5.0 + 2 * ctyd_gap
    y = ctyd_h / 2.0 + font_halfheight
    out.append(fp_text("reference", "REF**", (0, -y+2.50),
               "F.Fab", font_size, font_thickness))
    out.append(fp_text("value", name, (0, y+2.50),
               "F.Fab", font_size, font_thickness))
    return out


def side_smd_refs(name):
    out = []
    ctyd_h = 3.0 + 7.8 + 2*ctyd_gap
    y = ctyd_h / 2.0 + font_halfheight
    out.append(fp_text("reference", "REF**", (0, -y-2.55),
               "F.Fab", font_size, font_thickness))
    out.append(fp_text("value", name, (0, y-2.55),
               "F.Fab", font_size, font_thickness))
    return out


def pth_pads(pins):
    x = pins - 1
    pads = []
    for pin in range(pins):
        pads.append(pad(pin+1, "thru_hole", "circle", (x, 0), [1.6, 1.6],
                        ["*.Cu", "*.Mask"], drill=0.8))
        x -= 2
    return pads


def top_smd_pads(pins):
    x = pins - 1
    pads = []
    for pin in range(pins):
        pads.append(pad(pin+1, "smd", "rect", (x, 0), [1, 3.0],
                        ["F.Cu", "F.Mask", "F.Paste"]))
        x -= 2
    return pads


def side_smd_pads(pins):
    x = pins - 1
    pads = []
    for pin in range(pins):
        pads.append(pad(pin+1, "smd", "rect", (x, 1.5-0.15), [1, 2.7+2*0.15],
                        ["F.Cu", "F.Mask", "F.Paste"]))
        x -= 2
    return pads


def top_pth_mount(pins):
    x = ((2.0 * (pins - 1)) // 2) + 1.5
    size = [1.2, 1.2]
    layers = ["*.Mask"]
    return [
        pad("", "np_thru_hole", "circle", (x, -1.7), size, layers, drill=1.2)
    ]


def side_pth_mount(pins):
    x = ((2.0 * (pins - 1)) // 2) + 1.5
    size = [1.2, 1.2]
    layers = ["*.Mask"]
    return [
        pad("", "np_thru_hole", "circle", (x, -2.1), size, layers, drill=1.2),
        pad("", "np_thru_hole", "circle", (-x, -2.1), size, layers, drill=1.2)
    ]


def top_smd_mount(pins):
    out = []
    x = pins - 1
    for xx in (x+2.35, -x-2.35):
        out.append(pad("", "smd", "rect", (xx, 4.7), (1.8, 3.6),
                       ["F.Cu", "F.Mask", "F.Paste"]))
    return out


def side_smd_mount(pins):
    out = []
    x = pins - 1
    for xx in (x+2.35, -x-2.35):
        out.append(pad("", "smd", "rect", (xx, -3.25), (1.8, 3.8),
                       ["F.Cu", "F.Mask", "F.Paste"]))
    return out


def top_pth_silk(pins):
    s = draw_square(2*(pins-1)+4, 5.3, (0, 0), "F.SilkS", silk_width)
    return s[4]


def side_pth_silk(pins):
    out = []
    w = silk_width
    centre = (0, -2.35)
    nw, ne, se, sw, _ = draw_square(2*(pins-1)+4, 11.7, centre, "F.SilkS", w)
    out.append(fp_line(nw, ne, "F.SilkS", w))
    out.append(fp_line(ne, se, "F.SilkS", w))
    out.append(fp_line(se, (se[0]-1, se[1]), "F.SilkS", w))
    out.append(fp_line((se[0]-1, se[1]), (se[0]-1, se[1]-4), "F.SilkS", w))
    out.append(fp_line(nw, sw, "F.SilkS", w))
    out.append(fp_line(sw, (sw[0]+1, sw[1]), "F.SilkS", w))
    out.append(fp_line((sw[0]+1, sw[1]), (sw[0]+1, sw[1]-4), "F.SilkS", w))
    return out


def top_smd_silk(pins):
    out = []
    w = silk_width
    l = "F.SilkS"
    nw, ne, se, sw, _ = draw_square(2*pins+4, 5.7, (0, 3.35), l, w)
    # Top left corner
    out.append(fp_line((nw[0], nw[1]+2.4), (nw[0], nw[1]), l, w))
    out.append(fp_line((nw[0], nw[1]), (nw[0]+2.3, nw[1]), l, w))
    # Top right corner
    out.append(fp_line((ne[0], ne[1]+2.4), (ne[0], ne[1]), l, w))
    out.append(fp_line((ne[0], ne[1]), (ne[0]-2.3, ne[1]), l, w))
    # Bottom
    out.append(fp_line((sw[0]+1.8, sw[1]), (se[0]-1.8, se[1]), l, w))
    return out


def side_smd_silk(pins):
    out = []
    w = silk_width
    l = "F.SilkS"
    nw, ne, se, sw, _ = draw_square(2*pins+4, 8.9, (0, -3.5), l, w)
    out.append(fp_line(nw, (nw[0]+3, nw[1]), l, w))
    out.append(fp_line((nw[0]+3, nw[1]), (nw[0]+3, nw[1]+1.4), l, w))
    out.append(fp_line((nw[0]+3, nw[1]+1.4), (ne[0]-3, ne[1]+1.4), l, w))
    out.append(fp_line((ne[0]-3, ne[1]+1.4), (ne[0]-3, ne[1]), l, w))
    out.append(fp_line((ne[0]-3, ne[1]), ne, l, w))
    out.append(fp_line(ne, (ne[0], ne[1]+2.8-w), l, w))
    out.append(fp_line(nw, (nw[0], nw[1]+2.8-w), l, w))
    out.append(fp_line(se, (se[0], se[1]-2.3+w), l, w))
    out.append(fp_line(se, (se[0]-1.8, se[1]), l, w))
    out.append(fp_line(sw, (sw[0], sw[1]-2.3+w), l, w))
    out.append(fp_line(sw, (sw[0]+1.8, sw[1]), l, w))
    return out


def top_pth_fab(pins):
    out = []

    # Draw outline
    _, _, _, _, sq = draw_square(2*(pins-1)+4, 5.3, (0, 0), "F.Fab", fab_width)
    out += sq

    # Draw side leg
    x = pins - 1 + 1.5
    _, _, _, _, sq = draw_square(.8, .8, (x, -1.7), "F.Fab", fab_width)
    out += sq

    # Draw pins
    x = pins - 1
    for pin in range(pins):
        _, _, _, _, sq = draw_square(.5, .5, (x, 0), "F.Fab", fab_width)
        out += sq
        x -= 2

    return out


def side_pth_fab(pins):
    out = []
    w = fab_width
    centre = (0, -2.35)

    # Draw outline
    nw, ne, se, sw, _ = draw_square(2*(pins-1)+4, 11.7, centre, "F.Fab", w)
    out.append(fp_line(nw, ne, "F.Fab", w))
    out.append(fp_line(ne, se, "F.Fab", w))
    out.append(fp_line(se, (se[0]-1, se[1]), "F.Fab", w))
    out.append(fp_line((se[0]-1, se[1]), (se[0]-1, se[1]-4), "F.Fab", w))
    out.append(fp_line((se[0]-1, se[1]-4), (sw[0]+1, sw[1]-4), "F.Fab", w))
    out.append(fp_line(nw, sw, "F.Fab", w))
    out.append(fp_line(sw, (sw[0]+1, sw[1]), "F.Fab", w))
    out.append(fp_line((sw[0]+1, sw[1]), (sw[0]+1, sw[1]-4), "F.Fab", w))

    # Draw side legs
    x = (2*(pins-1)+4)//2 - 0.3
    _, _, _, _, sq = draw_square(0.6, 0.8, (x, -2.1), "F.Fab", w)
    out += sq
    _, _, _, _, sq = draw_square(0.6, 0.8, (-x, -2.1), "F.Fab", w)
    out += sq

    # Draw the pins
    x = pins - 1
    for pin in range(pins):
        sq = draw_square(0.5, 0.75, (x, -0.125), "F.Fab", fab_width)
        out += sq[4]
        out.append(fp_line((x-.25, -.25), (x+.25, -.25), "F.Fab", fab_width))
        x -= 2
    return out


def top_smd_fab(pins):
    out = []
    w = fab_width

    # Outline
    _, _, _, _, sq = draw_square(2*pins+4, 5.7, (0, 3.35), "F.Fab", w)
    out += sq

    # Pins
    x = pins - 1
    for pin in range(pins):
        _, _, _, _, sq = draw_square(0.5, 2.5, (x, -0), "F.Fab", w)
        out += sq
        x -= 2

    return out


def side_smd_fab(pins):
    out = []
    w = fab_width

    # Draw outline
    nw, ne, se, sw, sq = draw_square(2*pins+4, 8.9, (0, -3.5), "F.Fab", w)
    out.append(fp_line(nw, (nw[0]+3, nw[1]), "F.Fab", w))
    out.append(fp_line((nw[0]+3, nw[1]), (nw[0]+3, nw[1]+1.4), "F.Fab", w))
    out.append(fp_line((nw[0]+3, nw[1]+1.4), (ne[0]-3, ne[1]+1.4), "F.Fab", w))
    out.append(fp_line((ne[0]-3, ne[1]+1.4), (ne[0]-3, ne[1]), "F.Fab", w))
    out.append(fp_line((ne[0]-3, ne[1]), ne, "F.Fab", w))
    out.append(fp_line(ne, se, "F.Fab", w))
    out.append(fp_line(se, sw, "F.Fab", w))
    out.append(fp_line(sw, nw, "F.Fab", w))

    # Draw pins
    x = pins - 1
    for pin in range(pins):
        _, _, _, _, sq = draw_square(0.5, 2.5, (x, 2.5/2), "F.Fab", w)
        out += sq
        x -= 2
    return out


def top_pth_ctyd(pins):
    w = 2*(pins-1)+4 + 2*ctyd_gap
    h = 5.3 + 2*ctyd_gap
    grid = 2*ctyd_grid
    w = grid * int(math.ceil(w / grid))
    h = grid * int(math.ceil(h / grid))
    _, _, _, _, sq = draw_square(w, h, (0, 0), "F.CrtYd", ctyd_width)
    return sq


def side_pth_ctyd(pins):
    w = 2*(pins-1)+4 + 2*ctyd_gap
    h = 11.7 + 2*ctyd_gap
    grid = 2*ctyd_grid
    w = grid * int(math.ceil(w / (2*ctyd_grid)))
    h = grid * int(math.ceil(h / (2*ctyd_grid)))
    centre = (0, -2.35)
    _, _, _, _, sq = draw_square(w, h, centre, "F.CrtYd", ctyd_width)
    return sq


def top_smd_ctyd(pins):
    w = 2 * (pins - 1 + 1.45 + 1.8 + ctyd_gap)
    h = 3.0 + 5.0 + 2 * ctyd_gap
    grid = 2 * ctyd_grid
    w = grid * int(math.ceil(w / (2*ctyd_grid)))
    h = grid * int(math.ceil(h / (2*ctyd_grid)))
    centre = (0, 2.50)
    _, _, _, _, sq = draw_square(w, h, centre, "F.CrtYd", ctyd_width)
    return sq


def side_smd_ctyd(pins):
    w = 2 * (pins - 1 + 1.45 + 1.8 + ctyd_gap)
    h = 3.0 + 7.8 + 2*ctyd_gap
    grid = 2*ctyd_grid
    w = grid * int(math.ceil(w / (2*ctyd_grid)))
    h = grid * int(math.ceil(h / (2*ctyd_grid)))
    centre = (0, -2.55)
    _, _, _, _, sq = draw_square(w, h, centre, "F.CrtYd", ctyd_width)
    return sq


def top_pth_fp(pins):
    name = "B{:02d}B-PASK".format(pins)
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += top_pth_refs(name)
    sexp += top_pth_silk(pins)
    sexp += top_pth_fab(pins)
    sexp += top_pth_ctyd(pins)
    sexp += top_pth_mount(pins)
    sexp += pth_pads(pins)
    return name, sexp_generate(sexp)


def side_pth_fp(pins):
    name = "S{:02d}B-PASK-2".format(pins)
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += side_pth_refs(name)
    sexp += side_pth_silk(pins)
    sexp += side_pth_fab(pins)
    sexp += side_pth_ctyd(pins)
    sexp += side_pth_mount(pins)
    sexp += pth_pads(pins)
    return name, sexp_generate(sexp)


def top_smd_fp(pins):
    name = "BM{:02d}B-PASS".format(pins)
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += top_smd_refs(name)
    sexp += top_smd_silk(pins)
    sexp += top_smd_fab(pins)
    sexp += top_smd_ctyd(pins)
    sexp += top_smd_mount(pins)
    sexp += top_smd_pads(pins)
    return name, sexp_generate(sexp)


def side_smd_fp(pins):
    name = "SM{:02d}B-PASS".format(pins)
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += side_smd_refs(name)
    sexp += side_smd_silk(pins)
    sexp += side_smd_fab(pins)
    sexp += side_smd_ctyd(pins)
    sexp += side_smd_mount(pins)
    sexp += side_smd_pads(pins)
    return name, sexp_generate(sexp)


def main(prettypath, verify=False, verbose=False):
    for pins in range(2, 9):
        for generator in (top_pth_fp, side_pth_fp, top_smd_fp, side_smd_fp):
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
