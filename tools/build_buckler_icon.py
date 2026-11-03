"""Recolour the buckler's inventory icon to steel, matching the BucklerBetter mesh.

Without this the Better tier shows a new model and the base tier's picture, which is the
inconsistency the mesh work set out to remove, just moved one field along.

`recolor_icon_in_place` walks the icon's existing opcode stream and rewrites only the stored
colour values, leaving every control byte, run length and the overall file length identical.
That is the right tool here because the silhouette is already correct: this is the same
shield, in a different metal.

The transform matches the one agreed for the texture -- neutralise the copper toward steel
and lift the brightness -- recomputed in RGB565, which is what the icon format stores.

Usage: python tools/build_buckler_icon.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import FX, zf
import mdl16_format as m

SRC = "Cache/Models/Items/Inventory Images/Armor/Shield Buckler.mdl16"
DEST = "Cache/Models/Items/Inventory Images/Armor/Shield Buckler Better.mdl16"

# the texture recolour, in RGB565: keep 25% of the original hue, neutralise the rest toward
# a faintly cool steel, then gain to roughly match the agreed mean luminance
TINT = (0.98, 1.01, 1.07)
KEEP = 0.25
GAIN = 1.86


def steel(v):
    r = ((v >> 11) & 0x1F) * 255 // 31
    g = ((v >> 5) & 0x3F) * 255 // 63
    b = (v & 0x1F) * 255 // 31
    if r < 8 and g < 8 and b < 8:
        return v  # leave the backdrop exactly as it is
    y = 0.299 * r + 0.587 * g + 0.114 * b
    out = []
    for c, t in zip((r, g, b), TINT):
        x = (c * KEEP + (y * t) * (1 - KEEP)) * GAIN
        out.append(max(0, min(255, int(x + 0.5))))
    return ((out[0] * 31 // 255) << 11) | ((out[1] * 63 // 255) << 5) | (out[2] * 31 // 255)


src = zf.read(SRC)
out = m.recolor_icon_in_place(src, steel)
assert len(out) == len(src), "the recolour changed the file length: %d -> %d" % (len(src), len(out))
assert out != src, "the recolour changed nothing"
info = m.verify_icon(out)
print("icon: %s  %d bytes, unchanged length" % (DEST.split("/")[-1], len(out)))
print("   verify_icon: %s" % {k: info[k] for k in sorted(info) if k in
                              ("width", "height", "hotspot_x", "hotspot_y")})

p = FX / DEST
p.parent.mkdir(parents=True, exist_ok=True)
p.write_bytes(out)

# point the item's Better tier at it
rel = "Resources/Inventory Items/ShieldBuckler.InventoryItem"
t = (FX / rel).read_bytes().decode("latin-1")
old = "\tBetter=Items/Inventory Images/Armor/Shield Buckler\r\n"
new = "\tBetter=Items/Inventory Images/Armor/Shield Buckler Better\r\n"
if new in t:
    print("   item already points its Better tier at the new icon")
else:
    assert old in t, "the item's Better tier is not the base icon"
    (FX / rel).write_bytes(t.replace(old, new, 1).encode("latin-1"))
    print("   item Better tier -> Shield Buckler Better")
