"""Module providing Adapter object."""
import numpy as np


class Adapter:
    """Object representing inputs and outputs of a physical adapter.
    
    An Adapter is intialized with lists of all the input channels and
    output channels. It provides convenience methods to look up channnels
    or to chain adapters together using `+`.
    
    Properties:
    in2out : dict-like, looks up output for a specified input
    out2in : dict-like, looks up input for a specified output
    """
    def __init__(self, l1, l2=None):
        """Initialize a new adapter.
        
        l1 : list-like, list of channel ids for each channel on the
            input of the adapter. The channel ids can be any hashable Python 
            object, including integers or strings, but not a list.
        l2 : list-like, of same length as `d_or_l1`, of the outputs of the
            adapter, and in corresponding order to l1.
        
        If there is no corresponding input for a given output, put None
        at that point in the list (and vice versa). Therefore None cannot
        be used as a channel id.
        
        Internally everything is represented as a Nx2 ndarray called `table`.
        An alternative method of initialization is to pass this sort of array
        as `l1` and leave l2 as None.
        """
        self.table = None
        self._in2out = None
        self._out2in = None
        
        # Determine type of initialization
        if l2 is not None:
            # two list mapping
            a = [[i1, i2] for i1, i2 in zip(l1, l2)]
        else:
            # interpret l1 as a tble
            a = l1
        
        # Convert to internal representation
        self.table = np.asarray(a, dtype=np.object)
        if self.table.ndim != 2 or self.table.shape[1] != 2:
            raise Exception("table should be a Nx2 array")
    
    @property
    def in2out(self):
        # Return memoized dict
        if self._in2out is None:
            res = {}
            for i1, i2 in self.table:
                if i1 is None:
                    continue
                if i1 in res:
                    print "warning: duplicate keys in 'in' column"
                res[i1] = i2
            self._in2out = res
        return self._in2out
    
    @property
    def out2in(self):
        # Return memoized dict
        if self._out2in is None:
            res = {}
            for i2, i1 in self.table:
                if i1 is None:
                    continue
                if i1 in res:
                    print "warning: duplicate keys in 'out' column"
                res[i1] = i2
            self._out2in = res
        return self._out2in
    
    @property
    def outs(self):
        return self.table[:, 1]
    
    @property
    def ins(self):
        return self.table[:, 0]
    
    def __add__(self, a2):
        """Append a new column and keep the intermediaries?"""
        a3 = Adapter(self.ins.copy(), self.outs.copy())
        d = a2.in2out
        for n, i2 in enumerate(self.outs):
            try:
                a3.table[n, 1] = d[i2]
            except KeyError:
                a3.table[n, 1] = None
        return a3
    
    def __getitem__(self, key):
        return self.in2out[key]
    
    @property
    def inv(self):
        return Adapter(self.outs, self.ins)
    
    def slice(self, l):
        """Return new Adapater, slice of this one
        Reimplement sort_by with this
        """
        pass
    
    def sort_by(self, keys, reverse=False):
        if keys == 'ins':
            keys = sorted(self.table[:, 0])
        elif keys == 'outs':
            t = sorted(self.table[:, 1])
            keys = [self.out2in[tt] for tt in t]
            
        
        if reverse:
            keys = keys[::-1]
    
        l2 = [self.in2out[key] if key in self.in2out else None for key in keys]
        
        self.table = np.array([[ll1, ll2] for ll1, ll2 in zip(keys, l2)],
            dtype=np.object)
        
        return self


    