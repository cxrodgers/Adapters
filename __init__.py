"""Module for keeping track of adapters.

base.py provides the Adapter class
channels : the list of channels sorted geometrically as they are on each
    probe
probes : the mapping between the channel numbers and the Samtec numbers
    for each probe
probe_adapters : the mapping from Samtec numbers through the various
    kinds of adapters that I've made
headstages : the mapping onto Intan stuff
dataflow : constructing the complete flow of channels from probe to
    headstage
"""

from base import Adapter
import channels
reload(channels)
import probe_adapters
reload(probe_adapters)
import probes
reload(probes)
import headstages
reload(headstages)
import dataflow
reload(dataflow)