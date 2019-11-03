"""
build_lib_ic.py
Copyright 2016 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generate symbols for generic black-box ICs etc.

Symbols configuration:
Each symbol is defined by a .yaml file in the same path that the .lib file
should be placed. Each file contains the following keys:
designator: optional, default "IC", the default reference designator
footprint: optional, an associated footprint to autofill
datasheet: optional, a URL or path to a datasheet
ordercodes: optional, list of (supplier, code) for supplier order codes
description: description of the part, placed in the .dcm file
pins: list of lists of left and right pin groups
          (blocks of related pins with a space in-between).
      Each group contains a list of tuples of:
          (pin name, pin number, electrical type).
      Number and name may be given as a string or an integer.
      Electrical type must be a string out of:
          in, out, bidi, tri, passive, unspec, pwrin, pwrout,
          oc, od, oe, os, nc.
      These correspond to input, output, bidirectional, tristate, passive,
          unspecified, power_input, power_output, open_collector,
          open_emitter, and not_connected. They should be given as strings.

"""

from __future__ import print_function, division

import os
import sys
import yaml
import fnmatch
import argparse

pin_types = {
    "in": "I",
    "out": "O",
    "bidi": "B",
    "tri": "T",
    "passive": "P",
    "unspec": "U",
    "pwrin": "W",
    "pwrout": "w",
    "oc": "C",
    "od": "C",
    "oe": "E",
    "os": "E",
    "nc": "N",
}


def geometry(conf):
    # width is twice the width required to accommodate the longest name
    longest_name = max(max(max(len(pin[0]) for pin in grp) for grp in side)
                       for side in conf['pins'])
    width = 2 * (longest_name + 1) * 50
    width += width % 200

    # height is the maximum required on either side
    if len(conf['pins']) != 2:
        raise RuntimeError("IC schematic symbols must list pins on exactly "
                           "two sides.")
    left_pins = sum(len(x) for x in conf['pins'][0])
    right_pins = sum(len(x) for x in conf['pins'][1])
    left_groups = len(conf['pins'][0])
    right_groups = len(conf['pins'][1])

    height = 100 * max(
        left_pins + left_groups - 1, right_pins + right_groups - 1)

    # height must be an odd multiple of 0.1" or the grid breaks
    if (height // 100) % 2 == 0:
        height += 100

    # Pin length based on maximum pin number length
    longest_num = max(max(max(len(str(pin[1])) for pin in grp) for grp in side)
                      for side in conf['pins'])
    length = max(100, longest_num*50)
    # Ensure pins will align to a 100mil grid by making the part wider
    if length % 100 != 0:
        width += 100

    return width, height, length, left_groups


def fields(conf):
    width, height, _, lgroups = geometry(conf)
    field_x = -width//2
    field_y = height//2 + 50
    out = []

    # Designator at top
    out.append("F0 \"{}\" {} {} 50 H V L CNN".format(
        conf.get('designator', 'IC'), field_x, field_y))

    # Value/name at bottom
    out.append("F1 \"{}\" {} {} 50 H V L CNN".format(
        conf['name'], field_x, -field_y))

    # Either specify a footprint or just set its size, position, invisibility
    if "footprint" in conf:
        out.append("F2 \"{}\" {} {} 50 H I L CNN".format(
            conf['footprint'], field_x, -field_y-100))
    else:
        out.append("F2 \"\" {} {} 50 H I L CNN".format(field_x, -field_y-100))

    # Specify a datasheet if given
    if "datasheet" in conf:
        out.append("F3 \"{}\" {} {} 50 H I L CNN".format(
            conf['datasheet'], field_x, -field_y-200))
    else:
        out.append("F3 \"\" {} {} 50 H I L CNN".format(field_x, -field_y-200))

    # Order codes
    for idx, (supplier, code) in enumerate(conf.get("ordercodes", [])):
        out.append("F{} \"{}\" {} {} 50 H I L CNN \"{}\"".format(
            idx+4, code, field_x, -field_y-(300+idx*100), supplier))

    return out


def draw_pins(groups, x0, y0, direction, length):
    out = []
    pin_x = x0
    pin_y = y0
    for group in groups:
        for (name, num, t) in group:
            out.append("X {} {} {} {} {} {} 50 50 0 0 {}".format(
                name, num, pin_x, pin_y, length, direction, pin_types[t]))
            pin_y -= 100
        pin_y -= 100
    return out


def draw(conf):
    width, height, length, lgroups = geometry(conf)
    out = []
    out.append("DRAW")

    # Containing box
    out.append("S {} {} {} {} 0 1 0 f".format(
        -width//2, height//2, width//2, -height//2))

    # Pins
    x0 = -width//2 - length
    y0 = height//2 - 50
    out += draw_pins(conf['pins'][0], x0, y0, "R", length)
    out += draw_pins(conf['pins'][1], -x0, y0, "L", length)

    out.append("ENDDRAW")
    return out


def library(conf):
    out = []

    out.append("EESchema-LIBRARY Version 2.3")
    out.append("#encoding utf-8")
    out.append("#\n# {}\n#".format(conf['name']))
    out.append("DEF {} {} 0 40 Y Y 1 F N".format(
        conf['name'], conf.get('designator', 'IC')))

    out += fields(conf)
    out += draw(conf)

    out.append("ENDDEF\n#\n#End Library\n")
    return "\n".join(out)


def documentation(conf):
    out = []
    out.append("EESchema-DOCLIB  Version 2.0")
    out.append("$CMP {}".format(conf['name']))
    out.append("D {}".format(conf['description']))
    if "datasheet" in conf:
        out.append("F {}".format(conf['datasheet']))
    out.append("$ENDCMP\n")
    return "\n".join(out)


def load_items(libpath):
    config = {}
    for dirpath, dirnames, files in os.walk(libpath):
        dirnames.sort()
        files.sort()
        for fn in fnmatch.filter(files, "*.yaml"):
            path = os.path.join(dirpath, fn)
            with open(path) as f:
                item = yaml.safe_load(f)
                item["path"] = dirpath
                config[item["name"]] = item
    return config


def main(libpath, verify=False, verbose=False):
    config = load_items(libpath)
    for name, conf in config.items():
        conf['name'] = name
        path = os.path.join(conf.get("path", ""), name.lower()+".lib")
        dcmpath = os.path.splitext(path)[0] + ".dcm"

        lib = library(conf)
        dcm = documentation(conf)

        if verify and verbose:
            print("Verifying", path)

        # Check if anything has changed
        if os.path.isfile(path):
            with open(path) as f:
                oldlib = f.read()
            if os.path.isfile(dcmpath):
                with open(dcmpath) as f:
                    olddcm = f.read()
                if lib == oldlib and dcm == olddcm:
                    continue

        # If so, either verification failed or write the new files
        if verify:
            return False
        else:
            with open(path, "w") as f:
                f.write(lib)
            with open(dcmpath, "w") as f:
                f.write(dcm)

    # If we finished and didn't return yet, verification has succeeded
    if verify:
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("libpath", type=str, help=
                        "Path to libraries to process")
    parser.add_argument("--verify", action="store_true", help=
                        "Verify libraries are up to date")
    parser.add_argument("--verbose", action="store_true", help=
                        "Print out every library verified")
    args = vars(parser.parse_args())
    result = main(**args)
    if args['verify']:
        if result:
            print("OK: all libs up-to-date.")
            sys.exit(0)
        else:
            print("Error: libs not up-to-date.", file=sys.stderr)
            sys.exit(1)
