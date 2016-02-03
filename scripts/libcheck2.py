"""
libcheck.py
Copyright 2015-2016 Adam Greig

Check all library files in a directory against a set of consistency rules.
"""

from __future__ import print_function

import sys


def parse_lib(lib):
    """
    Turn lib, a string containing an EESchema Library file, into
    a list of parsed Symbol dictionaries.
    """
    liblines = lib.splitlines()
    lib = []

    # Check header
    if not liblines[0].startswith("EESchema-LIBRARY"):
        print("Error parsing library file; does not have correct header.",
              file=sys.stderr)
        return lib

    # Cut off header
    if liblines[1].startswith("#encoding"):
        liblines = liblines[2:]
    else:
        liblines = liblines[1:]

    # Accumulate symbols
    symlines = []
    for line in liblines:
        symlines.append(line)
        if line.startswith("ENDDEF"):
            lib.append(parse_sym(symlines))
            symlines = []

    # Return all the symbols we found
    return lib


def parse_sym(sym):
    header = []
    drawing = []
    for line in sym:
        if line.startswith("DRAW"):
            parse_sym_header(header)
        header.append(line)


def parse_sym_header(header):
    pass


def parse_sym_drawing(drawing):
    pass
