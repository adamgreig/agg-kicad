"""
build_mod_ic.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Create DFN, DFP, QFN, QFP, and BGA footprints from descriptions.
"""

from __future__ import print_function, division

# Style constants =============================================================

# Courtyard clearance
# Use 0.25 for IPC nominal and 0.10 for IPC least.
ctyd_gap = 0.25

# Courtyard grid
ctyd_grid = 0.05

# Courtyard line width
ctyd_width = 0.01

# Internal silk clearance from pads
silk_pad_igap = 0.5

# External silk clearance from pads
silk_pad_egap = 0.4

# Silk line width
silk_width = 0.15

# Internal silk pin1 arc radius
silk_pin1_ir = 0.6

# External two-row silk pin1 arc radius
silk_pin1_er = 0.3

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
import math
import subprocess
import argparse
import yaml
import fnmatch

from sexp import parse as sexp_parse, generate as sexp_generate
from kicad_mod import fp_line, fp_arc, fp_circle, fp_text, pad, draw_square, model


def pin_centres(conf):
    """
    Compute the locations of pin centres, (x, y).
    Generates centres for a 4-row chip, just ignore top/bottom rows if 2 rows.
    Returns (leftrow, bottomrow, rightrow, toprow).
    """

    # Handle non-square chips differently
    if "pins_first_row" in conf:
        v_pins_per_row = conf['pins_first_row']
        h_pins_per_row = (conf['pins'] - 2*v_pins_per_row) // 2
        hx = conf['row_pitch'][0] / 2.0
        vx = conf['row_pitch'][1] / 2.0
    else:
        h_pins_per_row = v_pins_per_row = conf['pins'] // conf['rows']
        hx = vx = conf['row_pitch'] / 2.0
    h_row_length = (h_pins_per_row - 1) * conf['pin_pitch']
    v_row_length = (v_pins_per_row - 1) * conf['pin_pitch']

    left_row = []
    bottom_row = []
    right_row = []
    top_row = []

    y = -v_row_length / 2.0
    for pin in range(v_pins_per_row):
        left_row.append((-hx, y))
        right_row.insert(0, (hx, y))
        y += conf['pin_pitch']
    y = -h_row_length / 2.0
    for pin in range(h_pins_per_row):
        top_row.insert(0, (y, -vx))
        bottom_row.append((y, vx))
        y += conf['pin_pitch']

    return left_row, bottom_row, right_row, top_row


def expand_skips(conf, letters=None):
    """
    Computes list of all pins to skip given a list of specifiers which
    may be either specific pins or ranges of pins.

    Optional letters gives expanded list of BGA pin letters in use.

    Returned list always contains strings.
    """
    if letters is None:
        letters = []
    skips = conf.get("skip_pins", [])
    out = []
    for skip in skips:
        skip = str(skip)
        if "-" not in skip:
            out.append(skip)
            continue
        match = re.search(r"^([A-Z]+(?:-[A-Z]+)?)?([0-9]+(?:-[0-9]+)?)$", skip)
        if not match:
            raise ValueError("Unknown skip specifier {}".format(skip))
        let, num = match.groups()
        if "-" in num:
            num_start, num_stop = [int(x) for x in num.split("-")]
            nums = list(range(num_start, num_stop+1))
        else:
            nums = [num]
        if "-" in let:
            let_start, let_stop = let.split("-")
            let_start_idx = letters.index(let_start)
            let_stop_idx = letters.index(let_stop)
            lets = letters[let_start_idx:let_stop_idx+1]
        else:
            lets = [let]
        for let in lets:
            for num in nums:
                out.append(let + str(num))
    return out


def bga_pin_centres(conf):
    """
    Compute the location of pin centres for BGA parts,
    including skipping any in `skip_pins`.
    Rows are labelled with letters and columns with numbers.
    Returns a list of (pin number, x, y) positions.
    """
    default_letters = "ABCDEFGHJKLMNPRTUVWY"
    letters = conf.get("letters", default_letters)
    letters = list(letters) + [a+b for a in letters for b in letters]
    skips = expand_skips(conf, letters)
    pitch = float(conf["pin_pitch"])
    out = []
    rows = int(conf['rows'])
    cols = int(conf['cols'])
    for row in range(rows):
        for col in range(cols):
            rowid = letters[row]
            colid = col + 1
            padid = rowid + str(colid)
            if padid in skips:
                continue
            x = (col * pitch) - ((cols-1)/2.0 * pitch)
            y = (row * pitch) - ((rows-1)/2.0 * pitch)
            out.append((padid, x, y))
    return out


