from pprint import pprint

from score.main import *

# This is PSUEDO-CODE!!!
"""
MOVARR y, 0, 0x44
MOVARR y, 1, 0x65
MOVARR y, 2, 0x6c
MOVARR y, 3, 0x6c
MOVARR y, 4, 0x6f
MOVARR y, 5, 0x2c
MOVARR y, 6, 0x20
MOVARR y, 7, 0x57
MOVARR y, 8, 0x6f
MOVARR y, 9, 0x72
MOVARR y, 10, 0x6c
MOVARR y, 11, 0x64
MOVARR y, 12, 0x21
MOVARR y, 13, 0
PRINT y
"""

hello_world = Score(
    operations=[
        Operation(i * 4, 0x0f)
        for i in range(14)
    ] + [
        Operation(14 * 4, 0x0c)
    ],
    data=[
        Datum(2, 0x44),
        Datum(6, 0x65),
        Datum(10, 0x6c),
        Datum(14, 0x6c),
        Datum(18, 0x6f),
        Datum(22, 0x2c),
        Datum(26, 0x20),
        Datum(30, 0x57),
        Datum(34, 0x6f),
        Datum(38, 0x72),
        Datum(42, 0x6c),
        Datum(46, 0x64),
        Datum(50, 0x21),
        Datum(54, 0x00),
    ],
    variables=[
        Variable(i * 4 + 1, 0x01)
        for i in range(14)
    ],
    labels=[],
)

pprint(hello_world.serialize())
