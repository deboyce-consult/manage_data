"""Process raw torsion data to make frame caches"""
from pathlib import Path
import numpy as np

from hexrd import imageseries


DATA = Path.home() / "Data"
DETS = (1, 2, 3, 4)

Pims = imageseries.process.ProcessedImageSeries


class Processor:

    FMT = 'image-files'

    def __init__(self, scan_group, scan_num, detector):
        self.scan_group = scan_group
        self.scan_num = scan_num
        self.detector = detector
        self.raw_ims = None

    @property
    def filename(self):
        return f"{self.scan_group}_{self.scan_num:06d}.{self.detector}"

    @property
    def directory(self):
        return f"../raw/{self.detector}"

    def load(self, num_empty=1):
        print("loading", flush=True)
        self.raw_ims = imageseries.open(
            self.imagefiles_yaml_tmpl(num_empty), self.FMT
        )

    def imagefiles_yaml_tmpl(self, num_empty=1):
        return f"""# Image files imageseries
image-files:
   directory: {self.directory}
   files: {self.filename}
options:
   empty-frames: {num_empty}
meta: {{}}
"""

    @property
    def dark_file(self):
        """Name of file to save/load dark image"""
        return f"dark-{self.filename}.npz"

    def save_dark(self, img):
        np.savez(self.dark_file, dark=img)

    def make_dark(self, nframes, nchunks):
        if self.raw_ims is None:
            self.load()
        print("making dark")
        i = 0
        for dark in imageseries.stats.median_iter(
                self.raw_ims, nchunks, nframes=nframes
        ):
            i += 1
            print(f"\r{i}/{nchunks}", end="", flush=True)
        return dark

    def dark(self, nframes, nchunks):
        p = Path(self.dark_file)
        if p.exists():
            dark = np.load(p)['dark']
        else:
            dark = self.make_dark(nframes, nchunks)
            self.save_dark(dark)
        return dark


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
