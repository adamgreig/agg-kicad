"""
build_lib_switch.py
Copyright 2016-2022 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generate switch.kicad_sym, generic nPmT switch symbols.
"""

import sys
import os.path

import sexp


def switch(n, m):
    """
    Generates a generic switch symbol for an nPsT sort of switch.
    Probably won't generate a useful pin numbering when T>2.
    """

    # Convert to stupid letters for 1 and 2
    name_letters = {1: "S", 2: "D"}
    name_n = name_letters[n] if n in name_letters else str(n)
    name_m = name_letters[m] if m in name_letters else str(m)

    # Number of pins on the right is n*m, plus one per pole for spacing,
    # minus the final spacing (n starts at 1), rounded up to nearest odd
    # number so that half the height is on the 100mil grid.
    n_pins_right = n * m + n - 1
    if n_pins_right % 2 == 0:
        n_pins_right += 1
    height = 100 * (n_pins_right - 1)
    hheight = height // 2

    # Ref goes at the top, 100 above the top pin, unless only one throw
    # in which case we also need to clear the switch graphic
    refheight = hheight + 100
    if m == 1:
        refheight += 50

    # Value/name goes below, unless m is even, in which case the bottom spacer
    # isn't there so needs to be ignored
    valheight = -(hheight + 100)
    if n % 2 == 1 and m % 2 == 0:
        valheight += 100

    refheight *= 2.54/100
    valheight *= 2.54/100

    # Output component header
    name = "SWITCH_{}P{}T".format(name_n, name_m)
    out = [
        'symbol', name,
        ['pin_names', 'hide'],
        ['in_bom', 'yes'],
        ['on_board', 'yes'],
        ['property', 'Reference', 'SW', ['id', 0], ['at', 0, refheight, 0],
         ['effects', ['font', ['size', 1.27, 1.27]]]],
        ['property', 'Value', name, ['id', 1], ['at', 0, valheight, 0],
         ['effects', ['font', ['size', 1.27, 1.27]]]],
        ['property', 'Footprint', '', ['id', 2], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
        ['property', 'Datasheet', '', ['id', 3], ['at', 0, 0, 0],
         ['effects', ['font', ['size', 1.27, 1.27]], 'hide']],
    ]

    # Output drawing
    drawing = []
    pins = []
    pole_top = hheight
    for pole in range(n):

        # Draw pole
        pole_num = pole*(m+1) + 2
        pole_y = pole_top - (100 * (m - 1))//2
        if m % 2 == 0:
            pole_y -= 50
        pole_y *= 2.54/100
        drawing.append([
            'polyline',
            ['pts', ['xy', -1.27, pole_y + .254], ['xy', 1.27, pole_y + 2.286]],
            ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
            ['fill', ['type', 'none']],
        ])
        drawing.append([
            'circle', ['center', -1.27, pole_y], ['radius', .254],
            ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
            ['fill', ['type', 'none']],
        ])
        pins.append([
            'pin', 'passive', 'line', ['at', -2.54, pole_y, 0], ['length', 1.016],
            ['name', '', ['effects', ['font', ['size', 1.27, 1.27]]]],
            ['number', str(pole_num),
             ['effects', ['font', ['size', 1.27, 1.27]]]],
        ])

        for throw in range(m):
            # Draw throws
            throw_num = pole_num + throw - 1
            throw_y = pole_top - 100 * throw
            throw_y *= 2.54/100
            if throw > 0:
                throw_num += 1
            drawing.append([
                'circle', ['center', 1.27, throw_y], ['radius', .254],
                ['stroke', ['width', 0], ['type', 'default'], ['color', 0, 0, 0, 0]],
                ['fill', ['type', 'none']],
            ])
            pins.append([
                'pin', 'passive', 'line', ['at', 2.54, throw_y, 180], ['length', 1.016],
                ['name', '', ['effects', ['font', ['size', 1.27, 1.27]]]],
                ['number', str(throw_num),
                 ['effects', ['font', ['size', 1.27, 1.27]]]],
            ])

        # Move down for next pole
        pole_top -= 100 * (m + 1)

    # Draw connecting dashed line
    if n > 1:
        pole_y = hheight - (100 * (m - 1))//2 + 50
        if m % 2 == 0:
            pole_y -= 50
        for _ in range(5*(m+1)*(n-1)):
            dash_start = pole_y * 2.54/100
            dash_end = dash_start - 0.127
            drawing.append([
                'polyline',
                ['pts', ['xy', 0, dash_start], ['xy', 0, dash_end]],
                ['stroke', ['width', 0], ['type', 'dot'], ['color', 0, 0, 0, 0]],
                ['fill', ['type', 'none']],
            ])
            pole_y -= 20

    out += drawing
    out += pins
    return out


def main(libpath, verify=False):
    out = ['kicad_symbol_lib',
        ['version', 20211014],
        ['generator', 'agg_kicad.build_lib_switch'],
    ]

    for n in (1, 2, 3):
        for m in (1, 2, 3):
            out.append(switch(n, m))

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
            print("OK: lib up-to-date.")
            sys.exit(0)
        else:
            print("Error: lib not up-to-date.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: {} <lib path> [--verify]".format(sys.argv[0]))
        sys.exit(1)
