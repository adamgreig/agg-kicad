"""
icmod.py
Copyright 2015 Adam Greig

Create a range of dual and quad SMD IC packages.

TODO:
    * Support exposed pads
        * Defined by width, height
        * Support multiple mask openings
        * Support multiple paste apertures
        * Support included vias
        * Needs external silk
    * Support non-square 4-row packages
    * Support other pad shapes, e.g. oval/half-oval
    * Support choosing internal or external silk
"""

# Package configuration =======================================================
# Dictionary of dictionaries.
# Top keys are package names, in the following format:
#   FAMILY-PINS[-MOD][-EP][-SPECIAL]
# MOD might be "W" for wide.
# SPECIAL might refer to a manufacturer's specific modified footprint.
# Examples: SOIC-8, SOIC-16-W, QFN48-EP
#
# Unless otherwise noted, all pad dimensions are as per IPC-7351B nominal,
# while fab layer annotatons are as per IPC-7351B package maximums.
#
# Valid inner keys are:
#   rows: either 2 or 4, for dual or quad packages
#   pins: total number of pins
#   pin_pitch: spacing between adjacent pins
#   row_pitch: spacing between rows of pins
#   pad_shape: (width, height) of a pad for a pin
#   pin_shape: (width, height) of the chip package pins (for Fab layer)
#   chip_shape: (width, height) of the actual chip package (for Fab layer)
#
# All lengths are in millimetres.

config = {

    # SOIC-8 from JEDEC MS-012AA
    # IPC-7351B: SOIC127P600X175-8N
    "SOIC-8": {
        "rows": 2,
        "pins": 8,
        "pin_pitch": 1.27,
        "row_pitch": 5.4,
        "pad_shape": (1.55, 0.6),
        "chip_shape": (4.0, 5.0),
        "pin_shape": (1.1, 0.5),
    },

    # SOIC-16 from JEDEC MS-012AC
    # IPC-7351B: SOIC127P600X175-16N
    "SOIC-16": {
        "rows": 2,
        "pins": 16,
        "pin_pitch": 1.27,
        "row_pitch": 5.4,
        "pad_shape": (1.55, 0.6),
        "chip_shape": (4.0, 10.0),
        "pin_shape": (1.1, 0.5),
    },

    # SOIC-16-W from JEDEC MS-013AA
    # IPC-7351B: SOIC127P1030X265-16N
    "SOIC-16-W": {
        "rows": 2,
        "pins": 16,
        "pin_pitch": 1.27,
        "row_pitch": 9.3,
        "pad_shape": (2.0, 0.6),
        "chip_shape": (7.6, 10.5),
        "pin_shape": (1.5, 0.5),
    },

    # MSOP-8 from JEDEC MO-187AA
    # IPC-7351B: SOP65P490X110-8N
    "MSOP-8": {
        "rows": 2,
        "pins": 8,
        "pin_pitch": 0.65,
        "row_pitch": 4.4,
        "pad_shape": (1.45, 0.45),
        "chip_shape": (3.1, 3.1),
        "pin_shape": (1.0, 0.38),
    },

    # LQFP-48 from JEDEC MS-026BBC
    # IPC-7351B: QFP50P900X900X160-48N
    "LQFP-48": {
        "rows": 4,
        "pins": 48,
        "pin_pitch": 0.5,
        "row_pitch": 8.4,
        "pad_shape": (1.5, 0.3),
        "chip_shape": (7.2, 7.2),
        "pin_shape": (1.0, 0.27),
    },

    # LQFP-64 from JEDEC MS-026BCD
    # IPC-7351B: QFP50P1200X1200X160-64N
    "LQFP-64": {
        "rows": 4,
        "pins": 64,
        "pin_pitch": 0.5,
        "row_pitch": 11.4,
        "pad_shape": (1.5, 0.3),
        "chip_shape": (10.2, 10.2),
        "pin_shape": (1.0, 0.27),
    },

    # LQFP-100 from JEDEC MS-026BED
    # IPC-7351B: QFP50P1600X1600X160-100N
    "LQFP-100": {
        "rows": 4,
        "pins": 100,
        "pin_pitch": 0.5,
        "row_pitch": 15.4,
        "pad_shape": (1.5, 0.3),
        "chip_shape": (14.2, 14.2),
        "pin_shape": (1.0, 0.27),
    },
}


# Other constants =============================================================

# Courtyard clearance
# Use 0.25 for IPC nominal and 0.10 for IPC least.
ctyd_gap = 0.25

# Courtyard grid
ctyd_grid = 0.05

# Courtyard line width
ctyd_width = 0.01

# Silk clearance from pads
silk_pad_gap = 0.5

# Silk line width
silk_width = 0.15

# Silk pin1 arc radius
silk_pin1_r = 0.6

# Fab layer line width
fab_width = 0.01

# Fab layer pin1 circle radius
fab_pin1_r = 0.4

