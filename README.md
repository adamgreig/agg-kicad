# @adamgreig's KiCAD Library

This repository contains my personal collection of KiCAD symbols, footprints, 
and related files.

[![Build Status](https://travis-ci.org/adamgreig/agg-kicad.svg?branch=master)](https://travis-ci.org/adamgreig/agg-kicad)

## Schematic Symbols

To use, add relevant `.lib` files to your project libraries. There is one 
`.lib` file per symbol.

Alternatively add `agg-kicad.lib` from the root directory, which includes all 
symbols. This file is built using `scripts/compile_lib.py` and kept up-to-date 
automatically.

Each part contains supplier order codes and manufacturer part numbers where 
possible and sensible. Parts are drawn as per the conventions in 
`lib/README.md`, based on the KiCAD project conventions.

Check the README in each library folder for details and notes on each part.

## PCB Footprints

To use, add `agg.pretty` to your project libraries, with nickname `agg` 
recommended for compatibility with the schematic symbols.

Where possible footprints are based on the appropriate standards and follow the 
conventions in `agg.pretty/README.md`, based on the KiCAD project conventions.

## Scripts

See the README in the scripts folder for detailed information on each script.

## Makefile

You can use the Makefile to:
* Rebuild all built-from-parameter files with `make build`
    * Just libraries with `make build-libs`
    * Just modules (footprints) with `make build-mods`
* Verify all built-from-parameter files are up-to-date with `make build-verify`
* Recompile all compiled outputs (the combined `.lib` and the `.pro`) with 
  `make compile`
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