def inner_apertures(ep, apertures):
    """
    Compute the position of apertures inside a pad,
    with:
        ep: (width, height) of pad
        apertures: (width, height, w_gap, h_gap) of apertures
    w_gap is the spacing in the x-axis between apertures.

    Fits as many apertures inside the pad as possible.

    Returns a list of (x,y) aperture centres.
    """
    out = []
    ep_w, ep_h = ep
    a_w, a_h, a_wg, a_hg = apertures

    n_x = int((ep_w - a_w) // (a_w + a_wg)) + 1
    n_y = int((ep_h - a_h) // (a_h + a_hg)) + 1

    x = -((n_x - 1)*(a_w + a_wg)/2.0)

    for ix in range(n_x):
        y = -((n_y - 1)*(a_h + a_hg)/2.0)
        for iy in range(n_y):
            out.append((x, y))
            y += a_h + a_hg
        x += a_w + a_wg

    return out


def exposed_pad(conf):
    """
    Compute pads for an exposed pad, which might have separate mask and paste
    apertures.
    """
    out = []
    ep_shape = conf['ep_shape']
    ep_layers = ["F.Cu"]
    ep_m_mask = None
    ep_m_paste = None

    # Mask apertures
    if "ep_mask_shape" not in conf:
        ep_layers.append("F.Mask")
        ep_m_mask = 0.001
    else:
        mask_shape = conf['ep_mask_shape']
        apertures = inner_apertures(ep_shape, mask_shape)
        layers = ["F.Mask"]
        for ap in apertures:
            out.append(pad("", "smd", "rect", ap, mask_shape[:2], layers,
                           m_mask=.001))

    # Paste apertures
    if "ep_paste_shape" not in conf:
        ep_layers.append("F.Paste")
        ep_m_paste = 0.001
    else:
        paste_shape = conf['ep_paste_shape']
        apertures = inner_apertures(ep_shape, paste_shape)
        layers = ["F.Paste"]
        for ap in apertures:
            out.append(
                pad("", "smd", "rect", ap, paste_shape[:2], layers,
                    m_paste=.001))

    # Vias
    if "ep_vias" in conf:
        v_d, v_s, v_g = conf['ep_vias']
        centres = inner_apertures(ep_shape, (v_s, v_s, v_g, v_g))
        layers = ["*.Cu"]
        for c in centres:
            p = pad("EP", "thru_hole", "circle", c, (v_s, v_s), layers,
                    drill=v_d)
            p.append(("zone_connect", 2))
            out.append(p)

    out.append(
        pad("EP", "smd", "rect", (0, 0),
            ep_shape, ep_layers, m_mask=ep_m_mask, m_paste=ep_m_paste))
    return out


def refs(conf):
    """Generate val and ref labels."""
    out = []

    if conf['rows'] == 2 or 'cols' in conf:
        ctyd_h = conf['chip_shape'][1] + 2 * ctyd_gap
    elif conf['rows'] == 4:
        # Handle non-square chips differently
        if isinstance(conf['row_pitch'], float):
            ctyd_h = conf['row_pitch'] + conf['pad_shape'][0] + 2 * ctyd_gap
        else:
            ctyd_h = conf['row_pitch'][1] + conf['pad_shape'][0] + 2 * ctyd_gap

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
    if 'rows' in conf and 'cols' in conf:
        bga = True
    else:
        bga = False

    chip_w, chip_h = conf['chip_shape']
    if bga:
        pin_r = conf['pin_shape']
    else:
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
    if bga:
        centres = bga_pin_centres(conf)
        for _, x, y in centres:
            out += [fp_circle((x, y), (x, y+pin_r//2), "F.Fab", fab_width)]
    else:
        leftr, bottomr, rightr, topr = pin_centres(conf)
        skips = [int(x) for x in expand_skips(conf)]
        idx = 1
        for pin in leftr:
            idx += 1
            if idx - 1 in skips:
                continue
            xy = -(chip_w + pin_w) / 2.0, pin[1]
            _, _, _, _, sq = draw_square(pin_w, pin_h, xy, "F.Fab", fab_width)
            out += [sq[0], sq[2], sq[3]]
        for pin in rightr:
            idx += 1
            if idx - 1 in skips:
                continue
            xy = (chip_w + pin_w) / 2.0, pin[1]
            _, _, _, _, sq = draw_square(pin_w, pin_h, xy, "F.Fab", fab_width)
            out += [sq[0], sq[1], sq[2]]
        if conf['rows'] == 4:
            for pin in topr:
                idx += 1
                if idx - 1 in skips:
                    continue
                xy = pin[0], -(chip_h + pin_w) / 2.0
                _, _, _, _, sq = draw_square(pin_h, pin_w, xy, "F.Fab", fab_width)
                out += [sq[0], sq[1], sq[3]]
            for pin in bottomr:
                idx += 1
                if idx - 1 in skips:
                    continue
                xy = pin[0], (chip_h + pin_w) / 2.0
                _, _, _, _, sq = draw_square(pin_h, pin_w, xy, "F.Fab", fab_width)
                out += [sq[1], sq[2], sq[3]]

    return out


def internal_silk(conf):
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

    width = row_pitch - pad_shape[0] - 2 * silk_pad_igap
    if rows == 2:
        height = (((pins // rows) - 1) * pin_pitch)
    elif rows == 4:
        height = width

    ir = silk_pin1_ir
    if ir > width:
        ir = width

    c = (0, 0)
    layer = "F.SilkS"
    nw, ne, se, sw, sq = draw_square(width, height, c, layer, silk_width)
    out.append(fp_line((nw[0] + ir, nw[1]), ne, layer, silk_width))
    out.append(fp_line(ne, se, layer, silk_width))
    out.append(fp_line(se, sw, layer, silk_width))
    out.append(fp_line(sw, (nw[0], nw[1] + ir), layer, silk_width))
    start = (nw[0], nw[1] + ir)
    end = (nw[0] + ir, nw[1])
    out.append(fp_line(start, end, "F.SilkS", silk_width))

    # Old circular pin1 indicator:
    # out += sq
    # start = nw
    # end = (start[0] + silk_pin1_ir, start[1])
    # out.append(fp_arc(start, end, 90, "F.SilkS", silk_width))

    return out


def external_silk(conf):
    """
    Generate an external silkscreen.
    For two row devices: Horizontal lines top and bottom, semicircle pin 1
    For four row devices: Three sharp corners and a cut corner for pin 1
    """
    out = []

    rows = conf['rows']
    chip_shape = conf['chip_shape']
    w = silk_width
    l = "F.SilkS"
    x = chip_shape[0]/2.0
    y = chip_shape[1]/2.0
    bga = 'cols' in conf

    if rows == 2 and not bga:
        r = silk_pin1_er
        out.append(fp_line((-x+2*r, -y), (x, -y), l, w))
        out.append(fp_line((-x, y), (x, y), l, w))
        out.append(fp_arc((-x+r, -y), (-x, -y), 180, l, w))
    elif rows == 4 or bga:
        if bga:
            dx = x//2
            dy = y//2
        else:
            if 'pins_first_row' in conf:
                v_pins_per_row = conf['pins_first_row']
                h_pins_per_row = (conf['pins'] - 2*v_pins_per_row) // 2
                pin_x = ((h_pins_per_row - 1) * conf['pin_pitch']) / 2.0
                pin_y = ((v_pins_per_row - 1) * conf['pin_pitch']) / 2.0
            else:
                pins_per_row = conf['pins'] // rows
                pin_x = pin_y = ((pins_per_row - 1) * conf['pin_pitch']) / 2.0
            dx = x - pin_x - silk_pad_egap
            dy = y - pin_y - silk_pad_egap

        # NW
        if bga:
            dp1 = 1.0
            out.append(fp_line((-x, -y+dy), (-x, -y+dp1), l, w))
            out.append(fp_line((-x, -y+dp1), (-x+dp1, -y), l, w))
            out.append(fp_line((-x+dx, -y), (-x+dp1, -y), l, w))
        else:
            dp1 = min(dx, dy)
            out.append(fp_line((-x, -y+dp1), (-x+dp1, -y), l, w))
        # NE
        out.append(fp_line((x-dx, -y), (x, -y), l, w))
        out.append(fp_line((x, -y), (x, -y+dy), l, w))
        # SE
        out.append(fp_line((x-dx, y), (x, y), l, w))
        out.append(fp_line((x, y), (x, y-dy), l, w))
        # SW
        out.append(fp_line((-x+dx, y), (-x, y), l, w))
        out.append(fp_line((-x, y), (-x, y-dy), l, w))

    return out


def silk(conf):
    if 'ep_shape' in conf or 'cols' in conf:
        default = 'external'
    else:
        default = 'internal'
    silk = conf.get('silk', default)
    if silk == 'external':
        return external_silk(conf)
    elif silk == 'internal':
        return internal_silk(conf)
    else:
        return []


def ctyd(conf):
    chip_w, chip_h = conf['chip_shape']

    if 'cols' in conf:
        width, height = chip_w + 2*ctyd_gap, chip_h + 2*ctyd_gap
    elif conf['rows'] == 2:
        pad_w, pad_h = conf['pad_shape']
        row_pitch = conf['row_pitch']
        width = row_pitch + pad_w + 2 * ctyd_gap
        height = chip_h + 2 * ctyd_gap
    elif conf['rows'] == 4:
        pad_w, pad_h = conf['pad_shape']
        row_pitch = conf['row_pitch']
        # We need to handle non-square chips slightly differently,
        # depending on whether row_pitch is given as (w, h) or just a scalar.
        if isinstance(row_pitch, float):
            height = width = row_pitch + pad_w + 2 * ctyd_gap
        else:
            width = row_pitch[0] + pad_w + 2 * ctyd_gap
            height = row_pitch[1] + pad_w + 2 * ctyd_gap

    # Ensure courtyard lies on a specified grid
    # (double the grid since we halve the width/height)
    grid = 2*ctyd_grid
    width = grid * int(math.ceil(width / (2*ctyd_grid)))
    height = grid * int(math.ceil(height / (2*ctyd_grid)))

    _, _, _, _, sq = draw_square(width, height, (0, 0), "F.CrtYd", ctyd_width)
    return sq


def pad_row(centres, num, idx, shape, size, layers, skip):
    out = []
    for centre in centres:
        idx += 1
        if idx - 1 in skip:
            continue
        out.append(pad(num, "smd", shape, centre, size, layers))
        num += 1
    return num, idx, out


def pads(conf):
    out = []
    layers = ["F.Cu", "F.Mask", "F.Paste"]
    size_lr = conf['pad_shape']
    size_tb = size_lr[1], size_lr[0]
    shape = "rect"
    skip = conf.get('skip_pins', [])
    leftr, btmr, rightr, topr = pin_centres(conf)
    num = 1
    idx = 1

    num, idx, pins = pad_row(leftr, num, idx, shape, size_lr, layers, skip)
    out += pins

    if conf['rows'] == 4:
        num, idx, pins = pad_row(btmr, num, idx, shape, size_tb, layers, skip)
        out += pins

    num, idx, pins = pad_row(rightr, num, idx, shape, size_lr, layers, skip)
    out += pins

    if conf['rows'] == 4:
        num, idx, pins = pad_row(topr, num, idx, shape, size_tb, layers, skip)
        out += pins

    # Exposed pad (potentially with separate mask/paste apertures)
    if "ep_shape" in conf:
        out += exposed_pad(conf)

    return out


def bga_pads(conf):
    out = []
    layers = ["F.Cu", "F.Mask", "F.Paste"]
    size = [conf['pad_shape']]*2
    margin = (conf['mask_shape'] - conf['pad_shape']) / 2.0
    for num, x, y in bga_pin_centres(conf):
        p = pad(num, "smd", "circle", (x, y), size, layers)
        p.append(["solder_mask_margin", margin])
        out.append(p)
    return out


def _3d(conf):
    if "model" in conf:
        return [model(**conf["model"])]
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


def bga_footprint(conf):
    tedit = format(int(time.time()), 'X')
    sexp = ["module", conf['name'], ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += refs(conf)
    sexp += fab(conf)
    sexp += silk(conf)
    sexp += ctyd(conf)
    sexp += bga_pads(conf)
    sexp += _3d(conf)
    return sexp_generate(sexp)


def git_version(libpath):
    args = ["git", "describe", "--abbrev=8", "--dirty=-dirty", "--always"]
    git = subprocess.Popen(args, cwd=libpath, stdout=subprocess.PIPE)
    return git.stdout.read().decode().strip()


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
        conf['name'] = name
        if 'rows' in conf and 'pins' in conf:
            assert conf['rows'] in (2, 4), \
                "Must have either two or four rows"
            assert conf['pins'] % conf['rows'] == 0, \
                "Pins must equally divide among rows"
            fp = footprint(conf)
        elif 'rows' in conf and 'cols' in conf:
            fp = bga_footprint(conf)
        else:
            raise ValueError("Must specify either rows+pins or rows+cols")
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
