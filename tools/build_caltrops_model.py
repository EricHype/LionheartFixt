"""Caltrops that look like caltrops. Reported from play after 0.99.19: "when thieves drop traps, they appear to be giant
metal spikes, taller than the thief or the player."

0.35.x showed the patch as `Environments/Outpost/Generic/Trap Spike 1` held on `Closed`. That is the Crypt and Alamut
floor trap at full extension: one needle 5 px wide and 73 px tall, about a character's height. Its other states do not
help (`Open` is a 5x4 speck, `Opening` animates the needle rising), and nothing in the game is a scatter of caltrops.

So this builds `Environments/Outpost/Generic/Fixt Caltrops` from the same file, with the needle's own pixels cut down
into a low cluster of four short spikes, and points `Fixt Caltrops Entity` at it.

**The file.** An environment sprite is a serialized entity graph (`CEntityAnimated`, `CDoorAI`, sounds, states) with one
CStandAloneFrame per state and shadow. Each frame delimits itself and is followed by 8 zero bytes and the next
length-prefixed string; nothing outside a frame records its size, so a frame can be replaced by one of another size.
Only `Closed` and `Closed Shadow` change, because the entity is held on `Closed`; `Open`, `Opening` and their shadows
stay byte-identical, so the file still describes every state the CDoorAI names.

* `Closed` becomes the cluster, buffer 1 only. The needle's edges are soft (buffer 5 colour at buffer 4 alpha), and the
  encoder writes opaque pixels only, so alpha >= 128 is kept and the rest dropped; at this size that reads as hard-edged
  iron. A buffer-1-only frame is not new to this file: `Open Shadow` already is one, and the encoder reproduces it byte
  for byte.
* `Closed Shadow` becomes an empty 1x1 frame. The vanilla shadow lives entirely in buffers 4/5, which this encoder cannot
  write, and a hard-edged dark copy would look worse than none on something ankle high.
* **The base stays where it was.** Every state's hotspot puts its bottom row 32 px below the anchor (`Closed` 73 tall at
  hotspot y 40, `Open` 4 tall at -29), so the cluster's hotspot is `height - 33`, and its centre column sits where the
  needle's did.

The embedded name and model-path strings still say `Trap Spike 1`; the game locates a model by its file path, as every
icon this project has shipped with a copied envelope shows.

A rerun is a no-op.

    python tools/build_caltrops_model.py
"""
import struct
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from build_shrine_repairs import register

sys.path.insert(0, str(lhbuild.MODTOOLS))
import mdl16_format as m

SOURCE = "Cache/Models/Environments/Outpost/Generic/Trap Spike 1.mdl16"
MODEL = "Environments/Outpost/Generic/Fixt Caltrops"
TARGET = "Cache/Models/" + MODEL + ".mdl16"
ENTITY = "Resources/Common Objects and Scripts/Fixt Caltrops Entity.can"
OLD_MODEL = "Environments/Outpost/Generic/Trap Spike 1"
BASE_BELOW_ANCHOR = 32          # every state's bottom row sits this far below the hotspot anchor

# (left x, spike height, how far its base sits above the frame's bottom row) -- staggered for depth
SPIKES = [(0, 11, 2), (4, 15, 0), (8, 9, 3), (12, 13, 1)]
SPIKE_W = 3                     # the needle's three solid columns; its outer two are soft shading


def frames(d):
    """[(offset, span, header)] of every CStandAloneFrame in an environment sprite, in file order."""
    out = []
    for off in range(len(d) - 40):
        if d[off] != m.MAGIC or d[off + 1] != 0x10:
            continue
        w, h = struct.unpack_from("<HH", d, off + 6)
        sizes = struct.unpack_from("<5I", d, off + 16)
        if not (1 <= w <= 2000 and 1 <= h <= 2000 and sizes[0]) or struct.unpack_from("<I", d, off + 36)[0] != sizes[0]:
            continue
        span = 36 + sum(s + 4 * h for s in sizes if s)
        out.append((off, span, m.find_header(d[off:off + span])))
    return out


def label(d, off):
    """The state name the serialized graph writes just before a frame, e.g. 'Closed' or 'Open Shadow'."""
    i = d.rfind(b"Transparent Mask", 0, off)
    for j in range(i - 6, max(0, i - 200), -1):   # strings are written as 01, u32 length, the characters
        if d[j] != 1:
            continue
        n = struct.unpack_from("<I", d, j + 1)[0]
        s = d[j + 5:j + 5 + n]
        if 0 < n < 64 and j + 5 + n <= i and all(32 <= c < 127 for c in s):
            return s.decode("latin-1")
    return ""


