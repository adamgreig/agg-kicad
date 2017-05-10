# PCB Footprints

## Common Guidelines
* Origin/anchor on part centre
* Pad 1 on the left and then at the top
* Ensure rotational symmetry for symmetric parts
* Text has size 1mm x 1mm and thickness 0.15mm (checked automatically)
* Aim to conform to IPC-7351B footprint design
* Reference and Value fields:
    * On the `F.Fab` layer (checked automatically)
    * May only be hidden for non-functional parts such as mounting holes
    * Place just outside the part courtyard, without overlapping the part
    * If the part is usually arrayed vertically, place on left and right, with 
      text running vertically
    * If the part is usually arrayed horizontally, place on top and bottom, 
      with text horizontal
    * Otherwise, prefer top and bottom
    * Reference on top or left, value on bottom or right
* Fabrication Layer:
    * Include reasonably accurate part drawing
* Courtyard:
    * Lines 0.01mm thick on 0.05mm grid (checked automatically)
    * Clearance:
        * 0.25mm normally
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

### 0201, 0201-L, 0402, 0402-L, 0603, 0603-L, 0805, 1206

Imperial sized chip device.

 * Footprints are IPC-7351B compliant
 * Default NOMINAL environment, `-L` parts in LEAST environment
 * Clearance and courtyards are all 0.25mm from the pad edges
 * Fabrication layer shows typical device and terminal size
 * Generally all tested in production but are by no means process-optimised

### 0603-LED

0603 (aka 1.6mm x 0.8mm) sized LED.

 * Standard 0603 footprint pads
 * LED polarity arrow with pin 1 as cathode
 * Farnell codes:
    * Red 2290329
    * Green 2290328
    * Amber 2290330 ("yellow")
    * Blue 1686062

### 0805-LED

0805 (aka 2.0mm x 1.25mm) sized LED.

 * Standard 0805 footprint pads
 * LED polarity arrow with pin 1 as cathode
 * Farnell codes:
    * Red 5790840
    * Green 5790852
    * Yellow 5790876
    * Orange 5790864
    * Blue 8554749

### SOIC, MSOP, LQFP, QFN, DFN, LGA, LPCC, others

Standard footprints, either from IPC-7351B in nominal environments or otherwise 
modified for a specific package or device.

Generated automatically by `scripts/icmod.py`. Please see the notes by each 
footprint in that script for further details.

### MICROUSB_MOLEX_47589-0001

MicroUSB connector.

 * Farnell 1568023
 * Not tested yet
 * Bottom mount (so USB cables will be upside down if footprint is on top)
 * Footprint uses round drill hits for oblong slots
 * Probably wants hand soldering the through connections

### MICROSD_MOLEX_503398-1892

MicroSD card holder.

 * Farnell 2358234
 * Used successfully

### M3_HOLE, M3_MOUNT

M3 sized mounting holes.

 * The `M3_MOUNT` variant includes a no-mask region with extra drill hits for a 
   locking washer.
 * The `M3_HOLE` courtyard does _not_ include space for a bolt head or washer 
   (as it may not always be required) so be sure to check this or use the 
   `M3_MOUNT` variant. 

### WIREPAD

3mm diameter circular copper pad. Useful for particularly large testpoints and 
pads for soldering wires to.

### PowerFLAT5x6

Dual switching N-MOSFET (not linked), 9mΩ Rdson.

 * STL15DN4F5
 * http://www.st.com/web/en/resource/technical/document/datasheet/CD00279555.pdf

### PowerPair3x3

Dual switching N-MOSFET totem pole, 14mΩ (upper) and 7mΩ (lower) Rdson.

 * SiZ340DT
 * http://www.vishay.com/docs/62877/siz340dt.pdf

### PowerPAK SC-75-6L-Single

Single switching N/P MOSFET.

 * SiB452DK, SiB433EDK
 * http://www.vishay.com/docs/68832/sib452dk.pdf
 * http://www.vishay.com/docs/65652/sib433ed.pdf

### PowerPAK-SO-8

Single switching P-MOSFET, 3mΩ Rdson.

 * Si7157DP
 * http://www.vishay.com/docs/62860/si7157dp.pdf

### SON2x2

Single switching P-MOSFET, 59mΩ Rdson.

 * CSD25310Q2
 * http://www.ti.com/lit/ds/symlink/csd25310q2.pdf

### VML1006

Single switching N MOSFET.

 * RV2C010UN
 * http://rohmfs.rohm.com/en/products/databook/datasheet/discrete/transistor/mosfet/rv2c010unt2l-e.pdf

### VLS201610HBX-1

VLS201610HBX-1 Inductor series.

 * https://product.tdk.com/info/en/catalog/datasheets/inductor_commercial_power_vls201610hbx-1_en.pdf
