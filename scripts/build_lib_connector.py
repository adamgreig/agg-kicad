"""
build_lib_connector.py
Copyright 2015-2022 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generates conn.kicad_sym, generic connector symbols in a range of number of
rows and pins.
"""

import sys
import os.path
import sexp

def onerow(n):
    name = f'CONN_01x{n:02}'
    out = ['symbol', name,
        ['pin_names', 'hide'],
        ['in_bom', 'yes'],
        ['on_board', 'yes'],
        ['property', 'Reference', 'J', ['id', 0], ['at', -0.635, 2.54, 0],
         ['effects', ['font', ['size', 1.27, 1.27]]]],
        ['property', 'Value', name, ['id', 1], ['at', -2.54, -(n-1)/2 * 2.54, 90],
         ['effects', ['font', ['size', 1.27, 1.27]]]],
        ['property', 'Footprint', '', ['id', 2], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['property', 'Datasheet', '', ['id', 3], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['rectangle', ['start', 0, -(n-1)*2.54 - 1.27], ['end', -1.27, 1.27],
         ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
         ['fill', ['type', 'background']]],
    ]
    boxes = []
    pins = []
    for pin in range(n):
        y = -pin * 2.54
        boxes.append(
            ['rectangle', ['start', 0, y+0.127], ['end', -0.635, y-0.127],
             ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
             ['fill', ['type', 'outline']],
            ]
        )
        pins.append(
            ['pin', 'passive', 'line', ['at', 2.54, y, 180], ['length', 2.54],
             ['name', str(pin+1), ['effects', ['font', ['size', 1.27, 1.27]]]],
             ['number', str(pin+1), ['effects', ['font', ['size', 1.27, 1.27]]]],
            ]
        )
    out += boxes
    out += pins
    return out

def tworow(n):
    name = f'CONN_02x{n:02}'
    out = ['symbol', name,
        ['pin_names', 'hide'],
        ['in_bom', 'yes'],
        ['on_board', 'yes'],
        ['property', 'Reference', 'J', ['id', 0], ['at', -1.27, 2.54, 0],
         ['effects', ['font', ['size', 1.27, 1.27]]]],
        ['property', 'Value', name, ['id', 1], ['at', -1.27, -n * 2.54, 0],
         ['effects', ['font', ['size', 1.27, 1.27]]]],
        ['property', 'Footprint', '', ['id', 2], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['property', 'Datasheet', '', ['id', 3], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['rectangle', ['start', 0, -(n-1)*2.54 - 1.27], ['end', -2.54, 1.27],
         ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
         ['fill', ['type', 'background']]],
    ]
    boxes = []
    pins = []
    for pin in range(n):
        y = -pin * 2.54
        boxes += [
            ['rectangle', ['start', 0, y+0.127], ['end', -0.635, y-0.127],
             ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
             ['fill', ['type', 'outline']],
            ],
            ['rectangle', ['start', -2.54, y+0.127], ['end', -1.905, y-0.127],
             ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
             ['fill', ['type', 'outline']],
            ],
        ]
        pins += [
            ['pin', 'passive', 'line', ['at', 2.54, y, 180], ['length', 2.54],
             ['name', str(2*pin+2), ['effects', ['font', ['size', 1.27, 1.27]]]],
             ['number', str(2*pin+2), ['effects', ['font', ['size', 1.27, 1.27]]]],
            ],
            ['pin', 'passive', 'line', ['at', -5.08, y, 0], ['length', 2.54],
             ['name', str(2*pin+1), ['effects', ['font', ['size', 1.27, 1.27]]]],
             ['number', str(2*pin+1), ['effects', ['font', ['size', 1.27, 1.27]]]],
            ],
        ]
    out += boxes
    out += pins
    return out

def main(libpath, verify=False):
    out = ['kicad_symbol_lib',
        ['version', 20211014],
        ['generator', 'agg_kicad.build_lib_connector']
    ]

    for pincount in list(range(1, 26)) + [32, 36, 40]:
        out.append(onerow(pincount))
        out.append(tworow(pincount))

    lib = sexp.generate(out)

    if os.path.isfile(libpath):
        with open(libpath) as f:
            oldlib = f.read()
            if lib == oldlib:
                return True

    if verify:
        return False
    else:
        with open(libpath, 'w') as f:
            f.write(lib)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[2] == "--verify":
        if main(sys.argv[1], verify=True):
            print("OK: lib up-to-date.")
            sys.exit(0)
        else:
            print("Error: lib not up-to-date.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: {} <lib path> [--verify]".format(sys.argv[0]))
        sys.exit(1)
