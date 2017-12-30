"""Complete flow of data, from probe to adapter to headstage."""

import pandas
import numpy as np

from probe_adapters import \
    samtecflipped2omnetics, \
    plexon64ch_samtec2plexonnumbers, \
    plexon64ch_omnetics2plexonnumbers, \
    ON2_samtec2omnetics, \
    ON4_samtec2omnetics

from probes import \
    samtec2nn, \
    samtec2janelia_top, \
    samtec2janelia_bottom, \
    samtec2janelia_64ch, \
    adrian_8shank2interposer, \
    interposer2samtec_shifted
    
from headstages import \
    intan2gui, \
    omnetics2intan, \
    omnetics2intan_64ch, \
    intan2gui_64ch

from channels import \
    poly2_NN_sort_by_depth, \
    edge_NN_sort_by_depth, \
    janelia_top_sort_by_depth, \
    janelia_bottom_sort_by_depth, \
    janelia_sort_by_depth, \
    janelia_depth_df, \
    h3_depth_df

## Construct the entire dataflow
# Neuronexus probes
dataflow_poly2 = (
    samtec2nn.inv + samtecflipped2omnetics + omnetics2intan + intan2gui).sort_by(
    poly2_NN_sort_by_depth)
dataflow_edge = (
    samtec2nn.inv + samtecflipped2omnetics + omnetics2intan + intan2gui).sort_by(
    edge_NN_sort_by_depth)

# Janelia top and bottom
dataflow_janelia_top = (
    samtec2janelia_top.inv + 
    samtecflipped2omnetics + 
    omnetics2intan + 
    intan2gui
    ).sort_by(janelia_top_sort_by_depth)
dataflow_janelia_bottom = (
    samtec2janelia_bottom.inv + 
    samtecflipped2omnetics + 
    omnetics2intan + 
    intan2gui
    ).sort_by(janelia_bottom_sort_by_depth)

# Janelia Plexon adapter
dataflow_janelia_64ch_plexon = (
    samtec2janelia_64ch.inv + 
    plexon64ch_samtec2plexonnumbers + 
    plexon64ch_omnetics2plexonnumbers.inv +
    omnetics2intan_64ch + 
    intan2gui_64ch
    ).sort_by(janelia_sort_by_depth)

# Janelia ON2 and ON4
dataflow_janelia_64ch_ON2 = (
    samtec2janelia_64ch.inv + 
    ON2_samtec2omnetics + 
    omnetics2intan_64ch + 
    intan2gui_64ch
    ).sort_by(janelia_sort_by_depth)

dataflow_janelia_64ch_ON4 = (
    samtec2janelia_64ch.inv + 
    ON4_samtec2omnetics + 
    omnetics2intan_64ch + 
    intan2gui_64ch
    ).sort_by(janelia_sort_by_depth)

# Adrian
dataflow_adrian = (
    adrian_8shank2interposer + 
    interposer2samtec_shifted + 
    ON4_samtec2omnetics + 
    omnetics2intan_64ch + 
    intan2gui_64ch
    )


# Dataframe it
dataflow_poly2_df = pandas.DataFrame(dataflow_poly2.table,
    columns=['NN', 'Sam', 'Om', 'Int', 'GUI'], dtype=np.int)
dataflow_edge_df = pandas.DataFrame(dataflow_edge.table,
    columns=['NN', 'Sam', 'Om', 'Int', 'GUI'], dtype=np.int)
dataflow_janelia_top_df = pandas.DataFrame(dataflow_janelia_top.table,
    columns=['J', 'Sam', 'Om', 'Int', 'GUI'], dtype=np.int)
dataflow_janelia_bottom_df = pandas.DataFrame(dataflow_janelia_bottom.table,
    columns=['J', 'Sam', 'Om', 'Int', 'GUI'], dtype=np.int)
dataflow_janelia_64ch_plexon_df = pandas.DataFrame(dataflow_janelia_64ch_plexon.table,
    columns=['J', 'Sam', 'Plx', 'Om', 'Int', 'GUI'], dtype=np.int)
dataflow_janelia_64ch_ON2_df = pandas.DataFrame(dataflow_janelia_64ch_ON2.table,
    columns=['J', 'Sam', 'Om', 'Int', 'GUI'], dtype=np.int)
dataflow_janelia_64ch_ON4_df = pandas.DataFrame(dataflow_janelia_64ch_ON4.table,
    columns=['J', 'Sam', 'Om', 'Int', 'GUI'], dtype=np.int)
dataflow_adrian_df = pandas.DataFrame(dataflow_adrian.table,
    columns=['E', 'Interp', 'Sam', 'Om', 'Int', 'GUI'], dtype=np.int)

# The dataflow for H3 is actually the same as for the others, except for
# the channel ordering (imposed below)
dataflow_h3_ON4_df = pandas.DataFrame(dataflow_janelia_64ch_ON4.table.copy(),
    columns=['Prb', 'Sam', 'Om', 'Int', 'GUI'], dtype=np.int)

# Join a depth column
# For Janelia and H3, this also inserts channel numbers
dataflow_poly2_df['Z'] = list(range(0, 32 * 25, 25))
dataflow_edge_df['Z'] = list(range(0, 32 * 20, 20))
dataflow_janelia_top_df = dataflow_janelia_top_df.join(
    janelia_depth_df.set_index('J'), on='J')
dataflow_janelia_bottom_df = dataflow_janelia_bottom_df.join(
    janelia_depth_df.set_index('J'), on='J') 
dataflow_janelia_64ch_plexon_df = dataflow_janelia_64ch_plexon_df.join(
    janelia_depth_df.set_index('J'), on='J')
dataflow_janelia_64ch_ON2_df = dataflow_janelia_64ch_ON2_df.join(
    janelia_depth_df.set_index('J'), on='J')
dataflow_janelia_64ch_ON4_df = dataflow_janelia_64ch_ON4_df.join(
    janelia_depth_df.set_index('J'), on='J')
dataflow_h3_ON4_df = dataflow_h3_ON4_df.join(
    h3_depth_df.set_index('Prb'), on='Prb')

## Sort by depth
dataflow_h3_ON4_df = dataflow_h3_ON4_df.sort_values('Z')
dataflow_h3_ON4_df.index = np.arange(len(dataflow_h3_ON4_df), dtype=np.int)

# I don't why this step isn't necessary for the janelia ones
assert np.all(
    np.sort(dataflow_janelia_64ch_ON2_df['Z'].values) == 
    dataflow_janelia_64ch_ON4_df['Z'].values)
assert np.all(
    np.sort(dataflow_janelia_64ch_ON2_df['Z'].values) == 
    dataflow_janelia_64ch_ON4_df['Z'].values)

# Join a Sorted column, which is 1+index after we've sorted by depth
dataflow_janelia_64ch_ON2_df.insert(dataflow_janelia_64ch_ON2_df.shape[1],
    'Srt',
    dataflow_janelia_64ch_ON2_df.index.values + 1)
dataflow_janelia_64ch_ON4_df.insert(dataflow_janelia_64ch_ON4_df.shape[1],
    'Srt',
    dataflow_janelia_64ch_ON4_df.index.values + 1)
dataflow_h3_ON4_df.insert(dataflow_h3_ON4_df.shape[1],
    'Srt',
    dataflow_h3_ON4_df.index.values + 1)
    
