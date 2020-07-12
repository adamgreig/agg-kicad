Names in the following format: `FAMILY-PINS[-MOD][-EP][-SPECIAL]`

MOD might be "W" for wide.

SPECIAL might refer to a manufacturer's specific modified footprint.

Examples: SOIC-8, SOIC-16-W, QFN48-EP

Unless otherwise noted, all pad dimensions are as per IPC-7351B nominal,
while fab layer annotatons are as per IPC-7351B package maximums.

## Keys (QFN/QFP/DFN/DFP)

* `rows`: either 2 or 4, for dual or quad packages.
* `pins`: total number of pins
* `pins_first_row`: optional when rows is 4, number of pins in row containing
  pin 1, for rectangular chips. Must also give `row_pitch` as a tuple. Defaults
  to pins/rows i.e. a square chip. Not applicable to 2-row chips.
* `row_pitch`: spacing between centres of rows of pins, or tuple of
  [horizontal pitch, vertical pitch] only if `pins_first_row` is given,
  where horizontal pitch is pin 1 to its opposite pin.
* `pad_shape`: (width, height) of a pad for a pin.
* `ep_shape`: (width, height) of an exposed pad underneath the chip.
  Leave out this parameter to skip the exposed pad.
* `ep_mask_shape`: (width, height, w_gap, h_gap) of mask apertures on EP.
  Multiple apertures will be created to fill. Leave out this parameter to cover
  the EP in mask aperture.
* `ep_paste_shape`: (width, height, w_gap, h_gap) of paste apertures on EP.
  Multiple apertures will be created to fill. Leave out this parameter to cover
  the EP in paste aperture.
* `ep_vias`: (drill, size, gap) of via hits to put in the EP.
  Leave out this parameter to not place any vias.
* `pin_shape`: (width, height) of the chip package pins (for Fab layer).
     Use negative widths for internal pins (e.g., QFNs).

## Keys (BGA only)

* `rows`: number of rows (identified by letters)
* `cols`: number of columns (identified by numbers)
* `pad_shape`: diameter of a pad for a pin.
* `mask_shape`: diameter of solder mask opening for a pin.
* `pin_shape`: diameter of the chip package pins (for Fab layer).
* `letters`: Optional string of sequential letters to use naming rows,
  defaults to standard ABCDEFGHJKLMNPRTUVWY.

## Keys (Common)

* `name`: Name to generate footprint under
* `description`: Footprint description
* `skip_pins`: optional, list of pin numbers to skip (leaving remaining pins in
  sequential order). Generates packages like SOT-23-3. Each list entry may be
  an exact pin to skip (eg 12 or B6) or a range of numbers or letters or both
  (eg 5-8 or B3-5 or A-C6 or A-C3-5)
* `pin_pitch`: spacing between centres of adjacent pins.
* `chip_shape`: (width, height) of the actual chip package (for Fab layer).
* `silk`: "internal" or "external" or None. Default is "internal" unless
  `ep_shape` is given in or on BGAs in which case default is "external".
* `model`: dictionary containing `path` string to 3d model, and optional
  `offset`, `scale`, and `rotate` lists of [x, y, z] values.

All lengths are in millimetres.
