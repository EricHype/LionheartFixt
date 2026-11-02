"""Prove that pre-0.89.0 saves keep their magic weapons, without replaying them.

A save stores the additions on an item **by resource path**. 0.89.0 moves the 29 melee
additions into different addition *groups* and adds 234 per-base copies, but it deliberately
does not delete or rename any original -- precisely so that these references keep resolving.

That makes `WM9` checkable rather than only playable. For every save on disk this collects
the addition paths it actually names, then asserts each one still exists in the built
`data.dat`. A path a save names that the build no longer carries is a magic weapon that
loses its enchantment, and this is what would catch it.

What it cannot do is prove the engine agrees, so WM9 still wants one look in play. It can
tell you *which save to load* and what should be on the weapon when you get there.

Usage: python tools/check_save_additions.py
"""
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import savecheck

GAME = Path(r"C:\Program Files (x86)\GOG Galaxy\Games\Lionheart - Legacy of the Crusader")
SAVES = GAME / "SaveGames"
MELEE_DIR = "Inventory/Inventory Additions/Weapons/"
REF = re.compile(r"(Inventory/Inventory Additions/[^\r\n\"=]+)")

with zipfile.ZipFile(GAME / "data.dat") as z:
    built = {n[len("Resources/"):-len(".InventoryAddition")]
             for n in z.namelist() if n.lower().endswith(".inventoryaddition")}

# The melee additions sitting directly under Weapons/, derived from the build rather
# than hardcoded. A superset of the 29 the release moved between groups, excluding
# the per-base copies and the ammunition and missile subfolders. These are the paths
# whose disappearance would be a regression caused by 0.89.0.
OWNED = {r for r in built
         if r.startswith(MELEE_DIR)
         and "/" not in r[len(MELEE_DIR):]}
print("additions in the built data.dat: %d  (%d of them melee weapon additions)"
      % (len(built), len(OWNED)))
print()

rows, missing = [], {}
for p in sorted(SAVES.glob("*.sav")):
    try:
        texts, env = savecheck.load(p)
    except Exception as exc:
        print("   skip %-34s %r" % (p.name, exc))
        continue
    refs = set()
    for t in [env] + texts:
        if t:
            refs |= {m.strip() for m in REF.findall(t)}
    melee = sorted(r for r in refs if r in OWNED)
    gone = sorted(r for r in refs if r not in built)
    for g in gone:
        missing.setdefault(g, []).append(p.name)
    rows.append((p.name, len(refs), melee, gone))

print("%-36s %5s %5s  %s" % ("save", "refs", "gone", "melee weapon additions it names"))
for name, n, melee, gone in rows:
    if not n:
        continue
    print("   %-33s %5d %5d  %s" % (
        name, n, len(gone),
        ", ".join(m.split("/")[-1] for m in melee[:5]) + (" ..." if len(melee) > 5 else "")))

OWNED_NAMES = OWNED
print()
withmelee = [r for r in rows if r[2]]
print("%d of %d saves name at least one melee weapon addition" % (len(withmelee), len(rows)))
if withmelee:
    best = max(withmelee, key=lambda r: len(r[2]))
    print()
    print("Best save to load for WM9: %s" % best[0])
    print("   it names %d melee addition(s):" % len(best[2]))
    for m in best[2]:
        print("      %s" % m)
    print("   every one of those should still be on its weapon, with its effect intact.")

print()
regressions = {r: s for r, s in missing.items() if r in OWNED_NAMES}
foreign = {r: s for r, s in missing.items() if r not in OWNED_NAMES}
if foreign:
    print("absent, but not this release's doing -- these came from other mods that were")
    print("installed when the save was made and are not enabled now:")
    for ref, saves in sorted(foreign.items()):
        print("   %-56s %s" % (ref.split("/")[-1], ", ".join(saves[:3])))
    print()
if regressions:
    print("FAIL -- 0.89.0 dropped a melee addition that saves reference:")
    for ref, saves in sorted(regressions.items()):
        print("   %-56s %s" % (ref, ", ".join(saves[:4])))
    sys.exit(1)
print("all %d melee addition paths survive in the build, and no save references one" % len(OWNED))
print("that 0.89.0 removed -- so nothing an old magic weapon points at has gone missing")
