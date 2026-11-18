"""Paint the Priestess's robe and hood skins, the art step behind build_priestess_model.py.

The Priestess cans have always named `Characters/Monsters/English Enemies/Priestess`, and that
model was never finished: its folder holds byte-for-byte copies of the base Terror, mesh and
animations, and no `Spellcast` clip. Fixt fields the Priestess from 0.19.0, so every one has been
a walking Terror with a woman's voice, and asking her to cast drew the "GRANNY MODEL" placeholder
and could crash (issue #15).

Her new body is the Barcelona townswoman mesh -- all four Woman Generic files share one mesh and
one UV layout, checked by hash -- repainted in the English Priest's own colours:

  * robe  -- Townswoman 2's clothes (long sleeves, high neck, belt at the waist): the blue
             becomes the Priest's navy, a broad gold yoke stands in for his mantle, and the
             skirt is a navy robe with a gold front panel over his gold under-robe. Belts copper,
             fringe and hem gold trim.
  * hood  -- Townswoman 3's head: her hair becomes navy cloth with a gold edge around the face,
             which is the nearest the fixed mesh comes to his hood.

Every target colour is sampled from the Priest's body skin, and each class keeps its source
shading by scaling luminance. Writes the two PNGs to tools/art/. Encoding needs the 32-bit
interpreter (granny2.dll is 32-bit):

    python tools/paint_priestess_skins.py
    %LOCALAPPDATA%\\Programs\\Python\\Python312-32\\python.exe <modtools>/binktc0_encode.py \\
        tools/art/priestess-robe-skin.png tools/art/priestess-robe-skin.binktc0
    (and the same for priestess-hood-skin)
"""
import colorsys
import struct
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
import gr2_format as gf
import gr2_to_gltf
from binktc0_decode import decode_binktc0

ART = HERE / "art"
TOWNIE = "Resources/Models3D/NPC/Barcelona/Female Human Generic/Female Townie%d/FemaleTownie0%d.MODEL.gr2"
PRIEST = "Resources/Models3D/Enemies/English Priest/Priest.MODEL.gr2"
NAMES = {n.lower(): n for n in lhbuild.zf.namelist()}


def one(e, n):
    return gr2_to_gltf.field(e if isinstance(e, list) else [e], n)


def skin(rel, idx):
    g = gf.GrannyFile.load_from_bytes(lhbuild.zf.read(NAMES[rel.lower()]))
    tex = one(g.root_elements, "Textures").value[idx]
    w, h = one(tex, "Width").value, one(tex, "Height").value
    px = one(one(one(tex, "Images").value, "MIPLevels").value, "Pixels")
    rgb = decode_binktc0(w, h, bytes(e.value for e in px.value), has_alpha=False)
    return w, h, [tuple(rgb[i * 3:i * 3 + 3]) for i in range(w * h)]


def png(path, w, h, pix):
    raw = b"".join(b"\0" + b"".join(bytes(p) for p in pix[y * w:(y + 1) * w]) for y in range(h))

    def chunk(t, d):
        c = t + d
        return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def hsv(p):
    return colorsys.rgb_to_hsv(*(c / 255 for c in p))


def lum(p):
    return 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]


def inside(x, y, r):
    return r[0] <= x <= r[2] and r[1] <= y <= r[3]


def mean(ps):
    return tuple(sum(c[i] for c in ps) / len(ps) for i in range(3))


# -- the Priest's palette, sampled from his body skin
pw, ph, pp = skin(PRIEST, 1)


def sample(r, test):
    return [pp[y * pw + x] for y in range(r[1], r[3]) for x in range(r[0], r[2]) if test(hsv(pp[y * pw + x]))]


NAVY = mean(sample((110, 85, 200, 130), lambda c: 0.55 < c[0] < 0.75 and c[2] > 0.08))
GOLD = mean(sample((5, 95, 60, 235), lambda c: 0.08 < c[0] < 0.2 and c[1] > 0.3))
COPPER = mean(sample((105, 172, 200, 186), lambda c: (c[0] < 0.1 or c[0] > 0.95) and c[1] > 0.3))
TGT = {"navy": tuple(c * 0.85 + 4 for c in NAVY),
       "gold": tuple(min(255, c * 1.4) for c in GOLD),
       "copper": COPPER,
       "trim": tuple(min(255, c * 1.7) for c in GOLD)}


def recolour(pix, w, cls_fn):
    cl = [cls_fn(i % w, i // w, p) for i, p in enumerate(pix)]
    groups = {}
    for p, c in zip(pix, cl):
        if c:
            groups.setdefault(c, []).append(lum(p))
    src = {k: sum(v) / len(v) for k, v in groups.items()}
    out = []
    for p, c in zip(pix, cl):
        if not c:
            out.append(p)
            continue
        k = max(0.2, min(2.2, lum(p) / max(1, src[c])))
        out.append(tuple(int(max(0, min(255, ch * k))) for ch in TGT[c]))
    return out


# -- robe: Townswoman 2's clothing sheet (texture 5)
SKIRT, HEM, PANEL = (95, 131, 255, 237), (95, 238, 255, 255), (150, 131, 196, 237)
BELTS = [(58, 126, 117, 142), (16, 225, 67, 242)]
FRINGE, BODICE, YOKE_Y = (115, 112, 250, 132), (140, 0, 255, 97), 30


def robe(x, y, p):
    H, S, V = hsv(p)
    blue = 0.5 < H < 0.72 and S > 0.15 and V > 0.1
    if any(inside(x, y, b) for b in BELTS) and not blue:
        return "copper"
    if inside(x, y, FRINGE) and S < 0.35 and V > 0.45:
        return "trim"
    if inside(x, y, HEM):
        return "trim"
    if inside(x, y, PANEL) and not blue:
        return "gold"
    if inside(x, y, SKIRT) and not blue:
        return "navy"
    if inside(x, y, BODICE) and y < YOKE_Y and (blue or V < 0.35):
        return "gold"
    return "navy" if blue else None


# -- hood: Townswoman 3's head sheet (texture 4); the hair above the hairline becomes cloth
hw, hh, hpix = skin(TOWNIE % (3, 3), 4)


def skinlike(p):
    H, S, V = hsv(p)
    return (H < 0.11 or H > 0.95) and 0.15 < S < 0.65 and V > 0.42


TOP_SKIN = []
for x in range(hw):
    ys = [y for y in range(101, hh) if skinlike(hpix[y * hw + x])]
    TOP_SKIN.append(min(ys) if ys else hh)


def hood(x, y, p):
    H, S, V = hsv(p)
    if V >= 0.42 or (y >= 128 and not (x < 24 and y < 180)):
        return None
    return "trim" if TOP_SKIN[x] - 8 <= y < TOP_SKIN[x] else "navy"


if __name__ == "__main__":
    tw, th, tpix = skin(TOWNIE % (2, 2), 5)
    png(ART / "priestess-robe-skin.png", tw, th, recolour(tpix, tw, robe))
    png(ART / "priestess-hood-skin.png", hw, hh, recolour(hpix, hw, hood))
    print("wrote", ART / "priestess-robe-skin.png", "and", ART / "priestess-hood-skin.png")
