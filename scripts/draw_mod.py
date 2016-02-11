"""
draw_mod.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Render a .kicad_mod file to a PNG.
"""

from __future__ import print_function, division

import sys
import math
import cairo

from sexp import parse as sexp_parse

# Settings ====================================================================

# Gap between courtyard and image edge, in fraction of axis length
border_ratio = 0.02

# Image size in pixels
image_size = 512

# Background colour
bg_colour = (1, 1, 1, 1)

# Drill/hole colour
drill_colour = (0, 1, 1, .7)

# Colour mapping
colours = {
    "F.CrtYd": (0, 0, 0, 1),
    "F.SilkS": (1, 0, 1, 0.8),
    "F.Fab": (0, 0, 1, 0.8),
    "F.Cu": (1, 0, 0, 1),
    "F.Mask": (0.5, 0, 1, 0.6),
    "F.Paste": (0.6, 0.6, 0.6, 1),
}

# Layer stack (bottom first)
layer_stack = [
    "F.Cu", "F.Mask", "F.Paste", "F.SilkS", "F.Fab", "F.CrtYd", "Drill"]

# End Settings ================================================================


def find_size(mod):
    """
    Use the courtyard and a little padding to determine the footprint extent.
    """
    left = right = top = bottom = 0

    for line in (n for n in mod if n[0] == "fp_line"):
        layer = [n for n in line if n[0] == "layer"][0]
        if layer[1] in ("F.CrtYd", "B.CrtYd"):
            start = [n for n in line if n[0] == "start"][0]
            end = [n for n in line if n[0] == "end"][0]
            for x, y in (start[1:], end[1:]):
                x = float(x)
                y = float(y)
                left = min(x, left)
                right = max(x, right)
                top = min(y, top)
                bottom = max(y, bottom)

    width = right - left
    height = bottom - top

    left -= width * border_ratio
    right += width * border_ratio
    top -= height * border_ratio
    bottom += height * border_ratio

    return left, right, top, bottom


def draw_line(ctxs, draw):
    layer = [n for n in draw if n[0] == "layer"][0][1]
    if layer in ctxs:
        ctx = ctxs[layer]
        rgba = colours[layer]
        width = [n for n in draw if n[0] == "width"][0][1]
        ctx.set_source_rgba(*rgba)
        ctx.set_line_width(float(width))
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        if draw[0] == "fp_line":
            start = [n for n in draw if n[0] == "start"][0]
            end = [n for n in draw if n[0] == "end"][0]
            ctx.move_to(float(start[1]), float(start[2]))
            ctx.line_to(float(end[1]), float(end[2]))
        elif draw[0] == "fp_circle":
            center = [n for n in draw if n[0] == "center"][0]
            end = [n for n in draw if n[0] == "end"][0]
            dx = float(end[1]) - float(center[1])
            dy = float(end[2]) - float(center[2])
            r = math.sqrt(dx**2 + dy**2)
            ctx.new_sub_path()
            ctx.arc(float(center[1]), float(center[2]), r, 0, 2*math.pi)
        elif draw[0] == "fp_arc":
            start = [n for n in draw if n[0] == "start"][0]
            end = [n for n in draw if n[0] == "end"][0]
            angle = [n for n in draw if n[0] == "angle"][0]
            dx = float(end[1]) - float(start[1])
            dy = float(end[2]) - float(start[2])
            r = math.sqrt(dx**2 + dy**2)
            a_start = math.atan2(dy, dx)
            a_end = a_start + float(angle[1]) * (math.pi / 180.0)
            ctx.new_sub_path()
            ctx.arc(float(start[1]), float(start[2]), r, a_start, a_end)
        ctx.stroke()


def hatch(positive, rgba):
    hs = 64
    hatch = cairo.ImageSurface(cairo.FORMAT_ARGB32, hs, hs)
    hctx = cairo.Context(hatch)
    if positive:
        hctx.move_to(0, 0)
        hctx.line_to(hs, hs)
    else:
        hctx.move_to(0, hs)
        hctx.line_to(hs, 0)
    hctx.set_line_width(16)
    hctx.set_source_rgba(*rgba)
    hctx.stroke()
    hpat = cairo.SurfacePattern(hatch)
    hpat.set_extend(cairo.EXTEND_REPEAT)
    hpat.set_matrix(cairo.Matrix(xx=image_size, yy=image_size))
    return hpat


hatch_mask = hatch(True, colours["F.Mask"])
hatch_paste = hatch(False, colours["F.Paste"])


