# Schematic Symbols

Directory                |  Contents
-------------------------|----------
[`connector`](connector) | Connectors
[`ic`](ic)               | ICs including microcontrollers, amplifiers, sensors,etc
[`misc`](misc)           | Other parts including generic/drawing symbols
[`module`](module)       | PCB subassemblies and modules
[`power`](power)         | Power symbols
[`passive`](passive)     | Passive and other two-terminal devices including crystals, etc
[`ui`](ui)               | User interface elements including buzzers, switches, etc


The file `agg-kicad.lib` in the root directory contains all of the symbols in 
this library.

## General Guidelines

### Enforced automatically

* One symbol per library, except for automatically generated libraries
* Library filename the same as the part name, except for multi-symbol libraries
* All pins on 100mil grid
* 100mil pin length for ICs and similar symbols
    * Increment by 50mil when required; all pins must be the same length
* No missing numbers in pin numbering sequence
* Text size 50mil (fields, pin names, pin numbers)
    * Exception for pin numbers that are words, e.g. "PAD"
* Part reference above the part
* Part name (value field) below the part
* Fields must be horizontal
* Name and reference fields must be visible unless explicitly overridden
* Other fields (footprint, datasheet, order codes) must be invisible
* ICs and similar symbols to be filled with background colour
* The following custom fields must be present, in order:
    * MFN (Manufacturer)
    * MPN (Manufacturer's Part Number)
    * SKU (Supplier Order Code)

### Must be checked manually

* Part name follows the manufacturer's part name or common generic name
* Part designator follows IEEE 315 where possible
* Origin on/close to centre of part
* Name and reference left-aligned with left edge on non-symmetrical symbols
* Name and reference centre-aligned on symmetrical symbols

### Helpful but not mandatory

* Populate MFN and MPN if part is not generic
* Include Farnell SKU if available
* Include link to datasheet if available
* Pre-fill with a footprint field if one is typical for the part

### Other Notes

Place any other notes in the `.lib` file prefixed with `# NOTE:`.
