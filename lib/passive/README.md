# Passives

### Ant
* Generic antenna

### R, C, L, D
* Generic resistor, non-polarised capacitor, inductor, diode

### ESD Diode
* Double TVS diode
* Farnell 2368169
* Use 0402 sized footprint

### LED
* Generic LED

### SMD Xtal
* Generic 4-pin SMD crystal
* Pins 1 and 3 connected to element
* Default footprint is XTAL20x16
* Double check rotation is correct, error on shrew-u r1

### Xtal
* Generic 2-pin crystal

### TCXO with Enable
* 4-pin TCXO with enable pin
* e.g. Digikey 535-12686-ND
* Used with the ASTXR-12 footprint on shrew-u r1 successfully

### NFET, PFET
* Generic FETs
* Gate is pin 1, Source is pin 2, Drain is pin 3

### NFET_GDS, PFET_GDS
* Generic FETs
* Gate, Source, Drain have pin numbers G, D, S
