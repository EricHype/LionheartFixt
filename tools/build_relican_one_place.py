"""Relican leaves the Slave Pit once he holds La Calle Perdida. Issue #15: "Even after Relican kills everyone at la
Calle Perdida, when you go to slave pit exterior he is both there and at la Calle Perdida."

`Slave Pit Exterior.zax` (not a Fixt file) spawns `Relican` from an unnamed generator, ungated. When the player uses
his ring in La Calle Perdida, `Player chooses to activate Ring` spawns `Relican Take over Calle Generator` there and
never removes the Slave Pit copy, who goes on saying "Apprentice, go find La Calle Perdida". Vanilla's bug.

Two routes, because no single edit reaches every save:

  * **the ring** -- its success branch (the one that also starts the takeover cutscene) now deletes `Relican` in
    `Wilderness Maps/Slave Pit Exterior` through `COtherMapAction`, the pattern vanilla uses for cross-map deletes.
    A map edit, so it reaches only a game that has not yet entered La Calle Perdida.
  * **his La Calle Perdida tree** -- "Tell me more about the tasks." and "Goodbye." in `5 Return Dialogue` carry the
    same delete. Every Dark Wielder talks to him there after the takeover, and a tree reaches every save, so a save
    already past the ring loses the stale copy the next time the player speaks to him. Deleting someone already gone
    does nothing, so repeats are harmless. `5 Return Dialogue` is only reachable from Relican in La Calle Perdida;
    the Slave Pit copy uses a different tree, `Levels/Wilderness/Dialog/Relican`.

The `INTRO MOVIE` variant of the Slave Pit map places no Relican. A rerun is a no-op.

    python tools/build_relican_one_place.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

MAP = "Levels/1 Barcelona/Calle Perdida.zax"
TREE = "Resources/Levels/1 Barcelona/Dialog/La Calle Perdida/Lord Relican.DialogTree"
RING = "Player chooses to activate Ring"
SLAVE_PIT = "Wilderness Maps/Slave Pit Exterior"
DELETE = B(*lhbuild.other_map(SLAVE_PIT, ("CDeleteAction", [("Target Name", "Relican")])))


def ring():
    z = lhbuild.read(MAP)
    i = z.index("\t\t\tName=" + RING + CR)
    s = z.rindex("Level Part=", 0, i)
    e = lhbuild.balanced(z, s)
    blk = z[s:e]
    if "Other Map Name=" + SLAVE_PIT + CR in blk and "Target Name=Relican" + CR in blk:
        return 0
    j = blk.index("Succeed Action=CMultipleActionsAction")
    k = blk.index("Item Count=", j)
    ke = blk.index(CR, k)
    n = int(blk[k + len("Item Count="):ke])
    assert n == 18, n
    assert "CBeginNonInteractiveSequenceAction" in blk[ke:ke + 200], "not the takeover branch"
    blk = blk[:k] + "Item Count=" + str(n + 1) + CR + "Action=" + DELETE.rstrip(CR) + blk[ke:]
    z = z[:s] + blk + z[e:]
    lhbuild.write_map(MAP, z)
    register([MAP])
    return 1


def tree():
    t = lhbuild.read(TREE)
    a = t.index("Node ID=5 Return Dialogue" + CR)
    b = t.index("-" * 60, a)
    node = t[a:b]
    action = "Custom Action=" + "".join(l.lstrip("\t") + CR for l in DELETE.split(CR) if l)
    done = 0
    for reply, nxt in (("Reply Text=Tell me more about the tasks." + CR, "Go to node ID=40 tasks" + CR),
                       ("Reply Text=Goodbye." + CR, "Go to node ID=10 Goodbye" + CR)):
        pair = reply + nxt
        if pair + action in node:
            continue
        assert node.count(pair) == 1, "cannot pin %r" % reply
        after = node[node.index(pair) + len(pair):]
        assert not after.startswith("Custom Action="), "%r already has an action" % reply
        node = node.replace(pair, pair + action)
        done += 1
    if done:
        n0 = t.count(CR)
        t = t[:a] + node + t[b:]
        assert t.count(CR) == n0 + done * action.count(CR)
        (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
        register([TREE])
    return done


def main():
    print("relican one place: ring", ring(), "tree replies", tree())


if __name__ == "__main__":
    main()
