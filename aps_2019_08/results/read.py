"""Update the HDF5 table"""
from collections import namedtuple
import argparse
import sys

import numpy as np
import h5py


# This is the GrainData  base class from hexrd, but we include it here so that
# we do not require the full hexrd package.

_flds = [
    "id", "completeness", "chisq", "expmap", "centroid", "inv_Vs", "ln_Vs"
]
GrainData = namedtuple("GrainData", _flds)


def read_graindata(hfile, sample):
    """Update the HDF5 file

    PARAMETERS
    ----------
    hfile: str or Path
        name of data file
    sample: str
        HDF5 path to data
    """
    with h5py.File(hfile, "r") as hf:
        gdata = _read_graindata(hf, sample)

    return gdata


def _read_graindata(hf, sample):
    """Read grain data

    PARAMETERS
    ----------
    hf: h5py.File instance
        the HDF5 data file
    sample: str
        HDF5 path to data
    """
    data = hf[sample]
    states = data["states"]
    nstates = len(states)
    ngrains = data[f"states/state_00/ff/table"].shape[0]
    #
    # Initialize the grain data arrays.
    #
    gid = np.zeros((nstates, ngrains), dtype=int)
    cmpl = np.zeros((nstates, ngrains))
    chisq = np.zeros((nstates, ngrains))
    expmap = np.zeros((nstates, ngrains, 3))
    cent = np.zeros((nstates, ngrains, 3))
    inv_V = np.zeros((nstates, ngrains, 6))
    ln_Vs = np.zeros((nstates, ngrains, 6))
    for i in range(nstates):
        table = data[f"states/state_{i:02d}/ff/table"]
        gid[i] = table[:,0]
        cmpl[i] = table[:,1]
        chisq[i] = table[:,2]
        expmap[i] = table[:, 3:6]
        cent[i] = table[:, 6:9]
        inv_V[i] = table[:, 9:15]
        ln_Vs[i] = table[:, 15:21]

    return GrainData(gid, cmpl, chisq, expmap, cent, inv_V, ln_Vs
                     )

def main(args):
    """main program

    args - from argparser
    """
    gdata = read_graindata(args.datafile, args.sample)
    print(gdata)


def argparser(*args):

    p = argparse.ArgumentParser(
        description="hdf5 updater for HEDM"
    )
    p.add_argument("datafile", help="HDF5 data file")
    p.add_argument("sample", help="name of sample")

    return p


if __name__ == "__main__":
    #
    #  Run.
    #
    p = argparser(*sys.argv)
    args = p.parse_args()
    main(args)