# Fab layer pin1 corner offset
fab_pin1_offset = 0.8

# Ref/Val font size (width x height)
font_size = (1.0, 1.0)

# Ref/Val font thickness
font_thickness = 0.15

# Ref/Val font spacing from centre to top/bottom edge
font_halfheight = 0.7

# End Constants ===============================================================

import os
import re
import sys
import time
import subprocess


def sexp_generate(sexp, depth=0):
    """Turn a list of lists into an s-expression."""
    single_word = re.compile("^-?[a-zA-Z0-9_*\.]*$")
    parts = []
    for node in sexp:
        if isinstance(node, str) and not single_word.match(node):
            node.replace("\"", "\\\"")
            node.replace("\n", "\\n")
            node = "\"{}\"".format(node)
        if isinstance(node, int):
            node = str(node)
        if isinstance(node, float):
            node = "{:.4f}".format(node)
        if isinstance(node, (list, tuple)):
            node = sexp_generate(node, depth+1)
        parts.append(node)
    return "\n{}({})".format(" "*depth*2, " ".join(parts))


def fp_line(start, end, layer, width):
    return ["fp_line",
            ["start", start[0], start[1]],
            ["end", end[0], end[1]],
            ["layer", layer],
            ["width", width]]


def fp_arc(start, end, angle, layer, width):
    return ["fp_arc",
            ["start", start[0], start[1]],
            ["end", end[0], end[1]],
            ["angle", angle],
            ["layer", layer],
            ["width", width]]


def fp_circle(centre, end, layer, width):
    return ["fp_circle",
            ["center", centre[0], centre[1]],
            ["end", end[0], end[1]],
            ["layer", layer],
            ["width", width]]


def fp_text(texttype, text, at, layer, size, thickness):
    return ["fp_text", texttype, text,
            ["at", at[0], at[1]],
            ["layer", layer],
            ["effects",
             ["font",
              ["size", size[0], size[1]],
              ["thickness", thickness]]]]


def pad(num, padtype, shape, at, size, layers):
    return ["pad", num, padtype, shape,
            ["at", at[0], at[1]],
            ["size", size[0], size[1]],
            ["layers"] + layers]


def draw_square(width, height, centre, layer, thickness):
    """Draw a square of (`width`, `height`) centered on `centre`."""
    out = []
    ne = (width/2 + centre[0], -height/2 + centre[1])
    nw = (-width/2 + centre[0], -height/2 + centre[1])
    se = (width/2 + centre[0], height/2 + centre[1])
    sw = (-width/2 + centre[0], height/2 + centre[1])
    out.append(fp_line(nw, ne, layer, thickness))
    out.append(fp_line(ne, se, layer, thickness))
    out.append(fp_line(se, sw, layer, thickness))
    out.append(fp_line(sw, nw, layer, thickness))
    return nw, ne, se, sw, out


def pin_centres(conf):
    """
    Compute the locations of pin centres, (x, y).
    Generates centres for a 4-row chip, just ignore top/bottom rows if 2 rows.
    Returns (leftrow, bottomrow, rightrow, toprow).
    """
    pins_per_row = conf['pins'] // conf['rows']
    row_length = (pins_per_row - 1) * conf['pin_pitch']

    left_row = []
    bottom_row = []
    right_row = []
    top_row = []

    x = conf['row_pitch'] / 2.0
    y = -row_length / 2.0
    for pin in range(pins_per_row):
        left_row.append((-x, y))
        right_row.insert(0, (x, y))
        top_row.insert(0, (y, -x))
        bottom_row.append((y, x))
        y += conf['pin_pitch']

    return left_row, bottom_row, right_row, top_row


def refs(conf):
    out = []

    if conf['rows'] == 2:
        ctyd_h = conf['chip_shape'][1] + 2 * ctyd_gap
    elif conf['rows'] == 4:
        ctyd_h = conf['row_pitch'] + conf['pad_shape'][0] + 2 * ctyd_gap

    y = ctyd_h/2.0 + font_halfheight

    out.append(fp_text("reference", "REF**", (0, -y),
               "F.Fab", font_size, font_thickness))
    out.append(fp_text("value", conf['name'], (0, y),
               "F.Fab", font_size, font_thickness))

    return out


