"""
iclib.py
Copyright 2016 Adam Greig

Generate symbols for generic black-box ICs etc.
"""

# Symbols configuration =======================================================
# Dictionary of dictionaries.
# Top keys are symbol names.
# Configuration format is:
# path: optional, sub-directory(s) to store the library in. Defaults to ".".
# designator: optional, default "IC", the default reference designator
# footprint: optional, an associated footprint to autofill
# datasheet: optional, a URL or path to a datasheet
# ordercodes: optional, dict of supplier:code for supplier order codes
# description: description of the part, placed in the .dcm file
# pins: list of lists of left and right pin groups
#           (blocks of related pins with a space in-between).
#       Each group contains a list of tuples of:
#           (pin name, pin number, electrical type).
#       Number and name may be given as a string or an integer.
#       Electrical type must be a string out of:
#           in, out, bidi, tri, passive, unspec, pwrin, pwrout, oc, oe, nc.
#       These correspond to input, output, bidirectional, tristate, passive,
#           unspecified, power_input, power_output, open_collector,
#           open_emitter, and not_connected. They should be given as strings.

config = {

    # STM32F1xxCxUx, in UFQFPN48 package
    "STM32F1xxCxUx": {
        "path": "ic/microcontroller",
        "footprint": "agg:QFN-48-EP-ST",
        "datasheet": "http://www.st.com/st-web-ui/static/active/en"
                     "/resource/technical/document/datasheet/CD00161566.pdf",
        "ordercodes": {
            "Farnell": "2060891",
        },
        "description": "STM32F1 48 pin UFQFPN package",
        "pins": [
            [
                [
                    ("VBAT", 1, "pwrin"),
                    ("VDD", 24, "pwrin"),
                    ("VDD", 48, "pwrin"),
                    ("VDDIO2", 36, "pwrin"),
                    ("VDDA", 9, "pwrin"),
                ], [
                    ("VSSA", 8, "pwrin"),
                    ("VSS", 23, "pwrin"),
                    ("VSS", 47, "pwrin"),
                    ("VSS", 35, "pwrin"),
                    ("VSS", "EP", "pwrin"),
                ], [
                    ("BOOT0", 44, "in"),
                    ("NRST", 7, "in"),
                ], [
                    ("PC13", 2, "bidi"),
                    ("PC14", 3, "bidi"),
                    ("PC15", 4, "bidi"),
                ], [
                    ("PF0", 5, "bidi"),
                    ("PF1", 6, "bidi"),
                ],
            ], [
                [
                    ("PA0", 10, "bidi"),
                    ("PA1", 11, "bidi"),
                    ("PA2", 12, "bidi"),
                    ("PA3", 13, "bidi"),
                    ("PA4", 14, "bidi"),
                    ("PA5", 15, "bidi"),
                    ("PA6", 16, "bidi"),
                    ("PA7", 17, "bidi"),
                ], [
                    ("PA8", 29, "bidi"),
                    ("PA9", 30, "bidi"),
                    ("PA10", 31, "bidi"),
                    ("PA11", 32, "bidi"),
                    ("PA12", 33, "bidi"),
                    ("PA13", 34, "bidi"),
                    ("PA14", 37, "bidi"),
                    ("PA15", 38, "bidi"),
                ], [
                    ("PB0", 18, "bidi"),
                    ("PB1", 19, "bidi"),
                    ("PB2", 20, "bidi"),
                    ("PB3", 39, "bidi"),
                    ("PB4", 40, "bidi"),
                    ("PB5", 41, "bidi"),
                    ("PB6", 42, "bidi"),
                    ("PB7", 43, "bidi"),
                ], [
                    ("PB8", 45, "bidi"),
                    ("PB9", 46, "bidi"),
                    ("PB10", 21, "bidi"),
                    ("PB11", 22, "bidi"),
                    ("PB12", 25, "bidi"),
                    ("PB13", 26, "bidi"),
                    ("PB14", 27, "bidi"),
                    ("PB15", 28, "bidi"),
                ],
            ],
        ],
    },

    # STM32F0xxCxTx, in LQFP48 package
    "STM32F0xxCxTx": {
        "path": "ic/microcontroller",
        "footprint": "agg:LQFP-48",
        "datasheet": "http://www.st.com/st-web-ui/static/active/en"
                     "/resource/technical/document/datasheet/DM00090510.pdf",
        "ordercodes": {
            "Farnell": "2432094",
        },
        "description": "STM32F0 48 pin LQFP package",
        "pins": [
            [
                [
                    ("VBAT", 1, "pwrin"),
                    ("VDD", 24, "pwrin"),
                    ("VDD", 48, "pwrin"),
                    ("VDDIO2", 36, "pwrin"),
                    ("VDDA", 9, "pwrin"),
                ], [
                    ("VSSA", 8, "pwrin"),
                    ("VSS", 23, "pwrin"),
                    ("VSS", 47, "pwrin"),
                    ("VSS", 35, "pwrin"),
                ], [
                    ("BOOT0", 44, "in"),
                    ("NRST", 7, "in"),
                ], [
                    ("PC13", 2, "bidi"),
                    ("PC14", 3, "bidi"),
                    ("PC15", 4, "bidi"),
                ], [
                    ("PF0", 5, "bidi"),
                    ("PF1", 6, "bidi"),
                ],
            ], [
                [
                    ("PA0", 10, "bidi"),
                    ("PA1", 11, "bidi"),
                    ("PA2", 12, "bidi"),
                    ("PA3", 13, "bidi"),
                    ("PA4", 14, "bidi"),
                    ("PA5", 15, "bidi"),
                    ("PA6", 16, "bidi"),
                    ("PA7", 17, "bidi"),
                ], [
                    ("PA8", 29, "bidi"),
                    ("PA9", 30, "bidi"),
                    ("PA10", 31, "bidi"),
                    ("PA11", 32, "bidi"),
                    ("PA12", 33, "bidi"),
                    ("PA13", 34, "bidi"),
                    ("PA14", 37, "bidi"),
                    ("PA15", 38, "bidi"),
                ], [
                    ("PB0", 18, "bidi"),
                    ("PB1", 19, "bidi"),
                    ("PB2", 20, "bidi"),
                    ("PB3", 39, "bidi"),
                    ("PB4", 40, "bidi"),
                    ("PB5", 41, "bidi"),
                    ("PB6", 42, "bidi"),
                    ("PB7", 43, "bidi"),
                ], [
                    ("PB8", 45, "bidi"),
                    ("PB9", 46, "bidi"),
                    ("PB10", 21, "bidi"),
                    ("PB11", 22, "bidi"),
                    ("PB12", 25, "bidi"),
                    ("PB13", 26, "bidi"),
                    ("PB14", 27, "bidi"),
                    ("PB15", 28, "bidi"),
                ],
            ],
        ],
    },

    # STM32F0xxRxHx, in UFBGA64 package
    "STM32F0xxRxHx": {
        "path": "ic/microcontroller",
        "footprint": "agg:UFBGA-64",
        "datasheet": "http://www.st.com/st-web-ui/static/active/en"
                     "/resource/technical/document/datasheet/DM00115237.pdf",
        "ordercodes": {
            "Farnell": "2503242",
        },
        "description": "STM32F0 64 pin UFBGA package",
        "pins": [
            [
                [
                    ("VBAT", "B2", "pwrin"),
                    ("VDD", "D2", "pwrin"),
                    ("VDD", "E4", "pwrin"),
                    ("VDD", "E5", "pwrin"),
                    ("VDDIO2", "E6", "pwrin"),
                    ("VDDA", "H1", "pwrin"),
                ], [
                    ("VSSA", "F1", "pwrin"),
                    ("VSS", "C2", "pwrin"),
                    ("VSS", "D4", "pwrin"),
                    ("VSS", "D5", "pwrin"),
                    ("VSS", "D6", "pwrin"),
                ], [
                    ("BOOT0", "B4", "in"),
                    ("NRST", "E1", "in"),
                ], [
                    ("PF0", "C1", "bidi"),
                    ("PF1", "D1", "bidi"),
                ], [
                    ("PA0", "G2", "bidi"),
                    ("PA1", "H2", "bidi"),
                    ("PA2", "F3", "bidi"),
                    ("PA3", "G3", "bidi"),
                    ("PA4", "H3", "bidi"),
                    ("PA5", "F4", "bidi"),
                    ("PA6", "G4", "bidi"),
                    ("PA7", "H4", "bidi"),
                ], [
                    ("PA8", "D7", "bidi"),
                    ("PA9", "C7", "bidi"),
                    ("PA10", "C6", "bidi"),
                    ("PA11", "C8", "bidi"),
                    ("PA12", "B8", "bidi"),
                    ("PA13", "A8", "bidi"),
                    ("PA14", "A7", "bidi"),
                    ("PA15", "A6", "bidi"),
                ],
            ], [
                [
                    ("PB0", "F5", "bidi"),
                    ("PB1", "G5", "bidi"),
                    ("PB2", "G6", "bidi"),
                    ("PB3", "A5", "bidi"),
                    ("PB4", "A4", "bidi"),
                    ("PB5", "C4", "bidi"),
                    ("PB6", "D3", "bidi"),
                    ("PB7", "C3", "bidi"),
                ], [
                    ("PB8", "B3", "bidi"),
                    ("PB9", "A3", "bidi"),
                    ("PB10", "G7", "bidi"),
                    ("PB11", "H7", "bidi"),
                    ("PB12", "H8", "bidi"),
                    ("PB13", "G8", "bidi"),
                    ("PB14", "F8", "bidi"),
                    ("PB15", "F7", "bidi"),
                ], [
                    ("PC0", "E3", "bidi"),
                    ("PC1", "E2", "bidi"),
                    ("PC2", "F2", "bidi"),
                    ("PC3", "G1", "bidi"),
                    ("PC4", "H5", "bidi"),
                    ("PC5", "H6", "bidi"),
                    ("PC6", "F6", "bidi"),
                    ("PC7", "E7", "bidi"),
                ], [
                    ("PC8", "E8", "bidi"),
                    ("PC9", "D8", "bidi"),
                    ("PC10", "B7", "bidi"),
                    ("PC11", "B6", "bidi"),
                    ("PC12", "C5", "bidi"),
                    ("PC13", "A2", "bidi"),
                    ("PC14", "A1", "bidi"),
                    ("PC15", "B1", "bidi"),
                ], [
                    ("PD2", "B5", "bidi"),
                ]
            ],
        ],
    },

    # STM32F3xxCxTx, in LQFP48 package
    "STM32F3xxCxTx": {
        "path": "ic/microcontroller",
        "footprint": "agg:LQFP-48",
        "datasheet": "http://www.st.com/st-web-ui/static/active/en"
                     "/resource/technical/document/datasheet/DM00058181.pdf",
        "ordercodes": {
            "Farnell": "2333254",
        },
        "description": "STM32F3 48 pin LQFP package",
        "pins": [
            [
                [
                    ("VBAT", 1, "pwrin"),
                    ("VDD", 24, "pwrin"),
                    ("VDD", 48, "pwrin"),
                    ("VDD", 36, "pwrin"),
                    ("VDDA", 9, "pwrin"),
                ], [
                    ("VSSA", 8, "pwrin"),
                    ("VSS", 23, "pwrin"),
                    ("VSS", 47, "pwrin"),
                    ("VSS", 35, "pwrin"),
                ], [
                    ("BOOT0", 44, "in"),
                    ("NRST", 7, "in"),
                ], [
                    ("PC13", 2, "bidi"),
                    ("PC14", 3, "bidi"),
                    ("PC15", 4, "bidi"),
                ], [
                    ("PF0", 5, "bidi"),
                    ("PF1", 6, "bidi"),
                ],
            ], [
                [
                    ("PA0", 10, "bidi"),
                    ("PA1", 11, "bidi"),
                    ("PA2", 12, "bidi"),
                    ("PA3", 13, "bidi"),
                    ("PA4", 14, "bidi"),
                    ("PA5", 15, "bidi"),
                    ("PA6", 16, "bidi"),
                    ("PA7", 17, "bidi"),
                ], [
                    ("PA8", 29, "bidi"),
                    ("PA9", 30, "bidi"),
                    ("PA10", 31, "bidi"),
                    ("PA11", 32, "bidi"),
                    ("PA12", 33, "bidi"),
                    ("PA13", 34, "bidi"),
                    ("PA14", 37, "bidi"),
                    ("PA15", 38, "bidi"),
                ], [
                    ("PB0", 18, "bidi"),
                    ("PB1", 19, "bidi"),
                    ("PB2", 20, "bidi"),
                    ("PB3", 39, "bidi"),
                    ("PB4", 40, "bidi"),
                    ("PB5", 41, "bidi"),
                    ("PB6", 42, "bidi"),
                    ("PB7", 43, "bidi"),
                ], [
                    ("PB8", 45, "bidi"),
                    ("PB9", 46, "bidi"),
                    ("PB10", 21, "bidi"),
                    ("PB11", 22, "bidi"),
                    ("PB12", 25, "bidi"),
                    ("PB13", 26, "bidi"),
                    ("PB14", 27, "bidi"),
                    ("PB15", 28, "bidi"),
                ],
            ],
        ],
    },

    # STM32F4xxVxTx, in LQFP100 package
    "STM32F4xxVxTx": {
        "path": "ic/microcontroller",
        "footprint": "agg:LQFP-100",
        "datasheet": "http://www.st.com/st-web-ui/static/active/en"
                     "/resource/technical/document/datasheet/DM00037051.pdf",
        "ordercodes": {
            "Farnell": "2215224",
        },
        "description": "STM32F4 100 pin LQFP package",
        "pins": [
            [
                [
                    ("VBAT", 6, "pwrin"),
                    ("VDD", 11, "pwrin"),
                    ("VDD", 19, "pwrin"),
                    ("VDD", 28, "pwrin"),
                    ("VDD", 50, "pwrin"),
                    ("VDD", 75, "pwrin"),
                    ("VDD", 100, "pwrin"),
                    ("VDDA", 22, "pwrin"),
                    ("VREF+", 21, "pwrin"),
                ], [
                    ("VCAP_1", 49, "passive"),
                    ("VCAP_2", 73, "passive"),
                ], [
                    ("VSSA", 20, "pwrin"),
                    ("VSS", 10, "pwrin"),
                    ("VSS", 27, "pwrin"),
                    ("VSS", 74, "pwrin"),
                    ("VSS", 99, "pwrin"),
                ], [
                    ("BOOT0", 94, "in"),
                    ("NRST", 14, "in"),
                ], [
                    ("PH0", 12, "bidi"),
                    ("PH1", 13, "bidi"),
                ], [
                    ("PA0", 23, "bidi"),
                    ("PA1", 24, "bidi"),
                    ("PA2", 25, "bidi"),
                    ("PA3", 26, "bidi"),
                    ("PA4", 29, "bidi"),
                    ("PA5", 30, "bidi"),
                    ("PA6", 31, "bidi"),
                    ("PA7", 32, "bidi"),
                ], [
                    ("PA8", 67, "bidi"),
                    ("PA9", 68, "bidi"),
                    ("PA10", 69, "bidi"),
                    ("PA11", 70, "bidi"),
                    ("PA12", 71, "bidi"),
                    ("PA13", 72, "bidi"),
                    ("PA14", 76, "bidi"),
                    ("PA15", 77, "bidi"),
                ], [
                    ("PB0", 35, "bidi"),
                    ("PB1", 36, "bidi"),
                    ("PB2", 37, "bidi"),
                    ("PB3", 89, "bidi"),
                    ("PB4", 90, "bidi"),
                    ("PB5", 91, "bidi"),
                    ("PB6", 92, "bidi"),
                    ("PB7", 93, "bidi"),
                ], [
                    ("PB8", 95, "bidi"),
                    ("PB9", 96, "bidi"),
                    ("PB10", 47, "bidi"),
                    ("PB11", 48, "bidi"),
                    ("PB12", 51, "bidi"),
                    ("PB13", 52, "bidi"),
                    ("PB14", 53, "bidi"),
                    ("PB15", 54, "bidi"),
                ],
            ], [
                [
                    ("PC0", 15, "bidi"),
                    ("PC1", 16, "bidi"),
                    ("PC2", 17, "bidi"),
                    ("PC3", 18, "bidi"),
                    ("PC4", 33, "bidi"),
                    ("PC5", 34, "bidi"),
                    ("PC6", 63, "bidi"),
                    ("PC7", 64, "bidi"),
                ], [
                    ("PC8", 65, "bidi"),
                    ("PC9", 66, "bidi"),
                    ("PC10", 78, "bidi"),
                    ("PC11", 79, "bidi"),
                    ("PC12", 80, "bidi"),
                    ("PC13", 7, "bidi"),
                    ("PC14", 8, "bidi"),
                    ("PC15", 9, "bidi"),
                ], [
                    ("PD0", 81, "bidi"),
                    ("PD1", 82, "bidi"),
                    ("PD2", 83, "bidi"),
                    ("PD3", 84, "bidi"),
                    ("PD4", 85, "bidi"),
                    ("PD5", 86, "bidi"),
                    ("PD6", 87, "bidi"),
                    ("PD7", 88, "bidi"),
                ], [
                    ("PD8", 55, "bidi"),
                    ("PD9", 56, "bidi"),
                    ("PD10", 57, "bidi"),
                    ("PD11", 58, "bidi"),
                    ("PD12", 59, "bidi"),
                    ("PD13", 60, "bidi"),
                    ("PD14", 61, "bidi"),
                    ("PD15", 62, "bidi"),
                ], [
                    ("PE0", 97, "bidi"),
                    ("PE1", 98, "bidi"),
                    ("PE2", 1, "bidi"),
                    ("PE3", 2, "bidi"),
                    ("PE4", 3, "bidi"),
                    ("PE5", 4, "bidi"),
                    ("PE6", 5, "bidi"),
                    ("PE7", 38, "bidi"),
                ], [
                    ("PE8", 39, "bidi"),
                    ("PE9", 40, "bidi"),
                    ("PE10", 41, "bidi"),
                    ("PE11", 42, "bidi"),
                    ("PE12", 43, "bidi"),
                    ("PE13", 44, "bidi"),
                    ("PE14", 45, "bidi"),
                    ("PE15", 46, "bidi"),
                ],
            ],
        ],
    },

    # STM32L4xxJxYx, in WLCSP72 package
    "STM32L4xxJxYx": {
        "path": "ic/microcontroller",
        "footprint": "agg:WLCSP72",
        "datasheet": "http://www.st.com/st-web-ui/static/active/en"
                     "/resource/technical/document/datasheet/DM00108833.pdf",
        "ordercodes": {
            "Farnell": "2503302",
        },
        "description": "STM32L4 72 pin WLCSP package",
        "pins": [
            [
                [
                    ("VBAT", "B9", "pwrin"),
                    ("VDD", "A9", "pwrin"),
                    ("VDD", "J1", "pwrin"),
                    ("VDD", "J8", "pwrin"),
                    ("VDDIO2", "B6", "pwrin"),
                    ("VDDUSB", "A1", "pwrin"),
                ], [
                    ("VSS", "A8", "pwrin"),
                    ("VSS", "B1", "pwrin"),
                    ("VSS", "J2", "pwrin"),
                    ("VSS", "J9", "pwrin"),
                ], [
                    ("VDDA", "H9", "pwrin"),
                    ("VREF+", "G8", "in"),
                    ("VSSA", "G9", "pwrin"),
                ], [
                    ("BOOT0", "D7", "in"),
                    ("NRST", "E9", "in"),
                ], [
                    ("PH0", "D9", "bidi"),
                    ("PH1", "D8", "bidi"),
                ], [
                    ("PA0", "H8", "bidi"),
                    ("PA1", "G4", "bidi"),
                    ("PA2", "G6", "bidi"),
                    ("PA3", "H7", "bidi"),
                    ("PA4", "G5", "bidi"),
                    ("PA5", "H6", "bidi"),
                    ("PA6", "H5", "bidi"),
                    ("PA7", "H4", "bidi"),
                ], [
                    ("PA8", "E2", "bidi"),
                    ("PA9", "E3", "bidi"),
                    ("PA10", "D2", "bidi"),
                    ("PA11", "D1", "bidi"),
                    ("PA12", "C1", "bidi"),
                    ("PA13", "C2", "bidi"),
                    ("PA14", "B2", "bidi"),
                    ("PA15", "A2", "bidi"),
                ],
            ], [
                [
                    ("PB0", "J5", "bidi"),
                    ("PB1", "J4", "bidi"),
                    ("PB2", "J3", "bidi"),
                    ("PB3", "A6", "bidi"),
                    ("PB4", "C6", "bidi"),
                    ("PB5", "C7", "bidi"),
                    ("PB6", "B7", "bidi"),
                    ("PB7", "A7", "bidi"),
                ], [
                    ("PB8", "E7", "bidi"),
                    ("PB9", "E8", "bidi"),
                    ("PB10", "H3", "bidi"),
                    ("PB11", "G3", "bidi"),
                    ("PB12", "H1", "bidi"),
                    ("PB13", "H2", "bidi"),
                    ("PB14", "G2", "bidi"),
                    ("PB15", "G1", "bidi"),
                ], [
                    ("PC0", "F9", "bidi"),
                    ("PC1", "F8", "bidi"),
                    ("PC2", "F7", "bidi"),
                    ("PC3", "G7", "bidi"),
                    ("PC4", "J7", "bidi"),
                    ("PC5", "J6", "bidi"),
                    ("PC6", "F3", "bidi"),
                    ("PC7", "F1", "bidi"),
                ], [
                    ("PC8", "F2", "bidi"),
                    ("PC9", "E1", "bidi"),
                    ("PC10", "D3", "bidi"),
                    ("PC11", "C3", "bidi"),
                    ("PC12", "B3", "bidi"),
                    ("PC13", "B8", "bidi"),
                    ("PC14", "C9", "bidi"),
                    ("PC15", "C8", "bidi"),
                ], [
                    ("PD2", "A3", "bidi"),
                ], [
                    ("PG9", "A4", "bidi"),
                    ("PG10", "B4", "bidi"),
                    ("PG11", "C4", "bidi"),
                    ("PG12", "C5", "bidi"),
                    ("PG13", "B5", "bidi"),
                    ("PG14", "A5", "bidi"),
                ],
            ],
        ],
    },

    # STM32F4xxZxJx, in UFBGA144 10x10 package
    "STM32F4xxZxJx": {
        "path": "ic/microcontroller",
        "footprint": "agg:UFBGA-144",
        "datasheet": "http://www.st.com/st-web-ui/static/active/en"
                     "/resource/technical/document/datasheet/DM00141306.pdf",
        "ordercodes": {
            "Farnell": "2488316",
        },
        "description": "STM32F4 144 pin 10x10 UFBGA package",
        "pins": [
            [
                [
                    ("VDD", "D3", "pwrin"),
                    ("VDD", "F10", "pwrin"),
                    ("VDD", "F4", "pwrin"),
                    ("VDD", "F5", "pwrin"),
                    ("VDD", "F6", "pwrin"),
                    ("VDD", "F7", "pwrin"),
                    ("VDD", "F8", "pwrin"),
                    ("VDD", "F9", "pwrin"),
                    ("VDD", "G5", "pwrin"),
                    ("VDD", "G6", "pwrin"),
                    ("VDD", "G7", "pwrin"),
                    ("VBAT", "C2", "pwrin"),
                    ("VDDUSB", "C11", "pwrin"),
                ], [
                    ("VSS", "D2", "pwrin"),
                    ("VSS", "E6", "pwrin"),
                    ("VSS", "E7", "pwrin"),
                    ("VSS", "G10", "pwrin"),
                    ("VSS", "G4", "pwrin"),
                    ("VSS", "G8", "pwrin"),
                    ("VSS", "H6", "pwrin"),
                ], [
                    ("VDDA", "M1", "pwrin"),
                    ("VREF+", "L1", "in"),
                    ("VREF-", "K1", "in"),
                    ("VSSA", "J1", "pwrin"),
                ], [
                    ("VCAP_1", "H7", "passive"),
                    ("VCAP_2", "G9", "passive"),
                ], [
                    ("PDR_ON", "E5", "in"),
                    ("BOOT0", "D5", "in"),
                    ("BYPASS_REG", "H5", "in"),
                    ("NRST", "F1", "in"),
                ], [
                    ("PA0", "J2", "bidi"),
                    ("PA1", "K2", "bidi"),
                    ("PA2", "L2", "bidi"),
                    ("PA3", "M2", "bidi"),
                    ("PA4", "J3", "bidi"),
                    ("PA5", "K3", "bidi"),
                    ("PA6", "L3", "bidi"),
                    ("PA7", "M3", "bidi"),
                    ("PA8", "E12", "bidi"),
                    ("PA9", "D12", "bidi"),
                    ("PA10", "D11", "bidi"),
                    ("PA11", "C12", "bidi"),
                    ("PA12", "B12", "bidi"),
                    ("PA13", "A12", "bidi"),
                    ("PA14", "A11", "bidi"),
                    ("PA15", "A10", "bidi"),
                ], [
                    ("PB0", "L4", "bidi"),
                    ("PB1", "M4", "bidi"),
                    ("PB2", "J5", "bidi"),
                    ("PB3", "A7", "bidi"),
                    ("PB4", "A6", "bidi"),
                    ("PB5", "B6", "bidi"),
                    ("PB6", "C6", "bidi"),
                    ("PB7", "D6", "bidi"),
                    ("PB8", "C5", "bidi"),
                    ("PB9", "B5", "bidi"),
                    ("PB10", "M9", "bidi"),
                    ("PB11", "M10", "bidi"),
                    ("PB12", "M11", "bidi"),
                    ("PB13", "M12", "bidi"),
                    ("PB14", "L11", "bidi"),
                    ("PB15", "L12", "bidi"),
                ], [
                    ("PC0", "H1", "bidi"),
                    ("PC1", "H2", "bidi"),
                    ("PC2", "H3", "bidi"),
                    ("PC3", "H4", "bidi"),
                    ("PC4", "J4", "bidi"),
                    ("PC5", "K4", "bidi"),
                    ("PC6", "G12", "bidi"),
                    ("PC7", "F12", "bidi"),
                    ("PC8", "F11", "bidi"),
                    ("PC9", "E11", "bidi"),
                    ("PC10", "B11", "bidi"),
                    ("PC11", "B10", "bidi"),
                    ("PC12", "C10", "bidi"),
                    ("PC13", "A1", "bidi"),
                    ("PC14", "B1", "bidi"),
                    ("PC15", "C1", "bidi"),
                ],
            ], [
                [
                    ("PD0", "E10", "bidi"),
                    ("PD1", "D10", "bidi"),
                    ("PD2", "E9", "bidi"),
                    ("PD3", "D9", "bidi"),
                    ("PD4", "C9", "bidi"),
                    ("PD5", "B9", "bidi"),
                    ("PD6", "A8", "bidi"),
                    ("PD7", "A9", "bidi"),
                    ("PD8", "L9", "bidi"),
                    ("PD9", "K9", "bidi"),
                    ("PD10", "J9", "bidi"),
                    ("PD11", "H9", "bidi"),
                    ("PD12", "L10", "bidi"),
                    ("PD13", "K10", "bidi"),
                    ("PD14", "K11", "bidi"),
                    ("PD15", "K12", "bidi"),
                ], [
                    ("PE0", "A5", "bidi"),
                    ("PE1", "A4", "bidi"),
                    ("PE2", "A3", "bidi"),
                    ("PE3", "A2", "bidi"),
                    ("PE4", "B2", "bidi"),
                    ("PE5", "B3", "bidi"),
                    ("PE6", "B4", "bidi"),
                    ("PE7", "M7", "bidi"),
                    ("PE8", "L7", "bidi"),
                    ("PE9", "K7", "bidi"),
                    ("PE10", "J7", "bidi"),
                    ("PE11", "H8", "bidi"),
                    ("PE12", "J8", "bidi"),
                    ("PE13", "K8", "bidi"),
                    ("PE14", "L8", "bidi"),
                    ("PE15", "M8", "bidi"),
                ], [
                    ("PF0", "C3", "bidi"),
                    ("PF1", "C4", "bidi"),
                    ("PF2", "D4", "bidi"),
                    ("PF3", "E2", "bidi"),
                    ("PF4", "E3", "bidi"),
                    ("PF5", "E4", "bidi"),
                    ("PF6", "F3", "bidi"),
                    ("PF7", "F2", "bidi"),
                    ("PF8", "G3", "bidi"),
                    ("PF9", "G2", "bidi"),
                    ("PF10", "G1", "bidi"),
                    ("PF11", "M5", "bidi"),
                    ("PF12", "L5", "bidi"),
                    ("PF13", "K5", "bidi"),
                    ("PF14", "M6", "bidi"),
                    ("PF15", "L6", "bidi"),
                ], [
                    ("PG0", "K6", "bidi"),
                    ("PG1", "J6", "bidi"),
                    ("PG2", "J12", "bidi"),
                    ("PG3", "J11", "bidi"),
                    ("PG4", "J10", "bidi"),
                    ("PG5", "H12", "bidi"),
                    ("PG6", "H11", "bidi"),
                    ("PG7", "H10", "bidi"),
                    ("PG8", "G11", "bidi"),
                    ("PG9", "E8", "bidi"),
                    ("PG10", "D8", "bidi"),
                    ("PG11", "C8", "bidi"),
                    ("PG12", "B8", "bidi"),
                    ("PG13", "D7", "bidi"),
                    ("PG14", "C7", "bidi"),
                    ("PG15", "B7", "bidi"),
                ], [
                    ("PH0", "D1", "bidi"),
                    ("PH1", "E1", "bidi"),
                ],
            ],
        ],
    },
}

