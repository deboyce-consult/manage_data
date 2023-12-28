"""Torsion data processing"""
import numpy as np

from process import Processor


scan, snum, det = "Ruby_line_ff", 17, "ge4"
processor = Processor(scan, snum, det)
processor.load()
processor.process()

save = True
#save = False
if save:
    threshold = 5
    processor.save_processed_ims(threshold)
    raise RuntimeError("quitting")

ims = processor.proc_ims
numpixels = ims[0].size
for thresh in (4, 5, 6):
    print(f"threshold: {thresh}, size = {processor.cache_size(thresh)}")

for i in range(0, 1000, 100):
    image = ims[i]
    print(f"image: {i}, dtype = {image.dtype}")

    nnz = np.count_nonzero(image)
    nzero = numpixels - nnz
    print(f"#pixels: {numpixels}, #zero: {nzero}, #nonzero: {nnz}")

    print(np.count_nonzero(image < 0.1))
    print(np.count_nonzero(image < 1.1))
    print(np.count_nonzero(image < 2.1))
    hvals, bins = np.histogram(image, range=[0, 60], bins=range(15))
    print(hvals, "\n", bins)
