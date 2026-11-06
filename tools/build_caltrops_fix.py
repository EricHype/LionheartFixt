"""Caltrops you can see, from every thief. Reported from play: thieves do not appear to drop traps.

0.35.0's script was sound, and two things kept it from being seen. It stays on the assassins and thieves it was built
for: the Thug family are not guild thieves, and do not get it. 0.35.0 missed the assassins most players meet, the
Montserrat and Assassin Master cans, so those nine join it. Machiavelli's belong to scripted scenes and stay out.


* **The model had never been seen.** Nothing else in the game uses `Ground lights/Smoke`.
* **In melee it could vanish at once.** You stand inside its 55 radius when it lands, so it fired on `Enter`, deleted
  itself, and showed as a spike hit and nothing else.

So the patch now fires from `Repeat Action`, the shape the 27 shipped golem and undead auras use, with an empty first
step. Whether or not the engine fires the first repeat on entry, you get at least `Repeat Every` to step off it.

A rerun is a no-op.

    python tools/build_caltrops_fix.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced

ENTITY = "Resources/Common Objects and Scripts/Fixt Caltrops Entity.can"
TEMPLATE = "Resources/Monster Cans/Thugs/Theif3 Mace.can"
MODEL = sys.argv[1] if len(sys.argv) > 1 else "Environments/Outpost/Generic/Trap Spike 1"
TIERS = ("", " Tough", " Super")
ASSASSINS = [f"Resources/Levels/2 Montserrat/Character Templates/Montserrat Assassin{t}.can" for t in TIERS] + \
            [f"Resources/Monster Cans/Assasin Master{t} {k}.can" for t in TIERS for k in ("CHARACTER", "SPELLCASTER")]


def entity():
    z = lhbuild.read(ENTITY)
    if "Repeat Every=1.25" in z:
        return
    s = z.index("Enter Action=CMultipleActionsAction")
    e = balanced(z, s)
    hit = z[s + len("Enter Action="):e]
    assert "CDeleteAction" in hit and "Spike Hit" in hit
    tail = z.index("Repeat Every=0", e)
    wait = ("CSucceedAction", [("Action", "")])
    series = ("CSeriesAction", [("Action", ("Array", [("Item Count", "2"), ("Action", wait), ("Action", hit)])),
                                ("When Done", "Repeat Last Action"), ("Require Success To Advance", "1"), ("Next Action Index", "0")])
    gap = z[e:tail]
    assert "Exit Action=" in gap and "Repeat Action=" in gap
    z = z[:s] + "Enter Action=" + CR + gap.lstrip(CR).replace("Repeat Action=", "Repeat Action=" + B(*series).rstrip(CR), 1) + \
        "Repeat Every=1.25" + z[tail + len("Repeat Every=0"):]
    assert z.count("Trigger Only Once=1") == 1
    z = z.replace("Trigger Only Once=1", "Trigger Only Once=0")
    z, n = re.subn(r"(\bModel=)Spell Effects/Ground lights/Smoke", lambda m: m.group(1) + MODEL, z)
    assert n == 1
    z, n = re.subn(r"Cur Sequence=Idle", "Cur Sequence=Closed", z)  # spikes up; it is a spike door in shipped maps
    assert n == 1
    lhbuild.write_map(ENTITY, z)


def layers():
    t = lhbuild.read(TEMPLATE)
    s = t.index("Damaged Script Action=CSeriesAction")
    e = balanced(t, s)
    block = t[s:e]
    assert "Fixt Caltrops Entity" in block
    for rel in ASSASSINS:
        z = lhbuild.read(rel)
        if "Fixt Caltrops Entity" in z:
            continue
        old = "Damaged Script Action=" + CR
        i = z.index(old)
        lhbuild.write_map(rel, z[:i] + block + CR + z[i + len(old):])


def main():
    entity()
    layers()


if __name__ == "__main__":
    main()
