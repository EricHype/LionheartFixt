"""Hrargrub talks instead of showing the attack cursor. Reported: "bhutu is in the back wandering around but my default
interaction is attack and he is not hostile".

0.31.0 pacified the heir at spawn and added a `GetCloseThenTalk` specifier for `1 the heir challenges you`, but a click
reads only an entity's first `CAIInteractionSpecifier` (`0x46b0f0`), and his monster can already carries
`GetCloseThenTriggerAndFight`. The report's quicksave shows exactly that: the fight specifier first, the talk one
sixth, `Valid Targets=` blank and `Category=Goblin`. So he could be neither talked to nor fought, and `BU5` could never
pass. The same trap 0.98.0 hit on the Crossroads standard.

  * The heir's generator `After Action` forgets the can's specifier before adding the talk one.
  * `70 combat`, the tree's only fight, now gives him back what the spawn took: `Player,Player Friend` targets, `Enemy`,
    and the fight specifier in place of the talk one, so he can be clicked to attack, then the two combat orders.

The spawn is a map edit: a `Ravine Cave East` not yet entered after Montserrat. The combat node is a tree: every save.
A rerun is a no-op.

    python tools/build_butu_heir_talks.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register
from build_crossroads_standard import forget_specifier, specifier

MAP = "Levels/Wilderness Maps/Ravine Cave East.zax"
TREE = "Resources/Levels/Wilderness/Dialog/Fixt Butu Heir.DialogTree"
HEIR = "Hrargrub"


def build_map():
    z = lhbuild.read(MAP)
    s = z.index("New Name=" + HEIR + CR)
    a = z.index("After Action=CMultipleActionsAction", s)
    e = lhbuild.balanced(z, a)
    body = z[a:e]
    if "CRemoveAIAction" in body:
        return []
    assert body.count("Item Count=3" + CR) == 1 and body.count("Action=CAddAIAction") == 1
    body = body.replace("Item Count=3" + CR, "Item Count=4" + CR)
    k = body.index("Action=CAddAIAction")
    line = body.rindex(CR, 0, k) + len(CR)
    body = body[:line] + "Action=" + B(*forget_specifier("$Instigator")) + body[line:]
    lhbuild.write_map(MAP, z[:a] + body + z[e:])
    return [MAP]


def build_tree():
    t = lhbuild.read(TREE)
    s = t.index("Node ID=70 combat" + CR)
    e = t.index("-" * 60, s)
    node = t[s:e]
    if "CRemoveAIAction" in node:
        return []
    assert node.count("Item Count=2" + CR) == 1
    hostile = [("CSetTargetTypeAction", [("Entity Name", HEIR), ("Name To Target", ""), ("Valid Targets", "Player,Player Friend")]),
               ("CAddCategoryAction", [("Target Name", HEIR), ("Categories to add", "Enemy")]),
               forget_specifier(HEIR),
               specifier(HEIR, "GetCloseThenTriggerAndFight", "")]
    k = node.index("Item Count=2" + CR) + len("Item Count=2" + CR)
    node = (node[:node.index("Item Count=2" + CR)] + "Item Count=" + str(2 + len(hostile)) + CR +
            "".join("Action=" + B(*h) for h in hostile) + node[k:])
    t = t[:s] + node + t[e:]
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    return [TREE]


def main():
    done = build_map() + build_tree()
    if done:
        register(done)
    print("butu heir talks:", done)


if __name__ == "__main__":
    main()
