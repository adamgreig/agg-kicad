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


The file `agg-kicad.lib` contains all of the symbols in this library.

## General Guidelines

### Enforced automatically

* One symbol per library
    * Exception for automatically generated libraries such as `conn.lib`
* Library filename the same as the part name
* All pins on 100mil grid
* 100mil pin length for ICs and similar symbols
* No missing numbers in pin numbering sequence
* Text size 50mil (fields, pin names, pin numbers)
    * Exception for pin numbers that are words, e.g. "PAD"
* Part reference above the part
* Part name (value field) below the part
* Fields must be horizontal
* Name and reference fields must be visible unless explicitly overridden
* Other fields (footprint, datasheet, order codes) must be invisible
* ICs and similar symbols to be filled with background colour

### Must be checked manually

* Part name follows the manufacturer or common generic name
* Part designator follows IEEE 315 where possible
* Origin on/close to centre of part
* Name and reference left-aligned with left edge on non-symmetrical symbols
* Name and reference centre-aligned on symmetrical symbols

### Helpful but not mandatory

* Include Farnell order code where applicable
* Include DigiKey and RS order codes where applicable and useful
* Pre-fill with a footprint field if one is very commonly used

## Associated documentation to include in README

* Link to datasheet/web page
* Common supplier order codes
* Names of available footprints
* Has the symbol been validated in practice? Where?
* Any other notes / gotchas