def cluster(needle):
    """Four short spikes cut from the needle's own solid columns, nearest-row resampled so each keeps tip and base."""
    nh = len(needle)
    width = max(x for x, _, _ in SPIKES) + SPIKE_W
    height = max(sh + lift for _, sh, lift in SPIKES)
    rows = [[(0, 0, 0, 0)] * width for _ in range(height)]
    for x0, sh, lift in SPIKES:
        bottom = height - 1 - lift
        tip = max(2, sh * 2 // 5)               # the top two fifths are the point: the needle's centre column only
        for k in range(sh):
            src = needle[round(k * (nh - 1) / (sh - 1))]
            for c in range(SPIKE_W):
                if k < tip and c != 1:
                    continue
                px = src[1 + c]
                if k < tip and px[3] < 128:         # the needle's own tip is faint; keep the point solid
                    px = needle[nh // 2][2]
                if px[3] >= 128:
                    rows[bottom - sh + 1 + k][x0 + c] = px
            if k == 0:                              # a glint on the point, from the needle's highlight
                rows[bottom - sh + 1][x0 + 1] = (148, 146, 148, 255)
    return width, height, rows


def build_model():
    if (lhbuild.FX / TARGET).exists():
        return 0
    with zipfile.ZipFile(lhbuild.VANILLA) as zf:
        d = zf.read(SOURCE)
    fs = frames(d)
    names = [label(d, off) for off, _, _ in fs]
    assert names[:2] == ["Closed", "Closed Shadow"], names
    (c_off, c_span, c_h), (s_off, s_span, s_h) = fs[0], fs[1]
    needle = m.decode_icon_composite(d[c_off:c_off + c_span], c_h)["rows"]
    w, h, rows = cluster(needle)
    # a frame's top-left sits at anchor - hotspot. The needle's centre column (2 of its 5) is at anchor + 2 - hx, so the
    # cluster's centre column goes there too; its bottom row goes BASE_BELOW_ANCHOR below the anchor, like every state's
    hx = w // 2 - 2 + c_h.hotspot_x
    hy = h - 1 - BASE_BELOW_ANCHOR
    closed = m.encode_icon_rle16(w, h, rows, hx, hy)
    shadow = m.encode_icon_rle16(1, 1, [[(0, 0, 0, 0)]], s_h.hotspot_x, s_h.hotspot_y)
    out = d[:c_off] + closed + d[c_off + c_span:s_off] + shadow + d[s_off + s_span:]
    # every frame after the two replaced ones is carried over byte for byte, and still parses
    new = frames(out)
    assert [label(out, off) for off, _, _ in new] == names
    assert [out[o:o + s] for o, s, _ in new[2:]] == [d[o:o + s] for o, s, _ in fs[2:]]
    back = m.decode_icon(out[new[0][0]:new[0][0] + new[0][1]], new[0][2])
    assert (back["width"], back["height"]) == (w, h)
    (lhbuild.FX / TARGET).parent.mkdir(parents=True, exist_ok=True)
    (lhbuild.FX / TARGET).write_bytes(out)
    register([TARGET])
    return 1


def build_entity():
    t = lhbuild.read(ENTITY)
    if "Model=" + MODEL + "\r\n" in t:
        return 0
    assert t.count("\tModel=" + OLD_MODEL + "\r\n") == 1
    t = t.replace("\tModel=" + OLD_MODEL + "\r\n", "\tModel=" + MODEL + "\r\n")
    (lhbuild.FX / ENTITY).write_bytes(t.encode("latin-1"))
    register([ENTITY])
    return 1


LOG_LINE = "You stepped on some caltrops."


def build_log():
    """A combat log line when the patch bites, requested after the scatter. It goes in the hit step beside the damage, and
    before the CDeleteAction that ends it, because an action after a CDeleteAction silently never runs."""
    t = lhbuild.read(ENTITY)
    if LOG_LINE in t:
        return 0
    flat = "\r\n".join(line.lstrip("\t") for line in t.split("\r\n"))
    hit = flat.index("Explosion Model=Spell Effects/Shots/Spike Hit")
    count = flat.rindex("Item Count=3\r\n", 0, hit)
    assert flat.count("CDeleteAction") == 1
    delete = flat.index("Action=CDeleteAction")
    assert count < hit < delete
    line = lhbuild.B("CPrintCombatTextAction", [("Text to print", LOG_LINE), ("Character to show text to", "Player1"),
                                                 ("Emphasize", "0"), ("Suppress Duplicates", "0")])
    flat = flat[:delete] + "Action=" + line + flat[delete:]
    flat = flat[:count] + "Item Count=4\r\n" + flat[count + len("Item Count=3\r\n"):]
    lhbuild.write_map(ENTITY, flat)
    register([ENTITY])
    return 1


def main():
    print("model:", build_model(), "| entity:", build_entity(), "| log line:", build_log())


if __name__ == "__main__":
    main()
