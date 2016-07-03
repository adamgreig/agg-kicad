#!/usr/bin/env python
"""
stickerbom.py
Copyright 2016 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.
"""

from __future__ import print_function, division, unicode_literals


import argparse
import os
import math
import cairo
import xml.etree.ElementTree as ET
import sexp


class Module:
    def __init__(self, mod):
        self.fab_lines = []
        self.fab_circs = []
        self.silk_lines = []
        self.silk_circs = []
        self.rect_pads = []
        self.circ_pads = []
        self._parse(mod)

    def render(self, cr):
        """"
        Render the footprint in the board coordinate system.
        """
        cr.save()
        cr.translate(self.at[0], self.at[1])
        cr.set_line_width(0.1)
        if len(self.at) == 3:
            cr.rotate(-self.at[2] * math.pi/180)
        if self.fab_lines or self.fab_circs:
            for line in self.fab_lines:
                cr.move_to(*line[0])
                cr.line_to(*line[1])
                cr.stroke()
            for circ in self.fab_circs:
                r = math.sqrt((circ[0][0] - circ[1][0])**2 +
                              (circ[0][1] - circ[1][1])**2)
                cr.new_sub_path()
                cr.arc(circ[0][0], circ[0][1], r, 0, 2*math.pi)
        else:
            for line in self.silk_lines:
                cr.move_to(*line[0])
                cr.line_to(*line[1])
                cr.stroke()
            for circ in self.silk_circs:
                r = math.sqrt((circ[0][0] - circ[1][0])**2 +
                              (circ[0][1] - circ[1][1])**2)
                cr.new_sub_path()
                cr.arc(circ[0][0], circ[0][1], r, 0, 2*math.pi)
                cr.stroke()
            for rect in self.rect_pads:
                cr.rectangle(rect[0][0], rect[0][1], rect[1][0], rect[1][1])
                cr.fill()
            for circ in self.circ_pads:
                cr.new_sub_path()
                cr.arc(circ[0][0], circ[0][1], circ[1], 0, 2*math.pi)
                cr.fill()
        cr.restore()

    def render_highlight(self, cr):
        """
        Render a highlight at the footprint's position and of its size.
        """
        cr.save()
        cr.translate(self.at[0], self.at[1])
        if len(self.at) == 3:
            cr.rotate(-self.at[2] * math.pi/180)
        x1, y1, x2, y2 = self.bounds
        a = 0.2
        x1 -= a
        y1 -= a
        x2 += a
        y2 += a
        r = 0.5
        pi2 = math.pi / 2.0
        cr.new_sub_path()
        cr.arc(x1+r, y1+r, r, 2*pi2, 3*pi2)
        cr.arc(x2-r, y1+r, r, 3*pi2, 4*pi2)
        cr.arc(x2-r, y2-r, r, 0*pi2, 1*pi2)
        cr.arc(x1+r, y2-r, r, 1*pi2, 2*pi2)
        cr.close_path()
        cr.fill()
        cr.restore()

    def _parse(self, mod):
        self.at = [float(x) for x in sexp.find(mod, "at")[1:]]
        self.bounds = [0, 0, 0, 0]
        for text in sexp.find_all(mod, "fp_text"):
            if text[1] == "reference":
                self.ref = text[2]
            elif text[1] == "value":
                self.val = text[2]

        for graphic in sexp.find_all(mod, "fp_line", "fp_circle"):
            self._parse_graphic(graphic)

        for pad in sexp.find_all(mod, "pad"):
            self._parse_pad(pad)

    def _parse_graphic(self, graphic):
        layer = sexp.find(graphic, "layer")[1]
        if graphic[0] == "fp_line":
            start = [float(x) for x in sexp.find(graphic, "start")[1:]]
            self._update_bounds(start)
        elif graphic[0] == "fp_circle":
            center = [float(x) for x in sexp.find(graphic, "center")[1:]]
            self._update_bounds(center)
        end = [float(x) for x in sexp.find(graphic, "end")[1:]]
        self._update_bounds(end)

        if layer == "F.Fab":
            if graphic[0] == "fp_line":
                self.fab_lines.append((start, end))
            elif graphic[0] == "fp_circle":
                self.fab_circs.append((center, end))
        elif layer == "F.SilkS":
            if graphic[0] == "fp_line":
                self.silk_lines.append((start, end))
            elif graphic[0] == "fp_circle":
                self.silk_circs.append((center, end))

    def _parse_pad(self, pad):
        layers = sexp.find(pad, "layers")[1]
        if "F.Cu" not in layers and "*.Cu" not in layers:
            return
        pad_type = pad[2]
        if pad_type not in ("smd", "thru_hole"):
            return
        at = [float(x) for x in sexp.find(pad, "at")[1:]]
        size = [float(x) for x in sexp.find(pad, "size")[1:]]
        drill = sexp.find(pad, "drill")
        if drill:
            offset = sexp.find(drill, "offset")
            if offset:
                at[0] += float(offset[1])
                at[1] += float(offset[2])
        topleft = at[0] - size[0]/2, at[1] - size[1]/2
        shape = pad[3]
        if shape in ("rect", "oval"):
            self.rect_pads.append((topleft, size))
            self._update_bounds(at, dx=size[0]/2, dy=size[1]/2)
        elif shape == "circle":
            self.circ_pads.append((at, size[0]/2))
            self._update_bounds(at, dx=size[0]/2, dy=size[0]/2)
        else:
            self._update_bounds(at)

    def _update_bounds(self, at, dx=0, dy=0):
        self.bounds[0] = min(self.bounds[0], at[0] - dx)
        self.bounds[1] = min(self.bounds[1], at[1] - dy)
        self.bounds[2] = max(self.bounds[2], at[0] + dx)
        self.bounds[3] = max(self.bounds[3], at[1] + dy)


