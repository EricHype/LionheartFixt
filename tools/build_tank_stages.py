"""DaVinci's siege tank describes the state it is in. Requested after 0.99.15.

The tank's description is `1 Siege Tank` in `Leonardo DaVinci Invention`, opened on proximity by two specifiers in
`Davinci Secret Chamber`: one on the tank itself (radius 200, the entity has no name) and one on `siege tank ai poly`
(radius 70). It said "Once completed..." for ever, so fitting the gear changed nothing you could see, and the spirit gem,
which DaVinci fits offscreen, never showed at all. Now there are three stages, read when the description opens:

- neither quest done: vanilla's `1 Siege Tank`
- the gear quest done: `4 Fixt the ring seated`, everything that moves is ready and nothing drives it
- the gear and the spirit gem quests done: `5 Fixt the tank awake`, DaVinci has finished it

Two routes, because the chamber is frozen into a save on its first visit:

1. **The map** (a save that has not entered the chamber): both openers read the quests before choosing a node.
2. **The fitting reply** (any save): fitting the gear at the tank swaps the opener that showed it (`$Trigger`, which is the
   tank when its wider radius caught you first, as it usually does) and the named poly for openers that read the quests.
   A gear fitted before this release, or by DaVinci in his scene, keeps the old description in a chamber already visited:
   his reply cannot reach a tank with no name.

A rerun is a no-op.

    python tools/build_tank_stages.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH, if_action, balanced
from build_shrine_druids import parts
from build_shrine_repairs import register

MAP = "Levels/1 Barcelona/Davinci Secret Chamber.zax"
TREE = "Resources/Levels/1 Barcelona/Dialog/Gate District/Leonardo DaVinci Invention.DialogTree"
TREE_REF = "Levels/1 Barcelona/Dialog/Gate District/Leonardo DaVinci Invention"
Q = "Levels/1 Barcelona/Quests/Gate District/"
GEAR = Q + "Create Mechanical Gears for DaVinci's Siege Tank"
GEM = "Levels/3 Montaillou/Quests/Obtain the spirit gem for DaVinci's siege machine"
POLY = "siege tank ai poly"
# a tree that names its own file in an action hangs the loader, so the swap the fitting reply runs lives in a canned object
SWAP_CAN = "Common Objects and Scripts/Fixt Tank Stages Swap"
SEATED = "4 Fixt the ring seated"
AWAKE = "5 Fixt the tank awake"
NODES = [
    (SEATED, "The turret ring is seated now, and the turret turns a hand's breadth under your palm before it stops. Every part of this "
             "machine that should move is ready to. All it lacks is something to drive it."),
    (AWAKE, "Something inside the hull is awake. The turret follows you across the room, and the great wheels sit with the stillness "
            "of a thing that has decided not to move yet. DaVinci has finished it."),
]


def done(quest):
    return ("CIsQuestCompletedAction", [("Quest", quest)])


def show(node):
    return ("CDisplayDialogTreeAction", [("Dialog Tree File", TREE_REF), ("Node ID", node), ("Speaker", "$trigger"),
                                         ("Player Being Spoken To", "$Instigator")])


def staged(original):
    """The description the tank's state calls for; `original` is vanilla's opener, kept verbatim for the first stage."""
    return if_action(done(GEAR), if_action(done(GEM), show(AWAKE), show(SEATED)), original)


def opener(radius):
    return ("CAIInteractionSpecifier", [("Marked For Deletion", "0"), ("Publisher", ""), ("Trigger Only Once", "0"), ("Was Triggered", "0"),
                                        ("Auto-Flip Switch", "1"), ("Trigge Must Have HP", "0"), ("Triggered By Anything", "0"),
                                        ("Triggered By Players", "1"), ("Triggered By Player Friends", "0"), ("Triggered By Enemies", "0"),
                                        ("Triggered By Projectiles", "0"), ("Triggered By Companions", "0"), ("Triggered By Name", ""),
                                        ("Interaction Description", ""), ("Interaction Type", "Interaction Specifiers/GetCloseThenTrigger"),
                                        ("Action", if_action(done(GEM), show(AWAKE), show(SEATED))),
                                        ("X Radius", radius), ("Attacker Range Modifier", "0"), ("YX Ratio", "0.712766"), ("Highlight Self Time", "0"),
                                        ("Highlight Until Clicked", "0"), ("Is Locked", "0"), ("Allow Interact If Has Target", "1"),
                                        ("Lock Pick Adjustment", "0"), ("Inventory item to use as key", "Inventory Items/!None"), ("Is Bussy Talking", "0")])


def swap(target, radius):
    return [("CRemoveAIAction", [("Target Name", target), ("AI", "CAIInteractionSpecifier"), ("Delay Between Removes", "0")]),
            ("CAddAIAction", [("Target Name", target), ("AI", opener(radius)), ("Delay Between Adds", "0")])]


def build_tree():
    t = lhbuild.read(TREE)
    if "Node ID=" + SEATED + CR in t:
        return 0
    assert t.count("\n") == t.count(CR)
    blocks = t.split(DASH)
    k = [n for n, b in enumerate(blocks) if "Node ID=3 Fixt the empty shaft" + CR in b]
    assert len(k) == 1
    b = blocks[k[0]]
    fit = b.index("Reply Text=(fit the rotary gear into the turret ring)")
    ca = b.index("Custom Action=CMultipleActionsAction", fit)
    m = re.compile(r"Item Count=(\d+)\r\n").search(b, ca)
    add = [("CUseCannedActionAction", [("Canned Object", SWAP_CAN)])]
    blocks[k[0]] = b[:m.start()] + "Item Count=" + str(int(m.group(1)) + len(add)) + CR + "".join("Action=" + B(*a) for a in add) + b[m.end():]
    t2 = DASH.join(blocks)
    nodes = [lhbuild.node(nid, text, []) for nid, text in NODES]
    assert t2.endswith("}" + CR)
    t2 = t2[:-len("}" + CR)] + CR + DASH + CR + (CR + DASH + CR).join(nodes) + "}" + CR
    assert t2.count("\n") == t2.count(CR)
    (lhbuild.FX / TREE).write_bytes(t2.encode("latin-1"))
    register([TREE])
    return 1


def build_swap_can():
    rel = "Resources/" + SWAP_CAN + ".can"
    if (lhbuild.FX / rel).exists():
        return 0
    obj = ("CMultipleActionsAction", [("Action", ("Array", [("Item Count", "4")] + [("Action", a) for a in swap("$Trigger", "200") + swap(POLY, "70")]))])
    lhbuild.write_map(rel, B("CCannedObject", [("Object", obj)]))
    register([rel])
    return 1


def build_map():
    z = lhbuild.read(MAP)
    if "Node ID=" + SEATED + CR in z:
        return 0
    n = 0
    for p in parts(z):
        if "Node ID=1 Siege Tank" + CR not in p:
            continue
        i = p.index("Node ID=1 Siege Tank" + CR)
        s = p.rindex("CDisplayDialogTreeAction", 0, i)
        e = balanced(p, s)
        q = p[:s] + B(*staged(("RAW", []))).rstrip() + p[e:]
        q = q.replace("RAW" + CR + "{" + CR + "}", p[s:e], 1)
        assert p[s:e] in q and "Node ID=" + SEATED in q
        z = z.replace(p, q, 1)
        n += 1
    assert n == 2, n
    lhbuild.write_map(MAP, z)
    register([MAP])
    return n


def main():
    print("swap:", build_swap_can(), "| tree:", build_tree(), "| map openers:", build_map())


if __name__ == "__main__":
    main()