def pad_all_layers_front(layers):
    for idx, layer in enumerate(layers):
        if layer[0] == "*":
            layers[idx] = "F" + layer[1:]


def pad_drill(drill, centre, ctx):
    try:
        drill_size = float(drill[0][1])
    except ValueError:
        pass
    else:
        ctx.arc(centre[0], centre[1], drill_size/2.0, 0, 2*math.pi)
        ctx.set_source_rgba(*drill_colour)
        ctx.fill()
    offset = [n for n in drill[0] if n[0] == "offset"]
    if offset:
        centre[0] += float(offset[0][1])
        centre[1] += float(offset[0][2])


def pad_margins(pad):
    mask_margin = [n for n in pad if n[0] == "solder_mask_margin"]
    paste_margin = [n for n in pad if n[0] == "solder_paste_margin"]
    paste_ratio = [n for n in pad if n[0] == "solder_paste_ratio"]
    mask_margin = float(mask_margin[0][1]) if mask_margin else 0
    paste_margin = float(paste_margin[0][1]) if paste_margin else 0
    paste_ratio = float(paste_ratio[0][1]) if paste_ratio else 0
    return mask_margin, paste_margin, paste_ratio


def draw_pad(ctxs, pad):
    shape = pad[3]
    layers = [n for n in pad if n[0] == "layers"][0][1:]
    pad_all_layers_front(layers)
    centre = [float(v) for v in [n for n in pad if n[0] == "at"][0][1:]]
    size = [float(v) for v in [n for n in pad if n[0] == "size"][0][1:]]

    drill = [n for n in pad if n[0] == "drill"]
    if drill:
        pad_drill(drill, centre, ctxs['Drill'])
    mask_margin, paste_margin, paste_ratio = pad_margins(pad)

    for layer in ["F.Cu", "F.Mask", "F.Paste"]:
        if layer in layers and layer in ctxs:
            ctx = ctxs[layer]
            rgba = colours[layer]
            if layer.endswith("Mask"):
                size[0] += 2*mask_margin
                size[1] += 2*mask_margin
                ctx.set_source(hatch_mask)
            elif layer.endswith("Paste"):
                size[0] += 2*paste_margin
                size[1] += 2*paste_margin
                size[0] += 2*paste_ratio*size[0]
                size[1] += 2*paste_ratio*size[1]
                ctx.set_source(hatch_paste)
            elif layer.endswith("Cu"):
                ctx.set_source_rgba(*rgba)

            if shape == "rect":
                x = centre[0] - size[0]/2.0
                y = centre[1] - size[1]/2.0
                ctx.rectangle(x, y, size[0], size[1])
            elif shape == "circle":
                ctx.arc(centre[0], centre[1], size[0]/2.0, 0, 2*math.pi)
            else:
                return

            ctx.fill()


def draw(mod):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, image_size, image_size)
    ctx = cairo.Context(surf)
    ctx.set_source_rgba(*bg_colour)
    ctx.paint()

    # Set up the context to map footprint coordinates to image coordinates
    # Footprint is in mm, with the origin at the centre, x increasing right,
    # and y increasing down.
    # Image is in pixels, with the origin at the top left, x increasing right,
    # and y increasing down.
    left, right, top, bottom = find_size(mod)
    length = float(max(right - left, bottom - top))

    ctxs = {}
    for layer in layer_stack:
        lsurf = cairo.ImageSurface(cairo.FORMAT_ARGB32, image_size, image_size)
        lctx = cairo.Context(lsurf)
        lctx.scale(image_size/length, image_size/length)
        lctx.translate(right, bottom)
        ctxs[layer] = lctx

    for pad in (n for n in mod if n[0] == "pad"):
        draw_pad(ctxs, pad)

    draw_types = ("fp_line", "fp_circle", "fp_arc")
    for draw in (n for n in mod if n[0] in draw_types):
        draw_line(ctxs, draw)

    for layer in layer_stack:
        lctx = ctxs[layer]
        ctx.set_source_surface(lctx.get_target())
        ctx.paint()

    return surf


def main(modpath, outpath):
    with open(modpath) as f:
        sexp = sexp_parse(f.read())
    img = draw(sexp)
    img.write_to_png(outpath)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        modpath = sys.argv[1]
        outpath = sys.argv[2]
        main(modpath, outpath)
    else:
        print("Usage: {} <.kicad_mod file> <output file>".format(sys.argv[0]))
        sys.exit(0)
