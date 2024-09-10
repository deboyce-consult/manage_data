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


def update(hfile, sample):
    """Update the HDF5 file

    PARAMETERS
    ----------
    hfile: str or Path
        name of data file
    sample: str
        HDF5 path to data
    """
    with h5py.File(hfile, "r+") as hf:
        read_graindata(hf, sample)


def read_graindata(hf, sample):
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
    for i in range(nstates):
        table = data[f"states/state_{i:02d}/ff/table"]
        print(i, table.shape)


def main(args):
    """main program

    args - from argparser
    """
    update(args.datafile, args.sample)


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
