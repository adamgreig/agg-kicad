"""
kicad_mod.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Helper functions for generating KiCAD footprint files.
"""

from __future__ import print_function, division

CTYD_GAP = 0.25
CTYD_GRID = 0.05
CTYD_WIDTH = 0.01
SILK_WIDTH = 0.15
FAB_WIDTH = 0.01
FONT_SIZE = (1.0, 1.0)
FONT_THICKNESS = 0.15
FONT_HALFHEIGHT = 0.7


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
            ["at"] + list(at),
            ["layer", layer],
            ["effects",
             ["font",
              ["size", size[0], size[1]],
              ["thickness", thickness]]]]


def pad(num, padtype, shape, at, size, layers, drill=None, offset=None,
        m_mask=None, m_paste=None):
    pad = ["pad", num, padtype, shape,
           ["at", at[0], at[1]],
           ["size"] + list(size),
           ["layers"] + list(layers)]
    if drill is not None or offset is not None:
        d = ["drill"]
        if drill is not None:
            if isinstance(drill, (float, int)):
                d.append(drill)
            else:
                d += drill
        if offset is not None:
            d.append(["offset"] + offset)
        pad.append(d)
    if m_mask is not None:
        pad.append(["solder_mask_margin", m_mask])
    if m_paste is not None:
        pad.append(["solder_paste_margin", m_paste])
    return pad


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


def model(path, offset=None, scale=None, rotate=None):
    if offset is None:
        offset = [0, 0, 0]
    if scale is None:
        scale = [1.0, 1.0, 1.0]
    if rotate is None:
        rotate = [0, 0, 0]
    return ["model", path,
            ["at", ["xyz", offset[0], offset[1], offset[2]]],
            ["scale", ["xyz", scale[0], scale[1], scale[2]]],
            ["rotate", ["xyz", rotate[0], rotate[1], rotate[2]]]]
