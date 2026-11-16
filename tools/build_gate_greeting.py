"""The Mongol Camp gate greets a goblin friend once, not every time you walk past. Reported from play after 0.99.25: "we
get challenged by the goblins guards again when exiting the level to the cave".

0.9.1 (1f2f9f9) gave the camp's entrance polygon a branch for a player the guards let through: with `welcomed at the gate`
on, crossing it opens `3 Return Dialogue`, *"Greetings goblin friend. What do you want?"*. The polygon retriggers and lies
across the path between the camp and the Warrens, so the greeting stopped the party on every crossing, both ways.

Now both of node 3's peaceful replies (the plain exit and the Speech audience with the Khan) switch `welcomed at the gate`
off. The polygon then takes its existing third branch, the challenge already given, which is vanilla's silence. The fight
replies are unchanged: they turn the camp hostile. The tree reaches every save, and `welcomed at the gate` exists in any
Mongol Camp entered since 0.9.1.

A rerun is a no-op.

    python tools/build_gate_greeting.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register
from build_troll_choices import node_span

TREE = "Resources/Levels/Wilderness/Dialog/GoblinEntranceGuard.DialogTree"
NODE = "3 Return Dialogue"
WELCOME = "welcomed at the gate"
EXIT = "Reply Text=Nothing today. I will be on my way." + CR + "Go to node ID=" + CR
AUDIENCE = ("Reply Text=I have come to seek an audience with your great leader." + CR + "Go to node ID=30 khan" + CR
            + "Action work in progress=(speech 40)" + CR)


DARSH = "Reply Text=I have come to find Inquisitor Darsh." + CR + "Go to node ID=10 darsh" + CR
DARSH_NODE = "11 darsh friend"
DARSH_TEXT = "<The guard shrugs.> The priest? He sits in our pens. The shaman Rakeb set his price. Take it up with Rakeb, friend, not with me."


def build_darsh():
    """Node 3's Darsh reply opened `10 darsh`, the challenge's *"you may join him...In our slave pens!"*, which turns the camp
    hostile: on a goblin friend. Now it opens its own node, pointing at Rakeb, who holds him against the devil fish."""
    from build_troll_choices import add_node
    t = lhbuild.read(TREE)
    if "Node ID=" + DARSH_NODE + CR in t:
        return 0
    i, j = node_span(t, NODE)
    blk = t[i:j]
    assert blk.count(DARSH) == 1
    blk = blk.replace(DARSH, DARSH.replace("10 darsh", DARSH_NODE) + "Custom Action=" + B(*lhbuild.deactivate(WELCOME)), 1)
    t = t[:i] + blk + t[j:]
    assert len(DARSH_TEXT) <= 200
    t = add_node(t, DARSH_NODE, DARSH_TEXT, [])
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    register([TREE])
    return 1


def main():
    print("darsh:", build_darsh())
    t = lhbuild.read(TREE)
    i, j = node_span(t, NODE)
    blk = t[i:j]
    off = "Custom Action=" + B(*lhbuild.deactivate(WELCOME))
    if blk.count(off) >= 2 and (EXIT + off) in blk:
        print("gate greeting: 0")
        return
    for anchor in (EXIT, AUDIENCE):
        assert blk.count(anchor) == 1, anchor
        after = blk[blk.index(anchor) + len(anchor):]
        assert not after.startswith("Custom Action="), anchor
        blk = blk.replace(anchor, anchor + off, 1)
    t = t[:i] + blk + t[j:]
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    register([TREE])
    print("gate greeting: 2")


if __name__ == "__main__":
    main()
