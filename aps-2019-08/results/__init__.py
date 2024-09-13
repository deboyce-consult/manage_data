"""Results for torsion data"""
from pathlib import Path

import numpy as np

from . import update_h5

HERE = Path(__file__).parent
FF_DATA = HERE / "2024_09_06_lshr_r6.h5"
SAMPLE = "sample_00"


def get_data():
    return update_h5.update(FF_DATA, SAMPLE)
