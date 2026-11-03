"""Author BucklerBetter: a third buckler skin, so the Better tier is not the base.

The buckler shipped with two skins, `Buckler` (weathered copper) and `BucklerSpecial`
(gilded), for three grades. Vanilla's own answer when a family is short of art is to collapse
Basic and Better -- Club, LongBow and Scimitar all do it -- but that leaves a *magic* buckler
looking mundane, which is the thing this whole run set out to fix.

So this makes the third skin. The two shipped skins differ mainly in metal colour, so a
recolour works along the axis the artists used: steel, between weathered copper and gold.

Route, all of it from docs/engine-notes.md "Textures, and repainting one":

  * decode the base skin from the gr2 (BinkTC0, 256x256, Encoding=3) and recolour it;
  * re-encode through `granny2.dll`'s builder API, which needs a **32-bit interpreter** --
    the dll is 32-bit and a 64-bit python raises WinError 193 loading it;
  * splice the payload into a copy of the gr2. `Pixels` is a reference-to-array: a `u32`
    count at the element's offset and a pointer immediately after it, recorded in that
    sector's fixup table at `offset + 4`. The pixels live in their own sector holding nothing
    else, so the new payload replaces that sector's contents outright and only the count
    needs changing -- `dst_offset` stays 0. The script asserts the sector really does hold
    exactly the old payload before relying on that.

Verification is by reloading the written file and checking the `granny_file_info` counts, as
the notes insist, not by inspecting the bytes we just wrote.

The recolour and the encode are done by the scratch scripts that produced the agreed art;
this tool takes the encoded payload as input so the slow, interactive part stays out of it.

Usage: python tools/build_buckler_better.py <payload.binktc0>
"""
import re
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import CR, T, FX, zf, read
import gr2_format as gf
import gr2_to_gltf
from gltf_to_gr2 import repack

SRC = "Resources/Models3D/Weapons/Shields/Buckler/Buckler"
DEST = "Resources/Models3D/Weapons/Shields/Buckler Better/BucklerBetter"
MALE = "Cache/Models/Characters/Player Characters/Human Male.mdl16"
FEMALE = "Cache/Models/Characters/Player Characters/Human Female.mdl16"
REGISTER = ("Models3D/Weapons/Shields/Buckler Better/BucklerBetter",
            "Models3D/Weapons/Shields/Buckler/Buckler")
BUCKLER_ADDS = "Resources/Inventory/Inventory Additions/Shield/BUCKLER/"
ARM = T * 4 + "Character Slot Types/Arm="


def one(elements, name):
    if not isinstance(elements, list):
        elements = [elements]
    return gr2_to_gltf.field(elements, name)


def splice_texture(raw, payload):
    header, off = gf.parse_header(raw)
    endian = ">" if header.big_endian else "<"
    file_info, off = gf.parse_file_info(raw, off, endian)
    infos, sectors = [], []
    for _ in range(file_info.sector_count):
        info, off = gf.parse_sector_info(raw, off, endian)
        infos.append(info)
        sectors.append(gf.load_sector(raw, endian, info))
    roots, _ = gf.parse_element(sectors, file_info.root_ref.sector, file_info.type_ref.sector,
                                file_info.root_ref.position, file_info.type_ref.position,
                                header.bits_64, endian)
    data = [bytearray(s.data) for s in sectors]

    tex = one(roots, "Textures").value[0]
    w, h = one(tex, "Width").value, one(tex, "Height").value
    px = one(one(one(tex, "Images").value, "MIPLevels").value, "Pixels")
    old_n = len(px.value)
    ptr = sectors[px.data_sector_id].pointer_table.get(px.offset + 4)
    assert ptr is not None, "no fixup for the Pixels pointer at offset %d" % (px.offset + 4)
    assert struct.unpack_from("<I", data[px.data_sector_id], px.offset)[0] == old_n, \
        "the count at the element offset is not the payload length"
    # the payload must own its sector outright, or replacing it would clobber a neighbour
    assert ptr.dst_offset == 0 and len(data[ptr.dst_sector]) == old_n, \
        "sector %d holds %d bytes for a %d-byte payload at offset %d -- not exclusively ours" % (
            ptr.dst_sector, len(data[ptr.dst_sector]), old_n, ptr.dst_offset)

    data[ptr.dst_sector] = bytearray(payload)
    struct.pack_into("<I", data[px.data_sector_id], px.offset, len(payload))
    touched = {ptr.dst_sector, px.data_sector_id}
    return (header, file_info, infos, sectors, data, touched, w, h, old_n)


