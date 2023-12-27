"""Test raw image processing"""
import numpy as np
import pytest

from process import Processor


@pytest.fixture
def ruby_line_17():
    scan, snum, det = "Ruby_line_ff", 17, "ge1"
    return Processor(scan, snum, det)


def test_fileinfo(ruby_line_17):
    assert ruby_line_17.filename == "Ruby_line_ff_000017.ge1"
