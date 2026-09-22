"""River bank and flow streak masks, derived from the exact build-018 files.

Reads : Belt_Residential_RiverMask.exr, Belt_Residential_Flow.exr
Writes: Belt_Residential_RiverBank.exr    ring around the river; wide on the main channel,
                                          thin on 1-pixel tributaries; width wanders with noise
        Belt_Residential_FlowStreaks.exr  the erosion flow map, stretched so runoff lines show

Why not a new Gaea build: every build after 018 lands ~2 px (15 m) off the mesh, which would
put the bank beside the carved channel instead of along its edge.
"""
import sys
from pathlib import Path

import numpy as np

from common import GAEA, box, grow, read_exr, write_exr

FLOW_LOW, FLOW_HIGH = 0.002, 0.014     # flow values mapped to 0 and 1 (only ~1% of the belt is above 0.02)


def main(out_dir=GAEA):
    river = read_exr(GAEA / "Belt_Residential_RiverMask.exr") > 0.5
    flow = read_exr(GAEA / "Belt_Residential_Flow.exr")

    # distance from the river in pixels (alternating 4/8-neighbour steps ~ round distance)
    dist = np.full(river.shape, 99.0, np.float32)
    dist[river] = 0.0
    cur = river.copy()
    for k in range(1, 21):
        nxt = grow(cur, eight=(k % 2 == 0))
        dist[nxt & ~cur] = k
        cur = nxt

    # slow noise so the bank edge wanders (fixed seed = the same mask every run)
    noise = np.random.default_rng(21).random(river.shape).astype(np.float32)
    for _ in range(3):
        noise = box(noise, 12)
    noise = (noise - noise.min()) / (noise.max() - noise.min())

    # how big is the nearest stream? ~0.14 for a 1-px tributary, 0.4+ for the main channel
    share = box(river.astype(np.float32), 3)
    size = box(box(share * river, 8), 8) / np.maximum(box(box(river.astype(np.float32), 8), 8), 1e-4)
    size = np.clip((size - 0.12) / (0.40 - 0.12), 0.0, 1.0)
    width = (1.5 + 8.5 * size) * (0.7 + 0.6 * noise)          # pixels: ~1-2 on tributaries, ~6-12 on the channel

    bank = np.clip((width - dist) / 2.0 + 0.5, 0.0, 1.0)      # 2-px soft outer edge
    bank = box(bank, 1)
    bank = np.maximum(bank, river.astype(np.float32))          # full strength under the river: no gap below the bed

    streaks = np.clip((flow - FLOW_LOW) / (FLOW_HIGH - FLOW_LOW), 0.0, 1.0)

    write_exr(Path(out_dir) / "Belt_Residential_RiverBank.exr", bank)
    write_exr(Path(out_dir) / "Belt_Residential_FlowStreaks.exr", streaks)
    print("river bank: %.1f%% of the belt | flow streaks > 0.5: %.1f%%" % (
        100 * (bank[:, 0:130] > 0.5).mean(), 100 * (streaks[:, 0:130] > 0.5).mean()))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else GAEA)
