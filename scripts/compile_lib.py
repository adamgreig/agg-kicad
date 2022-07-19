"""
compile_lib.py
Copyright 2015-2022 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Build a single KiCAD component library from multiple input libraries.

Usage: compile_lib.py <lib path> <outfile> [--verify]

With --verify, checks that <outfile> matches the library that would be
generated, exits with 0 if match and 1 otherwise.
"""

import sys
import os
import fnmatch
import datetime
import subprocess
import sexp


def git_version(libpath):
    # Handle running inside a git hook where the presence of these environment
    # variables will cause problems
    env = os.environ.copy()
    if 'GIT_DIR' in env:
        del env['GIT_DIR']
    if 'GIT_INDEX_FILE' in env:
        del env['GIT_INDEX_FILE']

    args = ["git", "describe", "--abbrev=8", "--dirty=-dirty", "--always"]
    git = subprocess.Popen(args, cwd=libpath, env=env, stdout=subprocess.PIPE)
    return git.stdout.read().decode().strip()


def writelib(libpath, outpath):
    newlib = compilelib(libpath)
    with open(outpath, "w") as f:
        f.write(newlib)


def checklib(libpath, outpath):
    with open(outpath) as f:
        old = f.read().split("\n")
        new = compilelib(libpath).split("\n")
        # Don't compare git versions
        old[3] = new[3] = ""
        return old == new


def compilelib(libpath):
    version = git_version(libpath)
    out = ['kicad_symbol_lib',
        ['version', 20211014],
        ['generator', f'agg-kicad-compiled-{version}'],
    ]

    for dirpath, dirnames, files in os.walk(libpath):
        dirnames.sort()
        for f in fnmatch.filter(sorted(files), "*.kicad_sym"):
            with open(os.path.join(dirpath, f)) as libf:
                part = sexp.parse(libf.read(), parse_nums=True)
                if not part[2][1].startswith("agg-kicad-compiled"):
                    out += part[3:]

    return sexp.generate(out)


def usage():
    print("Usage: {} <lib path> <outfile> [--verify]".format(sys.argv[0]))
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        usage()
    else:
        libpath = sys.argv[1]
        outpath = sys.argv[2]
        if len(sys.argv) == 3:
            writelib(libpath, outpath)
        elif len(sys.argv) == 4 and sys.argv[3] == "--verify":
            if checklib(libpath, outpath):
                print("OK: '{}' is up-to-date with '{}'."
                      .format(outpath, libpath))
                sys.exit(0)
            else:
                print("Error: '{}' is not up-to-date with '{}'."
                      .format(outpath, libpath), file=sys.stderr)
                print("Please run compile_lib.py to regenerate.",
                      file=sys.stderr)
                sys.exit(1)
        else:
            usage()
