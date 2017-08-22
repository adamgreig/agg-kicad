"""
    ibis2yaml.py
    Copyright 2017 Russ Garrett
    Licensed under the MIT licence, see LICENSE file for details.

    Convert the pin names from an IBIS file (such as provided by
    ST for the STM32 chips) into YAML suitable for putting into
    a symbol definition file.
"""
import sys
import re
import yaml


def parse(f):
    results = []
    for line in f:
        if line[0] == '|':
            continue
        key = line.split(' ', 1)[0]
        if key == '[Pin]':
            # We're only interested in the [Pin] section here
            for line in f:
                if line[0] == '[':
                    break
                # Some lines are commented out with a | but still have useful info.
                line = line.strip().lstrip('|').split()
                if len(line) < 2:
                    continue

                if re.match(r'^[0-9]+$', line[0]):
                    pin = int(line[0])
                else:
                    pin = str(line[0])

                # Guess pin types for common labels
                if re.match(r'^(VCC|VDD|VSS|VBAT)', line[1]):
                    pin_type = 'pwrin'
                elif re.match(r'^(NRST|BOOT0|VREF)', line[1]):
                    pin_type = 'in'
                else:
                    pin_type = 'bidi'
                results.append([line[1], pin, pin_type])
    return results


with open(sys.argv[1], 'r') as f:
    print(yaml.dump([[parse(f)]]))
