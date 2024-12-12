"""
The various adapters I've made that go from Samtec to headstage.

Samtec pin ordering:
I always have Pin #1 in the upper left when looking at the adapter, or at
the back side of the probe. If two Samtec connectors, the top one goes from
1-40 and the bottom one from 41 - 80.

Omnetics pin ordering:
Looking into the headstage when it's right-side up, Pin #1 is in the bottom
right. Pin #18 is on lower left. Pin #19 is upper left (wraps around),
and Pin #36 is on the upper right. If two Omnetics connectors, the first
goes from 1-36 and the second goes from 37-72.

"""

from builtins import zip
from builtins import range
import Adapters
import numpy as np

def inclusive_list(start, stop):
    """Return a list that goes from start to stop inclusively, not Pythonically
    
    """
    return list(range(start, stop + 1))


## wire64 and wire128 EIB 
# This is the White Matter EIB
# level 0 : EIB hole numbers. I made up this ordering, but it's meant to
#   match the White Matter ordering, so it starts with the left-most column
#   (as you are looking down at the connector side, with the connector up),
#   labels the holes from top to bottom, and then proceeds to columns on the 
#   right. That is, it starts with the A1-D1 tetrode and ends with A16-D16.
#   This will be 0-based even though everything else here is 1-based.
# level 1 : EIB hole names. These are taken from the White Matter image.
#   Importantly, I call it eg "A01" instead of "A1", so they're all length 3.

# level 0
wire64_level0_eib_numbers = list(range(64))
wire128_level0_eib_numbers = list(range(128))

# level 1
wire64_level1_eib_names = []
for column_number in inclusive_list(1, 16):
    for row_name in inclusive_list(ord('A'), ord('D')):
        name = '{:02}{}'.format(column_number, chr(row_name))
        wire64_level1_eib_names.append(name)
        
wire128_level1_eib_names = []
for column_number in inclusive_list(1, 32):
    for row_name in inclusive_list(ord('A'), ord('D')):
        name = '{:02}{}'.format(column_number, chr(row_name))
        wire128_level1_eib_names.append(name)

# Create adaptor
wire64_eib_numbers2names = Adapters.Adapter(
    wire64_level0_eib_numbers,
    wire64_level1_eib_names)

wire128_eib_numbers2names = Adapters.Adapter(
    wire128_level0_eib_numbers,
    wire128_level1_eib_names)

# This relates eib hole name to headstage channel number
# Thse are taken directly from the spreadsheet from Tim, except I added
# a zero before the number, and I put the row name last, to make it sort
# more nicely.
# I assume these  reflect the ordering of the channels in the data files 
# saved by WM, as well as the order they are displayed in Open Ephys, 
# as well as the ordering of the channels in the nanoZ when using Tim's 
# "NZA SSB-64" addition to the electrodes.ini config file.
wire64_eib_names_sorted_by_hs = [
    '01B', '05C', '01C', '05A', '01A', '05D', '05B', '01D', 
    '02A', '06A', '06C', '02C', '06B', '02B', '06D', '07A', 
    '02D', '03A', '07B', '07C', '03C', '08A', '03B', '07D', 
    '08B', '04A', '09A', '08C', '03D', '09B', '04B', '08D', 
    '10A', '04C', '13A', '10B', '09C', '04D', '11A', '13B', 
    '09D', '11B', '13D', '14B', '12A', '10C', '13C', '12B', 
    '14A', '14C', '16D', '10D', '15A', '11C', '14D', '16A', 
    '11D', '15C', '15B', '15D', '12C', '16B', '12D', '16C', 
    ]
wire64_eib_names2headstage = Adapters.Adapter(
    wire64_eib_names_sorted_by_hs,
    inclusive_list(1, 64))
    
wire128_eib_names_sorted_by_hs = [
    '01B', '05C', '01C', '05A', '01A', '05D', '05B', '01D', 
    '02A', '06A', '06C', '02C', '06B', '02B', '06D', '07A', 
    '02D', '03A', '07B', '07C', '03C', '08A', '03B', '07D', 
    '08B', '04A', '09A', '08C', '03D', '09B', '04B', '08D', 
    '10A', '04C', '13A', '10B', '09C', '04D', '11A', '13B', 
    '09D', '11B', '13D', '14B', '12A', '10C', '13C', '12B', 
    '14A', '14C', '16D', '10D', '15A', '11C', '14D', '16A', 
    '11D', '15C', '15B', '15D', '12C', '16B', '12D', '16C',
    '17B', '21C', '17C', '21A', '17A', '21D', '21B', '17D', 
    '18A', '22A', '22C', '18C', '22B', '18B', '22D', '23A', 
    '18D', '19A', '23B', '23C', '19C', '24A', '19B', '23D', 
    '24B', '20A', '25A', '24C', '19D', '25B', '20B', '24D', 
    '26A', '20C', '29A', '26B', '25C', '20D', '27A', '29B', 
    '25D', '27B', '29D', '30B', '28A', '26C', '29C', '28B', 
    '30A', '30C', '32D', '26D', '31A', '27C', '30D', '32A', 
    '27D', '31C', '31B', '31D', '28C', '32B', '28D', '32C',
    ]
