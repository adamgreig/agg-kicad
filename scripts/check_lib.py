"""
check_lib.py
Copyright 2015-2022 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Check all library files in a directory against a set of consistency rules.
"""

import sys
import os
import fnmatch
import re
import argparse
import sexp


EXCLUDE = {
    'one_symbol': ['power', 'conn', 'switch', 'switch_mom'],
    'pin_grid': [],
    'pin_length': ['opa455'],
    'pin_font': [],
    'missing_pins': ['tec2', 'tel10', 'relay_no'],
    'duplicate_pins': ['siz340dt'],
    'missing_box': [],
    'invisible_ref': ['power'],
    'invisible_val': ['power', 'sj2', 'sj2_nc', 'sj3', 'testpad', 'esd_diode'],
    'property_horizontal': ['conn'],
    'property_font': [],
    'ref_above_val': ['power'],
}


def excludes(libf):
    name = os.path.splitext(os.path.basename(libf))[0].lower()
    return [k for k in EXCLUDE if name in EXCLUDE[k]]


class Property:
    def __init__(self, cfg):
        self.cfg = cfg
        self.key = cfg[1]
        self.val = cfg[2]
        self.effects = [p for p in cfg if p and p[0] == 'effects'][0]
        self.font = [p for p in self.effects if p and p[0] == 'font'][0]
        self.font_size = [(float(p[1]), float(p[2])) for p in self.font
                          if p[0] == 'size'][0]
        self.hidden = any(p == 'hide' for p in self.effects)
        if any(p and p[0] == 'at' for p in cfg):
            self.at = [p[1:] for p in cfg if p and p[0] == 'at'][0]
            self.x = float(self.at[0])
            self.y = float(self.at[1])
            self.rot = float(self.at[2])



class Pin:
    def __init__(self, cfg):
        assert cfg[0] == 'pin'
        self.cfg = cfg
        self.etype = cfg[1]
        self.style = cfg[2]
        self.at = [c[1:] for c in cfg if c and c[0] == 'at'][0]
        self.x = float(self.at[0])
        self.y = float(self.at[1])
        self.rot = float(self.at[2])
        self.length = [float(c[1]) for c in cfg if c and c[0] == 'length'][0]
        self.prop_name = [Property(c) for c in cfg if c and c[0] == 'name'][0]
        self.prop_num = [Property(c) for c in cfg if c and c[0] == 'number'][0]
        self.name = self.prop_name.key
        self.num = self.prop_num.key


class Symbol:
    def __init__(self, cfg):
        assert cfg[0] == 'symbol'
        self.cfg = cfg
        self.name = cfg[1]
        self.props = [Property(p) for p in cfg if p and p[0] == 'property']
        self.prop_ref = [p for p in self.props if p.key == 'Reference'][0]
        self.prop_val = [p for p in self.props if p.key == 'Value'][0]
        self.prop_fp  = [p for p in self.props if p.key == 'Footprint'][0]
        self.ref = self.prop_ref.val
        self.val = self.prop_val.val
        self.fp = self.prop_fp.val
        self.pins = [Pin(p) for p in cfg if p and p[0] == 'pin']
        self.polys = [p for p in cfg if p and p[0] == 'polyline']
        self.rects = [p for p in cfg if p and p[0] == 'rectangle']
        for subsym in [s for s in cfg if s and s[0] == 'symbol']:
            self.pins += [Pin(p) for p in subsym if p and p[0] == 'pin']
            self.polys += [p for p in subsym if p and p[0] == 'polyline']
            self.rects += [p for p in subsym if p and p[0] == 'rectangle']


def is_multiple(n, m):
    a = n % m
    return a < 1e-10 or (m - a) < 1e-10


def check_symbols(symbols, libf, exclusions, errs):
    if 'one_symbol' not in exclusions:
        if len(symbols) > 1:
            errs.append(f"Found more than one symbol in library {libf}")
        elif len(symbols) == 0:
            errs.append(f"Did not find any symbols in library {libf}")
        symbol = symbols[0]
        libname = os.path.splitext(os.path.basename(libf))[0].lower()
        if symbol.name.lower() != libname:
            errs.append(f"Symbol name {symbol.name} does not match library {libf}")
        if symbol.val.lower() != symbol.name.lower():
            errs.append(f"Symbol value {symbol.val} does not match name {symbol.name}")


