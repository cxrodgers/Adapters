"""Info about my headstage and GUI channel mapping"""


from builtins import range
import Adapters

# This converts ordinal numbered Omnetics pins to Intan numbers using the
# picture of the headstage.
# Looking into the headstage when it is right-side up, pin #1 (GND) is in 
# the lower right. Pin numbers increase clockwise. Pin #36 is in the 
# upper right (REF).
omnetics2intan = Adapters.Adapter(
    list(range(1, 37)), [
    'GND', 7, 6, 5, 4, 3, 2, 1, 0, 31, 30, 29, 28, 27, 26, 25, 24, 'REF',
    'GND', 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 'REF'],
    )

# This is just a 64-channel version of omnetics2intan
# I'm assuming that MISO1 is first and MISO2 is second\
omnetics2intan_64ch = Adapters.Adapter(
    list(range(1, 73)), [
    'GND', 7, 6, 5, 4, 3, 2, 1, 0, 31, 30, 29, 28, 27, 26, 25, 24, 'REF',
    'GND', 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 'REF',
    'GND', 39, 38, 37, 36, 35, 34, 33, 32, 63, 62, 61, 60, 59, 58, 57, 56, 'REF',
    'GND', 55, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 'REF',
    ],
    )

# This is the 64-channel Intan headstage RHD2164
# (not the double 32-channel stuff above)
# http://intantech.com/RHD2164_amp_board.html
# I read these numbers off the image in the standard direction: Look into
# the bottom headstage, start on bottom right, proceed clockwise, end on 
# top right. Repeat for top headstage.
omnetics2rhd2164 = Adapters.Adapter(
    list(range(1, 73)), [
    'GND', 14, 12, 10, 8, 6, 4, 2, 0, 62, 60, 58, 56, 54, 52, 50, 48, 'REF',
    'GND', 49, 51, 53, 55, 57, 59, 61, 63, 1, 3, 5, 7, 9, 11, 13, 15, 'REF',
    'GND', 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 'REF',
    'GND', 46, 44, 42, 40, 38, 36, 34, 32, 30, 28, 26, 24, 22, 20, 18, 16, 'REF',
    ],
)    


## GUI numbers
# The GUI numbers are 1 + the intan numbers
# This is used for making the channel mapping
intan2gui = Adapters.Adapter(list(range(36)), list(range(1, 37)))

# This is a 64-ch version
intan2gui_64ch = Adapters.Adapter(list(range(72)), list(range(1, 73)))