# PCB Footprints

## Common Guidelines
* Origin on part centre
* Pad 1 on top left
* Ensure rotational symmetry for symmetric parts
* Text has size 1mm x 1mm and thickness 0.15mm (checked automatically)
* Silk lines are 0.15mm thick (checked automatically)
* Courtyard is 0.01mm thick on 0.05mm grid (checked automatically)
* Courtyard clearance:
    * 0.20mm normally
    * 0.50mm for connectors
    * Other clearances as applicable per-package

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
