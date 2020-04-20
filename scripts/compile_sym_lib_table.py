"""
compile_sym_lib_table.py
Copyright 2020 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generates a KiCad sym-lib-table file with all libraries in agg-kicad,
for use with the symbol editor. The generated file is for agg-kicad use
and should not generally be copied into other projects, which can instead
use the aggregate agg.lib file.
"""

from __future__ import print_function, division
import sys
import os
import fnmatch
import sexp


def maketable(libpath):
    libs = []
    for dirpath, dirnames, files in os.walk(libpath):
        dirnames.sort()
        for f in fnmatch.filter(sorted(files), "*.lib"):
            path = os.path.join(dirpath, f)
            name = os.path.splitext(os.path.basename(path))[0]
            path = path.replace("\\", "/")
            libs.append(["lib", ["name", name], ["type", "Legacy"],
                        ["uri", os.path.join("${KIPRJMOD}", path)],
                        ["options", ""], ["descr", ""]])
    return ["sym_lib_table"] + libs


def writetable(libpath, tblpath):
    tbl = maketable(libpath)
    with open(tblpath, "w") as f:
        f.write(sexp.generate(tbl))


def checktable(libpath, tblpath):
    tbl = maketable(libpath)
    with open(tblpath, "r") as f:
        old_tbl = sexp.parse(f.read(), empty_string_placeholder="")
    return tbl == old_tbl


if __name__ == "__main__":
    if len(sys.argv) in (3, 4):
        libpath = sys.argv[1]
        tblpath = sys.argv[2]
        if len(sys.argv) == 3:
            writetable(libpath, tblpath)
        elif len(sys.argv) == 4 and sys.argv[3] == "--verify":
            if checktable(libpath, tblpath):
                print("OK: '{}' is up-to-date with '{}'."
                      .format(tblpath, libpath))
                sys.exit(0)
            else:
                print("Error: '{}' is not up-to-date with '{}'."
                      .format(tblpath, libpath), file=sys.stderr)
                print("Please run compile_sym_lib_table.py to regenerate.",
                      file=sys.stderr)
    else:
        print("Usage: {} <lib dir path> <sym-lib-table path> [--verify]"
              .format(sys.argv[0]))
        sys.exit(1)
