"""
report_mod.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generate a report of all available footprints.
"""

from __future__ import print_function, division

import sys
import os
import glob

import moddraw


def main(prettypath, outpath):
    imgpath = os.path.join(outpath, "img")
    os.makedirs(imgpath, exist_ok=True)
    mods = []

    for f in glob.glob(os.path.join(prettypath, "*.kicad_mod")):
        modname = os.path.splitext(os.path.basename(f))[0]
        print("Processing", modname)
        moddraw.main(f, os.path.join(imgpath, modname + ".png"))
        mods.append(modname)

    with open(os.path.join(outpath, "index.html"), "w") as f:
        f.write("<!doctype html>\n")
        f.write("<table border=1>\n")
        for mod in mods:
            f.write("<tr><td><a href=img/{}.png>".format(mod))
            f.write("<img src=img/{}.png width=256 height=256>".format(mod))
            f.write("</a></td><td>{}</td></tr>\n".format(mod))
        f.write("</table>\n")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        prettypath = sys.argv[1]
        outpath = sys.argv[2]
        main(prettypath, outpath)
    else:
        print("Usage: {} <.pretty path> <report path>".format(sys.argv[0]))
