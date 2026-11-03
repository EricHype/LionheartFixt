"""Find gear that half-exists, in both directions.

The buckler was art with no item behind it: two meshes, two icons, composite registration,
and no `.InventoryItem` anywhere. That is one way for equipment to be unfinished. The other
is the inverse -- an item that exists, is fully specified, and is named by nothing that could
ever hand it to a player.

So this reports two lists:

  * **art without an item**, grouped so the *completeness* of each orphan set is visible. A
    lone icon is a sketch; an icon plus a pickup plus a mesh is something that was nearly
    made. The buckler scored highest on exactly this measure.
  * **items without a giver**, which walks every weapon, armour and shield item and asks
    whether any can, map, dialogue tree, merchant list or generator names it.

Both are leads, not findings. `docs/unused-content.md` is the place to write up anything this
turns over, and the fourth kind of orphan -- content this mod considered and cut -- cannot be
distinguished from the files at all, so grep releases.md before calling anything open.

Usage: python tools/unfinished_gear.py
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import FX, zf, read

EQUIP_SLOTS = ("Weapon", "Hand", "Arm", "Body", "Head", "Foot", "Waist", "Neck", "Finger")
SCAN = (".can", ".zax", ".dialogtree", ".inventoryitem", ".inventoryaddition", ".txt", ".character.txt")


def all_files():
    """Vanilla plus Fixt's own, so the question is 'reachable now', not 'in 2003'."""
    names = {n for n in zf.namelist()}
    names |= {"Resources/" + p.relative_to(FX / "Resources").as_posix()
              for p in (FX / "Resources").rglob("*") if p.is_file()}
    return sorted(names)


FILES = all_files()
print("scanning %d resources..." % len(FILES))

# ---------------------------------------------------------------- the corpus of references
blob = []
for n in FILES:
    if not n.lower().endswith(SCAN):
        continue
    try:
        blob.append(read(n))
    except Exception:
        continue
CORPUS = "\n".join(blob)
print("   %d text resources read\n" % len(blob))

# ---------------------------------------------------------------- A: art without an item
icons, pickups, meshes = {}, {}, {}
for n in FILES:
    if n.startswith("Cache/Models/Items/Inventory Images/") and n.endswith(".mdl16"):
        icons[n[len("Cache/Models/"):-len(".mdl16")]] = n
    elif n.startswith("Cache/Models/Items/PickUps/") and n.endswith(".mdl16"):
        pickups[n[len("Cache/Models/"):-len(".mdl16")]] = n
    elif n.upper().endswith(".MODEL.GR2") and (
            n.startswith("Resources/Models3D/Weapons")
            # armour and helmets live under the player composites, not Weapons/ --
            # scanning only Weapons/ would miss an armour equivalent of the buckler
            or "/Armor/" in n or "/Heads/" in n):
        meshes[n[len("Resources/"):-len(".MODEL.GR2")]] = n

composites = [n for n in FILES if n.endswith(".mdl16") and "/Characters/" in n]
regblob = b""
for n in composites:
    regblob += (FX / n).read_bytes() if (FX / n).exists() else zf.read(n)


def orphan(ref, leafmatch=False):
    if ref in CORPUS:
        return False
    if leafmatch and re.search(r"=\s*%s\s*$" % re.escape(ref.split("/")[-1]), CORPUS, re.M):
        return False
    return True


buckets = defaultdict(lambda: {"icon": [], "pickup": [], "mesh": [], "registered": False})


def key(ref):
    """Collapse 'Shield Buckler Best', 'BucklerSpecial', 'Buckler_PU' to one bucket."""
    s = re.sub(r"_PU$", "", ref.split("/")[-1])
    s = re.sub(r"(Better|Best|Special|Great|Small|Medium|Large|Lrg|Mdm)\b", "", s, flags=re.I)
    return re.sub(r"[^a-z]", "", s.lower()) or ref.split("/")[-1].lower()


for ref in icons:
    if orphan(ref):
        buckets[key(ref)]["icon"].append(ref.split("/")[-1])
for ref in pickups:
    if orphan(ref):
        buckets[key(ref)]["pickup"].append(ref.split("/")[-1])
for ref in meshes:
    if orphan(ref, leafmatch=True):
        b = buckets[key(ref)]
        b["mesh"].append(ref.split("/")[-1])
        b["registered"] = b["registered"] or ref.encode("latin-1") in regblob

print("== art with no item behind it, by how complete the set is")
rows = sorted(buckets.items(), key=lambda kv: -(len(kv[1]["icon"]) + len(kv[1]["pickup"]) + len(kv[1]["mesh"]) * 2))
for name, b in rows:
    score = len(b["icon"]) + len(b["pickup"]) + 2 * len(b["mesh"])
    bits = []
    if b["mesh"]:
        bits.append("mesh: " + ", ".join(sorted(b["mesh"])) + (" [composite-registered]" if b["registered"] else ""))
    if b["icon"]:
        bits.append("icon: " + ", ".join(sorted(b["icon"])))
    if b["pickup"]:
        bits.append("ground: " + ", ".join(sorted(b["pickup"])))
    print("   %-14s score %2d  %s" % (name, score, "  |  ".join(bits)))

# ---------------------------------------------------------------- B: items with no giver
print()
print("== equipment items that nothing hands out")
items = [n for n in FILES if n.lower().endswith(".inventoryitem")]
unreachable = []
for n in items:
    t = read(n)
    slot = re.search(r"Slot Used In=Character Slot Types/(\w+)", t)
    if not slot or slot.group(1) not in EQUIP_SLOTS:
        continue
    rel = n[len("Resources/"):-len(".InventoryItem")]
    # how many times is this item named anywhere other than its own file?
    hits = CORPUS.count(rel) - 1
    if hits <= 0:
        dn = re.search(r"Display Name=(.*)", t)
        unreachable.append((rel, slot.group(1), dn.group(1).strip() if dn else ""))
for rel, slot, dn in sorted(unreachable, key=lambda r: r[0]):
    print("   %-8s %-54s %s" % (slot, rel.split("/")[-1][:54], dn))
print()
print("%d equipment item(s) named by nothing" % len(unreachable))
