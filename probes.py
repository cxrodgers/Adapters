"""Pinout for each probe, from channel numbers to Samtec numbers."""

import Adapters

## This is for Adrian's 1x8 shank array
# This one goes from "electrode #" (depth?) to "interposer PCB #"
adrian_8shank2interposer = Adapters.Adapter(
    [27, 25, 21, 20, 9],
    [41, 45, 53, 55, 52],
)

# This one goes from interposer PCB # to Samtec numbers
# This uses the little handbuild adapter I made that is an ON1 (I think)
# superglued to a breadboard PCB and hand-wired.
# Here I will use 41-80 as Samtec numbers, with 1 in the upper left when
# looking into the next adapter (out of the probe).
# The reason to use 41-80 is because this will be used with the bottom
# connector on ON4.
interposer2samtec = Adapters.Adapter([
    33, 34, 35, 36, 37, 38, 39, 40, # first column (shank side to top side)
    41, 42, 43, 44, 45, 46, 47, 48, # second column (top side to shank side)
    49, 50, 51, #52, 53, 54, 55, # third column (shank side to top side)
    ], [
    53, 57, 58, 61, 62, 65, 73, 77,
    49, 45, 41, 80, 76, 72, 68, 63, 
    64, 60, 56,
    ]
)

# Hack the above
# The inner column of interposer doesn't have any useful sites, according
# to Adrian. And the outer column of my adapter isn't wired up fully.
# So, shift the interposer such that its inner column is floating.
# Same as above, except 
interposer2samtec_shifted = Adapters.Adapter([
    #33, 34, 35, 36, 37, 38, 39, 40, # first (innermost) column (shank side to top side)
    48, 47, 46, 45, 44, 43, 42, 41, # second column (shank side to top side)
    #41, 42, 43, 44, 45, 46, 47, 48, # second column (top side to shank side)
    49, 50, 51, 52, 53, 54, 55, # third column (shank side to top side)
    ], [
    53, 57, 58, 61, 62, 65, 73, 77,
    49, 45, 41, 80, 76, 72, 68, #63, 
    #64, 60, 56,
    ]
)


## End Adrian's array


# This is the A32 connector pinout from neuronexus.
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