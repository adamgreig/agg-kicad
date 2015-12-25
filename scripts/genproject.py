"""
genproject.py
Copyright 2015 Adam Greig

Generate a kicad .pro project file containing all the libraries in a given
directory and otherwise empty.
"""

from __future__ import print_function
import sys
import os
import fnmatch
import datetime

EXCLUSIONS = ("agg-kicad.lib",)

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


def main(libpath, prjpath):
    prj = tpl.format(
        date=datetime.datetime.utcnow().strftime("%a %d %b %Y %H:%M:%S GMT"))
    count = 1
    for dirpath, dirnames, files in os.walk(libpath):
        dirnames.sort()
        for f in fnmatch.filter(sorted(files), "*.lib"):
            if f not in EXCLUSIONS:
                path = os.path.splitext(os.path.join(dirpath, f))[0]
                prj += "LibName{}={}\n".format(count, path)
                count += 1

    with open(prjpath, "w") as f:
        f.write(prj)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        libpath = sys.argv[1]
        prjpath = sys.argv[2]
        main(libpath, prjpath)
    else:
        print("Usage: {} <lib dir path>".format(sys.argv[0]))
        sys.exit(1)
