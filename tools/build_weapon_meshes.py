"""Give magic weapons the Better and Special meshes the game shipped and never used.

Twenty-one weapon meshes sat in `Models3D/Weapons` referenced by nothing: a Better and a
Special variant for most base weapons, finished art, registered in the player composite,
and reachable by no item in the game. The inventory *icons* already tier off `Item Grade`
for nine base weapons, so the intent was built and only the on-body mesh was never wired.

Three things had to be true, and all three were established in play through the Playtest Kit
(`mods/playtest-kit`, node 9010) before any of this was written:

  1. An `InventoryAddition` can override the `Weapon` slot. Vanilla only ever overrides
     `Arm` (34 shield additions) and `Head` (10 helmet additions), so this was an
     assumption until a probe proved it.
  2. A mesh name absent from a character composite's registry renders **nothing** -- no
     fallback, no crash, a silent invisible weapon. That makes the registry a hard
     constraint rather than a nicety.
  3. Orientation and scale cannot be screened from the files. Known-good shipping meshes
     disagree with their family's base weapon by up to 177 degrees on every static metric
     tried, so each mesh was looked at in the hand.

What that pass found, and what this fixes:

  * `BowBetter` rendered 1.8x oversize. Six variant MODEL.TXT files carry
    `Short Name=undefined` and `Render Scaling=1`, the signature of metadata nobody filled
    in, beside a base weapon with a real value.

    `MaceGreat` carries that same signature and is deliberately **not** in the list. It is a
    shipped weapon, and every Great renders larger than its base -- but TwoHandedSwordGreat
    and BattleAxeGreat get there geometrically, with bigger meshes at the base's scale, while
    MaceGreat's mesh is the same size as Mace's. Its scale value is what carries its "Great",
    so copying the base's 0.9 would make the Great Mace render identical to a plain Mace.
  * `ScimitarSpecial` and `BattleAxeBetter` rendered with the blade facing up. Both are
    rotated 180 degrees about Y, the weapon's own length -- every mesh in the game runs along
    -Y from a handle at the origin, and these two already did, so the length was never wrong
    and only the roll about it was.
  * `ScimitarSpecial` and `WarHammerBetter` are missing from the male composite's registry
    (88 entries against the female's 90), which is why a male character held nothing at all.

Structure of the wiring. An addition cannot know which base weapon it landed on, so a group
shared across bases cannot name a mesh. Vanilla solved this for shields by triplicating the
additions into Small/Medium/Large groups, and bows and crossbows already have their own
per-base groups -- which is why those two are a drop-in and melee is not. Melee gets the
shield treatment: the 26 graded additions are copied per base weapon, each copy naming its
own base's mesh, reached through a per-base group that nests a shared group for the three
ungraded additions. The 29 originals are kept and repointed rather than deleted, because
existing saves hold magic weapons that reference them by path.

Usage: python tools/build_weapon_meshes.py
"""
import re
import shutil
import struct
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import CR, T, FX, zf, read, balanced
import resource_format
import gr2_format as gf
from gr2_to_gltf import field, _group_repeated_records
from gltf_to_gr2 import repack, _patch_floats

SLOTS = ["!None", "Arm", "Arrow", "Body", "Bolt", "Finger", "Foot", "Hand", "Head",
         "HotKey", "Neck", "Shield", "Waist", "Weapon"]
AG = "Inventory/Inventory Addition Groups/Weapons/"
IA = "Inventory/Inventory Additions/"
W3D = "Resources/Models3D/Weapons/"

# ---------------------------------------------------------------- asset fixes

# variant mesh -> (base weapon mesh whose Render Scaling it copies, that value)
SCALE = {
    "Bows/Bow Better/BowBetter": ("Bows/Bow/Bow-LP", "0.55"),
    "Bows/CrossBow Better/CrossBowBetter": ("Bows/CrossBow/CrossBow", "0.5"),
    "Bows/CrossBow Special/CrossBowSpecial": ("Bows/CrossBow/CrossBow", "0.5"),
    "Swords/Bastard Sword Better/BastardSwordBetter": ("Swords/Bastard Sword/BastardSword", "0.5"),
    "Swords/Bastard Sword Special/BastardSwordSpecial": ("Swords/Bastard Sword/BastardSword", "0.5"),
    "Misc_NonSwords/Mace Better/MaceBetter": ("Misc_NonSwords/Mace/Mace", "0.9"),
}
# mesh -> the base weapon it must end up agreeing with on the X asymmetry
ROTATE = {
    "Swords/Scimitar Special/ScimitarSpecial": "Swords/Scimitar/Scimitar",
    "Misc_NonSwords/Battle Axe Better/BattleAxeBetter": "Misc_NonSwords/Battle Axe/BattleAxe",
}
MALE = "Cache/Models/Characters/Player Characters/Human Male.mdl16"
FEMALE = "Cache/Models/Characters/Player Characters/Human Female.mdl16"
REGISTER = [
    ("Models3D/Weapons/Misc_NonSwords/WarHammer Better/WarHammerBetter",
     "Models3D/Weapons/Misc_NonSwords/WarHammer/WarHammer"),
    ("Models3D/Weapons/Swords/Scimitar Special/ScimitarSpecial",
     "Models3D/Weapons/Swords/Scimitar/Scimitar"),
]


