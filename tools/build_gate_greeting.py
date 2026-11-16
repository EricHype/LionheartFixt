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


def main():
    t = lhbuild.read(TREE)
    i, j = node_span(t, NODE)
    blk = t[i:j]
    off = "Custom Action=" + B(*lhbuild.deactivate(WELCOME))
    if off in blk:
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