wire128_eib_names2headstage = Adapters.Adapter(
    wire128_eib_names_sorted_by_hs,
    inclusive_list(1, 128))


## slimstack2headstage
# This is pasted on a file from tim PastedGraphic-1
# It maps SlimStack number to headstage numbers
# I number Slimstack with 'top_00' in the upper left corner as you look
# at the EIB with Slimstack up. 
# Tim's image is looking at the mating face, so it is flipped horizontally
# from that standard orientation.
# Also, nothing plugs into the corner pins of the Slimstack, these may 
# actually not be real pins. 
# this order will go from upper right to upper left in Tim's image, and
# then downward, but always right to left not wraparound
# Because I'm going from right to left here, this is actually the order
# you get when looking at the front of the EIB and going left to right.
#For 128 channels I included a top 1 and bot 1 for the first board and top 2 and
# and bot 2 for the second board with the first being the board highest on the stack. 
wire64_slimstack2headstage_hs_sorted_by_slimstack_geometry = [
     3,  8, 12, 17, 21, 29, 34, 38, 47, 43, 50, 55, 58, 60, 64, 51, 'GND',
     2,  6, 11, 15, 20, 24, 28, 32, 37, 41, 46, 52, 54, 57, 61, 63, 'REF',
     1,  5,  9, 14, 18, 23, 26, 31, 35, 40, 44, 49, 59, 53, 56, 62, 'GND',
     4,  7, 10, 13, 16, 19, 22, 25, 27, 30, 33, 36, 39, 42, 45, 48, 'REF',
    ]

wire128_slimstack2headstage_hs_sorted_by_slimstack_geometry = [ 
     3,  8, 12, 17, 21, 29, 34, 38, 47, 43, 50, 55, 58, 60, 64, 51, 'GND',
     2,  6, 11, 15, 20, 24, 28, 32, 37, 41, 46, 52, 54, 57, 61, 63, 'REF',
     1,  5,  9, 14, 18, 23, 26, 31, 35, 40, 44, 49, 59, 53, 56, 62, 'GND',
     4,  7, 10, 13, 16, 19, 22, 25, 27, 30, 33, 36, 39, 42, 45, 48, 'REF',
     67,72,76,81,85,93,98,102,111,107,114,119,122,124,128,115,'GND',
     66,70,75,79,84,88,92,96,101,105,110,116,118,121,125,127,'REF',
     65,69,73,78,82,87,90,95,99,104,108,113,123,117,120,126,'GND',
     68,71,74, 77,80,83, 86,89,91,94,97,100,103,106,109,112, 'REF',
     ]
# SlimStack channel numbers. These are the pins on the SlimStack
# connector on the EIB. 
# They are labeled top_00 to top_33, and bot_00 to bot_33, corresponding
# to the upper and lower SlimStack connectors, going first from left to right
# and then from top to bottom. (No wraparound.)
# The viewing direction is at the front of the EIB, with SlimStack up.
# Because of the way the SlimStack mates, this has to be flipped horizontally
# when looking at the headstage or at the nanoZ adapter.
wire64_slimstack_sorted_geometrically = (
    ['top_{:02d}'.format(num) for num in range(34)] + 
    ['bot_{:02d}'.format(num) for num in range(34)]
    )

wire64_slimstack2headstage = Adapters.Adapter(
    wire64_slimstack_sorted_geometrically,
    wire64_slimstack2headstage_hs_sorted_by_slimstack_geometry,
    )
#Similar to code above but extened for 128 channels
wire128_slimstack_sorted_geometrically = (
    ['top1_{:02d}'.format(num) for num in range(34)] + 
    ['bot1_{:02d}'.format(num) for num in range(34)] +
    ['top2_{:02d}'.format(num) for num in range(34)] + 
    ['bot2_{:02d}'.format(num) for num in range(34)]
    )

