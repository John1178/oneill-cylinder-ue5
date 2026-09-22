"""Rebuild every derived terrain mask from the Gaea build-018 files, in dependency order.

    python Tools/terrain_masks/build.py            rewrite the masks in SourceArt/Gaea
    python Tools/terrain_masks/build.py --check    build into a temp folder and compare with SourceArt/Gaea

Needs numpy and Pillow. Order matters: the 2048 masks are made from the 1024 river bank.
"""
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

import gen_bank_flow
import gen_river_2k
import gen_slope
from common import GAEA, read_exr

OUTPUTS = ["Belt_Residential_Slope.exr", "Belt_Residential_RiverBank.exr", "Belt_Residential_FlowStreaks.exr",
           "Belt_Residential_RiverMask_2k.exr", "Belt_Residential_RiverBank_2k.exr"]


def build(out_dir):
    gen_slope.main(out_dir)
    gen_bank_flow.main(out_dir)
    gen_river_2k.main(out_dir)


if __name__ == "__main__":
    if "--check" not in sys.argv:
        build(GAEA)
    else:
        tmp = Path(tempfile.mkdtemp())
        # the 2k step reads the 1024 bank from SourceArt, so check the chain in isolation
        build(tmp)
        for name in OUTPUTS:
            new, old = read_exr(tmp / name), read_exr(GAEA / name)
            diff = float(np.abs(new - old).max())
            print("%-38s %s" % (name, "identical" if diff == 0 else "max difference %.2e" % diff))
        shutil.rmtree(tmp)
