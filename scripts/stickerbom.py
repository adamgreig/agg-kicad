"""
stickerbom.py
Copyright 2015 Adam Greig
"""

from __future__ import print_function, division

import sys
import math
import svgwrite
from xml.etree import ElementTree

from sexp import sexp_parse


def find_bounds(board):
    for node in board:
        if node[0] == "general":
            for child in node:
                if child[0] == "area":
                    return [float(x) for x in child[1:]]


def draw_board(inpath, outpath):
    with open(inpath) as f:
        board = sexp_parse(f.read())
    dwg = svgwrite.Drawing(outpath, profile='tiny')

    x1, y1, x2, y2 = find_bounds(board)
    dwg.viewbox(x1, y1, x2-x1, y2-y1)

    parts = {}
    highlights = {}
    edges = dwg.g()

    for node in board:
        if node[0] == "module":
            min_x = float("+inf")
            max_x = float("-inf")
            min_y = float("+inf")
            max_y = float("-inf")
            at = [float(x) for x in [x for x in node if x[0] == "at"][0][1:]]
            ref = [x for x in node if x[1] == "reference"][0][2]
            grp = dwg.g(id=ref)
            fab_drawings = []
            silk_drawings = []
            for child in node:
                if child[0] not in ("fp_line", "fp_circle"):
                    continue
                layer = [x for x in child if x[0] == "layer"][0]
                if layer[1] in ("F.Fab", "F.SilkS"):
                    if child[0] == "fp_line":
                        start = [x for x in child if x[0] == "start"][0][1:]
                        end = [x for x in child if x[0] == "end"][0][1:]
                        min_x = min(float(start[0]), min_x)
                        max_x = max(float(start[0]), max_x)
                        min_y = min(float(start[1]), min_y)
                        max_y = max(float(start[1]), max_y)
                        min_x = min(float(end[0]), min_x)
                        max_x = max(float(end[0]), max_x)
                        min_y = min(float(end[1]), min_y)
                        max_y = max(float(end[1]), max_y)
                        line = dwg.line(start, end, stroke='black',
                                        stroke_width=0.1)
                        if layer[1] == "F.Fab":
                            fab_drawings.append(line)
                        elif layer[1] == "F.SilkS":
                            silk_drawings.append(line)
                    elif child[0] == "fp_circle":
                        center = [x for x in child if x[0] == "center"][0][1:]
                        end = [x for x in child if x[0] == "end"][0][1:]
                        r = max(abs(float(center[0]) - float(end[0])),
                                abs(float(center[1]) - float(end[1])))
                        min_x = min(float(start[0])-r, min_x)
                        max_x = max(float(start[0])+r, max_x)
                        min_y = min(float(start[1])-r, min_y)
                        max_y = max(float(start[1])+r, max_y)
                        circle = dwg.circle(center, r, stroke='black',
                                            stroke_width=0.1, fill='none')
                        if layer[1] == "F.Fab":
                            fab_drawings.append(circle)
                        elif layer[1] == "F.SilkS":
                            silk_drawings.append(circle)
            pads = []
            for child in node:
                if child[0] != "pad":
                    continue
                layers = [x for x in child if x[0] == "layers"][0][1:]
                if "F.Cu" not in layers and "*.Cu" not in layers:
                    continue
                pad_type = child[2]
                if pad_type not in ("smd", "thru_hole"):
                    continue
                pad_at = [x for x in child if x[0] == "at"][0][1:]
                pad_at = [float(x) for x in pad_at]
                pad_size = [x for x in child if x[0] == "size"][0][1:]
                pad_size = [float(x) for x in pad_size]
                pad_drill = [x for x in child if x[0] == "drill"]
                if pad_drill:
                    pad_offset = [x for x in pad_drill if x[0] == "offset"]
                    if pad_offset:
                        at[0] += float(pad_offset[1])
                        at[1] += float(pad_offset[2])
                insert = pad_at[0]-pad_size[0]/2, pad_at[1]-pad_size[1]/2
                shape = child[3]
                if shape in ("rect", "oval"):
                    if shape == "oval":
                        rx = pad_size[0]/2
                        ry = pad_size[1]/2
                    else:
                        rx = 0
                        ry = 0
                    pad = dwg.rect(insert, pad_size, rx, ry, stroke='none',
                                   fill='black')
                    pads.append(pad)
                elif shape == "circle":
                    pads.append(dwg.circle((pad_at[0], pad_at[1]),
                                           r=pad_size[0]/2))
            if min_x != float("inf"):
                min_x -= 0.5
                max_x += 0.5
                min_y -= 0.5
                max_y += 0.5
                highlight = dwg.rect((min_x, min_y),
                                     (max_x-min_x, max_y-min_y),
                                     rx=0.5, ry=0.5,
                                     stroke='none',
                                     fill='#ff8888', visibility='hidden',
                                     id="highlight-{}".format(ref))
                if len(at) == 3:
                    highlight.rotate(angle=-float(at[2]),
                                     center=(at[0], at[1]))
                highlight.translate(at[0], at[1])
                highlights[ref] = highlight
            if fab_drawings:
                for drawing in fab_drawings:
                    grp.add(drawing)
            else:
                for drawing in silk_drawings:
                    grp.add(drawing)
                for pad in pads:
                    grp.add(pad)
            if len(at) == 3:
                grp.rotate(angle=-float(at[2]), center=(at[0], at[1]))
            grp.translate(at[0], at[1])
            parts[ref] = grp
        elif node[0] == "gr_line":
            layer = [x for x in node if x[0] == "layer"][0]
            if layer[1] == "Edge.Cuts":
                start = [x for x in node if x[0] == "start"][0][1:]
                end = [x for x in node if x[0] == "end"][0][1:]
                edges.add(dwg.line(start, end,
                                   stroke='black',
                                   stroke_width=0.1))
        elif node[0] == "gr_arc":
            layer = [x for x in node if x[0] == "layer"][0]
            if layer[1] == "Edge.Cuts":
                center = [x for x in node if x[0] == "start"][0][1:]
                center = [float(x) for x in center]
                start = [x for x in node if x[0] == "end"][0][1:]
                start = [float(x) for x in start]
                r = max(abs(center[0] - start[0]),
                        abs(center[1] - start[1]))
                angle = float([x for x in node if x[0] == "angle"][0][1])
                dx = start[0] - center[0]
                dy = start[1] - center[1]
                start_angle = math.atan2(dy, dx)
                end_angle = (start_angle + angle * (math.pi/180.0))
                end_x = center[0] + r * math.cos(end_angle)
                end_y = center[1] + r * math.sin(end_angle)
                path = "M {} {} A {} {} 0 0 1 {} {}".format(
                    start[0], start[1], r, r, end_x, end_y)
                edges.add(dwg.path(path, fill='none',
                                   stroke='black', stroke_width=0.1))
    for highlight in highlights.values():
        dwg.add(highlight)
    for part in parts.values():
        dwg.add(part)
    dwg.add(edges)
    dwg.save()
    xml = dwg.get_xml()

    h = xml.find("rect[@id='highlight-IC1']")
    h.set('visibility', 'visible')
    et = ElementTree.ElementTree(element=xml)
    et.write(outpath+"-IC1.svg")

if __name__ == "__main__":
    draw_board(sys.argv[1], sys.argv[2])
