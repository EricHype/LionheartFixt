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

Reach: the chambers map, so a save that has not entered it since installing. A save that has already spawned the
leftover recovers by leaving and coming back: the leftover generator has placed its Torquemada and does not again, and
the relay deletes every `Grand Inquisitor` on entry. A rerun is a no-op.

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


def main():
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
