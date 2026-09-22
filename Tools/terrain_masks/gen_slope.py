"""Slope mask from the build-018 heightmap (the exact image the terrain mesh was displaced from).

Reads : SourceArt/Gaea/Belt_Residential_Height.exr   (0-1, x 400 m)
Writes: Belt_Residential_Slope.exr                   (slope in degrees / 90, so 1.0 = vertical)

Why not Gaea's Slope node: build 018 can't be regenerated, and its default range selects
gentle ground, which reads white across nearly the whole belt (median slope is 6.8 deg).
"""
import sys
from pathlib import Path

import numpy as np

from common import GAEA, read_exr, write_exr

TERRAIN_HEIGHT_M = 400.0            # Gaea terrain definition height
PIXEL_M = 7900.0 / 1024.0           # 7.9 km over 1024 pixels = 7.7 m per pixel


def main(out_dir=GAEA):
    h = read_exr(GAEA / "Belt_Residential_Height.exr").astype(np.float64) * TERRAIN_HEIGHT_M
    rise_y, rise_x = np.gradient(h, PIXEL_M)                     # metres of rise per metre
    degrees = np.degrees(np.arctan(np.hypot(rise_x, rise_y)))
    out = Path(out_dir) / "Belt_Residential_Slope.exr"
    write_exr(out, degrees / 90.0)
    print("slope: %.1f-%.1f deg -> %s" % (degrees.min(), degrees.max(), out.name))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else GAEA)
