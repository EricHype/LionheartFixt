"""Paint the Holy Shield's on-body skin and register the mesh.

The Holy Shield is the Lion Shield reconsecrated, so its mesh is the Lion Shield's mesh and
its skin is the Lion Shield's skin repainted: same silhouette, same riveted border, same
weathering and grain. What changes is the field and the device.

**The lion is kept as a ghost rather than erased.** Flattening it away means inpainting the
hole it leaves, and a column-wise inpaint smears vertical streaks down the field. Blending 30%
of the original back covers them with something that looks deliberate, and it says the right
thing: the shield an initiate forged, with the order's mark laid over it. At 15% the lion is
too faint to read as intentional and looks like dirt; at 45% it competes with the cross.

Three masks do the work, and unlike the La Mancha gauntlets they are all real:

* **The lion** is bright. Its median luminance is 244 against a field median of 131, so a
  threshold at 190 isolates it across the whole shield and clears both the darker orange rim
  and the grey rivets. Dilating three times swallows its dark outline, which the first attempt
  left behind as a ghost nobody asked for.
* **The border** is everything within 9px of the silhouette edge, by BFS from outside. It is
  kept as-is, because its gold rivets already match the gold studs on the `Shield Holy` icon.
* **The cross** is geometry, not a mask: a ringed Latin cross measured off the icon's own red
  pixels -- stem at u=0.50, arms spanning 0.21..0.80, ring centred at v=0.35. It is scaled by
  the shield's *width* on both axes, because the UV sheet is 98x189 while the icon is 81x102,
  and scaling by height stretched it into something thin and wrong.

The lion's forelimb reaches into the border band, so border pixels the lion touched are
retinted to the rim's own mean colour rather than left as a gold patch. That picked the rim's
full saturation back up, which matches the icon's studs better than the duller original.

**The splice is a tail replacement, not a sector swap.** `Shield Lion.MODEL.GR2` holds four
textures and all four share sector 5: three gold environment maps at offsets 0, 13388 and
26776, and `LionShield.tga` at 40124 running to the sector's end. So the buckler's assertion
from 0.91.0 -- that a payload owns its sector outright -- is false here and replacing the
sector would have destroyed three neighbours. What makes it safe instead is that **the skin is
the sector's tail and no pointer references anything past its start**, so it can be truncated
and regrown to any size. Both conditions are asserted before anything is written.

Usage:
    python tools/build_holy_shield_art.py [skin.png] [--ghost 0.30]

With no PNG it paints one and writes it to tools/art/shield-holy-skin.png, so the art is a
file someone can edit and feed back in rather than a binary they have to accept.
"""
import struct
import subprocess
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import FX, zf
import gr2_format as gf
import gr2_to_gltf
from gltf_to_gr2 import repack
from png_io import read_rgb, write_rgb
from binktc0_decode import decode_binktc0

SRC = "Resources/Models3D/Weapons/Shields/Shield Lion/Shield Lion"
DEST = "Resources/Models3D/Weapons/Shields/Shield Holy/Shield Holy"
MALE = "Cache/Models/Characters/Player Characters/Human Male.mdl16"
FEMALE = "Cache/Models/Characters/Player Characters/Human Female.mdl16"
REGISTER = ("Models3D/Weapons/Shields/Shield Holy/Shield Holy",
            "Models3D/Weapons/Shields/Shield Lion/Shield Lion")
SKIN_PNG = HERE / "art" / "shield-holy-skin.png"

# tier three: the same mesh and the same pipeline, painted gold. `--aegis` selects it.
AEGIS_DEST = "Resources/Models3D/Weapons/Shields/Shield Aegis/Shield Aegis"
AEGIS_REGISTER = ("Models3D/Weapons/Shields/Shield Aegis/Shield Aegis",
                  "Models3D/Weapons/Shields/Shield Lion/Shield Lion")
AEGIS_SKIN_PNG = HERE / "art" / "shield-aegis-skin.png"
PY32 = Path.home() / "AppData/Local/Programs/Python/Python312-32/python.exe"
TEX_INDEX = 3            # LionShield.tga; 0..2 are gold environment maps
BORDER = 9
LION = 190
DEFAULT_GHOST = 0.30


def one(e, n):
    return gr2_to_gltf.field(e if isinstance(e, list) else [e], n)


# --------------------------------------------------------------------------- painting

