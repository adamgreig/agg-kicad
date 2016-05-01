# agg-kicad scripts

You'll probably need to install PyYAML first:
`sudo apt-get install python-yaml` or `sudo pip install pyyaml` or so on.


## Builders

These scripts generate `.lib` and `.kicad_mod` files based on parameters inside 
the script. They typically are used to automate creation of tedious or similar 
parts.

Run with `--verify` as the final argument to instead verify that the existing 
compiled file is up-to-date (returns exit status 0 if up to date, 1 otherwise).

### build_lib_connector.py

This script generates `conn.lib` containing a number of similar connectors with 
different numbers of pins.

`python3 build_lib_connector.py ../lib/connectors/conn.lib`

### build_lib_ic.py

This script generates multiple `.lib` files, one per IC, configured by `.yaml`
files inside the library path you point it at.

`python3 build_lib_ic.py ../lib/`

### build_lib_power.py

This script generates `power.lib` containing a number of power symbols with 
different names, such as `VCC`, `VDD`, `3v3`, `GND`, `DGND`, etc.

`python3 powerlib.py ../lib/power/power.lib`

### build_mod_chip.py

Generate IPC-compliant chip packages. The list of packages to generate and 
their parameters are specified at the start of the file.

`python3 build_mod_chip.py ../agg.pretty/`

### build_mod_ic.py

Generate IC footprints for dual and quad packages. The list of packages to 
generate and their parameters are specified at the start of the file.

`python3 build_mod_ic.py ../agg.pretty/`

### build_mod_jstpa.py

Generate JST-PA connector footprints in top/side entry, pth and smd, in 
different pin counts.

`python3 build_mod_jstpa.py ../agg.pretty/`

## Checkers

These scripts check `.lib` and `.kicad_mod` files against a set of rules. They 
return with exit code 0 if all checks passed.

### check_lib.py

This script checks all the `.lib` files in a directory and validates that they 
conform to as many of the rules as can reasonably be automatically checked.

The top of the file includes a list of library files that are automatically 
generated, which are allowed to include more than one part per library.

Some exceptions can be enabled inside a library file, for example 
`#invisiblename` for parts where the name is allowed to be invisible and 
`#invisiblereference` where the reference may be invisible.

`python3 libcheck.py ../lib`

### check_mod.py

This script checks footprint module files in a directory against consistency 
rules.

`python3 scripts/modcheck.py agg.pretty`

## Compilers

These scripts generate an output by combining many existing files.

Run with `--verify` as the final argument to instead verify that the existing 
compiled file is up-to-date (returns exit status 0 if up to date, 1 otherwise).

### compile_lib.py

This script generates a single `agg-kicad.lib` file containing all the 
schematic symbols in all the individual `.lib` files.

Run with `--verify` as the final argument to instead verify that the existing 
compiled library is up-to-date.

`python3 compilelib.py ../lib ../agg-kicad.lib`

### compile_pro.py

This script creates a blank KiCAD project file containing all the schematic 
libraries in the given directory. Useful for generating a development project 
for editing schematic symbols.

`python3 genproject.py ../lib ../agg-kicad.pro`

## Other Scripts

### xml2bom.py

This script converts a KiCAD `.xml` BOM into a text file containing:
* Any detected problems, such as duplicate parts with different order codes
* Quick-paste format order BOMs for each detected supplier
* Assembly BOM with further details on every part

To use, add this line to your BOM scripts:

`python3 "/path/to/agg-kicad/scripts/xml2bom.py" "%I" "%O.bom"`

### pre-commit

This script is a Git hook that should be placed in `.git/hooks`. It will:

* Check that all built objects are up to date, stopping the commit if not
* Check that all the checks pass, stopping the commit if not

### post-commit

This script is a Git hook that should be placed in `.git/hooks`. After any 
commit it will check any compiled objects are up to date, and rebuild and 
commit them if not.

### moddraw.py

Render `.kicad_mod` files to PNGs. Used by `modreport.py` to generate images 
for the report.

### modreport.py

Generate an HMTL report of all the modules in a library, including rendered 
images. Not currently very sophisticated or automated.

### panelise.py

Step-repeat a `.kicad_pcb` PCB with a given pitch and number of repeats, 
generating a new `.kicad_pcb` file. Does not yet support any additional 
panelisation features like tabs, alignment holes, fiducials, etc.

`python3 panelise.py /tmp/in.kicad_pcb 2 30 2 10 /tmp/out.kicad_pcb`

## Utility Modules

### sexp.py

Parse and generate s-expressions for KiCAD pcbnew files.

### kicad_mod.py

Helper functions for generating `.kicad_mod` files.