def fab(conf):
    """
    Generate a drawing of the chip on the Fab layer, including its outline,
    the outline of the pins, and a pin 1 indicator.
    """
    chip_w, chip_h = conf['chip_shape']
    pin_w, pin_h = conf['pin_shape']
    out = []

    # Chip outline
    nw, _, _, _, sq = draw_square(chip_w, chip_h, (0, 0), "F.Fab", fab_width)
    out += sq

    # Pin 1
    centre = (nw[0] + fab_pin1_offset, nw[1] + fab_pin1_offset)
    end = (centre[0], centre[1] + fab_pin1_r)
    out.append(fp_circle(centre, end, "F.Fab", fab_width))

    # Pins
    leftr, bottomr, rightr, topr = pin_centres(conf)
    for pin in leftr:
        xy = -(chip_w + pin_w) / 2.0, pin[1]
        _, _, _, _, sq = draw_square(pin_w, pin_h, xy, "F.Fab", fab_width)
        out += [sq[0], sq[2], sq[3]]
    for pin in rightr:
        xy = (chip_w + pin_w) / 2.0, pin[1]
        _, _, _, _, sq = draw_square(pin_w, pin_h, xy, "F.Fab", fab_width)
        out += [sq[0], sq[1], sq[2]]
    if conf['rows'] == 4:
        for pin in topr:
            xy = pin[0], -(chip_h + pin_w) / 2.0
            _, _, _, _, sq = draw_square(pin_h, pin_w, xy, "F.Fab", fab_width)
            out += [sq[0], sq[1], sq[3]]
        for pin in bottomr:
            xy = pin[0], (chip_h + pin_w) / 2.0
            _, _, _, _, sq = draw_square(pin_h, pin_w, xy, "F.Fab", fab_width)
            out += [sq[1], sq[2], sq[3]]

    return out


def innersilk(conf):
    """
    Generate an internal silkscreen, with an outline of the part and a pin1
    indicator.
    """
    out = []

    pins = conf['pins']
    rows = conf['rows']
    pin_pitch = conf['pin_pitch']
    row_pitch = conf['row_pitch']
    pad_shape = conf['pad_shape']

    width = row_pitch - pad_shape[0] - 2 * silk_pad_gap
    if rows == 2:
        height = (((pins / rows) - 1) * pin_pitch)
    elif rows == 4:
        height = width

    nw, _, _, _, sq = draw_square(width, height, (0, 0), "F.SilkS", silk_width)
    out += sq

    start = nw
    end = (start[0] + silk_pin1_r, start[1])
    out.append(fp_arc(start, end, 90, "F.SilkS", silk_width))

    return out


def ctyd(conf):
    row_pitch = conf['row_pitch']
    pad_w, pad_h = conf['pad_shape']
    chip_w, chip_h = conf['chip_shape']

    width = row_pitch + pad_w + 2 * ctyd_gap
    if conf['rows'] == 2:
        height = chip_h + 2 * ctyd_gap
    elif conf['rows'] == 4:
        height = width

    # Ensure courtyard lies on a specified grid
    # (double the grid since we halve the width/height)
    width_um = int(width * 1000)
    height_um = int(height * 1000)
    grid_um = int(ctyd_grid * 2 * 1000)

    width_um += width_um % grid_um
    height_um += height_um % grid_um

    width = width_um / 1000.0
    height = height_um / 1000.0

    _, _, _, _, sq = draw_square(width, height, (0, 0), "F.CrtYd", ctyd_width)
    return sq


def pads(conf):
    out = []
    layers = ["F.Cu", "F.Paste", "F.Mask"]
    size_lr = conf['pad_shape']
    size_tb = size_lr[1], size_lr[0]
    padtype = "smd"
    shape = "rect"
    leftr, bottomr, rightr, topr = pin_centres(conf)
    num = 1
    for pin in leftr:
        out.append(pad(num, padtype, shape, pin, size_lr, layers))
        num += 1
    if conf['rows'] == 4:
        for pin in bottomr:
            out.append(pad(num, padtype, shape, pin, size_tb, layers))
            num += 1
    for pin in rightr:
        out.append(pad(num, padtype, shape, pin, size_lr, layers))
        num += 1
    if conf['rows'] == 4:
        for pin in topr:
            out.append(pad(num, padtype, shape, pin, size_tb, layers))
            num += 1
    return out


def footprint(conf):
    tedit = format(int(time.time()), 'X')
    sexp = ["module", conf['name'], ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += refs(conf)
    sexp += fab(conf)
    sexp += innersilk(conf)
    sexp += ctyd(conf)
    sexp += pads(conf)
    return sexp_generate(sexp)


def git_version(libpath):
    args = ["git", "describe", "--abbrev=8", "--dirty=-dirty", "--always"]
    git = subprocess.Popen(args, cwd=libpath, stdout=subprocess.PIPE)
    return git.stdout.read().decode().strip()


def main(prettypath):
    # TODO imbed version and timestamp somehow
    # version = git_version(prettypath)
    for name, conf in config.items():
        conf['name'] = name
        assert conf['rows'] in (2, 4), \
            "Must have either two or four rows"
        assert conf['pins'] % conf['rows'] == 0, \
            "Pins must equally divide among rows"
        fp = footprint(conf)
        with open(os.path.join(prettypath, name+".kicad_mod"), "w") as f:
            f.write(fp)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <.pretty path>".format(sys.argv[0]))
        sys.exit(1)
    else:
        prettypath = sys.argv[1]
        main(prettypath)
