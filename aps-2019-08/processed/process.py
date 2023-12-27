"""Process raw torsion data to make frame caches"""
from pathlib import Path
import numpy as np

from hexrd import imageseries


DATA = Path.home() / "Data"
FMT = 'image-files'
DETS = (1, 2, 3, 4)

Pims = imageseries.process.ProcessedImageSeries


class Processor:

    def __init__(self, scan_group, scan_num, detector):
        self.scan_group = scan_group
        self.scan_num = scan_num
        self.detector = detector

    @property
    def filename(self):
        return f"{self.scan_group}_{self.scan_num:06d}.{self.detector}"

    @property
    def directory(self):
        return f"../raw/ge{self.detector}"

    def imagefiles_yaml_tmpl(self, det):
        return """# Image files imageseries
image-files:
   directory: {directory}
   files: {file}
options:
   empty-frames: {num_empty}
meta: {{}}

"""


img_files_tmpl = """# Image files imageseries
image-files:
   directory: ../raw/ge{det}
   files: {scan}_{snum:06d}.ge{det}
options:
   empty-frames: {num_empty}
meta: {{}}

"""


def load(scan, snum, det):
    fstr = img_files_tmpl.format(
        scan=scan, snum=snum, det=det, num_empty=1
    )
    ims = imageseries.open(fstr, FMT)
    return ims


def process(ims, nchunk):
    i = 0
    for dark in imageseries.stats.median_iter(ims, nchunk):
        i += 1
        print(f"\r{i}/{nchunk}", end="", flush=True)
    print("\n")
    #
    oplist = [(Pims.DARK, dark)]
    pims = Pims(ims, oplist)
    return pims


def check(ims):
    """Check imageseries"""
    n = len(ims)
    print("length: ", n)
    imax = imageseries.stats.max(ims)
    imin = imageseries.stats.min(ims)
    print("min/max: ", imin.min(), imax.max())

    # Check cache size
    for threshold in (0, 25, 50, 100, 200):
        nzvals = cache_size(ims, threshold)
        print(f"threshold: {threshold}")
        print(f"cache size: {nzvals:,}")


def cache_size(ims, threshold):
    nzvals = 0
    n = len(ims)
    for i in range(n):
        nzvals += np.count_nonzero(ims[i] > threshold)

    return nzvals


def main():

    nchunk = 360
    scan, snum = "Ruby_line_ff", 17
    scan, snum = "Ruby_box_ff", 18
    for det in DETS:
        print("\n\nscan: ", scan, snum, det)
        ims = load(scan, snum, det)
        print("imageseries loaded, processing ...")
        pims = process(ims, nchunk)
        check(pims)


if __name__ == "__main__":
    main()
