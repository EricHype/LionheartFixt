"""Survey the game's art for assets nothing references.

`docs/unused-content.md` surveys cut *script* content -- items, enemies, wands, skills,
perks, factions. It has never looked at art, and art orphans are a different shape: an
asset that exists, loads, and is named by nothing.

Three kinds come out of this, and they want different work:

  * **stranded** -- an item exists and uses generic art while art named for it sits unused.
    Wiring it is one field, and the art tells you it was meant to be there.
  * **complete but unowned** -- a full art set with no item at all. Needs an item authored
    around it, which is a design decision rather than a repair.
  * **nameless** -- art naming something with no other trace in the game. Evidence of cut
    content, and the write-up is the deliverable rather than a fix.

Usage: python tools/orphan_art.py
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import CR, zf, FX, read

TEXTY = (".inventoryitem", ".inventoryaddition", ".can", ".zax", ".dialogtree", ".txt",
         ".characterslottype", ".derivedcharacterattribute", ".skill", ".perk", ".race")

# ---------------------------------------------------------------- what exists
icons, pickups, meshes = set(), set(), set()
for n in zf.namelist():
    if n.startswith("Cache/Models/Items/Inventory Images/") and n.endswith(".mdl16"):
        icons.add(n[len("Cache/Models/"):-len(".mdl16")])
    elif n.startswith("Cache/Models/Items/PickUps/") and n.endswith(".mdl16"):
        pickups.add(n[len("Cache/Models/"):-len(".mdl16")])
    elif n.upper().endswith(".MODEL.GR2") and n.startswith("Resources/Models3D/"):
        meshes.add(n[len("Resources/"):-len(".MODEL.GR2")])

# ---------------------------------------------------------------- what is named
named = set()
leaf_named = set()

# Scan vanilla AND Fixt's own files. Reading vanilla alone answers "was this unused in
# 2003", which is the wrong question: Fixt has already wired some of it. The Clover icon
# looks orphaned in vanilla and is in use now, because the item the Port District bar
# patron hands over did not exist until Fixt authored it.
sources = [(n, lambda n=n: zf.read(n)) for n in zf.namelist()]
sources += [("Resources/" + p.relative_to(FX / "Resources").as_posix(), lambda p=p: p.read_bytes())
            for p in (FX / "Resources").rglob("*") if p.is_file()]
for n, getter in sources:
    if not n.lower().endswith(TEXTY):
        continue
    try:
        t = getter().decode("latin-1")
    except Exception:
        continue
    for m in re.findall(r"=\s*(Items/(?:Inventory Images|PickUps)/[^\r\n]+)", t):
        named.add(m.strip())
    for m in re.findall(r"=\s*(Models3D/[^\r\n]+)", t):
        named.add(m.strip())
    # a mesh can also be named by its leaf alone, through Override Names
    for m in re.findall(r"Character Slot Types/\w+=([^\r\n]+)", t):
        m = m.strip()
        if m and "/" not in m:
            leaf_named.add(m.lower())

# Composites register their meshes in a binary blob, by path, and EVERY character is a
# composite -- not just the two player ones. Reading only the player pair reported 265
# orphaned meshes including the bear, the deer and the assassin, which is how the
# mistake surfaced.
for n in set(zf.namelist()) | {"Cache/" + p.relative_to(FX / "Cache").as_posix()
                               for p in (FX / "Cache").rglob("*") if p.is_file()}:
    if not n.endswith(".mdl16"):
        continue
    blob = (FX / n).read_bytes() if (FX / n).exists() else zf.read(n)
    for m in re.findall(rb"Models3D/[ -~]{3,}", blob):
        s = m.decode("latin-1")
        # the trailing byte of a length-prefixed string can be printable, so also
        # register the path one character short
        named.add(s)
        named.add(s[:-1])


def orphans(have):
    out = []
    for a in sorted(have):
        if a in named:
            continue
        if a.split("/")[-1].lower() in leaf_named:
            continue
        out.append(a)
    return out


# ---------------------------------------------------------------- item side
items = {}
item_files = {n for n in zf.namelist() if n.lower().endswith(".inventoryitem")}
item_files |= {"Resources/" + p.relative_to(FX / "Resources").as_posix()
               for p in (FX / "Resources").rglob("*.InventoryItem")}
for n in sorted(item_files):
    t = read(n)  # Fixt's copy wins, which is the state that matters
    rel = n[len("Resources/"):-len(".InventoryItem")]
    art = {m.strip() for m in re.findall(r"=\s*(Items/Inventory Images/[^\r\n]+)", t)}
    items[rel] = art

shared = defaultdict(list)
for rel, art in items.items():
    for a in art:
        shared[a].append(rel)
generic = {a for a, who in shared.items() if len(who) > 1}


# A magic item's art is named `<base item> <addition display name>` -- "Bracers Defense"
# for Bracers plus the Protection addition, whose display name is Defense. Collect the
# pools so that pattern can be matched; comparing against item names alone misses it, and
# missing it is what let Bracers Defense look like art with no item behind it.
base_by_icon = {}
pool_names = {}
for rel, art in items.items():
    t = read("Resources/" + rel + ".InventoryItem")
    b = re.search(r"\tBasic=(.*)" + CR, t)
    g = re.search(r"Inventory Addition Group=(.*)" + CR, t)
    if b and g:
        base_by_icon.setdefault(b.group(1).strip().split("/")[-1], []).append(
            (rel, g.group(1).strip()))
for n, getter in sources:
    if not n.lower().endswith(".inventoryaddition"):
        continue
    t = getter().decode("latin-1")
    g = re.search(r"Inventory Addition Group=(.*)" + CR, t)
    dn = re.search(r"Display Name=(.*)" + CR, t)
    win = re.search(r"Inventory Window=(.*)" + CR, t)
    if g and dn:
        pool_names.setdefault(g.group(1).strip(), []).append(
            (dn.group(1).strip(), n[len("Resources/"):-len(".InventoryAddition")],
             win.group(1).strip() if win else "?"))


def stranded(orphan_icons):
    """Art named for something that exists and is wearing generic art instead.

    Two shapes: named for an ITEM, and named for a base item plus an ADDITION."""
    out = []
    for a in orphan_icons:
        leaf = a.split("/")[-1]
        words = [w for w in re.split(r"[^a-z]+", leaf.lower()) if len(w) > 3]
        for rel, art in items.items():
            nm = rel.split("/")[-1].lower()
            if words and all(w in nm for w in words) and art & generic:
                out.append((a, rel, sorted(art)[0]))
        for prefix, owners in base_by_icon.items():
            if not leaf.lower().startswith(prefix.lower() + " "):
                continue
            suffix = leaf[len(prefix):].strip().lower()
            for item_rel, grp in owners:
                for dn, add_rel, win in pool_names.get(grp, []):
                    if dn.lower() == suffix and win in ("!Unknown Model", "?"):
                        out.append((a, add_rel, "inherits " + prefix))
    return out


oi, op, om = orphans(icons), orphans(pickups), orphans(meshes)
print("icons   : %4d exist, %3d orphaned" % (len(icons), len(oi)))
print("pickups : %4d exist, %3d orphaned" % (len(pickups), len(op)))
print("meshes  : %4d exist, %3d orphaned" % (len(meshes), len(om)))
print()
print("== STRANDED: art named for an item that is using generic art")
for a, rel, using in stranded(oi):
    print("   %-52s -> %s" % (a.split("/")[-1], rel))
    print("   %-52s    currently uses %s" % ("", using.split("/")[-1]))
print()
for label, rows in (("orphaned icons", oi), ("orphaned pickups", op), ("orphaned meshes", om)):
    print("== %s (%d)" % (label, len(rows)))
    for a in rows:
        print("   ", a)
    print()
