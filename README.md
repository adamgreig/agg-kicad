# @adamgreig's KiCAD Library

This repository contains my personal collection of KiCAD symbols, footprints, 
and related files.

[![Build Status](https://travis-ci.org/adamgreig/agg-kicad.svg?branch=master)](https://travis-ci.org/adamgreig/agg-kicad)

## Schematic Symbols

To use, add relevant `.lib` files to your project libraries. There is one 
`.lib` file per symbol.

Alternatively add `agg-kicad.lib` from the root directory, which includes all 
symbols. This file is built using `scripts/compilelib.py` and kept up-to-date 
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

You can use the Makefile to regenerate all automatically-generated files with 
`make build`, and to run all the automatic checks with `make check`. Travis-CI 
is configured to run `make check` to report on build status, and there is a
`pre-commit` hook in `scripts/` to run `check` locally.

## Licence

Until a reasonable level of stability is reached, this library is "all rights 
reserved". I intend to release it under an open source licence once I've 
completed a project using just this library.