def write(rel, data):
    p = FX / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def write_text(rel, text):
    assert text.count("\n") == text.count(CR), rel + " is not all-CRLF"
    write(rel, resource_format.parse_resource_text(text).to_text().encode("latin-1"))


def fix_scales():
    for rel, (base, scale) in SCALE.items():
        # vanilla, not read(): read() prefers Fixt's copy, so a rerun would see the
        # scaling this function just wrote and trip its own default-value assertion
        bt = zf.read(W3D + base + ".MODEL.TXT").decode("latin-1")
        assert re.search(r"Render Scaling=" + re.escape(scale) + CR, bt), \
            "%s is not at %s" % (base, scale)
        t = zf.read(W3D + rel + ".MODEL.TXT").decode("latin-1")
        assert re.search(r"Short Name=undefined" + CR, t), rel + " has an authored Short Name"
        assert t.count("Render Scaling=1" + CR) == 1, rel + " is not at the default scale"
        out = t.replace("Render Scaling=1" + CR, "Render Scaling=" + scale + CR)
        assert out.replace("Render Scaling=" + scale, "Render Scaling=1") == t
        write(W3D + rel + ".MODEL.TXT", out.encode("latin-1"))
    print("scale: %d MODEL.TXT files" % len(SCALE))


def _tip_x(raw):
    g = gf.GrannyFile.load_from_bytes(raw)
    pts = []
    for mesh in field(g.root_elements, "Meshes").value:
        for v in field(field(mesh, "PrimaryVertexData").value, "Vertices").value:
            pts.append([x for _, x in field(v, "Position").value])
    return min(pts, key=lambda p: p[1])[0]


def fix_rotations():
    """180 degrees about Y: keep Y, negate X and Z. Determinant +1, so winding survives and
    no triangle indices need reversing -- which a mirror would have required."""
    for rel, base in ROTATE.items():
        raw = zf.read(W3D + rel + ".MODEL.GR2")
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
        touched, n = set(), {"Position": 0, "Normal": 0}
        for mf in field(roots, "Models").value:
            for rec in _group_repeated_records(field(mf, "MeshBindings").value, ["Mesh"]):
                mesh = field(rec, "Mesh").value
                for v in field(field(mesh, "PrimaryVertexData").value, "Vertices").value:
                    for key in ("Position", "Normal"):
                        e = field(v, key)
                        if e is None:
                            continue
                        old = tuple(x for _, x in e.value)
                        _patch_floats(data, e, (-old[0], old[1], -old[2]))
                        touched.add(e.data_sector_id)
                        n[key] += 1
        assert n["Position"] and n["Normal"] == n["Position"], \
            "%s: %d positions, %d normals -- a partial rotation would light wrong" % (
                rel, n["Position"], n["Normal"])

        dest = FX / (W3D + rel + ".MODEL.GR2")
        dest.parent.mkdir(parents=True, exist_ok=True)
        repack(raw, header, file_info, infos, sectors, data, touched, str(dest))

        out = dest.read_bytes()
        now, was, want = _tip_x(out), _tip_x(raw), _tip_x(zf.read(W3D + base + ".MODEL.GR2"))
        assert abs(now + was) < 1e-3, rel + ": X did not invert"
        assert now * want > 0, "%s did not land on %s's side" % (rel, base)
    print("rotate: %d meshes, both now agree with their base weapon" % len(ROTATE))


