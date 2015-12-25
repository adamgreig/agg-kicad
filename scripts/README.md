# agg-kicad scripts

## xml2bom.py

This script converts a KiCAD `.xml` BOM into a text file containing:
* Any detected problems, such as duplicate parts with different order codes
* Quick-paste format order BOMs for each detected supplier
* Assembly BOM with further details on every part

To use, add this line to your BOM scripts:

`python3 "/path/to/agg-kicad/scripts/xml2bom.py" "%I" "%O.bom"`

## compilelib.py

This script generates a single `agg-kicad.lib` file containing all the 
schematic symbols in all the individual `.lib` files.

Run with `--verify` as the final argument to instead verify that the existing 
compiled library is up-to-date.

`python3 compilelib.py ../lib ../agg-kicad.lib`

## connectorlib.py

This script generates `conn.lib` containing a number of similar connectors with 
different numbers of pins.

`python3 connectorlib.py ../lib/connectors/conn.lib`

## powerlib.py

This script generates `power.lib` containing a number of power symbols with 
different names, such as `VCC`, `VDD`, `3v3`, `GND`, `DGND`, etc.

`python3 powerlib.py ../lib/power/power.lib`

## libcheck.py

This script checks all the `.lib` files in a directory and validates that they 
conform to as many of the rules as can reasonably be automatically checked.

The top of the file includes a list of library files to skip, which is set to 
the automatically-generated files that will contain presumably-valid symbols 
(but typically also many symbols, such as the compiled and connector 
libraries).

Some exclusions can be enabled inside a library file, for example 
`#invisiblename` for parts where the name is allowed to be invisible.

`python3 libcheck.py ../lib`

## pre-commit

This script is a Git hook that should be placed in `.git/hooks`. Whenever you 
commit it will check that the compiled library file `lib/agg-kicad.lib` is 
up-to-date and if not will recompile it and add it to the commit.

## genproject.py

This script creates a blank KiCAD project file containing all the schematic 
libraries in the given directory. Useful for generating a development project 
for editing schematic symbols.

`python3 scripts/genproject.py lib agg-kicad.pro`
