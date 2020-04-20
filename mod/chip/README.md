Name format is `SIZE[-SPECIAL]`. Examples: `0402`, `0603-LED`

## Keys
* *name*: Name
* *pad_shape*: [width, height] of the pads
* *pitch*: spacing between pad centres
* *chip_shape*: [width, height] of the chip (for Fab layer)
* *pin_shape*: [width, height] of chip pins (for Fab layer).
  Use negative widths for internal pins (e.g., chip resistors)
* *silk*: "internal", "external", "triangle", "internal_pin1", "external_pin1", or None.
  What sort of silk to draw. Default is "internal".
* *courtyard_gap*: minimum distance from footprint extreme to courtyard.
  If not specified, the default ctyd_gap is used.
* *model*:``
  {"path": <str>,
    "offset": [x,y,z],
    "scale": [x,y,z],
    "rotate": [x,y,z]}
``
   Defines which 3D model to associate with the footprint.

Except where otherwise noted, all packages are in IPC nominal environment.

Chip drawings are nominal sizes rather than maximum sizes.

All lengths are in millimetres.
