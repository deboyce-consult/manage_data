"""Torsion data processing"""
import numpy as np

from process import Processor


scan, snum, det = "Ruby_line_ff", 17, "ge1"
processor = Processor(scan, snum, det)
processor.load()
processor.process()
ims = processor.proc_ims

for i in range(0, 1000, 100):
    image = ims[i]
    print(f"i: {i}, #pixels: ", image.size)
    print(np.count_nonzero(image < 1.1))
    print(np.count_nonzero(image < 2.1))
    hvals, bins = np.histogram(image, range=[0, 60], bins=range(15))
    print(hvals, "\n", bins)
