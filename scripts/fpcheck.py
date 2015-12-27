"""
fpcheck.py
Copyright 2015 Adam Greig

Check all footprint files in a directory against a set of consistency fules.
"""

from __future__ import print_function

import sys
import os
import glob
from decimal import Decimal


def sexpparse(sexp):
    """
    Parse an S-expression into Python lists.
    """
    r = [[]]
    token = ''
    quote = False
    for c in sexp:
        if c == '(' and not quote:
            r.append([])
        elif c in (')', ' ', '\n') and not quote:
            if token:
                r[-1].append(token)
            token = ''
            if c == ')':
                t = r.pop()
                r[-1].append(t)
        elif c == '"':
            quote = not quote
        else:
            token += c
    return r[0][0]


def checkrefval(mod, errs):
    for fp_text in (node for node in mod if node[0] == "fp_text"):
        if fp_text[1] not in ("reference", "value"):
            continue
        layer = [n for n in fp_text if n[0] == "layer"][0]
        if layer[1] != "F.Fab":
            errs.append("Value and Reference fields must be on F.Fab")


def checkfont(mod, errs):
    for fp_text in (node for node in mod if node[0] == "fp_text"):
        effects = [n for n in fp_text if n[0] == "effects"][0]
        font = [n for n in effects if n[0] == "font"][0]
        size = [n for n in font if n[0] == "size"][0]
        thickness = [n for n in font if n[0] == "thickness"][0]
        if (Decimal(size[1]) != 1 or Decimal(size[2]) != 1):
            errs.append("Font must all be 1mm x 1mm size")
        if Decimal(thickness[1]) != Decimal("0.15"):
            errs.append("Font must be 0.15mm line thickness")


def checksilk(mod, errs):
    silk_types = ("fp_line", "fp_circle", "fp_arc", "fp_poly", "fp_curve")
    for silk in (node for node in mod if node[0] in silk_types):
        layer = [n for n in silk if n[0] == "layer"][0]
        width = [n for n in silk if n[0] == "width"][0]
        silk_layers = ("F.SilkS", "B.SilkS")
        if layer[1] in silk_layers:
            if Decimal(width[1]) != Decimal("0.15"):
                errs.append("Silk lines must be 0.15mm wide")


def checkctyd(mod, errs):
    found_ctyd = False
    for ctyd in (node for node in mod if node[0] == "fp_line"):
        layer = [n for n in ctyd if n[0] == "layer"][0]
        width = [n for n in ctyd if n[0] == "width"][0]
        start = [n for n in ctyd if n[0] == "start"][0]
        end = [n for n in ctyd if n[0] == "end"][0]
        ctyd_layers = ("F.CrtYd", "B.CrtYd")
        if layer[1] in ctyd_layers:
            found_ctyd = True
            if Decimal(width[1]) != Decimal("0.01"):
                errs.append("Courtyard lines must be 0.01mm wide")
            if (Decimal(start[1]) % Decimal("0.05") != 0
                    or Decimal(start[2]) % Decimal("0.05") != 0
                    or Decimal(end[1]) % Decimal("0.05") != 0
                    or Decimal(end[2]) % Decimal("0.05") != 0):
                errs.append("Courtyard lines must lie on a 0.05mm grid")
    if not found_ctyd:
        errs.append("No courtyard found")


def checkmod(path):
    errs = []

    with open(path) as f:
        mod = sexpparse(f.read())

    checkrefval(mod, errs)
    checkfont(mod, errs)
    checksilk(mod, errs)
    checkctyd(mod, errs)

    if len(errs) == 0:
        print("Checked '{}': OK".format(path))
        return True
    else:
        print("Checked '{}': Error:".format(path), file=sys.stderr)
        for err in errs:
            print("    " + err, file=sys.stderr)
        print("", file=sys.stderr)
        return False


def main(libpath):
    ok = True
    for f in glob.glob(os.path.join(libpath, "*.kicad_mod")):
        result = checkmod(f)
        if not result:
            ok = False
    return ok


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <.pretty path>".format(sys.argv[0]))
        sys.exit(1)
    else:
        libpath = sys.argv[1]
        success = main(libpath)
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
