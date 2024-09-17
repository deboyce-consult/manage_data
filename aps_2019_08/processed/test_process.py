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
    assert ruby_line_17.directory == "../raw/ge1"


def test_yaml_tmpl(ruby_line_17):
    print(ruby_line_17.imagefiles_yaml_tmpl())


def test_load(ruby_line_17):
    ruby_line_17.load()
    assert len(ruby_line_17.raw_ims) == 1440


def test_dark(ruby_line_17):
    dark = ruby_line_17.dark(100, 360)