payload = Path(sys.argv[1]).read_bytes()
raw = zf.read(SRC + ".MODEL.GR2")
header, file_info, infos, sectors, data, touched, w, h, old_n = splice_texture(raw, payload)

dest = FX / (DEST + ".MODEL.GR2")
dest.parent.mkdir(parents=True, exist_ok=True)
repack(raw, header, file_info, infos, sectors, data, touched, str(dest))
print("mesh: %s  %dx%d texture, payload %d -> %d bytes" % (
    DEST.split("/")[-1], w, h, old_n, len(payload)))

# -- reload and check the counts, which is the check the notes insist on
out = dest.read_bytes()
g = gf.GrannyFile.load_from_bytes(out)
counts = {k: len(one(g.root_elements, k).value)
          for k in ("Textures", "Materials", "Skeletons", "VertexDatas", "TriTopologies",
                    "Meshes", "Models")}
ref = gf.GrannyFile.load_from_bytes(raw)
want = {k: len(one(ref.root_elements, k).value)
        for k in counts}
assert counts == want, "reloaded counts %s, original %s" % (counts, want)
tex = one(g.root_elements, "Textures").value[0]
px = one(one(one(tex, "Images").value, "MIPLevels").value, "Pixels")
assert len(px.value) == len(payload), "the reloaded payload is %d bytes" % len(px.value)
print("   reloads clean: %s" % counts)

# -- MODEL.TXT, cloned from the base buckler's with its own Short Name
txt = zf.read(SRC + ".MODEL.TXT").decode("latin-1")
assert "Short Name=undefined" in txt, "the base buckler's Short Name is not undefined"
txt = txt.replace("Short Name=undefined", "Short Name=BucklerBetter", 1)
(FX / (DEST + ".MODEL.TXT")).write_bytes(txt.encode("latin-1"))
print("   MODEL.TXT: Short Name=BucklerBetter")


# -- register the name in both composites, the way 0.89.0 added the two missing meshes
def registry(b):
    first = b.find(b"Models3D/")
    count = struct.unpack_from("<I", b, first - 8)[0]
    p, out = first - 4, []
    for _ in range(count):
        ln = struct.unpack_from("<I", b, p)[0]
        out.append((p, b[p + 4:p + 4 + ln].decode("latin-1")))
        p += 4 + ln
    return first - 8, count, out, p


new, anchor = REGISTER
for rel in (MALE, FEMALE):
    base = (FX / rel).read_bytes() if (FX / rel).exists() else zf.read(rel)
    at, count, entries, end = registry(base)
    paths = [s for _, s in entries]
    if new in paths:
        print("   %s: already registered" % rel.split("/")[-1])
        continue
    assert paths.count(anchor) == 1, "cannot pin the insert point in " + rel
    off = next(o for o, s in entries if s == anchor)
    out = base[:off] + struct.pack("<I", len(new)) + new.encode("latin-1") + base[off:]
    out = out[:at] + struct.pack("<I", count + 1) + out[at + 4:]
    nat, ncount, nentries, nend = registry(out)
    assert ncount == count + 1 == len(nentries)
    assert [s for s in (x for _, x in nentries) if s != new] == paths
    assert out[:at] == base[:at] and out[nend:] == base[end:]
    assert struct.unpack_from("<I", out, nend)[0] == 14, "the slot-type block moved"
    p = FX / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(out)
    print("   %s: %d -> %d entries" % (rel.split("/")[-1], count, ncount))

# -- point the four Better additions at it
n = 0
for p in sorted((FX / BUCKLER_ADDS).glob("*.InventoryAddition")):
    rel = "Resources/" + p.relative_to(FX / "Resources").as_posix()
    t = read(rel)
    if re.search(r"Item Grade=(.*)" + CR, t).group(1).strip() != "Better":
        continue
    head, _, tail = t.partition("Override Names")
    m = re.search(re.escape(ARM) + r"(.*)" + CR, tail)
    assert m, rel + " has no Arm name"
    cur = m.group(1).strip()
    assert cur in ("Buckler", "BucklerBetter"), "%s names %r" % (rel, cur)
    tail = tail[:m.start()] + ARM + "BucklerBetter" + CR + tail[m.end():]
    p.write_bytes((head + "Override Names" + tail).encode("latin-1"))
    n += 1
print("additions: %d Better copies now name BucklerBetter" % n)
