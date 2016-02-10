"""
panelise.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.
"""

from __future__ import print_function, division


import sys
import copy
import datetime
from decimal import Decimal

from sexp import parse as sexp_parse, generate as sexp_generate


def simples(n, out, xr, xp, yr, yp):
    for x in range(xr):
        for y in range(yr):
            xx = x * xp
            yy = y * yp
            simple(n, out, xx, yy)


def simple(n, out, x, y):
    new = copy.deepcopy(n)
    for idx, child in enumerate(new):
        if child[0] in ("at", "start", "end"):
            new[idx][1] = Decimal(child[1]) + x
            new[idx][2] = Decimal(child[2]) + y
    out.append(new)


def zones(n, out, xr, xp, yr, yp):
    for x in range(xr):
        for y in range(yr):
            xx = x * xp
            yy = y * yp
            zone(n, out, xx, yy)


def zone(n, out, x, y):
    new = copy.deepcopy(n)
    for idx, child in enumerate(new):
        if child[0] in ("polygon", "filled_polygon"):
            new[idx][1] = ["pts"]
            for (xy, xx, yy) in n[idx][1][1:]:
                new[idx][1].append([xy, Decimal(xx)+x, Decimal(yy)+y])
    out.append(new)


def main(inpath, outpath, xr, xp, yr, yp):
    with open(inpath) as f:
        insexp = sexp_parse(f.read())

    outsexp = [
        "kicad_pcb",
        ["version", 4],
        ["host", "panelise.py", datetime.datetime.utcnow().isoformat()],
    ]

    simple_types = ("gr_arc", "gr_line", "gr_text", "segment", "via", "module")

    for node in insexp:
        if node[0] in ("page", "layers", "setup", "net", "net_class"):
            outsexp.append(node)
        elif node[0] in simple_types:
            simples(node, outsexp, xr, xp, yr, yp)
        elif node[0] == "zone":
            zones(node, outsexp, xr, xp, yr, yp)

    with open(outpath, "w") as f:
        f.write(sexp_generate(outsexp))


if __name__ == "__main__":
    if len(sys.argv) == 7:
        inpath = sys.argv[1]
        x_repeat = int(sys.argv[2])
        x_pitch = Decimal(sys.argv[3])
        y_repeat = int(sys.argv[4])
        y_pitch = Decimal(sys.argv[5])
        outpath = sys.argv[6]
        main(inpath, outpath, x_repeat, x_pitch, y_repeat, y_pitch)
    else:
        print("Usage: {} <in.kicad_pcb> <x repeat> <x pitch> <y repeat>"
              " <y pitch> <out.kicad_pcb>".format(sys.argv[0]))
