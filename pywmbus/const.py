"""This is a docstring."""
A_FIELD = 1
ACC_FIELD = 2
C_FIELD = 3
CI_FIELD = 4
CRC_FIELD = 5
L_FIELD = 6
M_FIELD = 7
ID_FIELD = 8
STATE_FIELD = 9
CONF_FIELD = 10
DIF_FIELD = 11
DIFE_FIELD = 12
VIF_FIELD = 13
VIFE_FIELD = 14

FIELD_TYPES = {
    3: "Gas",
    4: "Heat",
    6: "Warm Water (30 °C ... 90 °C)",
    7: "Water",
}

STATES = {
    0: "Kein Fehler",
    1: "Anwendung beschäftigt",
    2: "Beliebiger Anwendungsfehler",
    3: "Ungewöhnlicher Zustand/Alarm",
}

DIFS = {
    0b0000: {
        "desc": "Keine Daten",
        "length": 0
    },
    0b0001: {
        "desc": "Integer/binär, 8 Bit",
        "length": 1
    },
    0b0010: {
        "desc": "Integer/binär, 16 Bit",
        "length": 2
    },
    0b0011: {
        "desc": "Integer/binär, 24 Bit",
        "length": 3
    },
    0b0100: {
        "desc": "Integer/binär, 32 Bit",
        "length": 4
    },
    0b0101: {
        "desc": "Gleitkommazahl (Real), 32 Bit",
        "length": 4
    },
    0b0110: {
        "desc": "Integer/binär, 48 Bit",
        "length": 6
    },
    0b0111: {
        "desc": "Integer/binär, 64 Bit",
        "length": 8
    },
    0b1000: {
        "desc": "Selektion für Auslesen",
        "length": 4
    },
    0b1001: {
        "desc": "BCD, 2-stellig",
        "length": 1
    },
    0b1010: {
        "desc": "BCD, 4-stellig",
        "length": 2
    },
    0b1011: {
        "desc": "BCD, 6-stellig",
        "length": 3
    },
    0b1100: {
        "desc": "BCD, 8-stellig",
        "length": 4
    },
    0b1101: {
        "desc": "variable Länge",
        "length": 4
    },
    0b1110: {
        "desc": "BCD, 12-stellig",
        "length": 6
    },
    0b1111: {
        "desc": "Sonderfunktionen",
        "length": 0
    }
}

VIFS = {
    0b1101101: {
        "desc": "Datum und Uhrzeit (tatsächlich oder mit einer Speichernummer/Funktion assoziiert)"
    },
    0b0010011: {
        "desc": "Volumen: 10(nnn−6) m3"
    },
    0b1101100: {
        "desc": "Datum (tatsächliches oder mit einer Speichernummer/Funktion assoziiertes Datum)"
    },
    0b0111011: {
        "desc": "Durchflussmenge: 10(nnn−6) m3/h"
    },
    0b1010100: {
        "desc": "Massestrom: 10(nnn−3) kg/h"
    },
    0b0000101: {
        "desc": "Volumen: 10(nnn−3) Wh"
    },
    0b0101110: {
        "desc": "Leistung: 10(nnn−3) W"
    },
    0b1111101: {
        "desc": "Zweite Erweiterung der VIF-Codes"
    },
    0b1010101: {
        "desc": "Massestrom: 10(nnn−3) kg/h"
    },
    0b1111010: {
        "desc": "Adresse"
    },
    0b0111101: {
        "desc": "Durchflussmenge: 10(nnn−6) m3/h"
    }
}

VIFES = {
    0b0000000: {
        "desc": "Guthaben"
    },
    0b0001100: {
        "desc": "Modell/Version"
    },
    0b0001101: {
        "desc": "Hardware-Versionsnummer"
    },
    0b1101101: {
        "desc": "Betriebszeit Batterie"
    },
    0b0010111: {
        "desc": "Fehler-Flags"
    }
}

FUNCS = {
    0: "Momentanwert",
    1: "Höchster Wert",
    2: "Niedrigster Wert",
    3: "Wert im Fehlerzustand",
}

LOGGERS = {
    0: "__main__",
    1: __package__,
    2: "{}.datagram".format(__package__),
    3: "{}.datagram_field".format(__package__),
    4: "{}.datagram_headless".format(__package__),
    5: "{}.datagram_long".format(__package__),
    6: "{}.datagram_record".format(__package__),
    7: "{}.datagram_short".format(__package__),
    8: "{}.serial_device".format(__package__),
    9: "{}.cul_stick".format(__package__),
}