wire128_slimstack2headstage = Adapters.Adapter(
    wire128_slimstack_sorted_geometrically,
    wire128_slimstack2headstage_hs_sorted_by_slimstack_geometry,
    )



## NZA SSB-64 and SSB-128
# This is inferred from NZA-SSB6r2-adaptor-map.ini from Tim
# I assume these MUX numbers are in the same order as the headstage channels
# So I extracted the MUX numbers, and map them to inclusive_list(1, 64)
#I added an additional 64 channels for dual implant recordings. 
mux_sorted_by_headstage = [
     1, 57, 42, 10,  2, 33,  9, 41,  3, 12, 34, 44, 11,  4, 35, 14, 
    43,  6, 13, 36, 46, 16,  5, 38, 15,  8, 24, 37, 48, 23, 7, 40, 
    22, 45, 32, 21, 39, 47, 20, 31, 64, 19, 54, 30, 18, 63, 56, 17, 
    29, 55, 49, 62, 27, 61, 53, 26, 60, 52, 28, 51, 59, 25, 58, 50,
    65, 121, 106, 74, 66, 97, 73, 105, 67, 76, 98, 108, 75, 68, 99,  
    78, 107, 70, 77, 100, 110, 80, 69, 102, 79, 72, 88, 101, 112, 87,
    71, 104,  86, 109, 96, 85, 103, 111, 84, 95, 128, 83, 118, 94, 82, 127, 
    120, 81, 93, 119, 113, 126, 91, 125, 117, 90, 124, 116, 92, 115, 123, 89, 122, 114    
]
nza_SSB6_64 = Adapters.Adapter(
    mux_sorted_by_headstage,
    inclusive_list(1, 64))
    
nza_SSB6_128 = Adapters.Adapter(
    mux_sorted_by_headstage,
    inclusive_list(1, 128))

## nanoZ mux mapping
# This is taken from the image from the nanoZ manual
# I made the NC and G each unique to avoid warnings
nanoZ_mux_numbers = [
      25,'N1', 'G1',   1,  26,'N2','N3',   2,
      27,'N4','N5',   3,  28,'N6','N7',   4,
      29,  30,   5,   6,  31,  32,   7,   8,
      17,  18,   9,  10,  19,  20,  11,  12,
      21,  22,  13,  14,  23,  24,  15,  16,
      57,'N8', 'G2',  33,  58,'N9','NA',  34,
      59,'NB','NC',  35,  60,'ND','NE',  36,
      61,  62,  37,  38,  63,  64,  39,  40,
      49,  50,  41,  42,  51,  52,  43,  44,
      53,  54,  45,  46,  55,  56,  47,  48,
    ]
nanoz_mux2samtec = Adapters.Adapter(
    nanoZ_mux_numbers, inclusive_list(1, 80))
     
nanoZ_mux_numbers128 = [ 
      25,'N1', 'G1',   1,  26,'N2','N3',   2,
      27,'N4','N5',   3,  28,'N6','N7',   4,
      29,  30,   5,   6,  31,  32,   7,   8,
      17,  18,   9,  10,  19,  20,  11,  12,
      21,  22,  13,  14,  23,  24,  15,  16,
      57,'N8', 'G2',  33,  58,'N9','NA',  34,
      59,'NB','NC',  35,  60,'ND','NE',  36,
      61,  62,  37,  38,  63,  64,  39,  40,
      49,  50,  41,  42,  51,  52,  43,  44,
      53,  54,  45,  46,  55,  56,  47,  48,
      89,  'N1', 'G3',  65,  90,  'N2',  'N3',  66,
      91,  'N4', 'N5',  67,  92,  'N6', 'N7',  68,  
      93,  94,  69,  70,  95,  96,  71,  72,  
      81,  82, 73,  74,  83,  84,  75,  76,  
      85,  86,  77,  78,  87,  88,  79, 80,
      121, 'N8',  'G4',  97, 122,  'N9',  'NA',  98, 
      123, 'NB',  'NC',  99, 124,  'ND',  'NE', 100,
      125, 126, 101, 102, 127, 128, 103, 104,
      113, 114, 105, 106, 115, 116, 107, 108, 
      117, 118, 109, 110, 119, 120, 111, 112
    ]
nanoz_mux2samtec128 = Adapters.Adapter(
    nanoZ_mux_numbers, inclusive_list(1, 160))