def paint(rgb, w, h, ghost, gild=False):
    """Two shields from one source.

    **The Holy Shield keeps the Lion Shield's field untouched** and adds only the ringed cross.
    It is the original Templar shield with the order's mark on it, which is what it is for.

    **`gild` paints the tier-three Aegis**, which does repaint the face: steel, the lion dropped
    to a ghost, a gold cross and two heraldic lions. That one is meant to read as a shield
    remade rather than as the same one marked."""
    px = [list(rgb[i * 3:i * 3 + 3]) for i in range(w * h)]
    lum = [int(0.299 * r + 0.587 * g + 0.114 * b) for r, g, b in px]
    shield = [max(c) > 18 for c in px]

    dist = [10 ** 6] * (w * h)
    q = deque()
    for i in range(w * h):
        if not shield[i]:
            dist[i] = 0
            q.append(i)
    while q:
        i = q.popleft()
        x, y = i % w, i // w
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                j = ny * w + nx
                if dist[j] > dist[i] + 1:
                    dist[j] = dist[i] + 1
                    q.append(j)

    is_int = [shield[i] and dist[i] > BORDER for i in range(w * h)]
    xs = [i % w for i in range(w * h) if shield[i]]
    ys = [i // w for i in range(w * h) if shield[i]]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    SW, SH = x1 - x0, y1 - y0

    mask = [shield[i] and lum[i] > LION for i in range(w * h)]
    for _ in range(3):
        nxt = mask[:]
        for i in range(w * h):
            if not shield[i] or mask[i]:
                continue
            x, y = i % w, i // w
            if any(mask[ny * w + nx] for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
                   if 0 <= nx < w and 0 <= ny < h):
                nxt[i] = True
        mask = nxt

    clean = lum[:]
    for x in range(w):
        col = [y for y in range(h) if shield[y * w + x]]
        src = [y for y in col if not mask[y * w + x]]
        if not src:
            continue
        for y in col:
            if mask[y * w + x]:
                near = sorted(src, key=lambda s: abs(s - y))[:3]
                clean[y * w + x] = sum(lum[n * w + x] for n in near) // len(near)

    CX, RCY = x0 + 0.50 * SW, y0 + 0.30 * SH
    BAR, ARM = 0.078 * SW, 0.33 * SW
    RO, RI = 0.235 * SW, 0.150 * SW
    STEM_TOP, STEM_BOT = RCY - 0.34 * SW, y0 + 0.88 * SH

    def in_cross(x, y):
        if abs(x - CX) <= BAR and STEM_TOP <= y <= STEM_BOT:
            return True
        if abs(y - RCY) <= BAR and abs(x - CX) <= ARM:
            return True
        d = ((x - CX) ** 2 + (y - RCY) ** 2) ** 0.5
        return RI <= d <= RO

    def steel(L):
        L = max(0, min(255, L))
        if gild:   # brighter and a shade warm, so the gold cross sits on polished metal
            return [min(255, int(L * 1.10)), min(255, int(L * 1.07)), min(255, int(L * 1.00))]
        return [int(L * 0.97), int(L * 0.99), min(255, int(L * 1.04))]

    rim = [i for i in range(w * h) if shield[i] and not is_int[i] and not mask[i]]
    rr = sum(px[i][0] for i in rim) / len(rim)
    rg = sum(px[i][1] for i in rim) / len(rim)
    rb = sum(px[i][2] for i in rim) / len(rim)
    ravg = max(1.0, sum(lum[i] for i in rim) / len(rim))

    def gold(L):
        k = max(0.0, min(2.0, L / ravg))
        return [min(255, int(rr * k)), min(255, int(rg * k)), min(255, int(rb * k))]

    def gold_leaf(L):
        L = max(40, min(230, L))
        return [min(255, int(L * 1.28)), min(255, int(L * 0.98)), int(L * 0.34)]

    cross = {i for i in range(w * h) if is_int[i] and in_cross(i % w, i // w)}
    outline = set()
    for i in cross:
        x, y = i % w, i // w
        if any((ny * w + nx) not in cross for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
               if 0 <= nx < w and 0 <= ny < h):
            outline.add(i)
    for i in list(outline):
        x, y = i % w, i // w
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            j = ny * w + nx
            if 0 <= nx < w and 0 <= ny < h and j in cross:
                outline.add(j)

    out = [c[:] for c in px]
    if not gild:
        # The Holy Shield is the Lion Shield with the order's mark laid over it, and nothing
        # else: the same olive and gold, the same lion, the same wear. Only the cross is added.
        #
        # An earlier build repainted the whole face to steel and reduced the lion to a ghost.
        # Measured against the three skins' interior pixels, that made it the FURTHEST of the
        # three from the Lion Shield it is supposed to be an upgrade of -- 84% of pixels
        # changed, against the Aegis's 65% -- so the sequence went gold, steel, gold, and the
        # middle step read as a different object rather than the same one improved.
        for i in cross:
            L = lum[i] * 0.45
            out[i] = [int(L * 0.95), int(L * 0.97), min(255, int(L * 1.02))]
        for i in outline:
            L = max(80, min(160, lum[i]))
            out[i] = [min(255, int(L * 1.85)), int(L * 0.26), int(L * 0.24)]
    else:
        for i in range(w * h):
            if not shield[i]:
                continue
            L = clean[i] * (1 - ghost) + lum[i] * ghost if mask[i] else clean[i]
            if is_int[i]:
                out[i] = gold_leaf(L) if i in cross else steel(L)
            elif mask[i]:
                out[i] = gold(L)
        for i in outline:
            L = max(80, min(160, clean[i]))
            out[i] = [min(255, int(L * 1.80)), min(255, int(L * 1.32)), int(L * 0.34)]
    if gild:
        # Heraldic lions, to match the hand-painted icon: the lion stops being a ghost under
        # the cross and returns as two supporters flanking the stem. The source is the shield's
        # OWN lion -- the mask already isolates it -- scaled down and mirrored, so this is the
        # same beast in the same style rather than a new drawing.
        src = [i for i in range(w * h) if mask[i] and is_int[i]]
        sxs = [i % w for i in src]
        sys_ = [i // w for i in src]
        sx0, sx1, sy0, sy1 = min(sxs), max(sxs), min(sys_), max(sys_)
        sw, sh = sx1 - sx0 + 1, sy1 - sy0 + 1

        TW, TH = int(0.30 * SW), int(0.24 * SH)          # one lion's box, in face units
        gap = BAR + 0.055 * SW                            # clear of the stem
        top = y0 + 0.55 * SH
        boxes = [(int(CX - gap - TW), int(top), False),   # left, as drawn
                 (int(CX + gap), int(top), True)]         # right, mirrored

        # Area coverage, not nearest-neighbour. The lion is 71x163 and the target 29x45, so
        # point-sampling shreds its thin limbs into gold confetti. Each target pixel instead
        # takes the FRACTION of source pixels in its footprint that are lion, and uses that as
        # an alpha -- which anti-aliases the downscale and, blended rather than painted over,
        # gives the etched-into-the-metal look the hand-painted icon has. Painting it opaque
        # read as two bold gold blobs, which the icon's lions deliberately are not.
        ALPHA = 0.55
        placed = 0
        for bx, by, flip in boxes:
            for ty in range(TH):
                sj0, sj1 = sy0 + ty * sh // TH, sy0 + (ty + 1) * sh // TH
                for tx in range(TW):
                    px_, py_ = bx + tx, by + ty
                    if not (0 <= px_ < w and 0 <= py_ < h):
                        continue
                    j = py_ * w + px_
                    if not is_int[j] or j in cross:
                        continue
                    u = (TW - 1 - tx) if flip else tx
                    si0, si1 = sx0 + u * sw // TW, sx0 + (u + 1) * sw // TW
                    hit = tot = 0
                    acc = 0
                    for sj in range(sj0, max(sj0 + 1, sj1)):
                        for si in range(si0, max(si0 + 1, si1)):
                            k = sj * w + si
                            tot += 1
                            if mask[k]:
                                hit += 1
                                acc += lum[k]
                    if not hit:
                        continue
                    a = ALPHA * hit / tot
                    tint = gold_leaf(acc / hit * 0.92)
                    out[j] = [int(out[j][c] * (1 - a) + tint[c] * a) for c in range(3)]
                    placed += 1
        print("   heraldic lions: %dx%d each from a %dx%d source, %d px touched"
              % (TW, TH, sw, sh, placed))

    flat = bytearray()
    for c in out:
        flat += bytes(max(0, min(255, v)) for v in c)
    print("painted: ghost %.0f%%, %d lion px, %d cross px, rim mean %.0f,%.0f,%.0f"
          % (ghost * 100, sum(mask), len(cross), rr, rg, rb))
    return bytes(flat)


# --------------------------------------------------------------------------- gr2

def load(raw):
    header, off = gf.parse_header(raw)
    endian = ">" if header.big_endian else "<"
    fi, off = gf.parse_file_info(raw, off, endian)
    infos, sectors = [], []
    for _ in range(fi.sector_count):
        info, off = gf.parse_sector_info(raw, off, endian)
        infos.append(info)
        sectors.append(gf.load_sector(raw, endian, info))
    roots, _ = gf.parse_element(sectors, fi.root_ref.sector, fi.type_ref.sector,
                                fi.root_ref.position, fi.type_ref.position,
                                header.bits_64, endian)
    return header, fi, infos, sectors, roots


def splice_tail_texture(raw, index, payload):
    """Replace texture `index`, which must be the tail of its sector with nothing above it."""
    header, fi, infos, sectors, roots = load(raw)
    data = [bytearray(s.data) for s in sectors]

    tex = one(roots, "Textures").value[index]
    w, h = one(tex, "Width").value, one(tex, "Height").value
    px = one(one(one(tex, "Images").value, "MIPLevels").value, "Pixels")
    old_n = len(px.value)
    ptr = sectors[px.data_sector_id].pointer_table.get(px.offset + 4)
    assert ptr is not None, "no fixup for the Pixels pointer"
    assert struct.unpack_from("<I", data[px.data_sector_id], px.offset)[0] == old_n, \
        "the count at the element offset is not the payload length"

    sec, at = ptr.dst_sector, ptr.dst_offset
    assert at + old_n == len(data[sec]), \
        "payload ends at %d but sector %d is %d bytes -- not the tail" % (
            at + old_n, sec, len(data[sec]))
    above = [(s_i, o) for s_i, s in enumerate(sectors) for o, p in s.pointer_table.items()
             if p.dst_sector == sec and p.dst_offset > at]
    assert not above, "%d pointers reference sector %d above offset %d: %s" % (
        len(above), sec, at, above[:4])

    data[sec] = data[sec][:at] + bytearray(payload)
    struct.pack_into("<I", data[px.data_sector_id], px.offset, len(payload))
    touched = {sec, px.data_sector_id}
    return header, fi, infos, sectors, data, touched, w, h, old_n


def registry(b):
    first = b.find(b"Models3D/")
    count = struct.unpack_from("<I", b, first - 8)[0]
    p, out = first - 4, []
    for _ in range(count):
        ln = struct.unpack_from("<I", b, p)[0]
        out.append((p, b[p + 4:p + 4 + ln].decode("latin-1")))
        p += 4 + ln
    return first - 8, count, out, p


def register():
    new, anchor = REGISTER
    for rel in (MALE, FEMALE):
        base = (FX / rel).read_bytes() if (FX / rel).exists() else zf.read(rel)
        at, count, entries, end = registry(base)
        paths = [s for _, s in entries]
        if new in paths:
            print("   %-20s already registered" % rel.split("/")[-1])
            continue
        assert paths.count(anchor) == 1, "cannot pin the insert point in " + rel
        off = next(o for o, s in entries if s == anchor)
        out = base[:off] + struct.pack("<I", len(new)) + new.encode("latin-1") + base[off:]
        out = out[:at] + struct.pack("<I", count + 1) + out[at + 4:]
        nat, ncount, nentries, nend = registry(out)
        assert ncount == count + 1 == len(nentries)
        assert [s for _, s in nentries if s != new] == paths
        assert out[:at] == base[:at] and out[nend:] == base[end:]
        assert struct.unpack_from("<I", out, nend)[0] == 14, "the slot-type block moved"
        p = FX / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(out)
        print("   %-20s %d -> %d entries" % (rel.split("/")[-1], count, ncount))


def main():
    global DEST, REGISTER, SKIN_PNG
    args = [a for a in sys.argv[1:]]
    paint_only = "--paint-only" in args
    if paint_only:
        args.remove("--paint-only")
    gild = "--aegis" in args
    if gild:
        args.remove("--aegis")
        DEST, REGISTER, SKIN_PNG = AEGIS_DEST, AEGIS_REGISTER, AEGIS_SKIN_PNG
    ghost = DEFAULT_GHOST
    if "--ghost" in args:
        i = args.index("--ghost")
        ghost = float(args[i + 1])
        del args[i:i + 2]
    src_png = Path(args[0]) if args else None

    raw = zf.read(SRC + ".MODEL.GR2")

    if src_png:
        w, h, rgb = read_rgb(src_png)
        print("skin: %s (%dx%d), painting skipped" % (src_png.name, w, h))
    else:
        _, _, _, sectors, roots = load(raw)
        tex = one(roots, "Textures").value[TEX_INDEX]
        w, h = one(tex, "Width").value, one(tex, "Height").value
        px = one(one(one(tex, "Images").value, "MIPLevels").value, "Pixels")
        base = decode_binktc0(w, h, bytes(e.value for e in px.value), has_alpha=False)
        rgb = paint(base, w, h, ghost, gild=gild)
        SKIN_PNG.parent.mkdir(parents=True, exist_ok=True)
        write_rgb(SKIN_PNG, w, h, rgb)
        print("skin: -> %s" % SKIN_PNG.relative_to(HERE.parent))
        src_png = SKIN_PNG

    if paint_only:
        print("paint-only: stopping before the encode")
        return

    # the encode is 32-bit only: granny2.dll is 32-bit and a 64-bit python raises WinError 193
    out_bin = SKIN_PNG.with_suffix(".binktc0")
    assert PY32.exists(), "32-bit interpreter not found at %s" % PY32
    enc = Path.home() / "LionheartModTools" / "binktc0_encode.py"
    r = subprocess.run([str(PY32), str(enc), str(src_png), str(out_bin)],
                       capture_output=True, text=True)
    assert r.returncode == 0, "encode failed:\n%s\n%s" % (r.stdout, r.stderr)
    payload = out_bin.read_bytes()
    print("encode: %s" % r.stdout.strip())

    header, fi, infos, sectors, data, touched, tw, th, old_n = \
        splice_tail_texture(raw, TEX_INDEX, payload)
    dest = FX / (DEST + ".MODEL.GR2")
    dest.parent.mkdir(parents=True, exist_ok=True)
    repack(raw, header, fi, infos, sectors, data, touched, str(dest))
    print("mesh: %s  %dx%d  payload %d -> %d bytes" % (
        DEST.split("/")[-1], tw, th, old_n, len(payload)))

    # reload, check nothing else moved, and round-trip the pixels back
    out = dest.read_bytes()
    g = gf.GrannyFile.load_from_bytes(out)
    ref = gf.GrannyFile.load_from_bytes(raw)
    keys = ("Textures", "Materials", "Skeletons", "VertexDatas", "TriTopologies", "Meshes", "Models")
    got = {k: len(one(g.root_elements, k).value) for k in keys}
    want = {k: len(one(ref.root_elements, k).value) for k in keys}
    assert got == want, "reloaded counts %s, original %s" % (got, want)
    for i in range(len(want["Textures"]) if isinstance(want["Textures"], list) else want["Textures"]):
        a = one(g.root_elements, "Textures").value[i]
        b = one(ref.root_elements, "Textures").value[i]
        pa = one(one(one(a, "Images").value, "MIPLevels").value, "Pixels")
        pb = one(one(one(b, "Images").value, "MIPLevels").value, "Pixels")
        if i == TEX_INDEX:
            assert len(pa.value) == len(payload), "spliced payload reloads as %d" % len(pa.value)
        else:
            assert bytes(e.value for e in pa.value) == bytes(e.value for e in pb.value), \
                "texture %d changed and should not have" % i
    print("   reloads clean, the other %d textures are byte-identical" % (want["Textures"] - 1))

    back = decode_binktc0(tw, th, bytes(e.value for e in
                          one(one(one(one(g.root_elements, "Textures").value[TEX_INDEX],
                                        "Images").value, "MIPLevels").value, "Pixels").value),
                          has_alpha=False)
    src = read_rgb(src_png)[2]
    err = sum(abs(a - b) for a, b in zip(back, src)) / len(src)
    print("   round-trip mean abs error %.2f / 255" % err)
    assert err < 3.0, "round-trip error %.2f is too high" % err

    txt = zf.read(SRC + ".MODEL.TXT").decode("latin-1")
    name = DEST.split("/")[-1]
    if "Short Name=undefined" in txt:
        txt = txt.replace("Short Name=undefined", "Short Name=" + name, 1)
    (FX / (DEST + ".MODEL.TXT")).write_bytes(txt.encode("latin-1"))
    print("   MODEL.TXT: Short Name=%s" % name)

    print("registry:")
    register()


if __name__ == "__main__":
    main()
