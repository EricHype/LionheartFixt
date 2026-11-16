"""Death scripts give their rewards to the player, not to whoever landed the blow. Found from the 0.99.25 woodcutter report,
where Ernesto's kill put the eyes and liver in his inventory, and by the `killer-grants` gate (lhcheck A0.20) written for it.

In a destroyed script `$Instigator` is the killer. The proof is one save: Ernesto killed Felipe, the bare-`$instigator`
gives put both items in Ernesto's inventory, and `Woodcutter Dead`, written in the same script inside
`CForEachPlayerAction`, is on the player. Vanilla wraps `Relican Dead` the same way. So each site below is wrapped in
`CForEachPlayerAction`, which rebinds `$Instigator` to the player:

* **The four Titan stone hearts** (Titan Village): quest items, stranded on a companion like the eyes.
* **The Lava Troll Hide** (Troll Pit, Fixt 0.28.0): both drops, the troll's and the chief's.
* **The goblin kill counter.** Mongol Camp adds to the killer's counter, so a companion's kill does not count; Goblin
  Warrens already adds to `Player#1-9#` but reads the killer's, so a companion's twelfth kill never trips the check. Both
  now add to and read the player's, and the Goblin Slayer title and the Savage Heart step follow.
* **Felipe's -50 karma** (Woodcutter Forest): it already asked whether the killer was a player or a friend, and gave it to
  a companion when it was one.

The eyes and liver themselves are tools/build_woodcutter_fixes.py. All of these are maps, so each reaches a map not yet
entered, and new games.

A rerun is a no-op.

    python tools/build_killer_grants.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR
from build_shrine_repairs import register

COUNTER_ADD = "Derived character attribute to modify=Derived Character Attributes/Goblin Kill Counter" + CR
COUNTER_READ = "Character Attribute=Derived Character Attributes/Goblin Kill Counter" + CR
HEARTS = ["ThestoneheartofRhea", "Thestoneheart ofLethos", "ThestoneheartofMenoetius", "ThestoneheartofIapetus"]
SITES = {
    "Levels/3 Montaillou/Titan Village.zax": [("Inventory Item To Give=Inventory/Specific Item Cans/Quest Items/" + h + CR,
                                               "CActionGiveStandardInventoryItem", 1) for h in HEARTS],
    "Levels/Sewers/05 Troll Pit.zax": [("Inventory Item To Give=Inventory/Specific Item Cans/Quest Items/Lava Troll Hide" + CR,
                                        "CActionGiveStandardInventoryItem", 2)],
    "Levels/Wilderness Maps/Mongol Camp.zax": [(COUNTER_ADD, "CAddCharacterModifierToCharacterAction", 3),
                                               (COUNTER_READ, "CIfAction", 3)],
    "Levels/Wilderness Maps/Goblin Warrens.zax": [(COUNTER_READ, "CIfAction", 3)],
    "Levels/Wilderness Maps/Woodcutter Forest.zax": [("Category to check for=Player,Player Friend" + CR, "CIfAction", 1)],
}


def line_start(z, i):
    return z.rindex(CR, 0, i) + len(CR)


def is_wrapped(z, s):
    """The action at s is the Action= of a CForEachPlayerAction: the line two above names it."""
    a = line_start(z, line_start(z, s) - len(CR))   # the brace line
    b = line_start(z, a - len(CR))          # the line before it
    return z[b:a].strip().endswith("=CForEachPlayerAction")


def wrap(z, s):
    """Wrap the Key=CClass{...} block whose key starts at s (after its tabs) in CForEachPlayerAction."""
    e = lhbuild.balanced(z, s)
    key, value = z[s:e].split("=", 1)
    value = re.sub(r"\r\n\t*", CR, value)
    return z[:s] + key + "=CForEachPlayerAction" + CR + "{" + CR + "Action=" + value + CR + "}" + z[e:]


def build(rel, sites):
    z = lhbuild.read(rel)
    n = 0
    for anchor, cls, count in sites:
        assert z.count(anchor) == count, (rel, anchor, z.count(anchor))
        for k in range(count):
            # re-find each time, since every wrap moves the text after it
            pos = [m.start() for m in re.finditer(re.escape(anchor), z)][k]
            c = z.rindex("=" + cls + CR, 0, pos)
            s = line_start(z, c)
            s += len(z[s:c]) - len(z[s:c].lstrip("\t"))
            if is_wrapped(z, s):
                continue
            z = wrap(z, s)
            n += 1
    if n:
        lhbuild.write_map(rel, z)
        register([rel])
    return n


PERK_GIVE = re.compile(r"Character to give perk to=\$instigator\r\n", re.I)


def next_title(z):
    """The first death-script title grant still on the killer: the start of what to wrap, or None. That is the
    CConditionalAction or CIfAction around it when it asks the same character first (vanilla's "if he lacks it, give it"), else the
    give itself."""
    for d in re.finditer(r"New Destroyed Action=", z):
        end = lhbuild.balanced(z, d.start())
        for g in PERK_GIVE.finditer(z, d.start(), end):
            c = z.rindex("=CGiveCharacterPerkAction" + CR, d.start(), g.start())
            s = line_start(z, c)
            s += len(z[s:c]) - len(z[s:c].lstrip("\t"))
            k = max(z.rfind("=CConditionalAction" + CR, d.start(), s), z.rfind("=CIfAction" + CR, d.start(), s))
            if k >= 0:
                ks = line_start(z, k)
                ks += len(z[ks:k]) - len(z[ks:k].lstrip("\t"))
                block = z[ks:lhbuild.balanced(z, ks)]
                if g.group(0) in block and re.search(r"Character to get attributes from=\$instigator", block, re.I):
                    s = ks
            if not inside_for_each(z, d.start(), s):
                return s
    return None


def inside_for_each(z, lo, s):
    for f in re.finditer(r"=CForEachPlayerAction\r\n", z[lo:s]):
        fs = line_start(z, lo + f.start())
        fs += len(z[fs:lo + f.start()]) - len(z[fs:lo + f.start()].lstrip("\t"))
        if lhbuild.balanced(z, fs) > s:
            return True
    return False


def build_titles():
    n = {}
    for p in sorted((lhbuild.FX / "Levels").rglob("*.zax")):
        rel = str(p.relative_to(lhbuild.FX)).replace("\\", "/")
        z = lhbuild.read(rel)
        if not PERK_GIVE.search(z):
            continue
        k = 0
        while True:
            s = next_title(z)
            if s is None:
                break
            z = wrap(z, s)
            k += 1
        if k:
            lhbuild.write_map(rel, z)
            register([rel])
            n[p.stem] = k
    return n


def main():
    print(" | ".join("%s: %d" % (Path(r).stem, build(r, s)) for r, s in SITES.items()))
    print("titles:", build_titles())


if __name__ == "__main__":
    main()
