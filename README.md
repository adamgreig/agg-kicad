# @adamgreig's KiCAD Library

This repository contains my collection of KiCAD symbols, footprints,
and related files.

Every symbol and footprint is very carefully checked against either the
relevant standard (generally IPC-7351B) or specific manufacturer footprints.
Many are procedurally generated from a simple set of dimensions, which ensures
consistency and correctness. My objective is to have a useful collection of
correct parts that all look consistent and work well together.

I encourage other people to use these parts; they're all licensed under a
permissive MIT licence and it's easy to simply copy one or two files from the
repository, or submodule the entire repo.

Contributions are also very welcome; please open a pull request and I will
carefully review the proposed additions. All contributions are likewise
licensed under the MIT licence.

A number of automatic rules are checked against every footprint and symbol on
each commit by the build system. The current status is:
[![Build Status](https://travis-ci.org/adamgreig/agg-kicad.svg?branch=master)](https://travis-ci.org/adamgreig/agg-kicad)

## Schematic Symbols

To use, add relevant `.kicad_sym` files to your project libraries. There is one 
`.kicad_sym` file per symbol.

Alternatively add `agg-kicad.kicad_sym` from the root directory, which includes
all symbols. This file is built using `scripts/compile_lib.py` and kept
up-to-date automatically.

Each part contains supplier order codes and manufacturer part numbers where 
possible and sensible. Parts are drawn as per the conventions in 
`lib/README.md`, based on the KiCAD project conventions.

Symbols for many ICs and other "black-box" parts are drawn automatically from
`.yaml` files in the relevant directories, using the `build-lib-ic.py` script.
Check some of these out for an example of the syntax etc.

Check the README in each library folder for details and notes on each part.

## PCB Footprints

To use, add `agg.pretty` to your project libraries, with nickname `agg` 
recommended for compatibility with the schematic symbols.

Where possible footprints are based on the appropriate standards and follow the 
conventions in `agg.pretty/README.md`, based on the KiCAD project conventions.

Many footprints for 2-terminal chip devices and 2- or 4- row SMD ICs are 
automatically generated using the `build-mod-chip.py` and `build-mod-ic.py` 
scripts, which contain the parametric specifications for all the footprints 
they should build. This includes things like 0402 resistors, DFN and QFP ICs, 
and similar sorts of footprints.

## StickerBOM

StickerBOM is a script to convert your BOM into a PDF to print onto sticker 
labels, one label per BOM item. The labels have a drawing of the PCB to show 
you where that item goes, which makes hand assembly a lot nicer!

Check the [wiki page](https://github.com/adamgreig/agg-kicad/wiki/StickerBOM) 
for more information on StickerBOM.

## Scripts

See the README in the scripts folder for detailed information on each script.

The only requirement is PyYAML for some of the build scripts:
`sudo pip install pyyaml` or similar.

## Makefile

You can use the Makefile to:
* Rebuild all built-from-parameter files with `make build`
    * Just libraries with `make build-libs`
    * Just modules (footprints) with `make build-mods`
* Verify all built-from-parameter files are up-to-date with `make build-verify`
* Recompile all compiled outputs with `make compile`
* Verify all compiled outputs are up-to-date with `make compile-verify`
* Verify both built and compiled outputs with `make verify`
* Check all files against rules with `make check`
    * Just libraries with `make check-lib`
    * Just modules with `make check-mod`

Travis-CI is configured to run `make check` and `make verify` and reports the 
resulting status as the build status:
[![Build 
Status](https://travis-ci.org/adamgreig/agg-kicad.svg?branch=master)](https://travis-ci.org/adamgreig/agg-kicad)

Additionally in `scripts/` is `pre-commit` that stops any commits that do not 
pass `make check` and `make build-verify`, and `post-commit` that runs `make 
compile-verify` and if any compiled files are not up to date, recompiles them 
and commits the result. Copy these to `.git/hooks` for use.

## Licence

All content licensed under the MIT licence. See `LICENSE`.
