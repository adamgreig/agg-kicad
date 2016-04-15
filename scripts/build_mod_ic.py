"""
build_mod_ic.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Create a range of dual and quad SMD IC packages.

TODO:
    * Support non-square 4-row packages
    * Support other pad shapes, e.g. oval/half-oval
"""

from __future__ import print_function, division

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
#   rows: either 2 or 4, for dual or quad packages.
#   pins: total number of pins.
#   skip_pins: optional, list of pin numbers to skip (leaving remaining pins in
#              sequential order). Generates packages like SOT-23-3.
#   pin_pitch: spacing between adjacent pins.
#   row_pitch: spacing between rows of pins.
#   pad_shape: (width, height) of a pad for a pin.
#   ep_shape: (width, height) of an exposed pad underneath the chip.
#             Leave out this parameter to skip the exposed pad.
#   ep_mask_shape: (width, height, w_gap, h_gap) of mask apertures on EP.
#                  Multiple apertures will be created to fill.
#                  Leave out this parameter to cover the EP in mask aperture.
#   ep_paste_shape: (width, height, w_gap, h_gap) of paste apertures on EP.
#                   Multiple apertures will be created to fill.
#                   Leave out this parameter to cover the EP in paste aperture.
#   ep_vias: (drill, size, gap) of via hits to put in the EP.
#            Leave out this parameter to not place any vias.
#   chip_shape: (width, height) of the actual chip package (for Fab layer).
#   pin_shape: (width, height) of the chip package pins (for Fab layer).
#              Use negative widths for internal pins (e.g., QFNs).
#   silk: "internal" or "external" or None.
#          Default is "internal" unless ep_shape is given in which case
#          default is "external".
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

    # TSSOP-20 from JEDEC MO-153AC
    # IPC-7351B: SOP65P640X120-20N
    "TSSOP-20": {
        "rows": 2,
        "pins": 20,
        "pin_pitch": 0.65,
        "row_pitch": 5.75,
        "pad_shape": (1.35, 0.45),
        "chip_shape": (4.5, 6.6),
        "pin_shape": (0.95, .30),
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

    # UFQFPN-48 from JEDEC MO-220
    # Modified to meet the ST ECOPACK package of the same name:
    #   * Row pitch is 6.75mm instead of 7.0mm
    #   * Pads are 0.55mm long instead of 0.8mm
    #   * EP is 5.6mm
    # IPC-7351B: QFN50P700X700X80-49N
    "QFN-48-EP-ST": {
        "rows": 4,
        "pins": 48,
        "pin_pitch": 0.5,
        "row_pitch": 6.75,
        "pad_shape": (0.55, 0.30),
        "ep_shape": (5.6, 5.6),
        "ep_paste_shape": (1.0, 1.0, 1.5, 1.5),
        "ep_mask_shape": (2.0, 2.0, 0.5, 0.5),
        "ep_vias": (0.4, 0.6, 1.9),
        "chip_shape": (7.1, 7.1),
        "pin_shape": (-0.5, 0.3),
    },

    # UFQFPN-32 from JEDEC MO-220
    # Modified to meet the ST ECOPACK package of the same name:
    #   * Row pitch is 6.75mm instead of 7.0mm
    #   * Pads are 0.55mm long instead of 0.8mm
    #   * EP is 5.6mm
    # IPC-7351B: QFN50P700X700X80-33N
    "QFN-32-EP-ST": {
        "rows": 4,
        "pins": 32,
        "pin_pitch": 0.5,
        "row_pitch": 4.7,
        "pad_shape": (0.60, 0.30),
        "ep_shape": (3.45, 3.45),
        "ep_paste_shape": (1.0, 1.0, 1.5, 1.5),
        "ep_mask_shape": (2.0, 2.0, 0.5, 0.5),
        "ep_vias": (0.4, 0.6, 1.9),
        "chip_shape": (5.1, 5.1),
        "pin_shape": (-0.5, 0.28),
    },

    # QFN-40 from JEDEC MO-220
    # Modified to meet the UBLOX recommended footprint:
    #   * Pads are 0.5mm long instead of 1.0mm
    #   * Row pitch is 4.8mm instead of 4.9mm
    #   * EP is 3.7mm instead of 3.4mm
    #   * EP mask and paste defined by 16 0.55x0.55mm apertures
    # IPC-7351B: QFN40P500X500X80-41N (modified)
    "QFN-40-EP-UBLOX": {
        "rows": 4,
        "pins": 40,
        "pin_pitch": 0.4,
        "row_pitch": 4.8,
        "pad_shape": (0.5, 0.2),
        "ep_shape": (3.7, 3.7),
        "ep_mask_shape": (0.55, 0.55, 0.5, 0.5),
        "ep_paste_shape": (0.55, 0.55, 0.5, 0.5),
        "ep_vias": (0.4, 0.6, 0.45),
        "chip_shape": (5.1, 5.1),
        "pin_shape": (-0.35, 0.2),
    },

    # QFN-20 from JEDEC MO-220VGGD-8
    # For Si4460
    # IPC-7351B: QFN50P400X400X85-21V8N
    "QFN-20-EP-SI": {
        "rows": 4,
        "pins": 20,
        "pin_pitch": 0.5,
        "row_pitch": 4.0,
        "pad_shape": (0.75, 0.30),
        "ep_shape": (2.6, 2.6),
        "ep_paste_shape": (1.1, 1.1, 0.2, 0.2),
        "chip_shape": (4.1, 4.1),
        "pin_shape": (-.50, 0.30),
    },

    # QFN-24 from MPU-9250 datasheet
    # For MPU-9250
    # IPC-7351B: QFN40P300X300X100-24N
    "QFN-24-MPU9250": {
        "rows": 4,
        "pins": 24,
        "pin_pitch": 0.4,
        "row_pitch": 3.0,
        "pad_shape": (0.4, 0.2),
        "chip_shape": (3.0, 3.0),
        "pin_shape": (-0.3, 0.2),
    },

    # QFN-24 from MAXIM. Doc no. 21-0139
    # For MAX17435
    "QFN-24-EP-MAX": {
        "rows": 4,
        "pins": 24,
        "pin_pitch": 0.5,
        "row_pitch": 3.91,
        "pad_shape": (0.8, 0.3),
        "chip_shape": (4.0, 4.0),
        "pin_shape": (-0.4, 0.23),
        "ep_shape": (2.6, 2.6),
        "ep_mask_shape": (0.9, 0.9, 0.4, 0.4),
        "ep_paste_shape": (0.9, 0.9, 0.4, 0.4),
    },

    # QFN-16 from SKY65111-348LF datasheet
    # For SKY65111-348LF
    # IPC-7351B: QFN50P300X300X100-16N
    "QFN-16-EP-SKYWORKS": {
        "rows": 4,
        "pins": 16,
        "pin_pitch": 0.50,
        "row_pitch": 2.86,
        "pad_shape": (0.78, 0.26),
        "chip_shape": (3.0, 3.0),
        "pin_shape": (-0.3, 0.25),
        "ep_shape": (1.78, 1.78),
        "ep_paste_shape": (0.7, 0.7, 0.3, 0.3),
        "ep_vias": (0.3, 0.4, 0.2),
    },

    # QFN-40 from LTC3887 datasheet
    # JEDEC WJJD-2 VARIANT
    # IPC-7351B: QFN50P600X600X75-40N
    "QFN-40-EP-LTC-UJ": {
        "rows": 4,
        "pins": 40,
        "pin_pitch": 0.50,
        "row_pitch": 5.80,
        "pad_shape": (0.7, 0.25),
        "ep_shape": (4.42, 4.42),
        "ep_mask_shape": (0.73, 0.73, 0.5, 0.5),
        "ep_paste_shape": (0.73, 0.73, 0.5, 0.5),
        "ep_vias": (0.4, 0.8, 0.43),
        "chip_shape": (6.0, 6.0),
        "pin_shape": (-0.4, 0.25),
    },

    # DFN-10 from JEDEC MO-229WEED-2
    # For LTC3105 / LT package DD
    # For LTC4151
    # IPC-7351B: DFN50P300X300X75-11N
    "DFN-10-EP-LT": {
        "rows": 2,
        "pins": 10,
        "pin_pitch": 0.5,
        "row_pitch": 2.85,
        "pad_shape": (0.70, 0.25),
        "ep_shape": (1.65, 2.38),
        "ep_paste_shape": (1.2, 0.8, 0, 0.4),
        "chip_shape": (3.1, 3.1),
        "pin_shape": (-0.40, 0.30),
    },

    # DFN-12
    # For LTC3535 / LT package DD
    # IPC-7351B: DFN45P300X300X75-13N
    "DFN-12-EP-LT": {
        "rows": 2,
        "pins": 12,
        "pin_pitch": 0.45,
        "row_pitch": 2.8,
        "pad_shape": (0.70, 0.25),
        "ep_shape": (1.65, 2.38),
        "ep_paste_shape": (1.2, 0.8, 0, 0.4),
        "chip_shape": (3.1, 3.1),
        "pin_shape": (-0.40, 0.23),
    },

    # LPCC-16 for HMC5883L
    "LPCC-16-HMC5883L": {
        "rows": 4,
        "pins": 16,
        "pin_pitch": 0.50,
        "row_pitch": 2.55,
        "pad_shape": (0.45, 0.30),
        "chip_shape": (3.1, 3.1),
        "pin_shape": (-0.325, 0.25),
    },

    # LGA-16L for ST MEMS sensors
    "LGA-16L-ST": {
        "rows": 4,
        "pins": 16,
        "pin_pitch": 0.65,
        "row_pitch": 3.40,
        "pad_shape": (0.40, 0.30),
        "chip_shape": (4.1, 4.1),
        "pin_shape": (-0.5, 0.3),
    },

    # MS5611 sensor
    "MS5611": {
        "rows": 2,
        "pins": 8,
        "pin_pitch": 1.25,
        "row_pitch": 2.20,
        "pad_shape": (1.1, 0.6),
        "chip_shape": (3.0, 5.0),
        "pin_shape": (-0.9, 0.50),
        "silk": "external",
    },

    # SOT-23-3
    # JEDEC TO-236AB
    # IPC-7351B: SOT95P230X110-3N
    "SOT-23": {
        "rows": 2,
        "pins": 6,
        "skip_pins": (2, 4, 6),
        "pin_pitch": 0.95,
        "row_pitch": 2.30,
        "pad_shape": (1.0, 0.6),
        "chip_shape": (1.4, 3.0),
        "pin_shape": (0.55, 0.48),
    },

    # SOT-23-5
    # JEDEC MO-178
    # IPC-7351B: SOT95P280X135-5N
    "SOT-23-5": {
        "rows": 2,
        "pins": 6,
        "skip_pins": (5,),
        "pin_pitch": 0.95,
        "row_pitch": 2.60,
        "pad_shape": (1.10, 0.60),
        "chip_shape": (1.70, 3.00),
        "pin_shape": (0.75, 0.50),
    },

    # SOT-23-6
    # JEDEC MO-178AB
    # IPC-7351B: SOT95P280X145-6N
    "SOT-23-6": {
        "rows": 2,
        "pins": 6,
        "pin_pitch": 0.95,
        "row_pitch": 2.60,
        "pad_shape": (1.10, 0.60),
        "chip_shape": (1.75, 3.05),
        "pin_shape": (0.62, 0.50),
    },

    # SC-70-5
    # JEDEC MO-203-AA
    # IPC-7351B: SOT65P210X110-5N
    "SC-70-5": {
        "rows": 2,
        "pins": 6,
        "skip_pins": (5,),
        "pin_pitch": 0.65,
        "row_pitch": 2.20,
        "pad_shape": (0.95, 0.40),
        "chip_shape": (1.4, 2.15),
        "pin_shape": (0.5, 0.3),
    },

    # SOT-323
    # IPC-7351B: SOT65P210X110-3N
    "SOT-323": {
        "rows": 2,
        "pins": 6,
        "skip_pins": (2, 4, 6),
        "pin_pitch": 0.65,
        "row_pitch": 2.10,
        "pad_shape": (0.85, 0.55),
        "chip_shape": (1.35, 2.10),
        "pin_shape": (0.4, 0.3),
    },

    # DFN-8
    # IPC-7351B: DFN65P300X300X90-9N
    "DFN-8-EP-MICROCHIP": {
        "rows": 2,
        "pins": 8,
        "pin_pitch": 0.65,
        "row_pitch": 3.10,
        "pad_shape": (0.65, 0.35),
        "ep_shape": (1.55, 2.4),
        "ep_mask_shape": (0.8, 0.8, 0, 0.4),
        "ep_paste_shape": (0.8, 0.8, 0, 0.4),
        "chip_shape": (3.1, 3.1),
        "pin_shape": (-0.3, 0.30)
    },

    # DFN-16 from LTC4353
    # IPC-7351B: DFN45P300X400X75-17N
    "DFN-16-EP-LTC-DE": {
        "rows": 2,
        "pins": 16,
        "pin_pitch": 0.45,
        "row_pitch": 2.90,
        "pad_shape": (0.70, 0.25),
        "ep_shape": (1.70, 3.30),
        "ep_mask_shape": (0.8, 0.8, 0.2, 0.4),
        "ep_paste_shape": (0.8, 0.8, 0.2, 0.4),
        "chip_shape": (3.1, 4.1),
        "pin_shape": (-0.41, 0.28)
    },

    # HVQFN24 from PCA9502
    # IPC-7351B: QFN50P430X430X100-25N
    "HVQFN24-NXP": {
        "rows": 4,
        "pins": 24,
        "pin_pitch": 0.5,
        "row_pitch": 4.10,
        "pad_shape": (0.90, 0.24),
        "ep_shape": (2.10, 2.10),
        "ep_mask_shape": (0.45, 0.45, 0.4, 0.4),
        "ep_paste_shape": (0.45, 0.45, 0.4, 0.4),
        "chip_shape": (4.3, 4.3),
        "pin_shape": (-0.5, 0.3)
    },

    # HVQFN-16 from PCAL9538A
    # IPC-7351B: QFN50P300X300X100-17N
    "QFN-16-EP-NXP": {
        "rows": 4,
        "pins": 16,
        "pin_pitch": 0.5,
        "row_pitch": 3.10,
        "pad_shape": (0.90, 0.24),
        "ep_shape": (1.50, 1.50),
        "ep_paste_shape": (0.30, 0.30, 0.31, 0.31),
        "chip_shape": (3.0, 3.0),
        "pin_shape": (-0.4, 0.24)
    },

    # VQFN-16 from TPS6215
    # IPC-7351B: QFN26P300X300X100-17N
    "QFN-16-EP-TI": {
        "rows": 4,
        "pins": 16,
        "pin_pitch": 0.5,
        "row_pitch": 2.8,
        "pad_shape": (0.6, 0.25),
        "ep_shape": (1.7, 1.7),
        "ep_paste_shape": (1.5, 1.5, 0.2, 0.2),
        "ep_vias": (0.2, 0.3, 0.9),
        "chip_shape": (3.0, 3.0),
        "pin_shape": (-0.4, 0.25)
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
import sys
import time
import math
import subprocess

from sexp import parse as sexp_parse, generate as sexp_generate
from kicad_mod import fp_line, fp_arc, fp_circle, fp_text, pad, draw_square


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
        layers = ["F.Cu", "F.Mask"]
        for ap in apertures:
            out.append(pad("EP", "smd", "rect", ap, mask_shape[:2], layers,
                           m_mask=.001))

    # Paste apertures
    if "ep_paste_shape" not in conf:
        ep_layers.append("F.Paste")
        ep_m_paste = 0.001
    else:
        paste_shape = conf['ep_paste_shape']
        apertures = inner_apertures(ep_shape, paste_shape)
        layers = ["F.Cu", "F.Paste"]
        for ap in apertures:
            out.append(
                pad("EP", "smd", "rect", ap, paste_shape[:2], layers,
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
    idx = 1
    for pin in leftr:
        idx += 1
        if idx - 1 in conf.get('skip_pins', []):
            continue
        xy = -(chip_w + pin_w) / 2.0, pin[1]
        _, _, _, _, sq = draw_square(pin_w, pin_h, xy, "F.Fab", fab_width)
        out += [sq[0], sq[2], sq[3]]
    for pin in rightr:
        idx += 1
        if idx - 1 in conf.get('skip_pins', []):
            continue
        xy = (chip_w + pin_w) / 2.0, pin[1]
        _, _, _, _, sq = draw_square(pin_w, pin_h, xy, "F.Fab", fab_width)
        out += [sq[0], sq[1], sq[2]]
    if conf['rows'] == 4:
        for pin in topr:
            idx += 1
            if idx - 1 in conf.get('skip_pins', []):
                continue
            xy = pin[0], -(chip_h + pin_w) / 2.0
            _, _, _, _, sq = draw_square(pin_h, pin_w, xy, "F.Fab", fab_width)
            out += [sq[0], sq[1], sq[3]]
        for pin in bottomr:
            idx += 1
            if idx - 1 in conf.get('skip_pins', []):
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
        height = (((pins / rows) - 1) * pin_pitch)
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

    if rows == 2:
        r = silk_pin1_er
        out.append(fp_line((-x+2*r, -y), (x, -y), l, w))
        out.append(fp_line((-x, y), (x, y), l, w))
        out.append(fp_arc((-x+r, -y), (-x, -y), 180, l, w))
    elif rows == 4:
        pins = conf['pins'] / rows
        pin_y = ((pins - 1) * conf['pin_pitch']) / 2.0
        chip_y = chip_shape[1] / 2.0
        delta_y = chip_y - pin_y
        r = delta_y - silk_pad_egap

        # NW
        out.append(fp_line((-x, -y+r), (-x+r, -y), l, w))
        # NE
        out.append(fp_line((x-r, -y), (x, -y), l, w))
        out.append(fp_line((x, -y), (x, -y+r), l, w))
        # SE
        out.append(fp_line((x-r, y), (x, y), l, w))
        out.append(fp_line((x, y), (x, y-r), l, w))
        # SW
        out.append(fp_line((-x+r, y), (-x, y), l, w))
        out.append(fp_line((-x, y), (-x, y-r), l, w))

    return out


def silk(conf):
    default = 'internal' if 'ep_shape' not in conf else 'external'
    silk = conf.get('silk', default)
    if silk == 'external':
        return external_silk(conf)
    elif silk == 'internal':
        return internal_silk(conf)
    else:
        return []


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


def footprint(conf):
    tedit = format(int(time.time()), 'X')
    sexp = ["module", conf['name'], ("layer", "F.Cu"), ("tedit", tedit)]
    sexp += refs(conf)
    sexp += fab(conf)
    sexp += silk(conf)
    sexp += ctyd(conf)
    sexp += pads(conf)
    return sexp_generate(sexp)


def git_version(libpath):
    args = ["git", "describe", "--abbrev=8", "--dirty=-dirty", "--always"]
    git = subprocess.Popen(args, cwd=libpath, stdout=subprocess.PIPE)
    return git.stdout.read().decode().strip()


def main(prettypath, verify=False):
    for name, conf in config.items():
        conf['name'] = name
        assert conf['rows'] in (2, 4), \
            "Must have either two or four rows"
        assert conf['pins'] % conf['rows'] == 0, \
            "Pins must equally divide among rows"
        fp = footprint(conf)
        path = os.path.join(prettypath, name+".kicad_mod")

        if verify:
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
    if len(sys.argv) == 2:
        prettypath = sys.argv[1]
        main(prettypath)
    elif len(sys.argv) == 3 and sys.argv[2] == "--verify":
        prettypath = sys.argv[1]
        if main(prettypath, verify=True):
            print("OK: all footprints up-to-date.")
            sys.exit(0)
        else:
            print("Error: footprints not up-to-date.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: {} <.pretty path> [--verify]".format(sys.argv[0]))
        sys.exit(1)
