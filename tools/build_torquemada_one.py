"""One Torquemada. Reported: "there are two toquemadas now that I'm back from monserrat, the one i can talk to sends
me to jail and won't fight".

The chambers' `RESET MAP for Invulnerable Grand Inquisitor` relay runs on every spawn point and the secret door. In
vanilla it deletes `Grand Inquisitor`, clones `Grand Inquisitor generator` as `Used Grand Inquisitor Generator` (a
`CDelayAction` of 0, so the clone lands next tick) and deletes `Used Grand Inquisitor Generator` (this tick, so the
previous visit's clone). A generator places its creature when the player comes near, not when it is made.

0.95.0 (`build_torquemada.py`) split the spawn: before Montserrat the vanilla clone, after it a clone of a mortal copy,
`Used Fixt Mortal Inquisitor Generator`. Each arm deletes only its own leftover. So a vanilla clone from the last
visit before Montserrat that had not yet placed him survives into the first visit after, and places the invulnerable
Torquemada beside the mortal one: the jail hooks, and `Spell Immunity`. The fight relay sends everything named
`Grand Inquisitor` to combat, the leftover included, and the leftover answers combat with jail. The user's QuickSave
shows it: two `Used Grand Inquisitor Generator` in `Inquisition Chambers2`, one with `Already Generated=0`.

The relay now deletes both leftovers before it picks, whichever arm runs, as vanilla's one arm always did.

Reach: the chambers map, so a save that has not entered it since installing. A save whose chambers already hold the
leftover is reached through his fight reply instead (`build_tree`): leaving and coming back does not help, because the
leftover stays in the saved map and re-places him (reported: "there are still two"). A rerun is a no-op.

    python tools/build_torquemada_one.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, balanced
from build_shrine_repairs import register

MAP = "Levels/1 Barcelona/Inquisition Chambers2.zax"
RELAY = "RESET MAP for Invulnerable Grand Inquisitor"
LEFTOVERS = ["Used Grand Inquisitor Generator", "Used Fixt Mortal Inquisitor Generator"]
AFTER = "Target Name=Fixt Torquemada guard"


TREE = "Resources/Levels/1 Barcelona/Dialog/Temple District/GrandInquisitor.DialogTree"
FIGHT_THEN = ("Then=CTriggerRelayAction" + CR + "{" + CR + "Relay Name=Fixt Torquemada fight" + CR + "}" + CR)
SETTLE = 2  # seconds for the mortal generator, recloned by the reset, to place him before the fight is called


def build_tree():
    """For a save whose chambers already hold the leftover, the map cannot help: the leftover sits in the saved map, and
    re-entry does not delete it. The fight reply reaches every save. With two `Grand Inquisitor` alive it deletes the
    leftover generator, runs the chambers' own reset (which deletes both and reclones only the mortal one, the
    leftover being gone), and calls the fight once he stands again. With one, the fight as before."""
    t = lhbuild.read(TREE)
    if "Target Name=" + LEFTOVERS[0] + CR in t:
        return []
    s = t.index("Node ID=120 combat" + CR)
    e = t.index("-" * 60, s)
    assert t[s:e].count(FIGHT_THEN) == 1
    two = ("CIsAliveAction", [("Name To Check For", "Grand Inquisitor"), ("Desired Minimum Count", "2")])
    settle = lhbuild.multi([("CDeleteAction", [("Target Name", LEFTOVERS[0])]),
                            ("CTriggerRelayAction", [("Relay Name", RELAY)]),
                            lhbuild.delay(SETTLE, ("CTriggerRelayAction", [("Relay Name", "Fixt Torquemada fight")]))])
    new = "Then=" + B(*lhbuild.if_action(two, settle, ("CTriggerRelayAction", [("Relay Name", "Fixt Torquemada fight")])))
    k = t.index(FIGHT_THEN, s)
    t = t[:k] + new + t[k + len(FIGHT_THEN):]
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    return [TREE]


def main():
    done = build_tree()
    if done:
        register(done)
        print("torquemada tree:", done)
    z = lhbuild.read(MAP)
    i = z.index("\t\t\tName=" + RELAY + CR)
    s = z.rindex("\t\tLevel Part=", 0, i)
    e = balanced(z, s)
    p = z[s:e]
    # each arm deletes its own leftover once; after this build the mortal one is deleted twice
    if p.count("Target Name=" + LEFTOVERS[1] + CR) >= 2:
        print("torquemada one: []")
        return
    a = p.index("Action=CMultipleActionsAction")
    c = p.index("Item Count=", a)
    m = re.compile(r"Item Count=(\d+)").match(p, c)
    # the guard delete is a direct item of that array: insert the two leftovers' deletes after it
    k = p.index(AFTER + CR)
    d = p.rindex("Action=CDeleteAction", 0, k)
    end = balanced(p, d) + len(CR)
    add = "".join("Action=" + B("CDeleteAction", [("Target Name", n)]) for n in LEFTOVERS)
    p2 = p[:end] + add + p[end:]
    p2 = p2[:c] + "Item Count=" + str(int(m.group(1)) + len(LEFTOVERS)) + p2[m.end():]
    z = z[:s] + p2 + z[e:]
    lhbuild.write_map(MAP, z)
    register([MAP])
    print("torquemada one:", [MAP])


if __name__ == "__main__":
    main()
