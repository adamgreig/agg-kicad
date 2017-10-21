"""
check_mod.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Check all footprint files in a directory against a set of consistency fules.
"""

from __future__ import print_function, division

import sys
import os
import glob
from decimal import Decimal
import argparse

from sexp import parse as sexp_parse


def checkrefval(mod, errs):
    for fp_text in (node for node in mod if node[0] == "fp_text"):
        if fp_text[1] not in ("reference", "value"):
            continue
        layer = [n for n in fp_text if n[0] == "layer"][0]
        if layer[1] != "F.Fab":
            errs.append("Value and Reference fields must be on F.Fab")
        if fp_text[1] == "reference" and fp_text[2] != "REF**":
            errs.append("Reference field must contain REF**")
        if fp_text[1] == "value" and not mod[1].startswith(fp_text[2]):
            errs.append("Value field must contain module name")


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


def checklines(mod, errs, check_layers, check_width):
    line_types = ("fp_line", "fp_circle", "fp_arc", "fp_poly", "fp_curve")
    for line in (node for node in mod if node[0] in line_types):
        layer = [n for n in line if n[0] == "layer"][0]
        width = [n for n in line if n[0] == "width"][0]
        if layer[1] in check_layers:
            if Decimal(width[1]) != Decimal(check_width):
                errs.append("Lines on {} must be {}mm wide"
                            .format(check_layers, check_width))


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


def checkmod(path, verbose=False):
    errs = []

    with open(path) as f:
        mod = sexp_parse(f.read())

    checkrefval(mod, errs)
    checkfont(mod, errs)
    checklines(mod, errs, ("F.SilkS", "B.SilkS"), "0.15")
    checklines(mod, errs, ("F.Fab", "B.Fab"), "0.01")
    checkctyd(mod, errs)

    if len(errs) == 0:
        if verbose:
            print("Checked '{}': OK".format(path))
        return True
    else:
        print("Checked '{}': Error:".format(path), file=sys.stderr)
        for err in errs:
            print("    " + err, file=sys.stderr)
        print("", file=sys.stderr)
        return False


def main(prettypath, verbose=False):
    ok = True
    for f in glob.glob(os.path.join(prettypath, "*.kicad_mod")):
        result = checkmod(f, verbose)
        if not result:
            ok = False
    return ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prettypath", type=str,
                        help="Path to footprints")
    parser.add_argument("--verbose", action="store_true",
                        help="Print out every footprint checked even if OK")
    args = vars(parser.parse_args())
    result = main(**args)
    sys.exit(0 if result else 1)
