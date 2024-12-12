"""Pinout for each probe, from channel numbers to Samtec numbers.

This file is no longer used because we don't always even have Samtec numbers.
In that case just use probe_adapters.py
"""

from builtins import range
import Adapters


## This is the A32 connector pinout from neuronexus.
# Takes us from "Samtec numbers" to Neuronexus channel numbers.
# Samtec numbers go from 1-40, with 1 in the upper right when looking at
# the probe, or 1 in the upper left when looking at the adapter.
samtec2nn = Adapters.Adapter(list(range(1, 41)), [
    11, 'GND', 'GND', 32, 
    9, 'REF', 'NC', 30,
    7, 'NC', 'NC', 31,
    5, 'NC', 'NC', 28,
    3, 1, 26, 29,
    2, 4, 24, 27,
    6, 13, 20, 25,
    8, 14, 19, 22,
    10, 15, 18, 23,
    12, 16, 17, 21,
    ])

# This is for the Janelia pinout
# As before, Samtec numbers go from 1-40, with 1 in the upper right when
# looking at the probe. The source doc from Tim Harris shows the back side
# of the probe, so 1 is in the upper left (as it is for the adapter).
samtec2janelia_top = Adapters.Adapter(list(range(1, 41)), [
    1, 'NC', 'NC', 64,
    2, 'NC', 'NC', 63,
    3, 'NC', 'NC', 62,
    4, 'NC', 'NC', 61,
    5, 6, 59, 60,
    7, 8, 57, 58,
    9, 10, 55, 56,
    11, 12, 53, 54,
    13, 14, 51, 52,
    15, 16, 49, 50,
    ])
samtec2janelia_bottom = Adapters.Adapter(list(range(1, 41)), [
    17, 'NC', 'NC', 48,
    18, 'NC', 'NC', 47,
    19, 'NC', 'NC', 46,
    20, 'NC', 'NC', 45,
    21, 22, 43, 44,
    23, 28, 37, 42,
    24, 32, 33, 41,
    25, 29, 36, 40,
    26, 30, 35, 39,
    27, 31, 34, 38,
    ])    

# A 64-channel version with two samtecs, 1-40 on the top and 41-80 on the bottom
samtec2janelia_64ch = Adapters.Adapter(list(range(1, 81)),
    [
        1, 'NC', 'NC', 64,
        2, 'NC', 'NC', 63,
        3, 'NC', 'NC', 62,
        4, 'NC', 'NC', 61,
        5, 6, 59, 60,
        7, 8, 57, 58,
        9, 10, 55, 56,
        11, 12, 53, 54,
        13, 14, 51, 52,
        15, 16, 49, 50,
        17, 'NC', 'NC', 48,
        18, 'NC', 'NC', 47,
        19, 'NC', 'NC', 46,
        20, 'NC', 'NC', 45,
        21, 22, 43, 44,
        23, 28, 37, 42,
        24, 32, 33, 41,
        25, 29, 36, 40,
        26, 30, 35, 39,
        27, 31, 34, 38,
    ])