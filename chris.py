"""Module providing my specific adapters

Actually this is all outdated now, just for my old stuff.
"""
from __future__ import absolute_import
from builtins import range
from .base import Adapter

# Mat's adapters
hd5a_hdmi2dip = Adapter(
    list(range(2, 18)),
    [4, 12, 13, 5, 3, 11, 14, 6, 2, 10, 15, 7, 1, 9, 16, 8],
    )

hd5a_hdmi2dip = Adapter(
    list(range(2, 18)),
    [5, 13, 12, 4, 6, 14, 11, 3, 7, 15, 10, 2, 8, 16, 9, 1],
    )

ho4_hdmi2headstage = Adapter(
    list(range(1, 20)),
    ['ACGnd', 24, 9, 25, 10, 26, 11, 27, 12, 28, 13, 29, 14, 30, 15, 31, 16, None, 33]
    )


headstage2fea = Adapter(
    [32, 16, 31, 15, 30, 14, 29, 13, 28, 12, 27, 11, 26, 10, 25, 9] +
    [1, 17, 2, 18, 3, 19, 4, 20, 5, 21, 6, 22, 7, 23, 8, 24] + 
    ['ACGnd', 33],
    [31, 32, 29, 30, 27, 28, 25, 26, 23, 24, 21, 22, 19, 20, 17, 18] +
    list(range(1, 17)) + ['GND', 'REF'])

tetname2mdp = Adapter(
    ['GND', 'REF'] + 
    ['T1-1', 'T1-2', 'T1-3', 'T1-4'] + 
    ['T2-1', 'T2-2', 'T2-3', 'T2-4'] + 
    ['T3-1', 'T3-2', 'T3-3', 'T3-4'] + 
    ['T4-1', 'T4-2', 'T4-3', 'T4-4'],
    [1, 2, 3, 5, 7, 9, 4, 6, 8, 10, 11, 13, 15, 17, 12, 14, 16, 18]
    )

hd4_hdmi2dip = Adapter(
    [3, 5, 7, 9, 11, 13, 15, 17, 2, 4, 6, 8, 10, 12, 14, 16],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 16, 15, 14, 13, 12, 11, 10])

tetname2hdmi = Adapter(
    ['GND', 'REF'] + 
    ['T1-1', 'T1-2', 'T1-3', 'T1-4'] + 
    ['T2-1', 'T2-2', 'T2-3', 'T2-4'] + 
    ['T3-1', 'T3-2', 'T3-3', 'T3-4'] + 
    ['T4-1', 'T4-2', 'T4-3', 'T4-4'],
    [1, 19] + 
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])

# this is technically adapter DD1?? DD2
tetnamedual2mdpdual = Adapter(
    ['GND', 'REF'] + 
    ['T1A-1', 'T1A-2', 'T1A-3', 'T1A-4'] + 
    ['T2A-1', 'T2A-2', 'T2A-3', 'T2A-4'] + 
    ['T3A-1', 'T3A-2', 'T3A-3', 'T3A-4'] + 
    ['T4A-1', 'T4A-2', 'T4A-3', 'T4A-4'] + 
    ['T1P-1', 'T1P-2', 'T1P-3', 'T1P-4'] + 
    ['T2P-1', 'T2P-2', 'T2P-3', 'T2P-4'] + 
    ['T3P-1', 'T3P-2', 'T3P-3', 'T3P-4'] + 
    ['T4P-1', 'T4P-2', 'T4P-3', 'T4P-4'],    
    ['1P', '2P'] + 
    ['3A', '5A', '7A', '9A', '4A', '6A', '8A', '10A'] +
    ['11A', '13A', '15A', '17A', '12A', '14A', '16A', '18A'] +
    ['3P', '5P', '7P', '9P', '4P', '6P', '8P', '10P'] +
    ['11P', '13P', '15P', '17P', '12P', '14P', '16P', '18P']
    )


mdp2dip = Adapter(
    [1, 2, 3, 5, 7, 9, 4, 6, 8, 10, 11, 13, 15, 17, 12, 14, 16, 18],
    ['GND', 'REF', 1, 3, 5, 7, 2, 4, 6, 8, 9, 11, 13, 15, 10, 12, 14, 16])

do2_mdp2headstage = Adapter(
    ['1P', '2P'] + 
    ['3A', '5A', '7A', '9A', '4A', '6A', '8A', '10A'] +
    ['11A', '13A', '15A', '17A', '12A', '14A', '16A', '18A'] +
    ['3P', '5P', '7P', '9P', '4P', '6P', '8P', '10P'] +
    ['11P', '13P', '15P', '17P', '12P', '14P', '16P', '18P'],
    ['GND', 'REF'] + 
    [1, 2, 3, 4, 17, 18, 19, 20, 5, 6, 7, 8, 21, 22, 23, 24] + 
    [32, 31, 30, 29, 16, 15, 14, 13] + 
    [28, 27, 26, 25, 12, 11, 10, 9]
    )

dip2map_mdp_cols = Adapter(
    [1, 3, 5, 7, 2, 4, 6, 8, 9, 11, 13, 15, 10, 12, 14, 16],
    list(range(1, 17)))

do2_tetnamedual2headstage = tetnamedual2mdpdual + do2_mdp2headstage
do2_tetnamedual2fea = do2_tetnamedual2headstage + headstage2fea
tetname2dip = tetname2mdp + mdp2dip
tetname2map_mdp_cols = tetname2dip + dip2map_mdp_cols