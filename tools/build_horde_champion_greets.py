"""The Horde greets its Champion, shamans included. Reported on the Plains as the Khan's Champion: "my interaction cursor
with them was attack, and only the shamans were hostile. Given I'm the Kahn's champion, how should they treat me?"

Two faults in the Champion's stand-aside, which `tools/build_khan_heart.py` runs from each band generator's `After Action`
on the goblin it has just made:

  * **The shamans were never in it.** `build_carryovers.py` named the bands from generators of `Mongol Goblin` cans and
    skipped any with a shaman in it, from the call that shamans do not lead bands. The stand-aside rode on those names, so
    the shaman generators (three on the Plains, `Goblin Shaman near lake left` on the Lake) were left out and attack.
    Not leading a band is no reason to attack the Khan's Champion. They now get the same `After Action` as the bands: the
    Champion's stand-aside, or the Khan-slain slowdown.
  * **Standing aside kept the fight click.** It blanked the goblin's targets and removed `Enemy`, but a click reads the
    first specifier (0x46b0f0), and every goblin can's is a fight one, so the cursor was the sword and a click started a
    fight. The stand-aside now forgets that specifier and adds a talk one, as the English deserters do
    (`build_carryovers.py`), and the click shows one of their lines over the goblin:

      - "<The spear comes up, then all the way down.> Champion. Walk where you like."
      - "The Khan's Champion! Nobody touch it. Nobody even look hungry."
      - "<A bow, low and quick.> Good hunting, Champion. Leave us the small ones."
      - shamans: "The frogs croaked that you would come this way, Champion."

    The register is the Warrens villager's own Champion greeting, *"Forgive it, Champion..."*.

Map edits, so wilderness maps not yet entered, and new games. Run after `build_khan_heart.py`. A rerun is a no-op.

    python tools/build_horde_champion_greets.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, balanced, balloon, if_action, multi
from build_shrine_repairs import register
from build_carryovers import BANDS
from build_crossroads_standard import forget_specifier, specifier
from build_khan_heart import TAG, ME, champion, on_spawn

TREE = "Levels/Wilderness/Dialog/Fixt Horde Champion"
TREE_REL = "Resources/" + TREE + ".DialogTree"
GOBLIN = [("1 walk", "<The spear comes up, then all the way down.> Champion. Walk where you like."),
          ("2 hungry", "The Khan's Champion! Nobody touch it. Nobody even look hungry."),
          ("3 hunting", "<A bow, low and quick.> Good hunting, Champion. Leave us the small ones.")]
SHAMAN = [("10 frogs", "The frogs croaked that you would come this way, Champion.")]
for _, x in GOBLIN + SHAMAN:
    assert "—" not in x and "--" not in x
DONE_MARK = "Dialog Tree File=" + TREE + CR


def talk(lines):
    if len(lines) == 1:
        return balloon(TREE, lines[0][0], "$trigger", "-80")
    return ("CRandomAction", [("Action", ("Array", [("Item Count", str(len(lines)))] +
                                          [("Action", balloon(TREE, n, "$trigger", "-80")) for n, _ in lines]))])


def greets(lines):
    """The two actions the stand-aside gains: the fight click out, a talk click in."""
    return [forget_specifier(ME), specifier(ME, "GetCloseThenTalk", talk(lines))]


def build_tree():
    p = lhbuild.FX / TREE_REL
    if p.exists():
        return []
    t = "CDialogTree" + CR + "{" + CR + "Name=Horde Goblin" + CR + "Portrait=!None" + CR + "Should Have Voiceovers=0" + CR + "Default Canceled Node Action=" + CR
    for n, x in GOBLIN + SHAMAN:
        t += "-" * 60 + CR + lhbuild.node(n, x, [])
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes((t + "}" + CR).encode("latin-1"))
    return [TREE_REL]


def parts(z):
    return re.findall(r"(?ms)^\t\tLevel Part=\w+\r\n\t\t\{\r\n.*?^\t\t\}", z)


def with_greeting(part):
    """A band generator's stand-aside, `CSetTargetTypeAction` and `CRemoveCategoryAction` on $Instigator in a
    two-item array, gains the two greeting actions after them."""
    hits = [m.start() for m in re.finditer(r"Action=CSetTargetTypeAction\r\n\t*\{\r\n\t*Entity Name=\$Instigator\r\n", part)]
    assert len(hits) == 1, len(hits)
    i = hits[0]
    c = part.rindex("Item Count=2" + CR, 0, i)
    assert part[c + len("Item Count=2"):i].strip() == "", part[c:i]
    r = part.index("Action=CRemoveCategoryAction" + CR, i)
    assert "Categories To Remove=Enemy" in part[r:r + 300]
    e = balanced(part, r)
    extra = "".join(CR + "Action=" + B(*a).rstrip(CR) for a in greets(GOBLIN))
    out = part[:e] + extra + part[e:]
    return out[:c] + "Item Count=4" + out[c + len("Item Count=2"):]


def shaman_spawn():
    base = on_spawn()
    assert base[0] == "CIfAction" and base[1][2][0] == "Else"
    aside = [("CSetTargetTypeAction", [("Entity Name", ME), ("Name To Target", ""), ("Valid Targets", "")]),
             ("CRemoveCategoryAction", [("Target Name", ME), ("Categories To Remove", "Enemy")])]
    return if_action(champion(), multi(aside + greets(SHAMAN)), base[1][2][1])


def build_map(m):
    rel = "Levels/Wilderness Maps/" + m + ".zax"
    z = lhbuild.read(rel)
    if DONE_MARK in z:
        return 0, 0
    bands = shamans = 0
    for p in parts(z):
        if "CGeneratorAI" not in p:
            continue
        ents = [e for e in re.findall(r"Entity=([^\r\n]*)", p) if e]
        if "Modifier Description=" + TAG + CR in p:
            new = with_greeting(p)
            bands += 1
        elif ents and all(e.startswith("Monster Cans/Mongol Goblin Shaman") for e in ents) and re.search(r"(?m)^\t\t\tActive=1\r", p):
            a = re.search(r"(?m)^\t*After Action=\r\n", p)
            assert a, "a shaman generator with its own After Action"
            new = p[:a.start()] + "After Action=" + B(*shaman_spawn()) + p[a.end():]
            shamans += 1
        else:
            continue
        assert z.count(p) == 1
        z = z.replace(p, new)
    assert bands >= 4, (m, bands)
    lhbuild.write_map(rel, z)
    register([rel])
    return bands, shamans


def main():
    done = build_tree()
    if done:
        register(done)
    for m in BANDS:
        print(m, "band generators, shaman generators:", build_map(m))


if __name__ == "__main__":
    main()