# Other Constants =============================================================

# None yet.

# End Constants ===============================================================

import os
import sys


pin_types = {
    "in": "I",
    "out": "O",
    "bidi": "B",
    "tri": "T",
    "passive": "P",
    "unspec": "U",
    "pwrin": "W",
    "pwrout": "w",
    "oc": "C",
    "oe": "E",
    "nc": "N",
}


def geometry(conf):
    # width is twice the width required to accommodate the longest name
    longest_name = max(max(max(len(pin[0]) for pin in grp) for grp in side)
                       for side in conf['pins'])
    width = 2 * (longest_name + 1) * 50
    width += width % 200

    # height is the maximum required on either side
    left_pins = sum(len(x) for x in conf['pins'][0])
    right_pins = sum(len(x) for x in conf['pins'][1])
    left_groups = len(conf['pins'][0])
    right_groups = len(conf['pins'][1])

    height = 100 * max(
        left_pins + left_groups - 1, right_pins + right_groups - 1)

    # height must be an odd multiple of 0.1" or the grid breaks
    if (height // 100) % 2 == 0:
        height += 100

    # Pin length based on maximum pin number length
    longest_num = max(max(max(len(str(pin[1])) for pin in grp) for grp in side)
                      for side in conf['pins'])
    length = max(100, longest_num*50)
    # Ensure pins will align to a 100mil grid by making the part wider
    if length % 100 != 0:
        width += 100

    return width, height, length, left_groups


def fields(conf):
    width, height, _, lgroups = geometry(conf)
    field_x = -width//2
    field_y = height//2 + 50
    out = []

    # Designator at top
    out.append("F0 \"{}\" {} {} 50 H V L CNN".format(
        conf.get('designator', 'IC'), field_x, field_y))

    # Value/name at bottom
    out.append("F1 \"{}\" {} {} 50 H V L CNN".format(
        conf['name'], field_x, -field_y))

    # Either specify a footprint or just set its size, position, invisibility
    if "footprint" in conf:
        out.append("F2 \"{}\" {} {} 50 H I L CNN".format(
            conf['footprint'], field_x, -field_y-100))
    else:
        out.append("F2 \"\" {} {} 50 H I L CNN".format(field_x, -field_y-100))

    # Specify a datasheet if given
    if "datasheet" in conf:
        out.append("F3 \"{}\" {} {} 50 H I L CNN".format(
            conf['datasheet'], field_x, -field_y-200))
    else:
        out.append("F3 \"\" {} {} 50 H I L CNN".format(field_x, -field_y-200))

    # Order codes
    for idx, (supplier, code) in enumerate(conf.get("ordercodes", {}).items()):
        out.append("F{} \"{}\" {} {} 50 H I L CNN \"{}\"".format(
            idx+4, code, field_x, -field_y-(300+idx*100), supplier))

    return out


def draw_pins(groups, x0, y0, direction, length):
    out = []
    pin_x = x0
    pin_y = y0
    for group in groups:
        for (name, num, t) in group:
            out.append("X {} {} {} {} {} {} 50 50 0 0 {}".format(
                name, num, pin_x, pin_y, length, direction, pin_types[t]))
            pin_y -= 100
        pin_y -= 100
    return out


def draw(conf):
    width, height, length, lgroups = geometry(conf)
    out = []
    out.append("DRAW")

    # Containing box
    out.append("S {} {} {} {} 0 1 0 f".format(
        -width//2, height//2, width//2, -height//2))

    # Pins
    x0 = -width//2 - length
    y0 = height//2 - 50
    out += draw_pins(conf['pins'][0], x0, y0, "R", length)
    out += draw_pins(conf['pins'][1], -x0, y0, "L", length)

    out.append("ENDDRAW")
    return out


def library(conf):
    out = []

    out.append("EESchema-LIBRARY Version 2.3")
    out.append("#encoding utf-8")
    out.append("#\n# {}\n#".format(conf['name']))
    out.append("DEF {} {} 0 40 Y Y 1 F N".format(
        conf['name'], conf.get('designator', 'IC')))

    out += fields(conf)
    out += draw(conf)

    out.append("ENDDEF\n#\n#End Library\n")
    return "\n".join(out)


def documentation(conf):
    out = []
    out.append("EESchema-DOCLIB\tVersion 2.0")
    out.append("$CMP {}".format(conf['name']))
    out.append("D {}".format(conf['description']))
    out.append("$ENDCMP\n")
    return "\n".join(out)


def main(libpath):
    for name, conf in config.items():
        conf['name'] = name
        path = os.path.join(libpath, conf.get("path", ""), name.lower()+".lib")
        dcmpath = os.path.splitext(path)[0] + ".dcm"

        lib = library(conf)
        dcm = documentation(conf)

        # Check if anything has changed
        if os.path.isfile(path):
            with open(path) as f:
                oldlib = f.read()
            if os.path.isfile(dcmpath):
                with open(dcmpath) as f:
                    olddcm = f.read()
            else:
                olddcm = ""
            if lib == oldlib and dcm == olddcm:
                continue

        # If we've made changes, write them
        with open(path, "w") as f:
            f.write(lib)
        with open(dcmpath, "w") as f:
            f.write(dcm)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        libpath = sys.argv[1]
        main(libpath)
    else:
        print("Usage: {} <lib path>".format(sys.argv[0]))
        sys.exit(1)