def fix_registry():
    """The composite .mdl16 is a flat stream -- u32 count then that many u32-length-prefixed
    strings, no offset table, no size field, no checksum. Splice and bump the count."""
    def registry(data):
        first = data.find(b"Models3D/")
        count = struct.unpack_from("<I", data, first - 8)[0]
        p, out = first - 4, []
        for _ in range(count):
            ln = struct.unpack_from("<I", data, p)[0]
            out.append((p, data[p + 4:p + 4 + ln].decode("latin-1")))
            p += 4 + ln
        return first - 8, count, out, p

    # Later work (BucklerBetter, the Templar shields) registers more meshes in the shipped composite. It is built from
    # vanilla here, so once it exists a rerun would drop theirs.
    if (FX / MALE).exists():
        print("registry: male composite already shipped, left alone")
        return
    orig = zf.read(MALE)
    at, count, before, end = registry(orig)
    paths = [s for _, s in before]
    fem = [s for _, s in registry(zf.read(FEMALE))[2]]
    for path, anchor in REGISTER:
        assert path in fem, "not registered for the female composite either: " + path
        assert path not in paths, "already registered: " + path
        assert paths.count(anchor) == 1, "cannot pin the insert point: " + anchor

    out = orig
    for path, anchor in sorted(REGISTER, key=lambda a: paths.index(a[1]), reverse=True):
        off = next(o for o, s in before if s == anchor)
        out = out[:off] + struct.pack("<I", len(path)) + path.encode("latin-1") + out[off:]
    out = out[:at] + struct.pack("<I", count + len(REGISTER)) + out[at + 4:]

    new_at, new_count, after, new_end = registry(out)
    names = [s for _, s in after]
    assert new_at == at and new_count == count + len(REGISTER) == len(names)
    assert [s for s in names if s not in [p for p, _ in REGISTER]] == paths
    assert out[:at] == orig[:at] and out[new_end:] == orig[end:]
    assert struct.unpack_from("<I", out, new_end)[0] == 14, "the slot-type block moved"
    write(MALE, out)
    print("registry: male composite %d -> %d entries" % (count, new_count))


# ---------------------------------------------------------------- the wiring

def override_block(mesh, indent=2):
    t = T * indent
    out = t + "PlugIn Behavior=CPlugInBehaviorXRPGCharacterCompositeGrannyModelOverride" + CR + t + "{" + CR
    out += t + T + "Override Models=Array" + CR + t + T + "{" + CR
    for s in SLOTS:
        out += t + T * 2 + "Character Slot Types/" + s + "=Models3D/!None/!None" + CR
    out += t + T + "}" + CR + t + T + "Override Names=Array" + CR + t + T + "{" + CR
    for s in SLOTS:
        out += t + T * 2 + "Character Slot Types/" + s + "=" + (mesh if s == "Weapon" else "") + CR
    out += t + T + "}" + CR + t + T + "Override Active=0" + CR + t + "}" + CR
    return out


def add_override(text, mesh):
    """Splice the override plugin into `PlugIn Behaviors=Array` and bump its Item Count.

    The array's closing brace is found by brace matching, not by searching for an indented
    `}` -- an rfind on that lands inside the last plugin. Insert at the start of the closing
    brace's line, and apply the two edits back to front so the first does not shift the
    second's offsets.

    Idempotent: if the addition already carries an override, its Weapon name is rewritten
    rather than a second plugin added. Without that, rerunning the builder over its own
    output doubles the plugin, and this script reads through `lhbuild.read()`, which prefers
    Fixt's copy of a file over vanilla's.
    """
    if "GrannyModelOverride" in text:
        # rewrite the one name line by splitting on CR rather than with a regex: a
        # pattern for "anything but a line break" needs backslash escapes, and those do
        # not survive being written through a shell heredoc
        key = "Character Slot Types/Weapon="
        lines = text.split(CR)
        hits = [k for k, ln in enumerate(lines)
                if ln.strip().startswith(key)
                and not ln.strip()[len(key):].startswith("Models3D")]
        assert len(hits) == 1, "expected one Weapon override name, found %d" % len(hits)
        ln = lines[hits[0]]
        lines[hits[0]] = ln[:len(ln) - len(ln.lstrip())] + key + mesh
        return CR.join(lines)
    i = text.index(T + "PlugIn Behaviors=Array" + CR)
    end = balanced(text, i)
    assert text[end - 1] == "}"
    close = end - 1
    while text[close - 1] == T:
        close -= 1
    m = re.compile(re.escape(T * 2 + "Item Count=") + r"(\d+)" + re.escape(CR)).search(text, i, end)
    assert m, "no Item Count in the plugin array"
    out = text[:close] + override_block(mesh) + text[close:]
    out = out[:m.start()] + T * 2 + "Item Count=" + str(int(m.group(1)) + 1) + CR + out[m.end():]
    return out


def group_file(nested):
    out = ("CInventoryAdditionGroup" + CR + "{" + CR +
           T + "Other Group that are part of this group=Array" + CR + T + "{" + CR +
           T * 2 + "Item Count=" + str(len(nested)) + CR)
    for g in nested:
        out += T * 2 + "Inventory Addition Group=" + g + CR
    return out + T + "}" + CR + "}" + CR


