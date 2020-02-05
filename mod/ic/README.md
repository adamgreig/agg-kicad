Names in the following format: `FAMILY-PINS[-MOD][-EP][-SPECIAL]`

MOD might be "W" for wide.

SPECIAL might refer to a manufacturer's specific modified footprint.

Examples: SOIC-8, SOIC-16-W, QFN48-EP

Unless otherwise noted, all pad dimensions are as per IPC-7351B nominal,
while fab layer annotatons are as per IPC-7351B package maximums.

## Keys
* rows: either 2 or 4, for dual or quad packages.
* pins: total number of pins
* pins_first_row: optional when rows is 4, number of pins in row containing
  pin 1, for rectangular chips. Must also give row_pitch as a tuple. Defaults to pins/rows i.e. a square chip. Not applicable to 2-row chips.
* skip_pins: optional, list of pin numbers to skip (leaving remaining pins in
  sequential order). Generates packages like SOT-23-3.
* pin_pitch: spacing between centres of adjacent pins.
* row_pitch: spacing between centres of rows of pins, or tuple of
  [horizontal pitch, vertical pitch] only if pins_first_row is given, where horizontal pitch is pin 1 to its opposite pin.
* pad_shape: (width, height) of a pad for a pin.
* ep_shape: (width, height) of an exposed pad underneath the chip.
  Leave out this parameter to skip the exposed pad.
* ep_mask_shape: (width, height, w_gap, h_gap) of mask apertures on EP.
  Multiple apertures will be created to fill. Leave out this parameter to cover the EP in mask aperture.
* ep_paste_shape: (width, height, w_gap, h_gap) of paste apertures on EP.
  Multiple apertures will be created to fill. Leave out this parameter to cover the EP in paste aperture.
* ep_vias: (drill, size, gap) of via hits to put in the EP.
  Leave out this parameter to not place any vias.
* chip_shape: (width, height) of the actual chip package (for Fab layer).
* pin_shape: (width, height) of the chip package pins (for Fab layer).
     Use negative widths for internal pins (e.g., QFNs).
* silk: "internal" or "external" or None.
  Default is "internal" unless ep_shape is given in which case
 default is "external".
* model: ``{"path": <str>,
  "offset": [x,y,z],
  "scale": [x,y,z],
  "rotate": [x,y,z]}``
 Defines which 3D model to associate with the footprint.

All lengths are in millimetres.
