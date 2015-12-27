"""
libcheck.py
Copyright 2015 Adam Greig

Check all library files in a directory against a set of consistency rules.
"""

from __future__ import print_function

import sys
import os
import fnmatch
import re


EXCLUSIONS = ("agg-kicad.lib", "conn.lib", "power.lib")


re_defs = re.compile("^DEF (?P<name>[^ ]*) (?P<des>[^ ]*) ", re.MULTILINE)
re_pins = re.compile("^X (?P<name>[^ ]*) (?P<num>[^ ]*)"
                     " (?P<x>[0-9\-]*) (?P<y>[0-9\-]*) (?P<len>[0-9]*)"
                     " [A-Z] (?P<numsize>[0-9]*) (?P<namesize>[0-9]*)",
                     re.MULTILINE)
re_refn = re.compile("^F0 (?P<value>[^ ]*) (?P<x>[0-9\-]*) (?P<y>[0-9\-]*)"
                     " (?P<size>[0-9]*) (?P<orient>[VH]) (?P<visible>[IV])"
                     " (?P<hjust>[LRC]) (?P<vjust>[TBC]{1,3})",
                     re.MULTILINE)
re_name = re.compile("^F1 (?P<value>[^ ]*) (?P<x>[0-9\-]*) (?P<y>[0-9\-]*)"
                     " (?P<size>[0-9]*) (?P<orient>[VH]) (?P<visible>[IV])"
                     " (?P<hjust>[LRC]) (?P<vjust>[TBC]{1,3})",
                     re.MULTILINE)
re_poly = re.compile("^[SP] .* (?P<fill>[NfF])$", re.MULTILINE)


def checkdefs(contents, libf, errs):

    # Check there's only one symbol in the library
    n_defs = re_defs.findall(contents)
    if len(n_defs) > 1:
        errs.append("Found more than one component in library")
    elif len(n_defs) == 0:
        errs.append("Did not find any components in library")

    # Check symbol name matches library name
    partname = n_defs[0][0]
    designator = n_defs[0][1]
    libname = os.path.split(libf)[-1].split(".")[0]
    if partname.lower() != libname:
        errs.append("Part name '{}' does not match library name '{}'"
                    .format(partname, libname))

    return partname, designator


def checkpins(contents, designator, errs):
    pins = re_pins.findall(contents)
    nums = set()
    for name, num, x, y, length, numsize, namesize in pins:
        # Check pins lie on 100mil grid
        if int(x) % 100 != 0 or int(y) % 100 != 0:
            errs.append("Pin '{}' not on 100mil grid".format(name))
        # Check pins in IC and U parts are 100mil long
        if designator in ("IC", "U") and int(length) != 100:
            errs.append("Pin '{}' not 100mil long, but part is IC or U"
                        .format(name))
        # Check pin text fields are 50mil sized
        if int(namesize) != 50 or (int(numsize) != 50 and num.isdigit()):
            errs.append("Pin '{}' font size not 50mil".format(name))
        # Collect numeric pins
        if num.isdigit():
            nums.add(int(num))

    if nums:
        expected = set(range(min(nums), max(nums)+1))
        if nums != expected:
            missing = [str(x) for x in set(expected) - set(nums)]
            errs.append("Missing pins {}".format(", ".join(missing)))


def checkboxes(contents, designator, errs):
    if designator == "IC":
        boxes = re_poly.findall(contents)
        if "f" not in boxes:
            errs.append("No background-filled box/poly found, but part is IC")


def checkfields(contents, errs):
    refn_f = re_refn.findall(contents)
    name_f = re_name.findall(contents)

    for field, fn in (refn_f, "reference"), (name_f, "name"):
        for value, x, y, size, orient, visible, hjust, vjust in field:
            if visible != "V":
                if "#invisible{}".format(fn) not in contents:
                    errs.append("Component {} field not visible".format(fn))
            if orient != "H":
                errs.append("Component {} field not horizontal".format(fn))
            if size != "50":
                errs.append("Component {} field font size not 50".format(fn))

    refn_y = int(refn_f[0][2])
    name_y = int(name_f[0][2])

    if refn_y <= name_y:
        errs.append("Component reference not above component name")


def checklib(libf):
    errs = []

    # Check if there's a corresponding .dcm file
    dcmpath = ".".join(libf.split(".")[:-1]) + ".dcm"
    if not os.path.isfile(dcmpath):
        errs.append("No corresponding DCM found")

    with open(libf) as f:
        contents = f.read()

    # Check there's only one symbol and its name matches the library file
    partname, designator = checkdefs(contents, libf, errs)

    # Check pins
    checkpins(contents, designator, errs)

    # If part is an IC check at least one filled box/polyline is present
    checkboxes(contents, designator, errs)

    # Check fields
    checkfields(contents, errs)

    if len(errs) == 0:
        print("Checked '{}': OK".format(libf))
        return True
    else:
        print("Checked '{}': Error:".format(libf), file=sys.stderr)
        for err in errs:
            print("    " + err, file=sys.stderr)
        print("", file=sys.stderr)
        return False


def main(libpath):
    ok = True
    for dirpath, dirnames, files in os.walk(libpath):
        dirnames.sort()
        files.sort()
        for f in fnmatch.filter(files, "*.lib"):
            path = os.path.join(dirpath, f)
            if f not in EXCLUSIONS:
                result = checklib(path)
                if not result:
                    ok = False
            else:
                print("Skipping '{}'".format(path))
    return ok

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <lib path>".format(sys.argv[0]))
        sys.exit(1)
    else:
        libpath = sys.argv[1]
        success = main(libpath)
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
