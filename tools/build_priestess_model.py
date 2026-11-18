"""Give the Priestess a body: the robed townswoman, with a SpellCast clip.

Issue #15: "Game crashes when seeing druidess? enemy (again the granny model error)". The three
Priestess cans name `Characters/Monsters/English Enemies/Priestess`, and that model was never
finished. Its folder, `Models3D/Enemies/English Priestess/`, is byte-for-byte the base Terror:
the same `Terror.MODEL.gr2` (md5-identical to the Terror's) and the Terror's `Shared
Animations/original` set, the one Terror set with no `Spellcast`. The cans only cast (Spike and
Fireball, and Fixt's spell cycle), so every cast asked for a clip the model lacks, which is the
"GRANNY MODEL" placeholder and plausibly the crash. Vanilla never placed a Priestess, so nobody
saw it; Fixt has fielded them at the Shrine since 0.19.0.

The fix, with nothing outside the Priestess touched:

  * **mesh** -- a copy of Townswoman 3's `FemaleTownie03.MODEL.gr2`, at
    `Models3D/Enemies/English Priestess/Priestess`, with two textures replaced by the painted
    skins in tools/art (see paint_priestess_skins.py): the clothing sheet (texture 5,
    `dress.tif`) and the head sheet (texture 4, `facebrnhr.tif`). Both share a sector with the
    file's other textures, so each payload is appended to that sector and its fixup repointed,
    the fallback the retexturing notes give when a payload does not own its sector.
  * **names** -- the copy is `Priestess` everywhere: its `MODEL.TXT` `Short Name`, and the
    manifest's `Character Slot Types/Body` slot, which names the mesh by its file leaf (all 190
    character manifests agree). Left as `FemaleTownie03`, the slot would name a file that is not
    there, and she could draw no body.
  * **manifest** -- `Priestess.mdl16` becomes Woman Generic3's, with its one mesh path swapped
    for the copy. That brings the townswomen's eight shared clips, `SpellCast` among them. Only
    the three Priestess cans use this manifest, so no other creature changes.

The cans keep `Model=Characters/Monsters/English Enemies/Priestess`, unchanged.

Run after editing the art. Pure function of the vanilla archive and tools/art: it rebuilds both
outputs from scratch every time, so rerunning is safe.
"""
import dataclasses
import json
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import FX, zf
import gr2_format as gf
import gr2_to_gltf
from gltf_to_gr2 import repack
from binktc0_decode import decode_binktc0

ART = HERE / "art"
SRC = "Resources/Models3D/NPC/Barcelona/Female Human Generic/Female Townie3/FemaleTownie03"
LEAF = "Models3D/Enemies/English Priestess/Priestess"
DEST = "Resources/" + LEAF
MANIFEST_SRC = "Cache/Models/Characters/NPC/Barcelona/Generic Townspeople/Woman Generic3.mdl16"
MANIFEST = "Cache/Models/Characters/Monsters/English Enemies/Priestess.mdl16"
JOBS = [(5, "dress.tif", "priestess-robe-skin"), (4, "facebrnhr.tif", "priestess-hood-skin")]
NAMES = {n.lower(): n for n in zf.namelist()}


def zread(rel):
    return zf.read(NAMES[rel.lower()])


def one(e, n):
    return gr2_to_gltf.field(e if isinstance(e, list) else [e], n)