class PCB:
    def __init__(self, board):
        self.modules = []
        self.edge_lines = []
        self.edge_arcs = []
        self._parse(board)

    def render(self, cr, where, max_w, max_h, highlights=None):
        """
        Render the PCB, with the top left corner at `where`,
        occupying at most `max_w` width and `max_h` height,
        and draw a highlight under parts whose reference is in `highlights`.
        """
        cr.save()
        cr.set_line_width(0.1)

        # Set a clip to ensure we occupy at most max_w and max_h
        cr.rectangle(where[0], where[1], max_w, max_h)
        cr.clip()

        # Find bounds on highlighted modules
        hl_bounds = self._find_highlighted_bounds(highlights)
        bound_width = hl_bounds[2] - hl_bounds[0]
        bound_height = hl_bounds[3] - hl_bounds[1]
        bound_centre_x = hl_bounds[0] + bound_width/2
        bound_centre_y = hl_bounds[1] + bound_height/2

        # Scale to either 1.5:1 or smaller if necessary to fit bounds
        scale_x = max_w / bound_width
        scale_y = max_h / bound_height
        scale = min(min(1.5, scale_x), min(1.5, scale_y))
        cr.scale(scale, scale)

        # Can we shift the top edge of the PCB to the top and not cut off
        # the bottom of the highlight?
        if hl_bounds[3] - self.bounds[1] < max_h/scale:
            shift_y = -self.bounds[1]

        # Can we shift the bottom edge of the PCB to the bottom and not cut off
        # the top of the highlight?
        elif self.bounds[3] - hl_bounds[1] < max_h/scale:
            shift_y = -self.bounds[3] + max_h/scale

        # Otherwise centre the highlighted region vertically
        else:
            shift_y = (max_h/(2*scale))-bound_centre_y

        # Can we shift the left edge of the PCB to the left and not cut off
        # the right of the highlight?
        if hl_bounds[2] - self.bounds[0] < max_w/scale:
            shift_x = -self.bounds[0]

        # Can we shift the right edge of the PCB to the right and not cut off
        # the left of the highlight?
        elif self.bounds[2] - hl_bounds[0] < max_w/scale:
            shift_x = -self.bounds[2] + max_w/scale

        # Otherwise centre the highlighted region horizontally
        else:
            shift_x = (max_w/(2*scale))-bound_centre_x

        cr.translate(shift_x, shift_y)

        # Translate our origin to desired position on page
        cr.translate(where[0]/scale, where[1]/scale)

        # Render highlights below everything else
        cr.set_source_rgb(1.0, 0.5, 0.5)
        for module in self.modules:
            if module.ref in highlights:
                module.render_highlight(cr)

        # Render modules
        cr.set_source_rgb(0, 0, 0)
        for module in self.modules:
            module.render(cr)

        # Render edge lines
        for line in self.edge_lines:
            cr.move_to(*line[0])
            cr.line_to(*line[1])
            cr.stroke()

        # Render edge arcs
        for arc in self.edge_arcs:
            cr.new_sub_path()
            cr.arc(*arc)
            cr.stroke()

        cr.restore()

    def _find_highlighted_bounds(self, highlights):
        # Find bounds on highlighted modules
        # TODO: Deal with rotation in modules in a more elegant fashion
        # (Rotation includes bounds, so here we just take the biggest bound,
        #  which is both wasteful for high aspect ratio parts, and wrong for
        #  parts not on a 90' rotation).
        hl_bounds = [self.bounds[2], self.bounds[3],
                     self.bounds[0], self.bounds[1]]
        for module in self.modules:
            if module.ref not in highlights:
                continue
            a = max(module.bounds) * 2
            hl_bounds[0] = min(hl_bounds[0], module.at[0] - a)
            hl_bounds[1] = min(hl_bounds[1], module.at[1] - a)
            hl_bounds[2] = max(hl_bounds[2], module.at[0] + a)
            hl_bounds[3] = max(hl_bounds[3], module.at[1] + a)
        return hl_bounds

    def _parse(self, board):
        for module in sexp.find_all(board, "module"):
            self.modules.append(Module(module))

        # We compute the PCB bounds ourselves rather than relying on the file's
        # area tag which seems to sometimes be wrong. First go based on module
        # positions.
        self.bounds = [
            min(m.at[0] for m in self.modules),
            min(m.at[1] for m in self.modules),
            max(m.at[0] for m in self.modules),
            max(m.at[1] for m in self.modules)
        ]

        # We find all the board edges both for drawing and for bounds
        self._parse_edges(board)

        # Add a slight padding to ensure edge lines are properly drawn
        self.bounds[0] -= 1
        self.bounds[1] -= 1
        self.bounds[2] += 1
        self.bounds[3] += 1

        self.width = self.bounds[2] - self.bounds[0]
        self.height = self.bounds[3] - self.bounds[1]

    def _parse_edges(self, board):
        for graphic in sexp.find_all(board, "gr_line", "gr_arc", "gr_circle"):
            layer = sexp.find(graphic, "layer")[1]
            if layer != "Edge.Cuts":
                continue
            if graphic[0] == "gr_line":
                start = [float(x) for x in sexp.find(graphic, "start")[1:]]
                end = [float(x) for x in sexp.find(graphic, "end")[1:]]
                self.edge_lines.append((start, end))
                self._update_bounds(start)
                self._update_bounds(end)
            elif graphic[0] == "gr_arc":
                center = [float(x) for x in sexp.find(graphic, "start")[1:]]
                start = [float(x) for x in sexp.find(graphic, "end")[1:]]
                r = math.sqrt((center[0] - start[0])**2 +
                              (center[1] - start[1])**2)
                angle = float(sexp.find(graphic, "angle")[1]) * math.pi/180.0
                dx = start[0] - center[0]
                dy = start[1] - center[1]
                start_angle = math.atan2(dy, dx)
                end_angle = start_angle + angle
                self.edge_arcs.append((center[0], center[1], r,
                                       start_angle, end_angle))
                self._update_bounds(center, dx=r, dy=r)
            elif graphic[0] == "gr_circle":
                center = [float(x) for x in sexp.find(graphic, "center")[1:]]
                end = [float(x) for x in sexp.find(graphic, "end")[1:]]
                r = math.sqrt((center[0] - end[0])**2 +
                              (center[1] - end[1])**2)
                self.edge_arcs.append((center[0], center[1], r, 0, 2*math.pi))
                self._update_bounds(center, dx=r, dy=r)

    def _update_bounds(self, at, dx=0, dy=0):
        self.bounds[0] = min(self.bounds[0], at[0] - dx)
        self.bounds[1] = min(self.bounds[1], at[1] - dy)
        self.bounds[2] = max(self.bounds[2], at[0] + dx)
        self.bounds[3] = max(self.bounds[3], at[1] + dy)


