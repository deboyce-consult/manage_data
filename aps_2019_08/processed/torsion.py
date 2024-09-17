"""Torsion data processing"""
import numpy as np
import yaml

from process import Processor

# Check #frames

scandict = {
    "Ruby_line_ff": (17,),
    "Ruby_box_ff": (18,),

    "lshr_r6_s0_line_ff": range(42, 51),
    "lshr_r6_s1_line_ff": (56,),
    "lshr_r6_s2_line_ff": (62,),
    "lshr_r6_s3_line_ff": (68,),
    "lshr_r6_s4_line_ff": (74,),
    "lshr_r6_s5_line_ff": (80,),
    "lshr_r6_s6_line_ff": (87,),
    "lshr_r6_s7_line_ff": range(93, 102),
    "lshr_r6_s8_line_ff": (107,),
    "lshr_r6_s9_line_ff": (113,),
    "lshr_r6_s10_line_ff": (119,),
    "lshr_r6_s11_line_ff": (125,),
    "lshr_r6_s12_line_ff": (131,),
    "lshr_r6_s13_line_ff": (137,),
    "lshr_r6_s14_line_ff": (143,),
    "lshr_r6_s15_line_ff": (149,),
    "lshr_r6_s16_line_ff": range(155,164),

    "lshr_r6_s0_box_ff": range(31, 42),
    "lshr_r6_s1_box_ff": range(51, 56),
    "lshr_r6_s2_box_ff": range(57, 62),
    "lshr_r6_s3_box_ff": range(63, 68),
    "lshr_r6_s4_box_ff": range(69, 74),
    "lshr_r6_s5_box_ff": range(75, 80),
    "lshr_r6_s6_box_ff": range(81, 87),
    "lshr_r6_s7_box_ff": range(88, 93),
    "lshr_r6_s8_box_ff": range(102, 107),
    "lshr_r6_s9_box_ff": range(108, 113),
    "lshr_r6_s10_box_ff": range(114, 119),
    "lshr_r6_s11_box_ff": range(120, 125),
    "lshr_r6_s12_box_ff": range(126, 131),
    "lshr_r6_s13_box_ff": range(132, 137),
    "lshr_r6_s14_box_ff": range(138, 143),
    "lshr_r6_s15_box_ff": range(144, 149),
    "lshr_r6_s16_box_ff": range(150, 155),
}

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
    nbins = 15
    hvalmax = np.zeros(nbins)
    for i in frames:
        image = ims[i]
        print(f"\nimage: {i}, dtype = {image.dtype}")

        numpixels = image.size
        nnz = np.count_nonzero(image)
        nzero = numpixels - nnz
        print(
            f"#pixels: {numpixels}, #zero: {nzero}, #nonzero: {nnz}"
        )

        bins = np.hstack((range(15), 1e6))
        hvals, _ = np.histogram(image, bins)
        # print(hvals, "\n")
        hvalmax = np.maximum(hvalmax, hvals)

    return hvalmax


def check(scan, snum, thresh=5, cut=40000):
    for det in dets:
        print(1 * '\n', f"working on: {scan}-{snum}-{det}")
        # input(f"{scan}-{snum}-{det}: continue? ")
        processor = Processor(scan, snum, det)
        processor.load()
        processor.process()
        if len(processor.proc_ims) != 1440:
            raise ValueError("length of imageseries incorrect!")
        hvmax = image_histograms(processor.proc_ims)
        if hvmax[thresh] > cut:
            print(hvmax)
            raise RuntimeError(f"max value exceeds cutoff: {hvmax}")
        else:
            print(50 * '-', " Values are good!")

scan = "lshr_r6_s16_line_ff"

for snum in scandict[scan]:
    threshold = 5
    check(scan, snum)
    save_dets(scan, snum, dets, threshold)
