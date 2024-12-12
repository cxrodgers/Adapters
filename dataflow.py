"""Complete flow of data, from probe to adapter to headstage."""
from __future__ import absolute_import

from builtins import range
import pandas
import numpy as np

from .probe_adapters import \
    samtecflipped2omnetics, \
    plexon64ch_samtec2plexonnumbers, \
    plexon64ch_omnetics2plexonnumbers, \
    ON2_samtec2omnetics, \
    ON4_samtec2omnetics, \
    A64OM32x2sm_samtec2omnetics, \
    wire64_eib_numbers2names, \
    wire64_slimstack2headstage, \
    wire64_eib_names2headstage,\
    wire128_eib_numbers2names, \
    wire128_slimstack2headstage, \
    wire128_eib_names2headstage, \
    nza_SSB6_64,  \
    nza_SSB6_128, \
    nanoz_mux2samtec, \
    nanoz_mux2samtec128

from .probes import \
    samtec2nn, \
    samtec2janelia_top, \
    samtec2janelia_bottom, \
    samtec2janelia_64ch
    
from .headstages import \
    intan2gui, \
    omnetics2intan, \
    omnetics2intan_64ch, \
    intan2gui_64ch, \
    omnetics2rhd2164

from .channels import \
    poly2_NN_sort_by_depth, \
    edge_NN_sort_by_depth, \
    janelia_top_sort_by_depth, \
    janelia_bottom_sort_by_depth, \
    janelia_sort_by_depth, \
    janelia_depth_df, \
    h3_sort_by_depth, \
    h3_depth_df

## Construct the entire dataflow

# for wire64
"""
Checks:
* This should match the MUX numbers arranged by Samtec in nanoZ manual
  Adapters.dataflow.wire64_big_dataflow.set_index(
  'samtec')['mux'].sort_index().reindex(range(1, 81)).values.reshape(20, 4)
* This should match the HS numbers arranged by SlimStack in Tim's image of
  the headstage. GND/REF are excluded, top is on top, order is flipped to
  match Tim's image.
  Adapters.dataflow.wire64_big_dataflow.set_index(
  'slimstack')['hs'].sort_index().values.reshape(4, 16)[[2, 3, 0, 1], ::-1] 
* This should match the MUX numbers, sorted by headstage numbers, in the
  adaptors.ini addition for NZA SSB64 from Tim.
  Adapters.dataflow.wire64_big_dataflow.set_index('hs')['mux'].sort_index()
* This should match the MUX numbers, sorted by EIB numbers, in the V2 version
  of the adaptors.ini that I made to be in tetrode order.
  Adapters.dataflow.wire64_big_dataflow.set_index('enum')['mux'].sort_index()
* This should match the EIB names, sorted by hs number, in the spreadsheet
  from Tim
  Adapters.dataflow.wire64_big_dataflow.set_index('hs')['ename'].sort_index()
"""
wire64_big_dataflow = pandas.DataFrame((
    wire64_eib_numbers2names + # enum to ename
    wire64_eib_names2headstage +  # ename to hs
    nza_SSB6_64.inv + # hs to mux
    nanoz_mux2samtec # mux to samtec
    ).table, 
    columns=['enum', 'ename', 'hs', 'mux', 'samtec'])

wire64_big_dataflow = wire64_big_dataflow.join(
    pandas.DataFrame(wire64_slimstack2headstage.table, 
    columns=['slimstack', 'hs']).set_index('hs'), on='hs')
    
# for wire128
wire128_big_dataflow = pandas.DataFrame((
    wire128_eib_numbers2names + # enum to ename
    wire128_eib_names2headstage +  # ename to hs
    nza_SSB6_128.inv + # hs to mux
    nanoz_mux2samtec128 # mux to samtec
    ).table, 
    columns=['enum', 'ename', 'hs', 'mux', 'samtec'])

wire128_big_dataflow = wire128_big_dataflow.join(
    pandas.DataFrame(wire128_slimstack2headstage.table, 
    columns=['slimstack', 'hs']).set_index('hs'), on='hs')
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

# Helen's A64OM32x2sm and rhd2164 dataflow
dataflow_helen_64ch = (
    samtec2janelia_64ch.inv + # Defines ordering within the Samtec
    A64OM32x2sm_samtec2omnetics + # Samtec to Omnetics
    omnetics2rhd2164 + # Omnetics to Intan headstage
    intan2gui_64ch # Intan to GUI numbers
    ).sort_by(h3_sort_by_depth) # Sorts by H3 depth and excludes NC

# Dataframe it
dataflow_poly2_df = pandas.DataFrame(dataflow_poly2.table,
    columns=['NN', 'Sam', 'Om', 'Int', 'GUI'], dtype=int)
dataflow_edge_df = pandas.DataFrame(dataflow_edge.table,
    columns=['NN', 'Sam', 'Om', 'Int', 'GUI'], dtype=int)
dataflow_janelia_top_df = pandas.DataFrame(dataflow_janelia_top.table,
    columns=['J', 'Sam', 'Om', 'Int', 'GUI'], dtype=int)
dataflow_janelia_bottom_df = pandas.DataFrame(dataflow_janelia_bottom.table,
    columns=['J', 'Sam', 'Om', 'Int', 'GUI'], dtype=int)
dataflow_janelia_64ch_plexon_df = pandas.DataFrame(dataflow_janelia_64ch_plexon.table,
    columns=['J', 'Sam', 'Plx', 'Om', 'Int', 'GUI'], dtype=int)
dataflow_janelia_64ch_ON2_df = pandas.DataFrame(dataflow_janelia_64ch_ON2.table,
    columns=['J', 'Sam', 'Om', 'Int', 'GUI'], dtype=int)
dataflow_janelia_64ch_ON4_df = pandas.DataFrame(dataflow_janelia_64ch_ON4.table,
    columns=['J', 'Sam', 'Om', 'Int', 'GUI'], dtype=int)

# The dataflow for H3 is actually the same as for the others, except for
# the channel ordering (imposed below)
dataflow_h3_ON4_df = pandas.DataFrame(dataflow_janelia_64ch_ON4.table.copy(),
    columns=['Prb', 'Sam', 'Om', 'Int', 'GUI'], dtype=int)

# Construct the Helen dataflow
dataflow_helen_64ch_df = pandas.DataFrame(dataflow_helen_64ch.table,
    columns=['Prb', 'Sam', 'Om', 'Int', 'GUI'], dtype=int)

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

# Join depth column on Helen
dataflow_helen_64ch_df = dataflow_helen_64ch_df.join(
    h3_depth_df.set_index('Prb'), on='Prb')
    

## Sort by depth
dataflow_h3_ON4_df = dataflow_h3_ON4_df.sort_values('Z')
dataflow_h3_ON4_df.index = np.arange(len(dataflow_h3_ON4_df), dtype=int)

# This isn't necessary for the Janelia ones because they were sorted above
assert np.all(
    np.sort(dataflow_janelia_64ch_ON2_df['Z'].values) == 
    dataflow_janelia_64ch_ON4_df['Z'].values)
assert np.all(
    np.sort(dataflow_janelia_64ch_ON2_df['Z'].values) == 
    dataflow_janelia_64ch_ON4_df['Z'].values)
assert np.all(
    np.sort(dataflow_helen_64ch_df['Z'].values) == 
    dataflow_helen_64ch_df['Z'].values)

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
dataflow_helen_64ch_df.insert(dataflow_helen_64ch_df.shape[1],
    'Srt',
    dataflow_helen_64ch_df.index.values + 1)
