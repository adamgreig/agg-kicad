# PCB Footprints

## Common Guidelines
* Origin/anchor on part centre
* Pad 1 on the left and then at the top
* Ensure rotational symmetry for symmetric parts
* Text has size 1mm x 1mm and thickness 0.15mm (checked automatically)
* Reference and Value fields:
    * On the `F.Fab` layer (checked automatically)
    * May only be hidden for non-functional parts such as mounting holes
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
        * Other clearances as applicable per-package
* Silkscreen:
    * May be omitted only for very small footprints where inclusion would 
      impede close packing or soldering, or for non-functional parts such as 
      mounting holes
    * All lines 0.15mm thick (checked automatically)
    * Provide pin 1 indicator where applicable
    * No silk over exposed copper
    * Internal drawings where possible
        * Not for ICs with exposed pads
        * Be careful of situations where the height of the silk could cause 
          soldering issues
        * Placement alignment indications for no-lead packages will need to be 
          external
        * In general prefer less silk visible post-assembly

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