## Adapter ON4
# This is the Neuronexus A64-OM32x2 Adaptor
# level 0 : Canonical Samtec ordering, looking into adaptor, top connector
# pins 1-40, bottom connector pins 41-80.
# level 1 : Internal Neuronexus pin numbering
# level 2 : Canonical Omnetics pin numbering
#   right headstage is pins 1-36, left is pins 37-72
#   This is because I know I will plug the first Intan headstage into the
#   right Omnetics connector.
ON4_level0_samtec = inclusive_list(1, 80)
ON4_level1_internal = [
    1, 'G', 'G', 32, 2, 'R', 'R', 31, # Top rows 1-2
    3, 'NC', 'NC', 30, 4, 'NC', 'NC', 29, # Top rows 3-4
    5, 16, 17, 28, 6, 15, 18, 27, # Top rows 5-6
    7, 14, 19, 26, 8, 13, 20, 25, # Top rows 7-8
    9, 12, 21, 24, 10, 11, 22, 23, # Top rows 9-10
    33, 'G', 'G', 64, 34, 'R', 'R', 63, # Bottom rows 1-2
    35, 'NC', 'NC', 62, 36, 'NC', 'NC', 61,
    37, 48, 49, 60, 38, 47, 50, 59, 
    39, 46, 51, 58, 40, 45, 52, 57, 
    41, 44, 53, 56, 42, 43, 54, 55, # Bottom rows 9-10
]

# A mapping between samtec pins and neuronexus pins
ON4_samtec2nn = Adapters.Adapter(ON4_level0_samtec, ON4_level1_internal)


# Now we want the level 2 numbers, which are the Omnetics pin numbers
# ordered as above (Samtec ordering). Annoying to read this off the
# datasheet, it's easier to read the internal pin numbers in the Omnetics
# ordering, then invert it, then convert each internal number in 
# ON4_level1_internal to an Omnetics number.

# Read this directly off datasheet: internal pin numbers, in the Omnetics
# ordering. That is, bottom row right headstage, top row right headstage, 
# bottom row left headstage, top row left headstage, using the standard 
# Omnetics wraparound.
ON4_internal_ordered_by_omnetics = [
    'G1', 55, 54, 56, 53, 57, 52, 58, 51, 59, 50, 60, 49, 61, 62, 63, 64, 'PR1',
    'G2', 32, 31, 30, 29, 17, 28, 18, 27, 19, 26, 20, 25, 21, 24, 22, 23, 'HR2',
    'G3', 33, 34, 35, 36, 48, 37, 47, 38, 46, 39, 45, 40, 44, 41, 43, 42, 'PR3',
    'G4', 10, 11, 9, 12, 8, 13, 7, 14, 6, 15, 5, 16, 4, 3, 2, 1, 'HR4',
]

# Intermediate adapter just to conver those omnetics numbers to internal.
ON4_omnetics2internal = Adapters.Adapter(
    inclusive_list(1, 72),
    ON4_internal_ordered_by_omnetics)

# Invert the intermediate adapter and take the omnetics pins in the ordering
# of ON4_level1_internal
ON4_level2_omnetics = []
for internal_pin in ON4_level1_internal:
    # Try to invert the mapping to get the omnetics pin
    try:
        omnetics_pin = ON4_omnetics2internal.out2in[internal_pin]
    except KeyError:
        # e.g., 'HR' or whatever
        omnetics_pin = 'X'

    ON4_level2_omnetics.append(omnetics_pin)

# Finally, drop all non-integer values from each list
ON4_inputs_samtec = []
ON4_outputs_omnetics = []
assert len(ON4_level0_samtec) == 80
assert len(ON4_level1_internal) == 80
assert len(ON4_level2_omnetics) == 80
zobj = list(zip(ON4_level0_samtec, ON4_level1_internal, ON4_level2_omnetics))
for val0, val1, val2 in zobj:
    if type(val0) is str or type(val1) is str or type(val2) is str:
        continue
    else:
        ON4_inputs_samtec.append(val0)
        ON4_outputs_omnetics.append(val2)

# Generate the adapter
ON4_samtec2omnetics = Adapters.Adapter(ON4_inputs_samtec, ON4_outputs_omnetics)


## Adapter A64-OM32x2-sm
# https://neuronexus.com/wp-content/uploads/2018/09/Adpt-A64-OM32x2-sm-20180307.pdf
# Borrowed from Helen once

# Level 0 Samtec numbers
A64OM32x2sm_level0_samtec = inclusive_list(1, 80)

