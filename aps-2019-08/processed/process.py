"""Process raw torsion data to make frame caches"""
from pathlib import Path
import numpy as np

from hexrd import imageseries


DATA = Path.home() / "Data"
FMT = 'image-files'


img_files_tmpl = r"""# Image files imageseries
image-files:
   directory: ../raw/ge{det}
   files: {scan}_{snum:06d}.ge{det}
options:
   empty-frames: {num_empty}
meta: {{}}

"""

print(
    img_files_tmpl.format(
        scan="Ruby_box_ff", det=1, snum=17, num_empty=1
    )
 )


def load(scan, snum, det):
    fstr = img_files_tmpl.format(
        scan=scan, snum=snum, det=det, num_empty=1
    )
    ims = imageseries.open(fstr, FMT)
    return ims


def process(raw, scan, det):
    ...

print(load("Ruby_box_ff", 18, 1))
