"""Module for keeping track of adapters.

base.py provides the Adapter class
channels : the list of channels sorted geometrically as they are on each
    probe
probes : the mapping between the channel numbers and the Samtec numbers
    for each probe. This is now a misnomer, it seems to only be for 
    mapping Samtec pins to electrode numbers.
probe_adapters : the mapping from Samtec numbers through the various
    kinds of adapters that I've made. This is now the one we use for 
    almost everything, including stuff that doesn't go through Samtec.
headstages : the mapping onto Intan stuff
dataflow : constructing the complete flow of channels from probe to
    headstage
"""
from __future__ import absolute_import

from .base import Adapter
from . import channels
from . import probe_adapters
from . import probes
from . import headstages
from . import dataflow
