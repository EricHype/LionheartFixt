"""The Bonewright is named, and the dead it raised fall with it. Found in play, 0.99.12.

0.21.0's Bonewright, the Doomed Plateau captain that raises the fallen while it stands, had three faults a player found:

1. **It was called "Second Guardian" on screen**, because its generator spawns the vanilla `Second Guardian` cans that
   Retreat of Souls also uses for the Lance's guardian. Its lines called it the Bonewright, so nobody could connect them.
   It now spawns copies named `Bonewright`, under `Monster Cans/Fixt Captains/`; the guardian in Retreat of Souls is untouched.
2. **"The standard" was never shown.** Its opening line had it plant a standard, and its death line said "the standard
   goes over", for a prop that does not exist, beside Act 6's real standard at the Crossroads. Both lines are rewritten
   without it.
3. **Its death line was not true.** It said the half-risen "stop where they are and settle", but killing it only switched
   its wave generator off; what had already risen kept fighting. The wave's spawns now carry a name, `Bonewright Risen`,
   and the Bonewright's death kills every one of them, so the line describes what happens and killing it first pays.

The death script lives in the generator's `CSetDestroyedScriptActionAction`, which overrides the can's own slot, so the
collapse goes there, before the line.

The Revenant Sergeant, the third captain, had the same two faults. It spawned the ordinary Revenant cans (the
`Magical Greater Skeleton` family, on nine Act 4 maps), so it read "Revenant" like every other; it now spawns copies named
`Revenant Sergeant`. And its 66% line said its section "stops fighting the knights and closes around it", when the code
only switched an escort generator on. The line now says what it does, and its whistle now does it: the same branch fires
`CCallForReinforcementsAction` at 600, so every idle undead in earshot that listens turns on you (88 of the 92 undead
cans do; see docs/dormant-engine.md). Ones already fighting do not answer, which is what "in earshot" leaves room for.

A rerun is a no-op.

    python tools/build_bonewright.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH
from build_shrine_druids import parts
from build_shrine_repairs import register

MAP = "Levels/4 Crypt/7 Doomed Plateau.zax"
TREE = "Resources/Levels/4 Crypt/Dialog/The Crypt Captains.DialogTree"
U = "Monster Cans/Undead/"
COPY = "Monster Cans/Fixt Captains/Undead/"
CANS = ["Second Guardian", "Second Guardian Tough", "Second Guardian Super"]
RISEN = "Bonewright Risen"
SERGEANT_CANS = ["Magical Greater Skeleton", "Magical Greater Skeleton Tough", "Magical Greater Skeleton Super"]
EARSHOT = "600"
LINES = {
    "111 the sergeant rallies": "It whistles through the hole where its jaw was. As the dull whistle echoes, every undead in earshot "
                                "turns towards you. You are the problem now.",
    "100 the bonewright": "The Bonewright stops on the shale, and behind you the fallen begin to sit up. It is not raising them from "
                          "anywhere. It is raising them from here, from what is already on this ground, and it will go on doing it while it stands.",
    "101 the bonewright falls": "The Bonewright falls, and the dead it raised fall with it. For the first time since you came up here, "
                                "nothing new is getting to its feet.",
}


def name_of(x):
    m = re.search(r"(?m)^\t\t\tName=([^\r\n]*)", x)
    return m.group(1) if m else ""


def copies():
    done = 0
    for c in CANS:
        rel = "Resources/" + COPY + c + ".can"
        if (lhbuild.FX / rel).exists():
            continue
        t = lhbuild.read("Resources/" + U + c + ".can")
        t, n = re.subn(r"User Assigned Name=[^\r\n]*", "User Assigned Name=Bonewright", t, count=1)
        assert n == 1
        lhbuild.write_map(rel, t)
        register([rel])
        done += 1
    return done


def plateau():
    z = lhbuild.read(MAP)
    if "New Name=" + RISEN + CR in z:
        return 0
    gen = [x for x in parts(z) if name_of(x) == "Fixt Bonewright generator"]
    wave = [x for x in parts(z) if name_of(x) == "Fixt Bonewright wave"]
    assert len(gen) == len(wave) == 1
    g = gen[0]
    for c in CANS:
        g = g.replace("Entity=" + U + c + CR, "Entity=" + COPY + c + CR)
    assert COPY in g
    # the collapse, first in the destroyed script, before the line that describes it
    pain = B("CPainAction", [("Hit Points", "99999"), ("Damage Type", "Unavoidable"), ("Sound", "!None.wav"), ("Target", RISEN)]).rstrip()
    k = g.index("New Destroyed Action=CMultipleActionsAction")
    m = re.compile(r"Item Count=(\d+)\r\n").search(g, k)
    g = g[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + "Action=" + pain + CR + g[m.end():]
    w, n = re.subn(r"New Name=\r\n", "New Name=" + RISEN + CR, wave[0], count=1)
    assert n == 1
    z = z.replace(gen[0], g, 1).replace(wave[0], w, 1)
    lhbuild.write_map(MAP, z)
    register([MAP])
    return 1


def sergeant():
    z = lhbuild.read(MAP)
    if COPY + SERGEANT_CANS[0] in z:
        return 0
    for c in SERGEANT_CANS:
        rel = "Resources/" + COPY + c + ".can"
        if not (lhbuild.FX / rel).exists():
            t = lhbuild.read("Resources/" + U + c + ".can")
            t, n = re.subn(r"User Assigned Name=[^\r\n]*", "User Assigned Name=Revenant Sergeant", t, count=1)
            assert n == 1
            lhbuild.write_map(rel, t)
            register([rel])
    gen = [x for x in parts(z) if name_of(x) == "Fixt Sergeant generator"]
    assert len(gen) == 1
    g = gen[0]
    for c in SERGEANT_CANS:
        g = g.replace("Entity=" + U + c + CR, "Entity=" + COPY + c + CR)
    # the whistle: the 66% branch is the multi that shows `111 the sergeant rallies`
    i = g.index("Node ID=111 the sergeant rallies")
    k = g.rindex("CMultipleActionsAction", 0, i)
    m = re.compile(r"Item Count=(\d+)\r\n").search(g, k)
    call = B("CCallForReinforcementsAction", [("Requester Name", "$Trigger"), ("Max Distance", EARSHOT)]).rstrip()
    g = g[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + "Action=" + call + CR + g[m.end():]
    lhbuild.write_map(MAP, z.replace(gen[0], g, 1))
    register([MAP])
    return 1


def lines():
    t = lhbuild.read(TREE)
    crlf = t.count(CR)
    new = t
    for nid, text in LINES.items():
        new, n = re.subn(r"(Node ID=" + re.escape(nid) + r"\r\nText=)[^\r\n]*", lambda m: m.group(1) + text, new, count=1)
        assert n == 1, nid
    if new != t:
        assert new.count(CR) == crlf
        (lhbuild.FX / TREE).write_bytes(new.encode("latin-1"))
        register([TREE])
        return 1
    return 0


def main():
    print("Bonewright cans:", copies(), "| plateau:", plateau(), "| sergeant:", sergeant(), "| lines:", lines())


if __name__ == "__main__":
    main()
