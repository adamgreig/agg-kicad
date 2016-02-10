"""
compile_pro.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generate a kicad .pro project file containing all the libraries in a given
directory and otherwise empty.
"""

from __future__ import print_function, division
import sys
import os
import fnmatch
import datetime

tpl = """update={date}
version=1
last_client=kicad
[pcbnew]
version=1
LastNetListRead=
UseCmpFile=1
PadDrill=0.600000000000
PadDrillOvalY=0.600000000000
PadSizeH=1.500000000000
PadSizeV=1.500000000000
PcbTextSizeV=1.500000000000
PcbTextSizeH=1.500000000000
PcbTextThickness=0.300000000000
ModuleTextSizeV=1.000000000000
ModuleTextSizeH=1.000000000000
ModuleTextSizeThickness=0.150000000000
SolderMaskClearance=0.000000000000
SolderMaskMinWidth=0.000000000000
DrawSegmentWidth=0.200000000000
BoardOutlineThickness=0.100000000000
ModuleOutlineThickness=0.150000000000
[cvpcb]
version=1
NetIExt=net
[general]
version=1
[eeschema]
version=1
LibDir=
[eeschema/libraries]
"""


def makeprj(libpath):
    prj = tpl.format(
        date=datetime.datetime.utcnow().strftime("%a %d %b %Y %H:%M:%S GMT"))
    count = 1
    for dirpath, dirnames, files in os.walk(libpath):
        dirnames.sort()
        for f in fnmatch.filter(sorted(files), "*.lib"):
            path = os.path.join(dirpath, os.path.splitext(f)[0])
            path = path.replace("\\", "/")
            prj += "LibName{}={}\n".format(count, path)
            count += 1
    return prj


def writeprj(libpath, prjpath):
    prj = makeprj(libpath)
    with open(prjpath, "w") as f:
        f.write(prj)


def checkprj(libpath, prjpath):
    prj = makeprj(libpath).splitlines()
    with open(prjpath, "r") as f:
        oldprj = f.read().splitlines()
    return prj[1:] == oldprj[1:]


if __name__ == "__main__":
    if len(sys.argv) in (3, 4):
        libpath = sys.argv[1]
        prjpath = sys.argv[2]
        if len(sys.argv) == 3:
            writeprj(libpath, prjpath)
        elif len(sys.argv) == 4 and sys.argv[3] == "--verify":
            if checkprj(libpath, prjpath):
                print("OK: '{}' is up-to-date with '{}'."
                      .format(prjpath, libpath))
                sys.exit(0)
            else:
                print("Error: '{}' is not up-to-date with '{}'."
                      .format(prjpath, libpath), file=sys.stderr)
                print("Please run compile_pro.py to regenerate.",
                      file=sys.stderr)
                sys.exit(1)
    else:
        print("Usage: {} <lib dir path> <.pro file path> [--verify]"
              .format(sys.argv[0]))
        sys.exit(1)