def repoint(text, group):
    out = re.sub(r"Inventory Addition Group=.*" + CR, "Inventory Addition Group=" + group + CR, text)
    # no assertion that the text changed: on a rerun it is already pointed here, and
    # demanding a change would make the whole builder single-use
    assert out.count("Inventory Addition Group=") == 1, "expected exactly one group line"
    assert "Inventory Addition Group=" + group + CR in out, "group did not take"
    return out


# -- base weapon -> (Better mesh, Special mesh). None where the game shipped no such art.
MELEE = {
    "LongSword": ("LongSwordBetter", "LongSwordSpecial"),
    "ShortSword": ("ShortSwordBetter", "ShortSwordSpecial"),
    "BastardSword": ("BastardSwordBetter", "BastardSwordSpecial"),
    "TwoHandedSword": ("TwoHndedSwordBetter", "TwoHndedSwordSpecial"),
    "BattleAxe": ("BattleAxeBetter", "BattleAxeSpecial"),
    "Mace": ("MaceBetter", "MaceSpecial"),
    "MorningStar": ("MorningStarBetter", "MorningStarSpecial"),
    "WarHammer": ("WarHammerBetter", "WarHammerSpecial"),
    "Scimitar": (None, "ScimitarSpecial"),
    "Club": ("ClubBetter", None),
    "BattleAxeGreat": (None, None),
    "MaceGreat": (None, None),
    "TwoHandedSwordGreat": (None, None),
}
MELEE_GROUP = AG + "Melee Weapon Additions"
SHARED = AG + "Melee Shared Additions"
NOVIS = {"Better": AG + "Melee Better No Visual", "Special": AG + "Melee Special No Visual"}
GREAT = AG + "Great Melee Additions"
PERBASE = AG + "Per Base/%s Melee Additions"
COPY = IA + "Weapons/Per Base/%s/%s"

BOW_SHARED = AG + "Bow Shared Additions"
BOW_GROUP = AG + "Bow Additions"
COMPOSITE = AG + "Composite Bow Additions"
BOW_COPY = IA + "Weapons/Crossbows and Bows/Composite/%s"


def additions_in(group):
    """Every addition declaring this group, with its grade, keyed by resource-relative path."""
    out = {}
    for n in zf.namelist():
        if not n.lower().endswith(".InventoryAddition".lower()):
            continue
        rel = n[len("Resources/"):-len(".InventoryAddition")]
        t = read(n)
        m = re.search(r"Inventory Addition Group=(.*)" + CR, t)
        if m and m.group(1).strip() == group:
            out[rel] = (re.search(r"Item Grade=(.*)" + CR, t).group(1).strip(), t)
    return out


def copy_addition(src_rel, text, dest_rel, group, mesh):
    """A copy has to carry its own path: `CInventoryAdditionsNamedExpressionExpression`
    names its own addition, so a copy that kept the original path would read the original's
    numbers. Vanilla has no melee addition that excludes another, so nothing else re-points.
    """
    out = text.replace("InventoryAddition=" + src_rel + CR, "InventoryAddition=" + dest_rel + CR)
    out = repoint(out, group)
    if mesh:
        out = add_override(out, mesh)
    return out


