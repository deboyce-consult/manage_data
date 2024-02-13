"""Torsion data processing"""
import numpy as np
import yaml

from process import Processor

# Check #frames

scan, snum = "Ruby_line_ff", 17
scan, snum = "Ruby_box_ff", 18
scan, snum = "lshr_r6_s6_line_ff", 87
scan, snum_range = "lshr_r6_s3_box_ff", range(63, 68)
scan, snum_range = "lshr_r6_s4_box_ff", range(69, 74)


dets = ("ge1", "ge2", "ge3", "ge4")


def add_yaml_entry():
    with open("threshold.yaml", "r") as f:
        yml = yaml.load(f, Loader=yaml.SafeLoader)
        print(yml)
        raise RuntimeError("quitting")

def save_dets(scan, snum, dets, threshold):
    for det in dets:
        print(f"saving for detector {det}")
        processor = Processor(scan, snum, det)
        processor.load()
        processor.process()
        processor.save_processed_ims(threshold)


def image_histograms(ims):
    # frames = range(0, 1000, 100)
    frames = np.random.randint(1440, size=10)
    for i in frames:
        image = ims[i]
        print(f"\nimage: {i}, dtype = {image.dtype}")

        numpixels = image.size
        nnz = np.count_nonzero(image)
        nzero = numpixels - nnz
        print(f"#pixels: {numpixels}, #zero: {nzero}, #nonzero: {nnz}")

        bins = np.hstack((range(15), 1e6))
        hvals, _ = np.histogram(image, bins)
        print(hvals, "\n")


def check(scan, snum):
    for det in dets:
        input(f"{scan}-{snum}-{det}: continue? ")
        processor = Processor(scan, snum, det)
        processor.load()
        processor.process()
        if len(processor.proc_ims) != 1440:
            raise ValueError("length of imageseries incorrect!")
        image_histograms(processor.proc_ims)


for snum in snum_range:
    check(scan, snum)
    input(f"{50 * '='} ready to save ...")
    threshold = 5
    ans = input(f"save with threshold = {threshold}? [yes/no]: ")
    if ans == "yes":
        save_dets(scan, snum, dets, threshold)
    else:
        print("quitting without saving")
