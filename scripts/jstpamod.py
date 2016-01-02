"""
jstpamod.py
Copyright 2016 Adam Greig

Generate footprints for JST-PA connectors.
"""

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

from sexp import sexp_parse, sexp_generate
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


def pads_pth(pins):
    x = pins - 1
    pads = []
    for pin in range(pins):
        pads.append(pad(pin+1, "thru_hole", "circle", (x, 0), [1.6, 1.6],
                        ["*.Cu", "*.Mask"], drill=0.8))
        x -= 2.0
    return pads


def top_npth(pins):
    x = ((2.0 * (pins - 1)) // 2) + 1.5
    size = [1.2, 1.2]
    layers = ["*.Mask"]
    return [
        pad("", "np_thru_hole", "circle", (x, -1.7), size, layers, drill=1.2)
    ]


def side_npth(pins):
    x = ((2.0 * (pins - 1)) // 2) + 1.5
    size = [1.2, 1.2]
    layers = ["*.Mask"]
    return [
        pad("", "np_thru_hole", "circle", (x, -2.1), size, layers, drill=1.2),
        pad("", "np_thru_hole", "circle", (-x, -2.1), size, layers, drill=1.2)
    ]


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
        x -= 2.0

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
        x -= 2.0
    return out


def top_pth_ctyd(pins):
    w = 2*(pins-1)+4 + 2*ctyd_gap
    h = 5.3 + 2*ctyd_gap
    grid = 2*ctyd_grid
    w = grid * int(math.ceil(w / (2*ctyd_grid)))
    h = grid * int(math.ceil(h / (2*ctyd_grid)))
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


def top_pth_fp(pins):
    name = "B{:02d}B-PASK".format(pins)
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += top_pth_refs(name)
    sexp += top_pth_silk(pins)
    sexp += top_pth_fab(pins)
    sexp += top_pth_ctyd(pins)
    sexp += top_npth(pins)
    sexp += pads_pth(pins)
    return name, sexp_generate(sexp)


def side_pth_fp(pins):
    name = "S{:02d}B-PASK-2".format(pins)
    tedit = format(int(time.time()), 'X')
    sexp = ["module", name, ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += side_pth_refs(name)
    sexp += side_pth_silk(pins)
    sexp += side_pth_fab(pins)
    sexp += side_pth_ctyd(pins)
    sexp += side_npth(pins)
    sexp += pads_pth(pins)
    return name, sexp_generate(sexp)


def main(prettypath):
    for pins in range(2, 9):
        for generator in (top_pth_fp, side_pth_fp):
            # Generate the footprint
            name, fp = generator(pins)
            path = os.path.join(prettypath, name + ".kicad_mod")

            # Check if the file already exists and isn't changed
            if os.path.isfile(path):
                with open(path) as f:
                    old = f.read()
                old = [n for n in sexp_parse(old) if n[0] != "tedit"]
                new = [n for n in sexp_parse(fp) if n[0] != "tedit"]
                if new == old:
                    continue

            # Write the new file
            with open(path, "w") as f:
                f.write(fp)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        prettypath = sys.argv[1]
        main(prettypath)
    else:
        print("Usage: {} <.pretty path>".format(sys.argv[0]))
        sys.exit(0)
