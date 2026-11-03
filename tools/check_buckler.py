"""Verify the buckler: its stats, its pool, its art and its placement.

`check_weapon_pools.py` covers weapon pools; the buckler is a shield, so it needs its own.
The checks that matter are the ones a formatting gate cannot see: that the pool resolves to
the same twelve additions the small shield offers with nothing reachable twice, that every
copy points its named expressions and its exclusions at itself rather than the original, that
each grade names a mesh that actually exists, and that the placement reaches merchants without
touching the 69-site drop path.

Run after tools/build_buckler.py.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import CR, FX, zf, read

AG = "Inventory/Inventory Addition Groups/Shields and Armor/"
GROUP = AG + "Shield BUCKLER Additions"
MAGIC = "Inventory/Creating Random Magic Items/"
EXPECT_MESH = {"Basic": None, "Better": "Buckler", "Special": "BucklerSpecial"}
bad = []

# ---------------------------------------------------------------- the item
t = read("Resources/Inventory Items/ShieldBuckler.InventoryItem")
mods = {}
for m in re.finditer(r"Constant Value=(-?\S+)[\s\S]{0,200}?"
                     r"(?:Derived character attribute to modify|Skill to modify)=(\S[^\r\n]*)", t):
    mods[m.group(2).strip().split("/")[-1]] = m.group(1)
want = {"(AC) Armor Class": "1", "CriticalChance": "2", "Unarmed": "4"}
print("modifiers:", mods)
if mods != want:
    bad.append("modifiers are %s, wanted %s" % (mods, want))
for field, value in (("Encumbrance", "1"), ("Slot Used In", "Character Slot Types/Hand"),
                     ("Number Hands Needed", "One"),
                     ("On the ground", "Items/PickUps/Armor/Shield_Small_PU"),
                     ("Display Name", "Buckler"),
                     ("Inventory Addition Group", GROUP),
                     ("Origonal Item", "Inventory Items/ShieldBuckler")):
    got = re.search(re.escape(field) + r"=(.*)" + CR, t).group(1).strip()
    if got != value:
        bad.append("%s is %r, wanted %r" % (field, got, value))
icons = {k: v.strip() for k, v in re.findall(r"\t(Basic|Better|Special)=(.*)" + CR, t)}
print("icons    :", {k: v.split("/")[-1] for k, v in icons.items()})
arm = re.search(r"Character Slot Types/Arm=(.*)" + CR, t.split("Override Names")[1]).group(1).strip()
print("on-body  :", arm)
if arm != "Buckler":
    bad.append("the base item names %r on the arm" % arm)

# ---------------------------------------------------------------- the pool
adds = {}
for p in (FX / "Resources").rglob("*.InventoryAddition"):
    rel = p.relative_to(FX / "Resources").as_posix()[:-len(".InventoryAddition")]
    at = read("Resources/" + rel + ".InventoryAddition")
    g = re.search(r"Inventory Addition Group=(.*)" + CR, at)
    if g and g.group(1).strip() == GROUP:
        adds[rel] = at
print()
print("pool     : %d additions" % len(adds))
hist = {}
for rel, at in sorted(adds.items()):
    grade = re.search(r"Item Grade=(.*)" + CR, at).group(1).strip()
    hist[grade] = hist.get(grade, 0) + 1
    # self-references must name the copy
    stray = [x for x in re.findall(r"InventoryAddition=(.*)" + CR, at) if x.strip() != rel]
    if stray:
        bad.append("%s points its expressions at %s" % (rel.split("/")[-1], stray))
    # exclusions must stay inside the copied set
    for e in re.findall(r"Addition Cannot Be Combined With=(.*)" + CR, at):
        if e.strip() not in adds:
            bad.append("%s excludes %s, outside its own pool" % (rel.split("/")[-1], e.strip()))
    # ground art must not be overridden, since no buckler sprite exists
    gnd = re.search(r"On the ground=(.*)" + CR, at).group(1).strip()
    if gnd != "!Unknown Model":
        bad.append("%s overrides the ground art with %s" % (rel.split("/")[-1], gnd))
    # The mesh must be read out of the Override NAMES block specifically. Selecting the
    # line by "no Models3D in it" is what let a bad edit through: the builder had written
    # the mesh into the Override Models line, which then also matched that filter.
    key = "Character Slot Types/Arm="
    _, _, names_block = at.partition("Override Names")
    exp = EXPECT_MESH[grade]
    named = [l.strip()[len(key):] for l in names_block.split(CR)
             if l.strip().startswith(key)]
    got = (named[0] or None) if named else None
    if got != exp:
        bad.append("%s (%s) names %r in Override Names, wanted %r" % (
            rel.split("/")[-1], grade, got, exp))
    # and the Override Models block must be left exactly as vanilla wrote it
    models_block = at.partition("Override Names")[0]
    mline = [l.strip()[len(key):] for l in models_block.split(CR)
             if l.strip().startswith(key)]
    if mline and not mline[0].startswith("Models3D/"):
        bad.append("%s has %r in Override Models -- that block was edited" % (
            rel.split("/")[-1], mline[0]))
print("by grade :", hist)
if hist != {"Basic": 4, "Better": 4, "Special": 4}:
    bad.append("pool shape is %s, the small shield offers 4/4/4" % hist)
small = {n.split("/")[-1] for n in zf.namelist()
         if n.lower().endswith(".inventoryaddition")
         and re.search(r"Inventory Addition Group=" + re.escape(AG + "Shield Additions") + CR,
                       zf.read(n).decode("latin-1") or "")}
if {r.split("/")[-1] + ".InventoryAddition" for r in adds} != small:
    bad.append("the buckler pool is not the same twelve the small shield offers")

# ---------------------------------------------------------------- art exists
print()
for ref in sorted(set(icons.values())) + ["Items/PickUps/Armor/Shield_Small_PU"]:
    cache = "Cache/Models/" + ref + ".mdl16"
    ok = cache in zf.namelist() or (FX / cache).exists()
    print("   %-5s %s" % ("ok" if ok else "FAIL", ref))
    if not ok:
        bad.append("art missing: " + ref)
for mesh in ("Models3D/Weapons/Shields/Buckler/Buckler",
             "Models3D/Weapons/Shields/Buckler Special/BucklerSpecial"):
    ok = ("Resources/" + mesh + ".MODEL.GR2") in zf.namelist()
    reg = any(mesh.encode("latin-1") in zf.read(c) for c in
              ("Cache/Models/Characters/Player Characters/Human Male.mdl16",
               "Cache/Models/Characters/Player Characters/Human Female.mdl16"))
    print("   %-5s %-54s registered in a composite: %s" % ("ok" if ok and reg else "FAIL", mesh, reg))
    if not (ok and reg):
        bad.append("mesh unusable: " + mesh)

# ---------------------------------------------------------------- placement
print()
ms = read("Resources/" + MAGIC + "All Armor and Shields.can")
nests = [x.strip() for x in re.findall(r"Canned Item List=(.*)" + CR, ms)]
print("All Armor and Shields nests:", [n.split("/")[-1] for n in nests])
if MAGIC + "All Shields and Buckler" not in nests:
    bad.append("the merchant can does not nest the buckler list")
if MAGIC + "All Shields" in nests:
    bad.append("the merchant can still nests All Shields directly")
pure = zf.read("Resources/" + MAGIC + "All Shields.can").decode("latin-1")
live = read("Resources/" + MAGIC + "All Shields.can")
print("All Shields untouched (the 69-site path):", live == pure)
if live != pure:
    bad.append("All Shields was modified -- every chest in the game is affected")

print()
if bad:
    for x in bad:
        print("FAIL", x)
    sys.exit(1)
print("buckler is wired: stats, a 4/4/4 pool matching the small shield's, art that exists")
print("and is composite-registered, and merchant-only placement")
