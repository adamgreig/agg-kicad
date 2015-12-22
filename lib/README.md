# Schematic Symbols

Directory      |  Contents
---------------|----------
`connector`    | Connectors
`ic`           | ICs including microcontrollers, amplifiers, sensors, etc
`misc`         | Other parts including generic/drawing symbols
`module`       | PCB subassemblies and modules
`passive`      | Passive and other two-terminal devices including crystals, etc
`ui`           | User interface elements including buzzers, switches, etc


## General Guidelines

* One symbol per library (exception for parameterised symbols like connectors)
* Library filename the same as the part name
* Part name follows the manufacturer designator or common generic name
* All pins on 100mil grid
* Origin on centre of part
* 100mil pin length for ICs and similar symbols
* Text size 50mil (fields, pin names, pin numbers)
* Part reference above the part
* Part name (value field) below the part
* Fields left-aligned with left-edge of part drawing
* ICs and similar symbols to be filled with background colour
* Include Farnell order code if possible
* Include DigiKey and RS order codes if desired
* Pre-fill with a footprint field if one is very commonly used

## Associated Documentation

* Link to datasheet/web page
* Common supplier order codes
* Names of available footprints
* Has the symbol been validated in practice? Where?
* Any other notes / gotchas
