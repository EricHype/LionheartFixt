"""Prove the per-base restructure did not change which additions a weapon can roll.

The feature splits one shared pool of 29 melee additions into a pool per base weapon, so
that each copy can name its own base's mesh. The risk that nothing else catches is a pool
that came out the wrong shape: an addition reachable twice (double weight), reachable from
the wrong base, or no longer reachable at all. `validate.py` checks formatting and
structure, not reachability, so this does.

For every weapon base item it resolves `Inventory Addition Group` through the nesting tree,
collects what each reachable addition is, and asserts:

  * the grade histogram matches vanilla's for that base's group
  * no addition name is reachable twice
  * every reachable addition that names a mesh names the mesh for *this* base
  * every addition still carries a self-consistent named-expression path

Run after tools/build_weapon_meshes.py.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import CR, FX, zf, read

AG = "Inventory/Inventory Addition Groups/Weapons/"
MESH = {
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
    "LongBow": ("BowBetter", "BowSpecial"),
    "LongBow Composite": ("BowSpecial", "BowSpecial"),
    "Crossbow": ("CrossBowBetter", "CrossBowSpecial"),
}

# every addition in the mod or in vanilla, by resource-relative path
ADDS = {}
for n in zf.namelist():
    if n.lower().endswith(".inventoryaddition"):
        ADDS[n[len("Resources/"):-len(".InventoryAddition")]] = n
for p in (FX / "Resources").rglob("*.InventoryAddition"):
    rel = p.relative_to(FX / "Resources").as_posix()[:-len(".InventoryAddition")]
    ADDS[rel] = "Resources/" + rel + ".InventoryAddition"

BY_GROUP = {}
INFO = {}
for rel, n in ADDS.items():
    t = read(n)
    g = re.search(r"Inventory Addition Group=(.*)" + CR, t)
    grade = re.search(r"Item Grade=(.*)" + CR, t)
    key = "Character Slot Types/Weapon="
    mesh = None
    for ln in t.split(CR):
        s = ln.strip()
        if s.startswith(key) and not s[len(key):].startswith("Models3D") and s[len(key):]:
            mesh = s[len(key):]
    selfbad = [m for m in re.findall(r"InventoryAddition=(.*)" + CR, t) if m.strip() != rel]
    INFO[rel] = (grade.group(1).strip() if grade else "?", mesh, selfbad)
    if g:
        BY_GROUP.setdefault(g.group(1).strip(), []).append(rel)


def nested(group, seen=None):
    seen = seen if seen is not None else set()
    if group in seen:
        return []
    seen.add(group)
    out = list(BY_GROUP.get(group, []))
    gf = "Resources/" + group + ".AdditionGroup.txt"
    try:
        t = read(gf)
    except KeyError:
        return out
    for sub in re.findall(r"Inventory Addition Group=(.*)" + CR, t):
        out += nested(sub.strip(), seen)
    return out


VANILLA_SHAPE = {"Basic": 3, "Better": 20, "Special": 6}
MISSILE_SHAPE = {"Basic": 3, "Better": 4, "Special": 5}
bad = []
print("%-22s %-34s %s" % ("base weapon", "group", "pool"))
for base, (better, special) in MESH.items():
    rel = "Resources/Inventory Items/" + base + ".InventoryItem"
    group = re.search(r"Inventory Addition Group=(.*)" + CR, read(rel)).group(1).strip()
    pool = nested(group)
    names = [r.split("/")[-1] for r in pool]
    hist = {}
    for r in pool:
        hist[INFO[r][0]] = hist.get(INFO[r][0], 0) + 1

    want = MISSILE_SHAPE if "Bow" in base or "Crossbow" in base else VANILLA_SHAPE
    if hist != want:
        bad.append("%s pool is %s, vanilla shape is %s" % (base, hist, want))
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        bad.append("%s reaches these twice: %s" % (base, dupes))

    wrong = []
    for r in pool:
        grade, mesh, selfbad = INFO[r]
        if selfbad:
            bad.append("%s: %s points its named expressions at %s" % (base, r, selfbad))
        expect = better if grade == "Better" else (special if grade == "Special" else None)
        if mesh and mesh != expect:
            wrong.append("%s names %s, wanted %s" % (r.split("/")[-1], mesh, expect))
        if expect and grade in ("Better", "Special") and not mesh:
            wrong.append("%s (%s) names no mesh though %s exists" % (r.split("/")[-1], grade, expect))
    for w in wrong:
        bad.append("%s: %s" % (base, w))

    meshes = sorted({INFO[r][1] for r in pool if INFO[r][1]})
    print("   %-19s %-34s %s | meshes: %s" % (
        base, group.split("/")[-1], hist, ", ".join(meshes) or "none"))

print()
if bad:
    for b in bad:
        print("FAIL", b)
    sys.exit(1)
print("every pool keeps vanilla's shape, nothing is reachable twice,")
print("and every addition that names a mesh names the right one for its base")