def wire_melee():
    # snapshot across every group the originals may already sit in, so a rerun sees the
    # same 29 additions it saw the first time
    orig = {}
    for g in (MELEE_GROUP, SHARED, NOVIS["Better"], NOVIS["Special"]):
        orig.update(additions_in(g))
    assert len(orig) == 29, "expected 29 melee additions, found %d" % len(orig)
    by_grade = {g: {r: t for r, (gg, t) in orig.items() if gg == g} for g in ("Basic", "Better", "Special")}
    assert [len(by_grade[g]) for g in ("Basic", "Better", "Special")] == [3, 20, 6]

    # the 29 originals stay, repointed: they are what existing saves reference by path, and
    # they are the pool the three Great weapons draw from since no variant art exists for them
    for rel, (grade, t) in orig.items():
        write_text("Resources/" + rel + ".InventoryAddition",
                   repoint(t, SHARED if grade == "Basic" else NOVIS[grade]))

    groups = {SHARED: [], NOVIS["Better"]: [], NOVIS["Special"]: [],
              GREAT: [SHARED, NOVIS["Better"], NOVIS["Special"]]}
    copies = 0
    for base, (better, special) in MELEE.items():
        if not better and not special:
            continue
        g = PERBASE % base
        nested = [SHARED]
        if not better:
            nested.append(NOVIS["Better"])
        if not special:
            nested.append(NOVIS["Special"])
        groups[g] = nested
        for grade, mesh in (("Better", better), ("Special", special)):
            if not mesh:
                continue
            for rel, t in by_grade[grade].items():
                dest = COPY % (base, rel.split("/")[-1])
                write_text("Resources/" + dest + ".InventoryAddition",
                           copy_addition(rel, t, dest, g, mesh))
                copies += 1

    for g, nested in groups.items():
        write_text("Resources/" + g + ".AdditionGroup.txt", group_file(nested))

    for base, (better, special) in MELEE.items():
        rel = "Resources/Inventory Items/" + base + ".InventoryItem"
        t = read(rel)
        want = GREAT if not (better or special) else PERBASE % base
        # accept the vanilla group or the one this function assigns, so a rerun is a no-op;
        # anything else means the item was pointed somewhere unexpected by hand
        now = re.search(r"Inventory Addition Group=(.*)" + CR, t).group(1).strip()
        assert now in (MELEE_GROUP, want), "%s names %s" % (base, now)
        write_text(rel, repoint(t, want))

    print("melee: %d copies, %d groups, %d base items repointed, %d originals repointed"
          % (copies, len(groups), len(MELEE), len(orig)))


def wire_missiles():
    # snapshot first: the in-place wiring below writes into files/, and read() prefers those
    bow = {}
    for g in (BOW_GROUP, BOW_SHARED):
        bow.update(additions_in(g))
    assert len(bow) == 12, "bow snapshot has %d additions" % len(bow)

    xbow = additions_in(AG + "Crossbow Additions")
    assert len(xbow) == 12, "crossbow snapshot has %d additions" % len(xbow)

    for group, meshes, adds in ((BOW_GROUP, ("BowBetter", "BowSpecial"), bow),
                                (AG + "Crossbow Additions",
                                 ("CrossBowBetter", "CrossBowSpecial"), xbow)):
        n = 0
        for rel, (grade, t) in adds.items():
            if grade == "Basic":
                continue
            mesh = meshes[0] if grade == "Better" else meshes[1]
            write_text("Resources/" + rel + ".InventoryAddition", add_override(t, mesh))
            n += 1
        print("%s: %d graded additions wired" % (group.split("/")[-1], n))

    # The Composite Long Bow's own base mesh is BowSpecial, the best bow art in the game, so
    # a Better addition naming BowBetter would visibly downgrade it. It gets its own group
    # whose copies name BowSpecial at both tiers. `Extra Damage` is copied along with them
    # because it and `of Fire` exclude each other by path, and an exclusion that points at
    # the original would stop firing for the copy.
    adds = bow
    dup = {rel: t for rel, (grade, t) in adds.items()
           if grade != "Basic" or rel.endswith("/Extra Damage")}
    shared = [rel for rel, (grade, t) in adds.items() if rel not in dup]
    assert len(dup) == 10 and len(shared) == 2, "composite split is %d/%d" % (len(dup), len(shared))

    for rel in shared:
        write_text("Resources/" + rel + ".InventoryAddition", repoint(adds[rel][1], BOW_SHARED))
    pair = {rel.split("/")[-1]: BOW_COPY % rel.split("/")[-1] for rel in dup}
    for rel, t in dup.items():
        dest = BOW_COPY % rel.split("/")[-1]
        out = copy_addition(rel, t, dest, COMPOSITE,
                            "BowSpecial" if adds[rel][0] != "Basic" else None)
        for name, copy_rel in pair.items():  # keep exclusions inside the copied set
            out = out.replace("Addition Cannot Be Combined With=" + rel.rsplit("/", 1)[0] + "/" + name + CR,
                              "Addition Cannot Be Combined With=" + copy_rel + CR)
        write_text("Resources/" + dest + ".InventoryAddition", out)

    write_text("Resources/" + BOW_SHARED + ".AdditionGroup.txt", group_file([]))
    write_text("Resources/" + COMPOSITE + ".AdditionGroup.txt", group_file([BOW_SHARED]))
    write_text("Resources/" + BOW_GROUP + ".AdditionGroup.txt", group_file([BOW_SHARED]))
    rel = "Resources/Inventory Items/LongBow Composite.InventoryItem"
    write_text(rel, repoint(read(rel), COMPOSITE))
    print("composite bow: %d copies, %d shared, own group" % (len(dup), len(shared)))


if __name__ == "__main__":
    fix_scales()
    fix_rotations()
    fix_registry()
    wire_missiles()
    wire_melee()
