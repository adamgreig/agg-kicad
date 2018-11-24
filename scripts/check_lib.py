"""
check_lib.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Check all library files in a directory against a set of consistency rules.
"""

from __future__ import print_function, division

import sys
import os
import fnmatch
import re
import argparse


EXCLUSIONS = ("agg-kicad.lib", "conn.lib", "power.lib", "switch.lib",
              "tec2.lib")


re_defs = re.compile("^DEF (?P<name>[^ ]*) (?P<des>[^ ]*) ", re.MULTILINE)
re_pins = re.compile("^X (?P<name>[^ ]*) (?P<num>[^ ]*)"
                     " (?P<x>[0-9\-]*) (?P<y>[0-9\-]*) (?P<len>[0-9]*)"
                     " [A-Z] (?P<numsize>[0-9]*) (?P<namesize>[0-9]*)",
                     re.MULTILINE)
re_refn = re.compile("^F0 (?P<value>[^ ]*) (?P<x>[0-9\-]*) (?P<y>[0-9\-]*)"
                     " (?P<size>[0-9]*) (?P<orient>[VH]) (?P<visible>[IV])"
                     " (?P<hjust>[LRC]) (?P<vjust>[TBC]{1,3})", re.MULTILINE)
re_name = re.compile("^F1 (?P<value>[^ ]*) (?P<x>[0-9\-]*) (?P<y>[0-9\-]*)"
                     " (?P<size>[0-9]*) (?P<orient>[VH]) (?P<visible>[IV])"
                     " (?P<hjust>[LRC]) (?P<vjust>[TBC]{1,3})", re.MULTILINE)
re_fp = re.compile("^F2 (?P<value>[^ ]*) (?P<x>[0-9\-]*) (?P<y>[0-9\-]*)"
                   " (?P<size>[0-9]*) (?P<orient>[VH]) (?P<visible>[IV])"
                   " (?P<hjust>[LRC]) (?P<vjust>[TBC]{1,3})", re.MULTILINE)
re_ds = re.compile("^F3 (?P<value>[^ ]*) (?P<x>[0-9\-]*) (?P<y>[0-9\-]*)"
                   " (?P<size>[0-9]*) (?P<orient>[VH]) (?P<visible>[IV])"
                   " (?P<hjust>[LRC]) (?P<vjust>[TBC]{1,3})", re.MULTILINE)
re_oc = re.compile("^F[4-9] (?P<value>[^ ]*) (?P<x>[0-9\-]*) (?P<y>[0-9\-]*)"
                   " (?P<size>[0-9]*) (?P<orient>[VH]) (?P<visible>[IV])"
                   " (?P<hjust>[LRC]) (?P<vjust>[TBC]{1,3})", re.MULTILINE)
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
    nums = []
    for name, num, x, y, length, numsize, namesize in pins:
        # Check pins lie on 100mil grid
        if int(x) % 100 != 0 or int(y) % 100 != 0:
            errs.append("Pin '{}' not on 100mil grid".format(name))
        # Check pins in IC and U parts are 100mil long
        if designator in ("IC", "U") and int(length) not in (100, 150):
            errs.append("Pin '{}' not 100 or 150mil long, but part is IC or U"
                        .format(name))
        # Check pin text fields are 50mil sized
        if int(namesize) != 50 or (int(numsize) != 50 and num.isdigit()):
            errs.append("Pin '{}' font size not 50mil".format(name))
        # Collect numeric pins
        if num.isdigit():
            nums.append(int(num))

    if nums:
        expected = set(range(min(nums), max(nums)+1))
        if set(nums) != expected:
            missing = [str(x) for x in set(expected) - set(nums)]
            errs.append("Missing pins {}".format(", ".join(missing)))

        duplicates = set([str(x) for x in nums if nums.count(x) > 1])
        if duplicates:
            errs.append("Duplicated pins {}".format(", ".join(duplicates)))


def checkboxes(contents, designator, errs):
    if designator == "IC":
        boxes = re_poly.findall(contents)
        if "f" not in boxes:
            errs.append("No background-filled box/poly found, but part is IC")


def checkfields(contents, errs, prettypath):
    refn_f = re_refn.findall(contents)
    name_f = re_name.findall(contents)
    foot_f = re_fp.findall(contents)
    data_f = re_ds.findall(contents)
    code_f = re_oc.findall(contents)

    fields = ((refn_f, "reference"), (name_f, "name"), (foot_f, "footprint"),
              (data_f, "datasheet"), (code_f, "order code"))

    for field, fn in fields:
        for value, x, y, size, orient, visible, hjust, vjust in field:
            if fn in ("reference", "name"):
                if visible != "V":
                    if "#invisible{}".format(fn) not in contents:
                        errs.append("Field {} not visible".format(fn))
            else:
                if visible != "I":
                    errs.append("Field {} visible".format(fn))
            if orient != "H":
                errs.append("Field {} not horizontal".format(fn))
            if size != "50":
                errs.append("Field {} font size not 50".format(fn))

    refn_y = int(refn_f[0][2])
    name_y = int(name_f[0][2])

    if refn_y <= name_y:
        errs.append("Component reference not above component name")

    fp = foot_f[0][0][1:-1]
    if fp.startswith("agg:"):
        fp = fp.split(":")[1] + ".kicad_mod"
        path = os.path.join(prettypath, fp)
        if not os.path.exists(path):
            errs.append("Component references non-existent footprint {}"
                        .format(fp))
    elif len(fp) > 0 and ":" not in fp:
        errs.append("Footprint '{}' does not specify a library name"
                    .format(fp))


def checklib(libf, prettypath, verbose=False):
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
    checkfields(contents, errs, prettypath)

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
        for f in fnmatch.filter(files, "*.lib"):
            path = os.path.join(dirpath, f)
            if f not in EXCLUSIONS:
                result = checklib(path, prettypath, verbose)
                if not result:
                    ok = False
            elif verbose:
                print("Skipping '{}'".format(path))
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
