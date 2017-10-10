"""The various adapters I've made that go from Samtec to headstage.

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

import Adapters
import numpy as np

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


# Not sure what this is anymore, maybe the original time that I mapped
# out NN to Samtec to Intan instead of the individual stages as below
#~ # This is my NN2Intan adapter that takes us from Neuronexus numbering
#~ # to Intan numbering. Intan numbering is equivalent to datafile column
#~ # ordering, and to the GUI number - 1.
#~ nn2intan = Adapters.Adapter(list(range(1, 33)), [
    #~ 19, 16, 18, 17, 20, 14, 21, 12, 22, 10, 23, 8, 15, 13, 11, 9, 6, 4,
    #~ 2, 0, 7, 3, 5, 30, 1, 28, 31, 27, 29, 25, 26, 24]
   #~ )


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



## This is how ON1 was designed to be, but I never actually built this
## (see below)
#~ # This is from samtec numbers to Omnetics numbers
#~ # This is the actual numbering on the Omnetics connector, from 1-36
#~ samtec2omnetics = Adapters.Adapter([
    #~ [1, 17],
    #~ [3, 19],
    #~ [4, 20],
    #~ [5, 16],
    #~ [6, 18],
    #~ [8, 21],
    #~ [9, 15],
    #~ [12, 22],
    #~ [13, 14],
    #~ [16, 23],
    #~ [17, 12],
    #~ [18, 13],
    #~ [19, 24],
    #~ [20, 25],
    #~ [21, 10],
    #~ [22, 11],
    #~ [23, 26],
    #~ [24, 27],
    #~ [25, 8],
    #~ [26, 9],
    #~ [27, 28],
    #~ [28, 29],
    #~ [29, 6],
    #~ [30, 7],
    #~ [31, 30],
    #~ [32, 31],
    #~ [33, 4],
    #~ [34, 5],
    #~ [35, 32],
    #~ [36, 33],
    #~ [37, 2],
    #~ [38, 3],
    #~ [39, 34],
    #~ [40, 35]])

## This is for my actual adapter (ON1), which has the samtec numbering reversed
# within each row because I put the plug on the wrong side. 

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