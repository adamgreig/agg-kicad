"""
build_lib_power.py
Copyright 2015-2022 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generate generic power symbols for supply and ground nets.
"""

import sys
import os.path

import sexp

PWR_NAMES = [
    "VCC", "VDD", "AVCC", "AVDD",
    "1v1", "1v2", "1v8", "2v5", "3v3", "5v", "6v5", "9v", "10v",
    "12v", "15v", "24v", "48v",
    "-5v", "-9v", "-10v", "-12v", "-15v", "-24v", "-48v",
    "VBATT", "VSHORE",
]

GND_NAMES = [
    "GND", "AGND", "DGND", "PGND", "CHASSIS", "EARTH"
]


def gnd(name):
    return [
        'symbol', name, ['power'],
        ['pin_numbers', 'hide'], ['pin_names', ['offset', 0], 'hide'],
        ['in_bom', 'no'], ['on_board', 'no'],
        ['property', 'Reference', '#PWR', ['id', 0], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['property', 'Value', name, ['id', 1], ['at', 0, -2.54, 0],
         ['effects', ['font', ['size', 1.27, 1.27]]]],
        ['property', 'Footprint', '', ['id', 2], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['property', 'Datasheet', '', ['id', 3], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['polyline', ['pts', ['xy', 0, 0], ['xy', 0, -0.762]],
         ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
         ['fill', ['type', 'none']]],
        ['polyline', ['pts', ['xy', -0.762, -0.762], ['xy', 0.762, -0.762],
                             ['xy', 0, -1.524], ['xy', -0.762, -0.762]],
         ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
         ['fill', ['type', 'background']]],
        ['pin', 'power_in', 'line', ['at', 0, 0, 180], ['length', 0], 'hide',
         ['name', name, ['effects', ['font', ['size', 1.27, 1.27]]]],
         ['number', '1', ['effects', ['font', ['size', 1.27, 1.27]]]]],
    ]


def pwr(name):
    return [
        'symbol', name, ['power'],
        ['pin_numbers', 'hide'], ['pin_names', ['offset', 0], 'hide'],
        ['in_bom', 'no'], ['on_board', 'no'],
        ['property', 'Reference', '#PWR', ['id', 0], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['property', 'Value', name, ['id', 1], ['at', 0, 2.286, 0],
         ['effects', ['font', ['size', 1.27, 1.27]]]],
        ['property', 'Footprint', '', ['id', 2], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['property', 'Datasheet', '', ['id', 3], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['polyline', ['pts', ['xy', 0, 1.27], ['xy', 0.508, 0.508]],
         ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
         ['fill', ['type', 'none']]],
        ['polyline', ['pts', ['xy', 0, 0], ['xy', 0, 1.27], ['xy', -0.508, 0.508]],
         ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
         ['fill', ['type', 'none']]],
        ['pin', 'power_in', 'line', ['at', 0, 0, 180], ['length', 0], 'hide',
         ['name', name, ['effects', ['font', ['size', 1.27, 1.27]]]],
         ['number', '1', ['effects', ['font', ['size', 1.27, 1.27]]]]],
    ]


def flag():
    return [
        'symbol', 'FLAG', ['power'],
        ['pin_numbers', 'hide'], ['pin_names', ['offset', 0], 'hide'],
        ['in_bom', 'no'], ['on_board', 'no'],
        ['property', 'Reference', '#FLG', ['id', 0], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['property', 'Value', 'FLAG', ['id', 1], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['property', 'Footprint', '', ['id', 2], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['property', 'Datasheet', '', ['id', 3], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['property', 'ki_description', 'Power flag. Adds power output to nets.',
         ['id', 4], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['polyline', ['pts', ['xy', 0, 0.508], ['xy', -0.508, 1.016],
                             ['xy', 0, 1.524], ['xy', 0.508, 1.016],
                             ['xy', 0, 0.508]],
         ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
         ['fill', ['type', 'background']]],
        ['pin', 'power_out', 'line', ['at', 0, 0, 90], ['length', 0.508],
         ['name', 'FLAG', ['effects', ['font', ['size', 1.27, 1.27]]]],
         ['number', '1', ['effects', ['font', ['size', 1.27, 1.27]]]]],
    ]


def main(libpath, verify=False):
    out = ['kicad_symbol_lib',
           ['version', 20211014], ['generator', 'agg_kicad.build_lib_power']]
    for name in PWR_NAMES:
        out.append(pwr(name))
    for name in GND_NAMES:
        out.append(gnd(name))
    out.append(flag())

    lib = sexp.generate(out)

    # Check if the library has changed
    if os.path.isfile(libpath):
        with open(libpath) as f:
            oldlib = f.read()
            if lib == oldlib:
                return True

    # If so, validation has failed or update the library file
    if verify:
        return False
    else:
        with open(libpath, "w") as f:
            f.write(lib)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[2] == "--verify":
        if main(sys.argv[1], verify=True):
            print("OK: libs up-to-date.")
            sys.exit(0)
        else:
            print("Error: lib not up-to-date.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: {} <lib path> [--verify]".format(sys.argv[0]))
        sys.exit(1)