# Level 1
# Read this off the datasheet
# They are the little numbers printed inside the schematic of the Samtecs
# Top row (left to right), second row, ..., bottom row
# No ground or reference is marked here, not that it matters I guess
A64OM32x2sm_level1_internal = [
    24, 'NC', 'NC', 41, 27, 'NC', 'NC', 38, # Top rows 1-2
    22, 'NC', 'NC', 43, 28, 'NC', 'NC', 37,
    29, 26, 39, 36, 20, 25, 40, 45, 
    18, 23, 42, 47, 16, 21, 44, 49, 
    14, 19, 46, 51, 12, 17, 48, 53, 
    10, 'NC', 'NC', 55, 15, 'NC', 'NC', 50, # Bottom rows 1-2
    8, 'NC', 'NC', 57, 13, 'NC', 'NC', 52,
    6, 11, 54, 59, 4, 5, 60, 61, 
    9, 32, 33, 56, 2, 3, 62, 63, 
    7, 30, 35, 58, 1, 31, 34, 64, # Bottom rows 9-10
]

# A mapping between samtec pins and neuronexus pins
A64OM32x2sm_samtec2nn = Adapters.Adapter(
    A64OM32x2sm_level0_samtec, A64OM32x2sm_level1_internal)

# Now we want the level 2 numbers, which are the Omnetics pin numbers
# ordered as above (Samtec ordering). Annoying to read this off the
# datasheet, it's easier to read the internal pin numbers in the Omnetics
# ordering, then invert it, then convert each internal number in 
# level1_internal to an Omnetics number.

# Read this off the adapter datasheet: internal pin numbers, in the Omnetics
# ordering. I'll define the Omnetics ordering as follows: Looking into the
# headstage, start with bottom right pin on bottom headstage. Proceed
# clockwise, ending with the upper right bin. Then repeat for top headstage.
# The important thing is that this is consistent with the numbering for
# the mating 64-channel headstage in headstages.py.
#
# Because the datasheet is looking out of the headstage, it's actually bottom
# left proceeding counter-clockwise to upper left.
A64OM32x2sm_internal_ordered_by_omnetics = [
    'G1', 48, 46, 44, 42, 40, 39, 43, 41, 24, 22, 26, 25, 23, 21, 19, 17, 'PR1',
    'G2', 12, 14, 16, 18, 20, 29, 28, 27, 38, 37, 36, 45, 47, 49, 51, 53, 'PR2',
    'G3', 64, 58, 63, 56, 61, 59, 52, 50, 15, 13, 6, 4, 9, 2, 7, 1, 'HR3',
    'G4', 31, 30, 3, 32, 5, 11, 8, 10, 55, 57, 54, 60, 33, 62, 35, 34, 'HR4',
]

# Intermediate adapter just to conver those omnetics numbers to internal.
A64OM32x2sm_omnetics2internal = Adapters.Adapter(
    inclusive_list(1, 72),
    A64OM32x2sm_internal_ordered_by_omnetics)

# Invert the intermediate adapter and take the omnetics pins in the ordering
# of ON4_level1_internal
A64OM32x2sm_level2_omnetics = []
for internal_pin in A64OM32x2sm_level1_internal:
    # Try to invert the mapping to get the omnetics pin
    try:
        omnetics_pin = A64OM32x2sm_omnetics2internal.out2in[internal_pin]
    except KeyError:
        # e.g., 'HR' or whatever
        omnetics_pin = 'X'

    A64OM32x2sm_level2_omnetics.append(omnetics_pin)

# Finally, drop all non-integer values from each list
A64OM32x2sm_inputs_samtec = []
A64OM32x2sm_outputs_omnetics = []
assert len(A64OM32x2sm_level0_samtec) == 80
assert len(A64OM32x2sm_level1_internal) == 80
assert len(A64OM32x2sm_level2_omnetics) == 80
zobj = list(zip(
    A64OM32x2sm_level0_samtec, 
    A64OM32x2sm_level1_internal, 
    A64OM32x2sm_level2_omnetics,
))
for val0, val1, val2 in zobj:
    if type(val0) is str or type(val1) is str or type(val2) is str:
        continue
    else:
        A64OM32x2sm_inputs_samtec.append(val0)
        A64OM32x2sm_outputs_omnetics.append(val2)

# Generate the adapter
A64OM32x2sm_samtec2omnetics = Adapters.Adapter(
    A64OM32x2sm_inputs_samtec, A64OM32x2sm_outputs_omnetics)


