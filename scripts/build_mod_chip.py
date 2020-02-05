"""
build_mod_chip.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Create two-terminal chip packages.
"""
from __future__ import print_function, division

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
import yaml
import fnmatch

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


def load_items(modpath):
    config = {}
    for dirpath, dirnames, files in os.walk(modpath):
        dirnames.sort()
        files.sort()
        for fn in fnmatch.filter(files, "*.yaml"):
            path = os.path.join(dirpath, fn)
            with open(path) as f:
                item = yaml.safe_load(f)
                item["path"] = dirpath
                config[item["name"]] = item
    return config


def main(prettypath, modpath, verify=False, verbose=False):
    config = load_items(modpath)
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
    parser.add_argument("modpath", type=str, help=
                        "Path to .yaml files defining footprints")
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
