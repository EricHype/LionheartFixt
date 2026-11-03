"""Build the Gauntlets of La Mancha icon from its hand-painted source.

The gauntlets are leather with metal accents, and nothing in the original icon separates the
two: 97% of its pixels share one warm hue family and the bright pixels are specular speckle
scattered over leather and metal alike. So a recolour could only ever tint the whole glove,
which is why the first attempt looked wrong. This art was painted by hand instead -- leather
kept, accents gilded, and small windmills on the back of each hand, the ones Quixote tilted at.

Two things have to be derived rather than read. The painting is 400x368, exactly 4x the
native 100x92, so each 4x4 block averages to one pixel, which also absorbs brush
anti-aliasing. And it has no alpha channel, so the silhouette is the **union** of the
original icon's opaque pixels and the painting's non-black ones: the painting strays 311 px
beyond the original outline, which clipping would trim, and leaves 16 px dark inside it,
which would otherwise punch holes.

`recolor_icon_in_place` cannot do this -- it transforms colour *values*, so it cannot make
per-pixel changes. This uses `build_icon_file`, which needs a **buffer-1-only** donor; the
gauntlets' own file uses three buffers, so `Deed Silver Mine` stands in for the skeleton.

Verify by decoding what was written and comparing to the painting. Expect a mean absolute
error around 4, which is RGB565 quantisation rather than loss.

Usage: python tools/build_lamancha_icon.py
"""

import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path.home() / "LionheartModTools"))
import mdl16_format as m
import lhbuild
from lhbuild import CR, FX, read
from png_io import read_rgb as read_png_rgb, write_rgb as write_png

SRC = Path(__file__).resolve().parent / "art" / "lamancha-gauntlets.png"
ORIG = "Cache/Models/Items/Inventory Images/Armor/Gauntlets.mdl16"
zf = zipfile.ZipFile(r"C:\Program Files (x86)\GOG Galaxy\Games\Lionheart - Legacy of the Crusader\data.dat.vanilla.bak")

d = m.decode_icon(zf.read(ORIG))
W, H = d["width"], d["height"]
orig_rows = d["rows"]


def opaque(px):
    if len(px) > 3:
        return px[3] >= 128
    return max(px[0], px[1], px[2]) > 8


bw, bh, big = read_png_rgb(SRC)
assert (bw, bh) == (W * 4, H * 4), "painting is %dx%d, expected %dx%d" % (bw, bh, W * 4, H * 4)

# average each 4x4 block down to one native pixel
native = []
for y in range(H):
    row = []
    for x in range(W):
        r = g = b = 0
        for dy in range(4):
            for dx in range(4):
                o = ((y * 4 + dy) * bw + (x * 4 + dx)) * 3
                r += big[o]; g += big[o + 1]; b += big[o + 2]
        row.append((r // 16, g // 16, b // 16))
    native.append(row)

# how well does the painting agree with the original silhouette?
painted_out, blank_in, both = 0, 0, 0
for y in range(H):
    for x in range(W):
        was = opaque(orig_rows[y][x])
        now = max(native[y][x]) > 8
        if now and not was:
            painted_out += 1
        elif was and not now:
            blank_in += 1
        elif was and now:
            both += 1
print("silhouette: %d px in both, %d painted outside the original, %d left blank inside"
      % (both, painted_out, blank_in))
print("            (outside pixels would be clipped; blank-inside would show as holes)")

rows = []
for y in range(H):
    row = []
    for x in range(W):
        r, g, b = native[y][x]
        # union of both silhouettes: keeps the 311 px painted beyond the original
        # outline, and fills the 16 the painting left dark inside it
        keep = opaque(orig_rows[y][x]) or max(r, g, b) > 8
        row.append((r, g, b, 255 if keep else 0))
    rows.append(row)

# build_icon_file needs a buffer-1-only donor; the gauntlets' own file uses three
DONOR = next(n for n in zf.namelist()
             if n.endswith(".mdl16") and "Deed Silver Mine" in n)
print("donor:", DONOR.split("/")[-1])
out = m.build_icon_file(zf.read(DONOR), W, H, rows, hotspot_x=W // 2, hotspot_y=H // 2)
info = m.verify_icon(out)
print("built %d bytes; verify_icon: %s" % (
    len(out), {k: info[k] for k in sorted(info) if k in ("width", "height", "hotspot_x", "hotspot_y")}))

dest = Path.home() / "LionheartFixt" / "files" / "Cache/Models/Items/Inventory Images/Armor/Gauntlets La Mancha.mdl16"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_bytes(out)
print("wrote", dest.name)

# round-trip: decode what was written and compare to the painting
back = m.decode_icon(dest.read_bytes())
flat, diffs, n = bytearray(), 0, 0
for y in range(H):
    for x in range(W):
        px = back["rows"][y][x]
        flat += bytes(px[:3])
        if opaque(orig_rows[y][x]) or max(native[y][x]) > 8:
            n += 1
            diffs += max(abs(px[k] - native[y][x][k]) for k in range(3))
print("round-trip: mean abs error %.2f over %d opaque px (RGB565 quantisation is ~4)"
      % (diffs / n, n))
# point the item at it, and prove the change is exactly one field
rel = "Resources/Inventory/Specific Item Cans/Unique Magic Items/Gauntlets of La Mancha.InventoryItem"
NEW = "Items/Inventory Images/Armor/Gauntlets La Mancha"
OLD = "Items/Inventory Images/Armor/Gauntlets"
t = read(rel)
tiers = re.findall(r"\t(Basic|Better|Special)=(.*)" + CR, t)
assert len(tiers) == 3, "expected three icon tiers, found %d" % len(tiers)
have = {v.strip() for _, v in tiers}
assert have in ({OLD}, {NEW}), "La Mancha points at %s" % have
if have == {NEW}:
    print("item: already points at the painted icon")
else:
    out = t
    for grade, _ in tiers:
        out = out.replace("\t%s=%s%s" % (grade, OLD, CR), "\t%s=%s%s" % (grade, NEW, CR), 1)
    after = {v.strip() for _, v in re.findall(r"\t(Basic|Better|Special)=(.*)" + CR, out)}
    assert after == {NEW}, "came out as %s" % after
    assert out.count(CR) == t.count(CR), "line count changed"
    (FX / rel).parent.mkdir(parents=True, exist_ok=True)
    (FX / rel).write_bytes(out.encode("latin-1"))
    print("item: Gauntlets of La Mancha -> Gauntlets La Mancha")