## Adapter ON2
ON2_samtec2omnetics = Adapters.Adapter(
    [1, 4, 5, 8, 9, 12, 13, 16] + list(range(17, 41)) +
    [41, 44, 45, 48, 49, 52, 53, 56] + list(range(57, 81)),
    [   56, 53, 57, 52, 58, 51, 59, 50, # Rows 1-4 on top
        60, 61, 49, 48, # Row 5
        62, 63, 47, 46, # Row 6
        64, 65, 45, 44, # Row 7
        66, 67, 43, 42, # Row 8
        68, 69, 41, 40, # Row 9
        70, 71, 39, 38, # Row 10
    ] +
    [   20, 17, 21, 16, 22, 15, 23, 14, # Rows 1-4 on bottom
        24, 25, 13, 12, # Row 5 
        26, 27, 11, 10, # Row 6
        28, 29, 9, 8, # Row 7
        30, 31, 7, 6, # Row 8
        32, 33, 5, 4, # Row 9
        34, 35, 3, 2] # Row 10
    )


# This is for the Plexon double-neuronexus to double-omnetics connector
# Looking at the datasheet, the Samtec connectors are oriented like
# looking into the probe. So pin 1 is in the upper right of the top connector.
# Pin 41 is in the upper right of the bottom connector
# The output is "Plexon channel numbers", which only makes sense after
# converting to my Omnetics numbering
plexon64ch_samtec2plexonnumbers = Adapters.Adapter(
    [1, 4, 5, 8, 9, 12, 13, 16] + list(range(17, 41)) +
    [41, 44, 45, 48, 49, 52, 53, 56] + list(range(57, 81)),
    [   48, 32, 64, 16, 47, 31, 63, 15,
        46, 62, 14, 30, 45, 61, 13, 29, 44, 60, 12, 28, 43, 59, 11, 27, 
        42, 58, 10, 26, 41, 57, 9, 25] + 
    [   56, 8, 40, 24, 55, 7, 39, 23,
        38, 54, 6, 22, 37, 53, 5, 21, 36, 52, 4, 20, 
        35, 51, 3, 19, 34, 50, 2, 18, 33, 49, 1, 17])


# This converts plexon numbering to Omnetics numbering. Sadly, their
# Omnetics numbering doesn't match mine, so I'll just use mine. This is valid
# if we line up the connectors such that the "Omnetics" logo matches.
# Mine goes from #1 (bottom right looking into right-side up headstage)
# to #36 (but not using 1, 18, 19, or 36) and then from #37 to #72 
# (but not using 37, 54, 55, or 72).
# My Pin #1 is their Pin #19, and my Pin #36 is their pin #1
# This also assumes that we plug the MISO1 Omnetics adapter on the flexible
# adapter into the Omnetics connector labeled CH1-32
plexon64ch_omnetics2plexonnumbers = Adapters.Adapter(
    list(range(2, 18)) + list(range(20, 36)) + 
    list(range(38, 54)) + list(range(56, 72)),
    list(range(32, 16, -1)) + list(range(1, 17)) +
    list(range(64, 48, -1)) + list(range(33, 49))
    )


## This is for my actual adapter (ON1), which has the samtec numbering reversed
## within each row because I put the plug on the wrong side. 

#~ # This is how you can generate it
#~ flipped_ordering = np.concatenate([np.array([3, 2, 1, 0]) + start 
    #~ for start in range(1, 38, 4)])
#~ flipped_ins, flipped_outs = [], []
#~ for nidx, idx in enumerate(flipped_ordering):
    #~ if idx in samtec2omnetics.ins:
        #~ flipped_ins.append(nidx + 1)
        #~ flipped_outs.append(samtec2omnetics[idx])
#~ samtecflipped2omnetics1 = Adapters.Adapter(flipped_ins, flipped_outs)
#~ samtecflipped2omnetics1.sort_by('ins')

## The actual adapter ON1, hard-coded
samtecflipped2omnetics = Adapters.Adapter([
    [1, 20],
    [2, 19],
    [4, 17],
    [5, 21],
    [7, 18],
    [8, 16],
    [9, 22],
    [12, 15],
    [13, 23],
    [16, 14],
    [17, 25],
    [18, 24],
    [19, 13],
    [20, 12],
    [21, 27],
    [22, 26],
    [23, 11],
    [24, 10],
    [25, 29],
    [26, 28],
    [27, 9],
    [28, 8],
    [29, 31],
    [30, 30],
    [31, 7],
    [32, 6],
    [33, 33],
    [34, 32],
    [35, 5],
    [36, 4],
    [37, 35],
    [38, 34],
    [39, 3],
    [40, 2]])