def build_mesh():
    raw = zread(SRC + ".MODEL.gr2")
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
    touched = set()
    payloads = {}
    for idx, source_name, art in JOBS:
        payload = (ART / (art + ".binktc0")).read_bytes()
        payloads[idx] = payload
        tex = one(roots, "Textures").value[idx]
        assert one(tex, "FromFileName").value.lower().endswith(source_name.lower()), \
            "texture %d is %s, not %s" % (idx, one(tex, "FromFileName").value, source_name)
        assert (one(tex, "Width").value, one(tex, "Height").value) == (256, 256)
        px = one(one(one(tex, "Images").value, "MIPLevels").value, "Pixels")
        old_n = len(px.value)
        ptr = sectors[px.data_sector_id].pointer_table.get(px.offset + 4)
        assert ptr is not None, "no fixup for texture %d's Pixels pointer" % idx
        assert struct.unpack_from("<I", data[px.data_sector_id], px.offset)[0] == old_n
        assert bytes(data[ptr.dst_sector][ptr.dst_offset:ptr.dst_offset + old_n]) == \
            bytes(e.value for e in px.value), "texture %d's payload is not where its pointer says" % idx
        blk = data[ptr.dst_sector]
        while len(blk) % 4:
            blk.append(0)
        at = len(blk)
        blk += payload
        sectors[px.data_sector_id].pointer_table[px.offset + 4] = dataclasses.replace(ptr, dst_offset=at)
        struct.pack_into("<I", data[px.data_sector_id], px.offset, len(payload))
        touched |= {ptr.dst_sector, px.data_sector_id}
        print("   %s: %d -> %d bytes" % (art, old_n, len(payload)))

    dest = FX / (DEST + ".MODEL.gr2")
    dest.parent.mkdir(parents=True, exist_ok=True)
    repack(raw, header, file_info, infos, sectors, data, touched, str(dest))

    # reload and check: counts unchanged, and each texture decodes from the new payload
    g = gf.GrannyFile.load_from_bytes(dest.read_bytes())
    ref = gf.GrannyFile.load_from_bytes(raw)
    for k in ("Textures", "Materials", "Skeletons", "VertexDatas", "TriTopologies", "Meshes", "Models"):
        assert len(one(g.root_elements, k).value) == len(one(ref.root_elements, k).value), k
    for idx, _, art in JOBS:
        tex = one(g.root_elements, "Textures").value[idx]
        px = one(one(one(tex, "Images").value, "MIPLevels").value, "Pixels")
        got = bytes(e.value for e in px.value)
        assert got == payloads[idx], "texture %d did not reload as written" % idx
        assert len(decode_binktc0(256, 256, got, has_alpha=False)) == 256 * 256 * 3
    print("mesh: %s reloads clean" % DEST)

    # its own Short Name, as BucklerBetter has, so nothing keyed on the name can confuse the two
    txt = zread(SRC + ".MODEL.TXT").decode("latin-1")
    assert txt.count("Short Name=FemaleTownie03") == 1
    txt = txt.replace("Short Name=FemaleTownie03", "Short Name=Priestess")
    (FX / (DEST + ".MODEL.TXT")).write_bytes(txt.encode("latin-1"))


def build_manifest():
    m = bytearray(zread(MANIFEST_SRC))
    old = SRC[len("Resources/"):].encode("latin-1")
    at = m.find(old)
    assert m.count(old) == 1 and at >= 4, "Woman Generic3's mesh path is not unique in its manifest"
    assert struct.unpack_from("<I", m, at - 4)[0] == len(old), "the mesh path is not length-prefixed"
    m[at - 4:at + len(old)] = struct.pack("<I", len(LEAF)) + LEAF.encode("latin-1")
    # the Body slot names the mesh by its FILE leaf (all 190 character manifests agree, case
    # aside), so it must follow the rename or she draws no body at all
    slot = b"Character Slot Types/Body"
    oldname, newname = old.split(b"/")[-1], LEAF.split("/")[-1].encode("latin-1")
    hits = [i for i in range(len(m)) if m.startswith(slot, i)]
    named = [i + len(slot) for i in hits
             if m[i + len(slot) + 4:i + len(slot) + 4 + len(oldname)] == oldname
             and struct.unpack_from("<I", m, i + len(slot))[0] == len(oldname)]
    assert len(named) == 1, "expected one Body slot naming %s, found %d" % (oldname, len(named))
    j = named[0]
    m[j:j + 4 + len(oldname)] = struct.pack("<I", len(newname)) + newname
    assert oldname not in m, "the townswoman's name survives somewhere in the manifest"
    out = FX / MANIFEST
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(bytes(m))
    assert b"/SpellCast" in m, "the manifest lost its SpellCast clip"
    print("manifest: %s -> %s" % (MANIFEST.split("/")[-1], LEAF))


def register():
    path = FX.parent / "mod.json"
    text = path.read_bytes().decode("utf8")
    doc = json.loads(text)
    want = [MANIFEST, DEST + ".MODEL.gr2", DEST + ".MODEL.TXT"]
    files = doc["files"]
    added = [w for w in want if w not in files]
    if not added:
        return
    # mostly sorted, with later additions out of place: insert each entry before the first
    # existing one that sorts after it, and move nothing else
    for w in added:
        k = next((i for i, f in enumerate(files) if f > w), len(files))
        files.insert(k, w)
    lines = text.split("\n")
    start = lines.index('  "files": [')
    end = next(k for k in range(start + 1, len(lines)) if lines[k].strip() in ("]", "],"))
    body = ['    "%s",' % f for f in files]
    body[-1] = body[-1].rstrip(",")
    new = "\n".join(lines[:start + 1] + body + lines[end:])
    assert json.loads(new)["files"] == files and json.loads(new).keys() == doc.keys()
    path.write_bytes(new.encode("utf8"))
    print("mod.json: +%d entries" % len(added))


if __name__ == "__main__":
    build_mesh()
    build_manifest()
    register()