def check_pins(symbol, exclusions, errs):
    nums = []
    nums_numeric = []
    for pin in symbol.pins:
        # Check pins lie on 100mil grid
        if 'pin_grid' not in exclusions:
            if not is_multiple(pin.x, 2.54) or not is_multiple(pin.y, 2.54):
                errs.append(f"Pin {pin.name} not on 100mil grid")
        if 'pin_length' not in exclusions:
            if symbol.ref in ("IC", "U") and pin.length not in (2.54, 3.81):
                errs.append(f"Pin {pin.name} not 100 or 150mil long")
        if 'pin_font' not in exclusions:
            if pin.prop_name.font_size != (1.27, 1.27):
                errs.append(f"Pin {pin.name} font not 50mil")
            if pin.num.isdigit() and pin.prop_num.font_size != (1.27, 1.27):
                errs.append(f"Pin {pin.name} font not 50mil")
        nums.append(pin.num)
        if pin.num.isdigit():
            nums_numeric.append(int(pin.num))

    if 'missing_pins' not in exclusions and nums_numeric:
        expected = set(range(min(nums_numeric), max(nums_numeric)+1))
        if set(nums_numeric) != expected:
            missing = [str(x) for x in set(expected) - set(nums_numeric)]
            errs.append(f"{symbol.name} missing pins {missing}")

    if 'duplicate_pins' not in exclusions and nums:
        duplicates = set([str(x) for x in nums if nums.count(x) > 1])
        if duplicates:
            errs.append(f"{symbol.name} has duplicate pins {duplicates}")



def check_drawings(symbol, exclusions, errs):
    if symbol.val == "IC" and 'missing_box' not in exclusions:
        got_box = False
        for rect in symbol.rects:
            for p in rect:
                if p[0] == 'fill':
                    for q in p:
                        if q[0] == 'type':
                            if q[1] == "background":
                                got_box = True
        if not got_box:
            errs.append("No background-filled box/poly found, but part is IC")


def check_fields(symbol, exclusions, errs, prettypath):
    if 'invisible_ref' not in exclusions and symbol.prop_ref.hidden:
        errs.append(f"{symbol.name} reference field hidden")
    if 'invisible_val' not in exclusions and symbol.prop_val.hidden:
        errs.append(f"{symbol.name} value field hidden")
    if 'property_horizontal' not in exclusions:
        if any(p.rot != 0 for p in symbol.props):
            errs.append(f"{symbol.name} field not horizontal")
    if 'property_font' not in exclusions:
        if any(p.font_size != (1.27, 1.27) for p in symbol.props):
            errs.append(f"{symbol.name} field font size not 50mil")
    if 'ref_above_val' not in exclusions:
        if symbol.prop_ref.y <= symbol.prop_val.y:
            errs.append(f"{symbol.name} reference not above value")
    if symbol.fp.startswith("agg:"):
        fp = symbol.fp.split(":")[1] + ".kicad_mod"
        path = os.path.join(prettypath, fp)
        if not os.path.exists(path):
            errs.append(f"Component references non-existant footprint {fp}")
    elif len(symbol.fp) > 0 and ":" not in symbol.fp:
        errs.append(f"Footprint {symbol.fp} doesn't specify a library name")


def checklib(libf, prettypath, verbose=False):
    errs = []
    exclusions = excludes(libf)

    with open(libf) as f:
        contents = sexp.parse(f.read())

    symbols = []
    for node in contents:
        if node[0] == 'symbol':
            symbols.append(Symbol(node))

    check_symbols(symbols, libf, exclusions, errs)

    for symbol in symbols:

        # Check pins
        check_pins(symbol, exclusions, errs)

        # If part is an IC check at least one filled box/polyline is present
        check_drawings(symbol, exclusions, errs)

        # Check fields
        check_fields(symbol, exclusions, errs, prettypath)

    if len(errs) == 0:
        if verbose:
            print("Checked '{}': OK".format(libf))
        return True
    else:
        print("Checked '{}': Error:".format(libf), file=sys.stderr)
        for err in errs:
            print("    " + err, file=sys.stderr)
        print("", file=sys.stderr)
        return False


def main(libpath, prettypath, verbose=False):
    ok = True
    for dirpath, dirnames, files in os.walk(libpath):
        dirnames.sort()
        files.sort()
        for f in fnmatch.filter(files, "*.kicad_sym"):
            path = os.path.join(dirpath, f)
            result = checklib(path, prettypath, verbose)
            if not result:
                ok = False
    return ok

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("libpath", type=str, help=
                        "Path to libraries")
    parser.add_argument("prettypath", type=str, help=
                        "Path to footprints")
    parser.add_argument("--verbose", action="store_true", help=
                        "Print out every library checked even if OK or "
                        "skipped.")
    args = vars(parser.parse_args())
    result = main(**args)
    sys.exit(0 if result else 1)
