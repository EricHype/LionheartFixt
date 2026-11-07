"""The English say what they just did, and stop talking about shields they do not carry. Both reported from play.

The 48 abilities of 0.33.0 and 0.34.0 heal or buff from a can's Damaged Script Action with a spawned effect and nothing
else, so the player saw a flash and damage vanish with no line in the log. Each now prints what it did, through
`CPrintCombatTextAction`, beside its effect, so it fires exactly as often as the effect does. Shown to Player1 because a
companion's hit can trigger it too, and the numbers are the can's own.

No English model carries a shield, so the two bark lines that said so are reworded.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_enemy_ability_log.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX

CANS = FX / "Resources/Monster Cans"
BARKS = "Resources/Levels/7 English Shrine/Dialog/Fixt Soldier Barks.DialogTree"
DRAUGHT = "drinks a healing draught and recovers a third of their health."
TEXT = {
    "English Soldier": "closes ranks: +12 resistance to blades, blows and arrows for 20 seconds.",
    "English Sergeant": "fights with both hands: +2 Strength and faster attacks for 15 seconds.",
    "English Guardsman": "fights with both hands: +2 Strength and faster attacks for 15 seconds.",
    "English Bowman": "steadies the draw: +2 Perception and faster shots for 20 seconds.",
    "Druid": "prays faster: quicker casting for 20 seconds.",
    "Druidess": "prays faster: quicker casting for 20 seconds.",
    "Fire WarGolem": "vents its furnace: +20 fire resistance and faster attacks for 20 seconds.",
    "Ice WarGolem": "rimes over: +20 cold resistance and faster attacks for 20 seconds.",
    "Lightning WarGolem": "arcs over its plating: +20 electrical resistance and faster attacks for 20 seconds.",
    "English Captain": DRAUGHT,
    "English Lieutenant": DRAUGHT,
    "English Bowmaster": DRAUGHT,
    "Royal Guardsman": DRAUGHT,
}


def line(text):
    return "Action=" + B("CPrintCombatTextAction", [("Text to print", text), ("Character to show text to", "Player1"), ("Emphasize", "0"), ("Suppress Duplicates", "0")])


def logs():
    done = 0
    for f in sorted(CANS.rglob("*.can")):
        rel = f.relative_to(FX).as_posix()
        z = lhbuild.read(rel)
        m = re.search(r"Damaged Script Action=C[\s\S]*?Damaged Effect Action=", z)
        if not m or not re.search(r"CAddCharacterModifierToCharacterAction|CGiveHealthToCharacterAction", m.group(0)):
            continue
        if "CPrintCombatTextAction" in m.group(0):
            continue
        name = re.search(r"User Assigned Name=([^\r\n]*)", z).group(1)
        text = TEXT[name]
        k = z.index("Action=CSpawnEffectAction", m.start())
        assert k < m.end()
        s = z.rindex(CR, 0, k) + len(CR)
        tabs = z[s:k]
        # The effect's own Action array, not a modifier's array at the same depth, which sits between them on the buffs.
        c = z.index("Item Count=", z.rindex(tabs[:-1] + "Action=Array", 0, s))
        c = z.rindex(CR, 0, c) + len(CR)
        n = re.match(r"\t*Item Count=(\d+)", z[c:])
        assert n and c > m.start()
        z = z[:s] + tabs + line(name + " " + text) + z[s:]
        z = z[:c] + tabs + "Item Count=" + str(int(n.group(1)) + 1) + z[c + n.end():]
        lhbuild.write_map(rel, z)
        done += 1
    print(done, "cans")


def barks():
    z = lhbuild.read(BARKS)
    if "Shields up!" not in z:
        return
    for a, b in (("<He sets his shield and advances>", "<He sets his feet and advances>"), ("Shields up!", "Blades up!")):
        assert z.count(a) == 1, a
        z = z.replace(a, b)
    (FX / BARKS).write_bytes(z.encode("latin-1"))


def main():
    logs()
    barks()


if __name__ == "__main__":
    main()
