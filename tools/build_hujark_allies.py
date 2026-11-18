"""Allied Hujark are allies, not enemies standing still. Issue #15: "When siding with the Hurjak they are still targetable
and treated as an enemy (without having to press the force attack setting) thus making it difficult to not kill them
when throwing AOE spells or fighting in general, they should be the same as the ogres, talkable and targetable only
when force attack option is selected."

`build_hujark_war.py` (0.17.0, reworked 0.97.3) stands the Hujark down on the allied and safe-conduct routes by
retargeting them, `Valid Targets=Scripted Custom 2`, and nothing else. Two things left them enemies:

  * they kept `Category=Enemy`, so area spells and companions treat them as targets;
  * their click is `GetCloseThenTriggerAndFight`, whose type has `Fight When Close=1`: a plain click attacks.

The allied ogres in the same act do both halves. Their spawn drops `Enemy` (`CRemoveCategoryAction`), and their click
is a talk type. `GetCloseThenTalk` has `Fight When Close=0` and `Fight When Attack Is Forced=1`, so a click talks and
force attack (K) still fights. Fixt's 0.98.0 Crossroads soldiers use the same pair.

So every stand-down now also drops `Enemy` and swaps the click to `GetCloseThenTalk`, whose action is a random battle
cry from vanilla's `HujarkWarriorCanned`. Lines `10 Never`, `20`, `30`, `50` and `70` fit allies fighting the English;
`40` ("you have spilled Hujark blood") and the others do not, and are left out. That covers both stand-down sites:

  * the spawn template's Succeed branch (`$Instigator`), which every Hujark generator on these maps runs;
  * the by-name retargets on `Player sides with the Hujark`, `Player buys safe passage`, `Activate English generators`
    and `Passage granted`, for Hujark already standing when the player allies.

Revoking passage undoes it. Force-attacking an ally still fires the existing damage script, which triggers `Passage
revoked`, and `Passage revoked here` on all ten maps now gives every Hujark `Enemy` and the fight click back, the
pattern of vanilla's `Player attacks any of the Hujark in this fight`. That leaves them exactly as a revoke left them
before this release.

A map edit, so it reaches act 5 maps not yet entered. A rerun is a no-op.

    python tools/build_hujark_allies.py
"""
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX
from build_hujark_war import NAMES, FLAG

D = "Levels/5 Nostrodomus/"
TREE = "Levels/5 Nostrodomus/Dialog/HujarkWarriorCanned"
CRIES = ["10 Never", "20", "30", "50", "70"]
SHOUT = ("CRandomAction", [("Action", ("Array", [("Item Count", str(len(CRIES)))] +
                                       [("Action", lhbuild.balloon(TREE, n, "$trigger", "-80")) for n in CRIES]))])
TALK = lhbuild.specifier("GetCloseThenTalk", SHOUT, radius="80")
FIGHT = lhbuild.specifier("GetCloseThenTriggerAndFight", "", radius="80")
MARK = "Interaction Type=Interaction Specifiers/GetCloseThenTalk" + CR
STAND = re.compile(r"Name To Check For=" + re.escape(FLAG) + r"\r\n\t*Desired Minimum Count=1\r\n\t*\}\r\n\t*Succeed Action=")


def ally(target):
    return [("CRemoveCategoryAction", [("Target Name", target), ("Categories To Remove", "Enemy")])] + \
        lhbuild.swap_specifier(target, TALK)


def foe(target):
    return [("CAddCategoryAction", [("Target Name", target), ("Categories to add", "Enemy")])] + \
        lhbuild.swap_specifier(target, FIGHT)


def block(tup):
    return B(*tup).rstrip(CR)


def wrapped(old, extra):
    """`old` (a block's text) and the extra actions, as one CMultipleActionsAction, so no outer count changes."""
    items = [old] + [block(t) for t in extra]
    return ("CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=" + str(len(items)) +
            CR + "".join("Action=" + a + CR for a in items) + "}" + CR + "}")


def swap_retargets(z, find_start):
    """Wrap every CSetTargetTypeAction that find_start locates, once. Returns (text, count)."""
    n, k = 0, 0
    while True:
        s = find_start(z, k)
        if s is None:
            break
        e = lhbuild.balanced(z, s)
        old = z[s:e]
        assert old.startswith("CSetTargetTypeAction"), old[:60]
        assert "Valid Targets=Scripted Custom 2" + CR in old, old
        # already wrapped: the retarget is the first item of a multi whose next item drops Enemy
        if "Categories To Remove=Enemy" + CR in z[e:e + 300]:
            k = e
            continue
        target = re.search(r"Entity Name=([^\r]*)\r", old).group(1)
        new = wrapped(old, ally(target))
        z = z[:s] + new + z[e:]
        k = s + len(new)
        n += 1
    return z, n


def spawn_start(z, k):
    m = STAND.search(z, k)
    while m and not z.startswith("CSetTargetTypeAction", m.end()):
        # a site this builder already wrapped: Succeed is now the multi; skip past it
        m = STAND.search(z, m.end())
    return m.end() if m else None


def name_start(z, k):
    i = z.find("Entity Name=" + NAMES + CR, k)
    return z.rindex("CSetTargetTypeAction", 0, i) if i >= 0 else None


def spawn_sites(z):
    """The template: Succeed=CSetTargetTypeAction{$Instigator, Scripted Custom 2} gains the ally swap."""
    return swap_retargets(z, spawn_start)


def name_sites(z):
    """The by-name retargets, CSetTargetTypeAction{Entity Name=NAMES}, gain the ally swap by the same names."""
    return swap_retargets(z, name_start)


def revoke(z):
    i = z.find("\t\t\tName=Passage revoked here" + CR)
    if i < 0:
        return z, 0
    s = z.rindex("Level Part=", 0, i)
    part = z[s:lhbuild.balanced(z, s)]
    if "Categories to add=Enemy" + CR in part:
        return z, 0
    from build_shrine_repairs import into_relay
    extra = "".join("Action=" + B(*t) for t in foe(NAMES))
    return into_relay(z, "Passage revoked here", extra, 3), 1


def main():
    total = {"spawn": 0, "names": 0, "revoke": 0}
    for f in sorted(os.listdir(FX / D)):
        if not f.endswith(".zax"):
            continue
        z0 = lhbuild.read(D + f)
        z, a = spawn_sites(z0)
        z, b = name_sites(z)
        z, c = revoke(z)
        if z != z0:
            lhbuild.write_map(D + f, z)
        total["spawn"] += a
        total["names"] += b
        total["revoke"] += c
        if a or b or c:
            print("  %s: %d spawn, %d by name, %d revoke" % (f, a, b, c))
    print("hujark allies:", total)


if __name__ == "__main__":
    main()