class BOM:
    def __init__(self, xmlpath):
        self.tree = ET.parse(xmlpath)
        self.lines = []
        self.suppliers = {}
        self._find_parts()
        self._generate_lines()

    def _find_parts(self):
        for comp in self.tree.getroot().iter('comp'):
            ref = comp.get('ref')
            val = comp.findtext('value')
            ftp = comp.findtext('footprint')
            fields = {}
            part = {"ref": ref, "val": val, "ftp": ftp, "fields": fields}
            for field in comp.iter('field'):
                supplier = field.get('name')
                code = field.text
                fields[supplier] = code

                if supplier not in self.suppliers:
                    self.suppliers[supplier] = {}
                if code not in self.suppliers[supplier]:
                    self.suppliers[supplier][code] = []
                self.suppliers[supplier][code].append(part)

    def _generate_lines(self):
        for supplier in self.suppliers:
            for code in self.suppliers[supplier]:
                part = self.suppliers[supplier][code][0]
                refs = []
                for part in self.suppliers[supplier][code]:
                    refs.append(part['ref'])
                line = Line(refs, part['val'], part['ftp'], supplier, code)
                self.lines.append(line)


class Line:
    def __init__(self, refs, value, footprint, supplier, code):
        self.refs = refs
        self.value = value
        self.footprint = footprint
        self.supplier = supplier
        self.code = code

        if self.footprint is not None:
            self.footprint = self.footprint.split(":")[1]
        else:
            self.footprint = ""

    def render(self, cr, where, w, h):
        cr.save()

        # Clip to permissible area
        cr.rectangle(where[0], where[1], w, h)
        cr.clip()

        # Draw first line
        cr.set_source_rgb(0, 0, 0)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(3.0)
        cr.move_to(where[0]+3, where[1]+5)
        cr.show_text(" ".join(self.refs))

        # Draw second line
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(3.0)
        cr.move_to(where[0]+3, where[1]+9)
        cr.show_text("{}x  {}  {}"
                     .format(len(self.refs), self.value, self.footprint))

        # Draw third line
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(3.0)
        cr.move_to(where[0]+3, where[1]+12)
        cr.show_text("{} {}".format(self.supplier, self.code))

        cr.restore()


