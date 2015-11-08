# agg-kicad scripts

## xml2bom.py

This script converts a KiCAD `.xml` BOM into a text file containing:
* Any detected problems, such as duplicate parts with different order codes
* Quick-paste format order BOMs for each detected supplier
* Assembly BOM with further details on every part

To use, add this line to your BOM scripts:

```
python3 "/path/to/agg-kicad/scripts/xml2bom.py" "%I" "%O.bom"
```
