"""Butu's warriors watch instead of attacking, so the heir can be reached and talked to. Reported after the arrival fix:
"bhutu's goblins are there at the start, which is good, but they are hostile. Didn't we plan them talking to me?"

0.31.0 spawned the eight Butu posts as ordinary hostile goblins and stood them down only after the poetry book (`BU17`),
but Hrargrub waits at the far end with every post between him and the door, so the talk route meant killing his tribe
first. His own line describes something else: *"The red ones will watch you to the door, and if you come back in
through it with a blade out, they will not."*

  * **Every Butu post spawns watchful** (unless the tribe has already turned): targets blanked, `Enemy` removed, the
    can's fight specifier swapped for a talk one that says one of four short lines pointing at the heir, and the damaged
    script set to `Fixt Butu warriors turn`, as the Mongol Camp and the Khan's goblins here do.
  * **`Fixt Butu warriors turn`** (once): lights `Fixt Butu warriors turned`, restores `Player,Player Friend` and `Enemy`
    on `Butu Warriors` and gives them back the fight specifier, and does the same for Hrargrub.
  * **The heir's fight** (`70 combat`) fires that relay before its two combat orders, so choosing the fight turns the
    whole tribe.
  * The book's `Butu alliance` is unchanged: the tribe stays peaceful, and still turns if struck.

The posts are a map edit: a `Ravine Cave East` not yet entered. The tree and the line bank reach every save. A rerun is
a no-op.

    python tools/build_butu_warriors_watch.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, relay, activate, if_action, multi, balloon
from build_shrine_repairs import register
from build_crossroads_standard import forget_specifier, specifier

MAP = "Levels/Wilderness Maps/Ravine Cave East.zax"
HEIR_TREE = "Resources/Levels/Wilderness/Dialog/Fixt Butu Heir.DialogTree"
LINES_PATH = "Levels/Wilderness/Dialog/Fixt Butu Warrior Lines"
LINES_TREE = "Resources/" + LINES_PATH + ".DialogTree"
WARRIORS = "Butu Warriors"
HEIR = "Hrargrub"
TURN = "Fixt Butu warriors turn"
TURNED = "Fixt Butu warriors turned"
LINES = {
    "1 watch": "The heir is at the back. Walk slowly, smooth thing.",
    "2 watch": "<The goblin does not lower its spear.> Hrargrub will see you. We will watch you see him.",
    "3 watch": "Butu's line does not bite first. Remember that we said so.",
    "4 watch": "Keep your blade low. The heir talks at the back of the cave, and we listen.",
}
for v in LINES.values():
    assert "—" not in v and "--" not in v and v.count("<") <= 1


def hostile(name):
    return [("CSetTargetTypeAction", [("Entity Name", name), ("Name To Target", ""), ("Valid Targets", "Player,Player Friend")]),
            ("CAddCategoryAction", [("Target Name", name), ("Categories to add", "Enemy")]),
            forget_specifier(name),
            specifier(name, "GetCloseThenTriggerAndFight", "")]


TALK = ("CRandomAction", [("Action", ("Array", [("Item Count", str(len(LINES)))] +
                                     [("Action", balloon(LINES_PATH, n, "$trigger", "-80")) for n in LINES]))])
WATCH = if_action(("CNotAction", [("Action", ("CCheckExistenceAction", [("Name To Check For", TURNED), ("Desired Minimum Count", "1")]))]),
                  multi([("CSetTargetTypeAction", [("Entity Name", "$Instigator"), ("Name To Target", ""), ("Valid Targets", "")]),
                         ("CRemoveCategoryAction", [("Target Name", "$Instigator"), ("Categories To Remove", "Enemy")]),
                         forget_specifier("$Instigator"),
                         specifier("$Instigator", "GetCloseThenTalk", TALK),
                         ("CSetDamagedScriptActionAction", [("New Damaged Action", relay(TURN)), ("Target Name", "$Instigator")])]))
TURN_ACTION = multi([activate(TURNED)] + hostile(WARRIORS) + hostile(HEIR))


def build_lines():
    if (lhbuild.FX / LINES_TREE).exists():
        return []
    t = lhbuild.tree("Fixt Butu Warrior Lines", [lhbuild.node(n, x, []) for n, x in LINES.items()])
    (lhbuild.FX / LINES_TREE).write_bytes(t.encode("latin-1"))
    return [LINES_TREE]


def build_map():
    z = lhbuild.read(MAP)
    if "Name=" + TURN + CR in z:
        return []
    n = 0
    for k in range(1, 9):
        s = z.index("\t\t\tName=Butu Post " + str(k) + CR)
        e = lhbuild.balanced(z, z.rindex("Level Part=", 0, s))
        p = z[s:e]
        assert p.count("New Name=" + WARRIORS + CR) == 1 and p.count("After Action=" + CR) == 1, k
        p = p.replace("After Action=" + CR, "After Action=" + B(*WATCH))
        z = z[:s] + p + z[e:]
        n += 1
    z = lhbuild.add_parts(z, [lhbuild.checker(TURNED, 2280, 760), lhbuild.relay_part(TURN, TURN_ACTION, 2300, 760)])
    lhbuild.write_map(MAP, z)
    return [MAP]


def build_heir_tree():
    t = lhbuild.read(HEIR_TREE)
    s = t.index("Node ID=70 combat" + CR)
    e = t.index("-" * 60, s)
    node = t[s:e]
    if "Relay Name=" + TURN in node:
        return []
    m = re.search(r"Item Count=(\d+)\r\n", node)
    node = node[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + "Action=" + B(*relay(TURN)) + node[m.end():]
    t = t[:s] + node + t[e:]
    (lhbuild.FX / HEIR_TREE).write_bytes(t.encode("latin-1"))
    return [HEIR_TREE]


def main():
    done = build_lines() + build_map() + build_heir_tree()
    if done:
        register(done)
    print("butu warriors watch:", done)


if __name__ == "__main__":
    main()
