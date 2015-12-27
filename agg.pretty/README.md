# PCB Footprints

## Common Guidelines
* Origin on part centre
* Pad 1 on top left
* Ensure rotational symmetry for symmetric parts
* Text has size 1mm x 1mm and thickness 0.15mm (checked automatically)
* Reference and Value fields:
    * On the `F.Fab` layer (checked automatically)
    * Not hidden (checked automatically)
    * As close as possible to the part without overlapping
    * If the part is usually arrayed vertically, place on left and right
    * If the part is usually arrayed horizontally, place on top and bottom
    * Otherwise, prefer top and bottom
    * Reference on top or left
* Fabrication Layer:
    * Include reasonably accurate part drawing
* Courtyard:
    * Lines 0.01mm thick on 0.05mm grid (checked automatically)
    * Clearance:
        * 0.20mm normally
        * 0.50mm for connectors
        * Other clearances as applicable per-package
* Silkscreen:
    * All lines 0.15mm thick (checked automatically)
    * Internal drawings where possible

## Associated Documentation
* Has the footprint been validated in practice? With what symbol? Where?
* Link to any specific layout recommendations or requirements
* Any other notes / gotchas

Footprints in `unchecked/` have not been standardised or documented yet.

## Footprints

### 0201, 0402, 0603, 0805, 1206

Imperial sized chip device.

 * Pads are half the width of the device
 * Pads are the same or slightly taller than the device
 * Clearance and courtyards are all 0.2mm from the pad edges
 * Fabrication layer shows typical device and terminal size
 * Generally all tested in production but are by no means process-optimised

### LED0603

0603 (aka 1.6mm x 0.8mm) sized LED.

 * Standard 0603 footprint pads
 * LED polarity arrow with pin 1 as cathode
 * Farnell codes:
    * Red 2290329
    * Green 2290328
    * Orange 2290330 ("yellow")
    * Blue 1686062

### SOIC8, SOIC16

Standard SOIC footprints.

 * Used successfully
 * `-W` for wide variant
