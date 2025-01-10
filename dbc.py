"""All results for Diagnostic Biochips probes.

From now on, I think it makes more sense to organize this module by 
probe type. 

And each individual probe should be a function, so if there's an error
somewhere it doesn't break the whole module. 
"""

import numpy as np
import pandas

def h3_64ch_assy_325():
    """Return dataflow for Diagnostic Biochips 64-4
    
    This probe was renamed ASSY-325 H3 & L3 by Cambridge Neurotech.
    """
    # Channel numbers are always sorted from superficial to deep
    # Supposedly these channel numbers are OpenEphys numbers    
    # This is for Diagnostic Biochips 64-4, which was renamed ASSY-325 H3 & L3
    # by Cambridge Neurotech. I don't know if it's literally the same as
    # the old H3 I used to use. These numbers are read straight off the 
    # datasheet from Jesse Goins.
    # Supposedly these channel numbers are OpenEphys numbers, so the 
    # bottom channel will be OpenEphys 62, no further mapping necessary.
    assy325_sort_by_depth = np.array([
        0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1,
        16, 18, 20, 22, 24, 26, 28, 30, 31, 29, 27, 25, 23, 21, 19, 17,
        47, 45, 43, 41, 39, 37, 35, 33, 32, 34, 36, 38, 40, 42, 44, 46,
        63, 61, 59, 57, 55, 53, 51, 49, 48, 50, 52, 54, 56, 58, 60, 62,
        ])


    ## Make dataflow for assy-325
    # Take each of the entries in the lists above and rename them Intan because
    # they are Intan numbers in geometric order
    assy325_dataflow = pandas.Series(
        assy325_sort_by_depth).rename('Intan').to_frame()

    # Define a site number which really just defines a geometric ordering
    assy325_dataflow.index.name = 'site'
    assy325_dataflow = assy325_dataflow.reset_index()

    # Add depth
    assy325_dataflow['Z'] = assy325_dataflow['site'] * 20

    # Add GUI order, which is just 1 + Intan order
    assy325_dataflow['GUI'] = assy325_dataflow['Intan'] + 1

    # Always index by site
    assy325_dataflow = assy325_dataflow.sort_index()
    
    return assy325_dataflow

def h12_128ch_assy_350():
    """Return dataflow for Diagnostic Biochips 128-2
    
    This probe was renamed ASSY-350 H12 & L13 by Cambridge Neurotech.
    
    With the connectorized side facing you and shanks pointing downward, 
    Shank A is on the right, and the actual electrodes are on the back side.
    """
    # Supposedly these channel numbers are OpenEphys numbers
    assy350_shank_a_sort_by_depth = np.array([
        15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0,
        31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 
        47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 
        63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48,
        ])

    assy350_shank_b_sort_by_depth = assy350_shank_a_sort_by_depth + 64

    # By convention, sort first Shank A and then Shank B, both from 
    # superficial to deep
    assy350_both_shanks_canonical_sort_order = np.concatenate([
        assy350_shank_a_sort_by_depth,
        assy350_shank_b_sort_by_depth,
        ])


    ## Make dataflow for assy-350
    # Concatenate the Intan numbers for each shank
    assy350_dataflow = pandas.concat([
        pandas.Series(assy350_shank_a_sort_by_depth).rename('A'),
        pandas.Series(assy350_shank_b_sort_by_depth).rename('B'),
        ], axis=1)
    assy350_dataflow.columns.name = 'shank'
    assy350_dataflow.index.name = 'shank_site'

    # Stack them (shank first) and label them Intan
    assy350_dataflow = assy350_dataflow.T.stack().rename('Intan').reset_index()

    # Define and pop a 'site' index, which defines the standard ordering
    assy350_dataflow.index.name = 'site'
    assy350_dataflow = assy350_dataflow.reset_index()

    # Add depth
    assy350_dataflow['Z'] = assy350_dataflow['shank_site'] * 20

    # Add GUI order, which is just 1 + Intan order
    assy350_dataflow['GUI'] = assy350_dataflow['Intan'] + 1

    # Always index by site
    assy350_dataflow = assy350_dataflow.sort_index()
    
    return assy350_dataflow
