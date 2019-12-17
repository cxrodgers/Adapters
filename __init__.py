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
from __future__ import absolute_import

from .base import Adapter
from . import channels
reload(channels)
from . import probe_adapters
reload(probe_adapters)
from . import probes
reload(probes)
from . import headstages
reload(headstages)
from . import dataflow
reload(dataflow)