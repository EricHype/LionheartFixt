"""Build the Holy Shield's inventory icon: the Lion Shield's, lion faded, cross over it.

**The orphaned `Shield Holy` art is not this shield.** It was claimed in 0.93.0 because it was
unused and unmistakably Templar -- a steel heater with a red haloed cross. But the Holy Shield is
the Lion Shield consecrated, and that steel heater has nothing to do with the Lion Shield. So the
inventory showed a different object from the one on the player's back, which is exactly the
icon-versus-model split that got the Spirit Templar Shield reported, and it is what "it looks
like the Aegis with a red cross" was describing all along: both `Shield Holy` and `Shield Aegis`
are that same steel heater, differing only in the colour of the cross.

So this icon is built the same way the mesh skin is: take the Lion Shield's own art, fade the
lion, lay the ringed cross over it. Inventory and character then show one object.

`Shield Holy` goes back to being unused. Claiming it was a guess, and the guess was wrong.

Geometry is measured from this icon rather than copied from the mesh: the icon is 84x129 and the
mesh UV is 98x189, so the same fractions do not land in the same places.

Usage: python tools/build_holy_icon.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path.home() / "LionheartModTools"))
import lhbuild
from lhbuild import FX, zf
import mdl16_format as m
from png_io import write_rgb

SRC = "Cache/Models/Items/Inventory Images/Quest Items/Lion Shield.mdl16"
DONOR = "Cache/Models/Items/Inventory Images/Quest Items/Deed Silver Mine.mdl16"
DEST = "Cache/Models/Items/Inventory Images/Armor/Shield Holy Fixt.mdl16"
PREVIEW = Path("dist/icon-candidates/shield-holy-icon.png")

GHOST = 0.30          # how much of the lion survives, matching the mesh skin
LION = 190            # the lion is far brighter than its field; 190 isolates it


def main():
    d = m.decode_icon(zf.read(SRC))
    W, H, rows = d["width"], d["height"], d["rows"]
    hx, hy = d["hotspot_x"], d["hotspot_y"]
    print("source %dx%d hotspot (%d,%d)" % (W, H, hx, hy))

    opaque = [(x, y) for y in range(H) for x in range(W) if rows[y][x][3] >= 128]
    lum = {(x, y): int(0.299 * rows[y][x][0] + 0.587 * rows[y][x][1] + 0.114 * rows[y][x][2])
           for x, y in opaque}
    xs = [p[0] for p in opaque]
    ys = [p[1] for p in opaque]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    SW, SH = x1 - x0, y1 - y0

    # the lion, dilated to take its dark outline with it
    # The lion is its bright body AND its dark outline, and both must fade together. A
    # threshold alone takes only the body -- the outline is among the darkest 32% of the icon --
    # so it survived at full strength and the beast dominated the white field instead of
    # haunting it. Dilate once to catch the anti-aliased edge, then crawl along DARK
    # neighbours, which follows the outline without eating into the field.
    mask = {p for p in opaque if lum[p] > LION}
    grow = set()
    for (x, y) in mask:
        for q in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if q in lum:
                grow.add(q)
    mask |= grow
    for _ in range(4):
        grow = set()
        for (x, y) in mask:
            for q in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if q in lum and q not in mask and lum[q] < 95:
                    grow.add(q)
        if not grow:
            break
        mask |= grow
    field = [p for p in opaque if p not in mask]
    print("lion %d px, field %d px" % (len(mask), len(field)))

    fl = max(1.0, sum(lum[p] for p in field) / len(field))
    fr = sum(rows[y][x][0] for x, y in field) / len(field) / fl
    fg = sum(rows[y][x][1] for x, y in field) / len(field) / fl
    fb = sum(rows[y][x][2] for x, y in field) / len(field) / fl

    # fill the lion with field colour at a locally borrowed brightness, column-wise
    clean = dict(lum)
    for x in range(W):
        col = [y for y in range(H) if (x, y) in lum]
        src = [y for y in col if (x, y) not in mask]
        if not src:
            continue
        for y in col:
            if (x, y) in mask:
                near = sorted(src, key=lambda s: abs(s - y))[:3]
                clean[(x, y)] = sum(lum[(x, n)] for n in near) // len(near)

    # the ringed cross, in this icon's own proportions
    # Scaled off the shield's WIDTH but tuned for this canvas: the icon is 84x129 where the
    # mesh UV is 98x189, so the mesh's fractions produce a cross that swamps the shield.
    CX = x0 + 0.50 * SW
    RCY = y0 + 0.30 * SH
    BAR, ARM = 0.060 * SW, 0.26 * SW
    RO, RI = 0.185 * SW, 0.120 * SW
    TOP, BOT = RCY - 0.26 * SW, y0 + 0.86 * SH

    def in_cross(x, y):
        if abs(x - CX) <= BAR and TOP <= y <= BOT:
            return True
        if abs(y - RCY) <= BAR and abs(x - CX) <= ARM:
            return True
        dd = ((x - CX) ** 2 + (y - RCY) ** 2) ** 0.5
        return RI <= dd <= RO

    cross = {p for p in opaque if in_cross(*p)}
    # The edge test must be GEOMETRIC. Testing membership of `cross` -- which holds only
    # opaque pixels -- turns each of the Lion Shield icon's 146 enclosed transparent holes
    # into a false edge, and the device came out speckled with red where the art happens to
    # be see-through.
    outline = {(x, y) for (x, y) in cross
               if not all(in_cross(nx, ny)
                          for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)))}
    # no thickening pass: at 84x129 a 2px outline closes the ring's quadrant holes and the
    # device turns into a red blob. The skin at 256x256 does thicken.

    # A WHITE field with a red cross, laid over the shield you forged -- the Templar shield
    # proper. The lion survives underneath at GHOST, showing through the white: meant to be
    # noticed rather than announced.
    #
    # The rim is kept. Distance from the silhouette decides what is rim: anything further in
    # than RIM px is resurfaced, which is tighter than the interior band the mesh uses, or a
    # ring of the old olive field shows between the gold border and the white.
    from collections import deque
    WHITE = (218, 214, 203)   # linen, not paper: a bright white fights the gold rim
    RED = (168, 32, 34)
    RIM = 4

    # Seed only from transparent pixels connected to the FRAME, not from every transparent
    # pixel. This icon has 146 enclosed holes inside the art, and seeding from those puts a
    # "distance from the edge" of nearly zero in the middle of the shield -- so the lion's
    # surroundings were classed as rim and kept their old olive while everything else turned
    # white. Second time these holes have caused a bug; the first made the cross speckle red.
    outside = set()
    q = deque()
    for y in range(H):
        for x in range(W):
            if (x in (0, W - 1) or y in (0, H - 1)) and rows[y][x][3] < 128:
                outside.add((x, y))
                q.append((x, y))
    while q:
        x, y = q.popleft()
        for nq in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            nx, ny = nq
            if 0 <= nx < W and 0 <= ny < H and nq not in outside and rows[ny][nx][3] < 128:
                outside.add(nq)
                q.append(nq)

    dist = {}
    q = deque()
    for pt in outside:
        dist[pt] = 0
        q.append(pt)
    while q:
        x, y = q.popleft()
        for nq in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if nq in lum and nq not in dist:
                dist[nq] = dist[(x, y)] + 1
                q.append(nq)

    inner = [p0 for p0 in opaque if dist.get(p0, 0) > RIM]
    fl = max(1.0, sum(lum[p0] for p0 in inner) / max(1, len(inner)))

    out = []
    for y in range(H):
        row = []
        for x in range(W):
            p0 = (x, y)
            if rows[y][x][3] < 128:
                if p0 in outside:
                    row.append((0, 0, 0, 0))
                    continue
                # An enclosed hole. Against the old olive art these were invisible; against a
                # white field they read as holes punched in the shield, so they are closed at
                # the field's own brightness.
                row.append(tuple(min(255, int(c)) for c in WHITE) + (255,))
                continue
            if dist.get(p0, 0) <= RIM:
                row.append(rows[y][x][:3] + (255,))        # the rim, untouched
                continue
            # Compress ALL contrast toward the field's mean, rather than masking the lion
            # and fading only that. A threshold took the lion's bright body and left its
            # outline and its mid-tones at full strength, so the beast dominated the white
            # instead of haunting it. Flattening everything to GHOST of its original spread
            # fades the lion, its outline, the grain and the wear together -- which is what
            # "faintly showing through" actually means.
            L = fl + (lum[p0] - fl) * GHOST
            k = max(0.55, min(1.30, L / fl))
            src = RED if p0 in cross else WHITE
            row.append(tuple(min(255, int(c * k)) for c in src) + (255,))
        out.append(row)

    donor = zf.read(DONOR)
    dh = m.find_header(donor)
    assert dh.buffer_sizes[1] == 0 and dh.buffer_sizes[2] == 0, "donor is not buffer-1-only"
    blob = m.build_icon_file(donor, W, H, out, hotspot_x=hx, hotspot_y=hy)
    info = m.verify_icon(blob)
    assert (info["width"], info["height"]) == (W, H)
    p = FX / DEST
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(blob)
    print("icon: %s  %d bytes  %dx%d" % (DEST.split("/")[-1], len(blob), W, H))

    back = m.decode_icon(blob)["rows"]
    diff = [abs(a - b) for y in range(H) for x in range(W) if out[y][x][3]
            for a, b in zip(back[y][x][:3], out[y][x][:3])]
    print("   round-trip mean abs error %.2f / 255" % (sum(diff) / max(1, len(diff))))

    S, BG = 4, (18, 18, 22)
    img = bytearray(bytes(BG) * (W * S * H * S))
    for y in range(H * S):
        for x in range(W * S):
            r, g, b, a = back[y // S][x // S]
            if a < 128:
                continue
            o = (y * W * S + x) * 3
            img[o:o + 3] = bytes((r, g, b))
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    write_rgb(PREVIEW, W * S, H * S, bytes(img))
    print("   preview -> %s" % PREVIEW)


if __name__ == "__main__":
    main()
