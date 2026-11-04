"""Build the Aegis of the Templars' inventory icon from its hand-painted source.

The first attempt was a recolour: take the Holy Shield's icon, turn the red cross gold, polish
the steel. It worked and it was dull, because a recolour can only ever restate the same device
in a different metal. What the tier needed was *heraldry* -- so the lion came back, as two small
gold lions rampant flanking the stem, painted by hand.

That completes a progression the chain had been missing. The lion **is** the device in act 1; it
is a ghost under the cross in act 4, 30% of the original showing through the steel; and at
Paladin it returns as formal supporters beside the cross. Three stages of the same heraldry
rather than three brightnesses of the same picture.

Three things are derived rather than read:

* **The painting is 324x408, exactly 4x the native 81x102**, so each 4x4 block averages to one
  pixel, which also absorbs the brush's anti-aliasing.
* **It has no alpha channel**, and its backdrop is `(18, 18, 22)` -- the colour the preview
  renderer uses, not black. So La Mancha's "non-black means opaque" test at a threshold of 8
  would have declared the entire canvas opaque and produced a rectangular shield. Measured
  instead: the painting strays **0 pixels** beyond the original outline, so the silhouette is
  simply the Holy Shield icon's own alpha. 404 native pixels inside that outline are legitimately
  dark (the shield's unlit left half), which any brightness test would have punched out as holes.
* **The hotspot is the original's**, (41, 49), not the centre of the canvas.

`recolor_icon_in_place` cannot do this: it transforms colour *values*, so it cannot add a lion.
`build_icon_file` can, and it needs a **buffer-1-only** donor -- `Shield Holy` has five buffers
(13372, 0, 0, 255, 944), so `Deed Silver Mine` lends the envelope, as it did for La Mancha.

Usage: python tools/build_aegis_icon.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path.home() / "LionheartModTools"))
import lhbuild
from lhbuild import FX, zf
import mdl16_format as m
from png_io import read_rgb, write_rgb

SRC = HERE / "art" / "shield-aegis-icon.png"
ORIG = "Cache/Models/Items/Inventory Images/Armor/Shield Holy.mdl16"
DONOR = "Cache/Models/Items/Inventory Images/Quest Items/Deed Silver Mine.mdl16"
DEST = "Cache/Models/Items/Inventory Images/Armor/Shield Aegis.mdl16"
PREVIEW = Path("dist/icon-candidates/shield-aegis-icon-built.png")
BACKDROP = (18, 18, 22)


def main():
    d = m.decode_icon(zf.read(ORIG))
    W, H, orig = d["width"], d["height"], d["rows"]
    hx, hy = d["hotspot_x"], d["hotspot_y"]

    w, h, px = read_rgb(SRC)
    assert w % W == 0 and h % H == 0, "painting %dx%d is not an integer multiple of %dx%d" % (w, h, W, H)
    S = w // W
    assert S == h // H, "non-uniform scale"
    print("painting %dx%d at %dx -> %dx%d, hotspot (%d,%d)" % (w, h, S, W, H, hx, hy))

    # the silhouette is the original's: measured, the painting strays nowhere outside it
    outside = 0
    rows = []
    for y in range(H):
        row = []
        for x in range(W):
            if orig[y][x][3] < 128:
                # confirm the painter did not rely on this pixel; if they did, say so loudly
                blk = [px[((y * S + dy) * w + x * S + dx) * 3:((y * S + dy) * w + x * S + dx) * 3 + 3]
                       for dy in range(S) for dx in range(S)]
                if max(max(b) for b in blk) > max(BACKDROP) + 12:
                    outside += 1
                row.append((0, 0, 0, 0))
                continue
            r = g = b = 0
            for dy in range(S):
                base = (y * S + dy) * w + x * S
                for dx in range(S):
                    o = (base + dx) * 3
                    r += px[o]; g += px[o + 1]; b += px[o + 2]
            n = S * S
            row.append((r // n, g // n, b // n, 255))
        rows.append(row)
    print("native px painted beyond the original outline: %d" % outside)
    assert outside < 40, "the painting strays %d px outside; the silhouette needs widening" % outside

    donor = zf.read(DONOR)
    dh = m.find_header(donor)
    assert dh.buffer_sizes[1] == 0 and dh.buffer_sizes[2] == 0, \
        "donor is not buffer-1-only: %s" % (dh.buffer_sizes,)
    blob = m.build_icon_file(donor, W, H, rows, hotspot_x=hx, hotspot_y=hy)
    info = m.verify_icon(blob)
    assert (info["width"], info["height"]) == (W, H), "verify_icon says %s" % info

    p = FX / DEST
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(blob)
    print("icon: %s  %d bytes  %dx%d" % (DEST.split("/")[-1], len(blob), W, H))

    back = m.decode_icon(blob)["rows"]
    diff = [abs(a - b) for y in range(H) for x in range(W) if rows[y][x][3]
            for a, b in zip(back[y][x][:3], rows[y][x][:3])]
    err = sum(diff) / max(1, len(diff))
    print("   round-trip mean abs error %.2f / 255 (RGB565 quantisation is ~4)" % err)
    assert err < 8.0, "round-trip error %.2f is too high" % err

    S2 = 4
    OW, OH = W * S2, H * S2
    img = bytearray(bytes(BACKDROP) * (OW * OH))
    for y in range(OH):
        for x in range(OW):
            r, g, b, a = back[y // S2][x // S2]
            if a < 128:
                continue
            o = (y * OW + x) * 3
            img[o:o + 3] = bytes((r, g, b))
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    write_rgb(PREVIEW, OW, OH, bytes(img))
    print("   preview -> %s" % PREVIEW)


if __name__ == "__main__":
    main()
