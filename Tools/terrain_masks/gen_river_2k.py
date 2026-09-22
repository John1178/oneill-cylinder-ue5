"""2048 smooth versions of the river and river-bank masks (Gaea Community caps builds at 1024).

Reads : Belt_Residential_RiverMask.exr, Belt_Residential_RiverBank.exr   (1024)
Writes: Belt_Residential_RiverMask_2k.exr, Belt_Residential_RiverBank_2k.exr   (2048)

At 1024 over 7.9 km each pixel is 7.7 m and the river is ~2 px wide, so its edges step.
A centre-aligned bicubic upsample keeps the exact UV mapping (same Mask UV, same half-texel
offset); a light blur rounds the corners; the river is remapped so its 0.5 edge covers the
same area as the original. Checked 2026-09-21: alignment peaks at zero shift (within 0.02 m).
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from common import GAEA, box, read_exr, write_exr


def upsample_2x(a):
    """Centre-aligned bicubic 2x upsample of a float image."""
    return np.asarray(Image.fromarray(a.astype(np.float32), mode="F").resize((2048, 2048), Image.BICUBIC), np.float32)


def main(out_dir=GAEA):
    river = (read_exr(GAEA / "Belt_Residential_RiverMask.exr") > 0.5).astype(np.float32)
    bank = read_exr(GAEA / "Belt_Residential_RiverBank.exr")
    target = river[:, 0:130].mean()                          # river area in the belt strip

    smooth = upsample_2x(river)
    for _ in range(2):
        smooth = box(smooth, 1)

    # find the threshold whose covered area matches the original river (bisection)
    lo, hi = 0.0, 1.0
    for _ in range(40):
        t = 0.5 * (lo + hi)
        if (smooth[:, 0:260] > t).mean() > target:
            lo = t
        else:
            hi = t
    t = 0.5 * (lo + hi)
    river2k = np.clip((smooth - (t - 0.1)) / 0.2, 0.0, 1.0)   # 0.5 exactly on the matched edge

    bank2k = np.clip(upsample_2x(bank), 0.0, 1.0)
    for _ in range(2):
        bank2k = box(bank2k, 1)
    bank2k = np.maximum(bank2k, river2k)

    write_exr(Path(out_dir) / "Belt_Residential_RiverMask_2k.exr", river2k)
    write_exr(Path(out_dir) / "Belt_Residential_RiverBank_2k.exr", bank2k)
    print("river 2k: edge threshold %.3f, area %.2f%% (original %.2f%%)" % (
        t, 100 * (river2k[:, 0:260] > 0.5).mean(), 100 * target))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else GAEA)
