"""Shared helpers for the terrain mask scripts: EXR in/out, blur, grow.

Gaea writes single-channel ("Y"), 32-bit float, uncompressed scanline EXRs.
These helpers read and write exactly that format, so no OpenEXR install is needed.
"""
import struct
from pathlib import Path

import numpy as np

PROJECT = Path(__file__).resolve().parents[2]
GAEA = PROJECT / "SourceArt" / "Gaea"          # masks live here (LFS-tracked)
STRIP = slice(0, 130)                          # image columns the terrain mesh samples


def read_exr(path):
    """Return the first channel of an uncompressed scanline EXR as a float32 array."""
    b = open(path, "rb").read()
    assert struct.unpack("<I", b[:4])[0] == 0x01312F76, "not an EXR"
    p, attrs = 8, {}

    def cstr(p):
        e = b.index(b"\0", p)
        return b[p:e].decode("latin1"), e + 1

    while b[p] != 0:
        name, p = cstr(p)
        typ, p = cstr(p)
        size = struct.unpack("<i", b[p:p + 4])[0]
        p += 4
        attrs[name] = b[p:p + size]
        p += size
    p += 1
    assert attrs["compression"][0] == 0, "only uncompressed EXRs are supported"
    cd, q, chans = attrs["channels"], 0, []
    while cd[q] != 0:
        e = cd.index(b"\0", q)
        name = cd[q:e].decode("latin1")
        q = e + 1
        ptype = struct.unpack("<i", cd[q:q + 4])[0]
        q += 16
        chans.append((name, ptype))
    chans.sort()
    xmin, ymin, xmax, ymax = struct.unpack("<iiii", attrs["dataWindow"])
    w, h = xmax - xmin + 1, ymax - ymin + 1
    size = {0: 4, 1: 2, 2: 4}
    dtype = {0: "<u4", 1: "<f2", 2: "<f4"}
    offsets = struct.unpack(f"<{h}Q", b[p:p + 8 * h])
    out = np.zeros((h, w), np.float32)
    for i in range(h):
        o = offsets[i]
        y = struct.unpack("<i", b[o:o + 4])[0]
        o += 8
        name, ptype = chans[0]
        out[y - ymin] = np.frombuffer(b[o:o + w * size[ptype]], dtype[ptype]).astype(np.float32)
    return out


def write_exr(path, arr):
    """Write a single-channel 'Y' 32-bit float uncompressed EXR (same format Gaea uses)."""
    arr = np.ascontiguousarray(arr.astype("<f4"))
    h, w = arr.shape
    out = bytearray(struct.pack("<II", 0x01312F76, 2))

    def attr(name, typ, data):
        return name.encode() + b"\0" + typ.encode() + b"\0" + struct.pack("<i", len(data)) + data

    out += attr("channels", "chlist", b"Y\0" + struct.pack("<iBxxxii", 2, 0, 1, 1) + b"\0")
    out += attr("compression", "compression", bytes([0]))
    out += attr("dataWindow", "box2i", struct.pack("<iiii", 0, 0, w - 1, h - 1))
    out += attr("displayWindow", "box2i", struct.pack("<iiii", 0, 0, w - 1, h - 1))
    out += attr("lineOrder", "lineOrder", bytes([0]))
    out += attr("pixelAspectRatio", "float", struct.pack("<f", 1.0))
    out += attr("screenWindowCenter", "v2f", struct.pack("<ff", 0.0, 0.0))
    out += attr("screenWindowWidth", "float", struct.pack("<f", 1.0))
    out += b"\0"
    table = len(out)
    out += b"\0" * (8 * h)
    offsets = []
    for y in range(h):
        offsets.append(len(out))
        out += struct.pack("<ii", y, w * 4) + arr[y].tobytes()
    out[table:table + 8 * h] = struct.pack(f"<{h}Q", *offsets)
    Path(path).write_bytes(bytes(out))


def box(a, r):
    """Box blur with radius r (edge pixels repeat). Run it 2-3 times for a smooth, Gaussian-like blur."""
    p = np.pad(a, ((r, r), (0, 0)), mode="edge")
    c = np.vstack([np.zeros((1, p.shape[1])), np.cumsum(p, axis=0, dtype=np.float64)])
    a = (c[2 * r + 1:] - c[:-2 * r - 1]) / (2 * r + 1)
    p = np.pad(a, ((0, 0), (r, r)), mode="edge")
    c = np.hstack([np.zeros((p.shape[0], 1)), np.cumsum(p, axis=1, dtype=np.float64)])
    return ((c[:, 2 * r + 1:] - c[:, :-2 * r - 1]) / (2 * r + 1)).astype(np.float32)


def grow(mask, eight):
    """Grow a True/False mask by one pixel (4 neighbours, or 8 when eight=True)."""
    n = mask.copy()
    n[1:, :] |= mask[:-1, :]
    n[:-1, :] |= mask[1:, :]
    n[:, 1:] |= mask[:, :-1]
    n[:, :-1] |= mask[:, 1:]
    if eight:
        n[1:, 1:] |= mask[:-1, :-1]
        n[:-1, :-1] |= mask[1:, 1:]
        n[1:, :-1] |= mask[:-1, 1:]
        n[:-1, 1:] |= mask[1:, :-1]
    return n