# Forever yields a new (x, y) of successive label top-left positions,
# calling cr.show_page() when the current page is exhausted.
def sheet_positions(cr, label_width, label_height, labels_x, labels_y,
                    margin_top, margin_left, spacing_x, spacing_y):
    while True:
        for x in range(labels_x):
            for y in range(labels_y):
                xx = margin_left + x*(label_width + spacing_x)
                yy = margin_top + y*(label_height + spacing_y)
                yield (xx, yy)
        cr.show_page()


def xmlpath(path):
    if os.path.exists(path):
        return path
    raise TypeError("XML file must exist.")


def pdfpath(path):
    if path[-4:].lower() != ".pdf":
        return path + ".pdf"
    return path


def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("xmlpath", type=xmlpath,
                        help="Path to the xml BOM file to be parsed.")
    parser.add_argument("pdfpath", type=pdfpath,
                        help="Path to the pdf file that will "
                             "contain the stickers.")

    parser.add_argument("--label_width", type=int, default=72,
                        help="Width of a label (mm).")
    parser.add_argument("--label_height", type=int, default=63.5,
                        help="Height of a label (mm).")
    parser.add_argument("--labels-x", type=int, default=4,
                        help="Number of columns of labels on a page.")
    parser.add_argument("--labels-y", type=int, default=3,
                        help="Number of rows of labels on a page.")
    parser.add_argument("--margin-top", type=int, default=7.75,
                        help="Margin at the top of the page (mm).")
    parser.add_argument("--margin-left", type=int, default=4.5,
                        help="Margin at the left side of the page (mm).")
    parser.add_argument("--spacing-x", type=int, default=0.0,
                        help="Gap between columns of labels (mm).")
    parser.add_argument("--spacing-y", type=int, default=2.0,
                        help="Gap between rows of labels (mm).")
    parser.add_argument("--page-width", type=int, default=297,
                        help="Width of a page (mm).")
    parser.add_argument("--page-height", type=int, default=210,
                        help="Height of a page (mm).")

    parser.add_argument("--suppliers",
                        default="Farnell,RS,DigiKey,Digikey,Mouser",
                        help="Comma seperated list of names of suppliers "
                             "to output stickers for (Note: this really "
                             "means 'custom schematic symbol property "
                             "field names' to output stickers for).")

    parser.add_argument("--include-parts-without-footprint",
                        action="store_true",
                        help="Include parts that do not have a footprint.")
    return parser.parse_args()


def main():
    args = get_args()

    bom = BOM(args.xmlpath)

    with open(args.xmlpath[:-3] + "kicad_pcb") as f:
        pcb = PCB(sexp.parse(f.read()))

    mm_to_pt = 2.835
    ps = cairo.PDFSurface(args.pdfpath,
                          args.page_width*mm_to_pt,
                          args.page_height*mm_to_pt)
    cr = cairo.Context(ps)

    # Scale user units to millimetres
    cr.scale(mm_to_pt, mm_to_pt)

    labels = sheet_positions(cr,
                             args.label_width, args.label_height,
                             args.labels_x, args.labels_y,
                             args.margin_top, args.margin_left,
                             args.spacing_x, args.spacing_y)

    suppliers = [name.strip() for name in args.suppliers.split(",")]

    for line in bom.lines:
        if line.supplier not in suppliers:
            continue
        if not line.footprint and not args.include_parts_without_footprint:
            continue
        label = next(labels)
        line.render(cr,
                    (label[0]+1, label[1]),
                    args.label_width-2, 14)
        pcb.render(cr,
                   (label[0]+1, label[1]+14),
                   args.label_width-2, args.label_height-14,
                   line.refs)
    cr.show_page()


if __name__ == "__main__":
    main()
