# agg-kicad Contributing Guidelines

Thank you for considering contributing to agg-kicad!

I am very grateful for new symbols and footprints, and of course fixes for any
errors or improvements to the build scripts.

If you are contributing a new symbol or footprint, there are a few things to
consider:

* Please provide a link to the documentation you worked from
* If you're adding a generic box symbol (most ICs and modules etc), please
  create a `.yaml` file instead of a KiCAD symbol directly; these are rendered
  to KiCAD symbols using the `build-lib-ic.py` script (called via `make`)
* If you're adding a surface mount chip device (like a resistor), please add it
  to the `build-mod-chip.py` script
* If you're adding a surface mount IC (like a DFN or QFN or QFP), please add it
  to the `build-mod-ic.py` script
* Please check out the guidelines in the `lib/README.md` and
  `agg.pretty/README.md` files for specific rules for symbols/footprints

I'm happy to accept most parts, but anything weirdly niche or specific or not
generally available might not get accepted. Feel free to check with me
beforehand.

To the extent that your contribution is copyrightable, you agree to licence it
under the same MIT licence as the rest of agg-kicad.
