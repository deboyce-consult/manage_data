"""Results for torsion data"""
from pathlib import Path

import numpy as np

from . import read

HERE = Path(__file__).parent
FF_DATA = HERE / "2024_09_06_lshr_r6.h5"
SAMPLE = "sample_00"


def get_data():
    return read.read_graindata(FF_DATA, SAMPLE)
