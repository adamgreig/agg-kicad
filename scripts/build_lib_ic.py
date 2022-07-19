"""
build_lib_ic.py
Copyright 2016-2022 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generate symbols for generic black-box ICs etc.

Symbols configuration:
Each symbol is defined by a .yaml file in the same path that the .kicad_sym
file should be placed. Each file contains the following keys:
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

import os
import sys
import yaml
import fnmatch
import argparse

import sexp

pin_types = {
    "in": "input",
    "out": "output",
    "bidi": "bidirectional",
    "tri": "tri_state",
    "passive": "passive",
    "unspec": "unspecified",
    "pwrin": "power_in",
    "pwrout": "power_out",
    "oc": "open_collector",
    "od": "open_collector",
    "oe": "open_emitter",
    "os": "open_emitter",
    "nc": "no_connect",
    "free": "free",
}


def longest_num(units):
    return max(max(
        max([0] + [max(len(str(p[1])) for p in grp) for grp in left_pins]),
        max([0] + [max(len(str(p[1])) for p in grp) for grp in right_pins]))
        for (left_pins, right_pins) in units)


def geometry(unit, longest_num):
    left_pins, right_pins = unit

    length = max(100, longest_num * 50)

    # Find longest name of all pins
    longest_name = max(
        max([0] + [max(len(p[0]) for p in grp) for grp in left_pins]),
        max([0] + [max(len(p[0]) for p in grp) for grp in right_pins]))

    # Width is either that required for longest name or twice that for
    # dual-sided parts, rounded up to nearest 2.54. If length is not a
    # multiple of 100, add extra width to ensure pins are on 0.1" grid.
    width = (longest_name + 1) * 50
    width += width % 100
    if left_pins and right_pins:
        width *= 2
    if ((width//2)+length) % 100 != 0:
        width += 2 * (((width//2)+length) % 100)

    # Height is maximum required between each side
    n_left_pins = sum(len(grp) for grp in left_pins)
    n_right_pins = sum(len(grp) for grp in right_pins)
    n_left_groups = len(left_pins)
    n_right_groups = len(right_pins)
    height = 100 * max(
        n_left_pins + n_left_groups - 1, n_right_pins + n_right_groups - 1)

    # Ensure height is an odd multiple of 0.1" to keep everything aligned
    # to the 0.1" grid. This is responsible for the unseemly gaps at the
    # bottom of parts with an even number of pins, but preserves symmetry.
    if (height // 100) % 2 == 0:
        height += 100

    # Convert to millimetres.
    height *= (2.54/100)
    width *= (2.54/100)
    length *= (2.54/100)

    return width, height, length


def normalise_pins(pins):
    """
    Convert YAML representation of pins into a normal structure, which is
    a list of (left, right) tuples, where each tuple is a symbol unit,
    and left and right are either empty lists, or lists of groups,
    where each group is a list of [name, number, type] pins.
    """
    output = []
    # Get what might be either the first pin or the first group of pins,
    # depending on whether the list is 3 deep (one unit) or 4 (multiple units)
    first_pin_or_grp = pins[0][0][0]
    if first_pin_or_grp is None:
        # For right-hand-only parts, we might need to check the second entry
        first_pin_or_grp = pins[1][0][0]
    if isinstance(first_pin_or_grp[0], str):
        # Str means a name, so this is a pin, so there's only
        # one unit, so wrap in a new list.
        pins = [pins]
    for unit in pins:
        if len(unit) == 1:
            # Only one side: left groups only
            output.append((unit[0], []))
        elif len(unit) == 2:
            if unit[0][0][0] is None:
                # Empty left side: right groups only
                output.append(([], unit[1]))
            else:
                # Both sides
                output.append((unit[0], unit[1]))
        else:
            raise ValueError("Invalid pins")
    return output


def fields(conf, units):
    n = longest_num(units)
    geoms = [geometry(unit, n) for unit in units]
    width = max(g[0] for g in geoms)
    height = max(g[1] for g in geoms)
    field_x = -width/2
    field_y = height/2 + 1.27
    out = []

    out.append([
        'property', 'Reference', conf.get('designator', 'IC'),
        ['id', 0], ['at', field_x, field_y, 0],
        ['effects', ['font', ['size', 1.27, 1.27]], ['justify', 'left']],
    ])
    out.append([
        'property', 'Value', conf['name'],
        ['id', 1], ['at', field_x, -field_y, 0],
        ['effects', ['font', ['size', 1.27, 1.27]], ['justify', 'left']],
    ])
    out.append([
        'property', 'Footprint', conf.get('footprint', ''),
        ['id', 2], ['at', field_x, -field_y-2.54, 0],
        ['effects', ['font', ['size', 1.27, 1.27]], ['justify', 'left'],
         'hide'],
    ])
    out.append([
        'property', 'Datasheet', conf.get('datasheet', ''),
        ['id', 3], ['at', field_x, -field_y-5.08, 0],
        ['effects', ['font', ['size', 1.27, 1.27]], ['justify', 'left'],
         'hide'],
    ])

    for idx, (supplier, code) in enumerate(conf.get("ordercodes", [])):
        out.append([
            'property', supplier, code, ['id', idx+4],
            ['at', field_x, -field_y-(7.62+idx*2.54), 0],
            ['effects', ['font', ['size', 1.27, 1.27]], ['justify', 'left'],
             'hide']
        ])

    n = 4 + len(conf.get('ordercodes', []))
    out.append([
        'property', 'ki_description', conf.get('description', ''),
        ['id', n+1], ['at', 0, 0, 0],
        ['effects', ['font', ['size', 1.27, 1.27]], 'hide'],
    ])
    if len(units) > 1:
        out.append([
            'property', 'ki_locked', '',
            ['id', n+2], ['at', 0, 0, 0],
            ['effects', ['font', ['size', 1.27, 1.27]], 'hide'],
        ])

    return out


def draw_pins(groups, x0, y0, direction, length):
    out = []
    angle = 0 if direction == 'R' else 180
    pin_x = x0
    pin_y = y0
    for group in groups:
        for (name, num, t) in group:
            out.append([
                'pin', pin_types[t], 'line', ['at', pin_x, pin_y, angle],
                ['length', length],
                ['name', str(name), ['effects', ['font', ['size', 1.27, 1.27]]]],
                ['number', str(num), ['effects', ['font', ['size', 1.27, 1.27]]]],
            ])
            pin_y -= 2.54
        pin_y -= 2.54
    return out


def draw(conf, units):
    out = []

    n = longest_num(units)

    for unit_idx, unit in enumerate(units):
        if len(units) > 1:
            # For multi-unit parts, unit indices start at 1,
            # while for single-unit parts, everything is unit 0.
            unit_idx += 1
        sym = ['symbol', f"{conf['name']}_{unit_idx}_0"]
        width, height, length = geometry(unit, n)

        # Containing box
        sym.append(['rectangle',
            ['start', -width/2, height/2],
            ['end', width/2, -height/2],
            ['stroke', ['width', 0], ['type', 'default'],
             ['color', 0, 0, 0, 0]],
            ['fill', ['type', 'background']]
        ])

        # Pins
        x0 = -width/2 - length
        y0 = height/2 - 1.27
        left_pins, right_pins = unit
        if left_pins:
            sym += draw_pins(left_pins, x0, y0, "R", length)
        if right_pins:
            sym += draw_pins(right_pins, -x0, y0, "L", length)
        out.append(sym)

    return out


def library(conf):
    units = normalise_pins(conf['pins'])
    out = [
        'kicad_symbol_lib',
        ['version', 20211014],
        ['generator', 'agg_kicad.build_lib_ic'],
        ['symbol', conf['name'], ['pin_names', ['offset', 1.016]],
         ['in_bom', 'yes'], ['on_board', 'yes']],
    ]

    out[-1] += fields(conf, units)
    out[-1] += draw(conf, units)

    return sexp.generate(out)


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
        path = os.path.join(conf.get("path", ""), name.lower()+".kicad_sym")

        lib = library(conf)

        if verify and verbose:
            print("Verifying", path)

        # Check if anything has changed
        if os.path.isfile(path):
            with open(path) as f:
                oldlib = f.read()
                if lib == oldlib:
                    continue

        # If so, either verification failed or write the new files
        if verify:
            return False
        else:
            with open(path, "w") as f:
                f.write(lib)

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
