"""Act 5's choice works. Allying with the Hujark, or taking Huko's safe conduct, was meant to take them off your back.

Three things stopped it, and a fourth was vanilla's.

* **22 generators never pacified.** 0.17.0 put the `the Hujark let you live` check inside their below-50%-health balloon,
  so a fighter stood down only after being half killed. The block was right and the slot was wrong, so it is copied
  to the spawn, and the same block goes on the event groups, whose vanilla scripts had no check at all.
* **The ones already standing.** A generator's script runs at spawn, and the map you meet Huko on has spawned before
  you reach him. `Player sides with the Hujark`, `Player buys safe passage` and their relays on the other maps now
  retarget by name. The names are the cans' `User Assigned Name`, because these spawn with a blank `New Name`.
* **The seer.** `Kill all 3 guys` needs three deaths for his talk AI. On these routes only the Assassin and the English
  twin are hostile, so the third was a friend. Those routes now count one up front.
* **The war.** English target `Scripted Custom 1`, which vanilla gave to 0 of 20 generators on map 03 and 3 of 41 on 02.
  Every Hujark now carries it and fights back.

Scripted actors are left out: the voices, the apprentice scene and the cast of the seer's room. A generator keeps its
own script, wrapped, and gains only what it lacks.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_hujark_war.py
"""
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, exists, relay

D = "Levels/5 Nostrodomus/"
FLAG = "the Hujark let you live"
WAR = "Player,Player Friend,Scripted Custom 2"
SKIP = re.compile(r"voice|Snakebreed Summoner Clone|apprentice generator")
NAMES = "Hujark Warrior, Hujark Blademaster, Hujark Shieldsman, Hujark Acolyte, Hujark Shaman"
STANDS = re.compile(r"Name To Check For=" + FLAG + r"\s+Desired Minimum Count=1\s+\}\s+Succeed Action=CSetTargetTypeAction")
SEER = "05 Nostrodomus Demesne.zax"
KILL = "Kill all 3 guys get AI added to Nostrodomus"


def own_slot(part):
    """Return (start, end, text) of the generator's own After Action line or block."""
    i = part.index("New Name=")
    ind = re.search(r"(?m)^(\t+)Remove Default AIs=", part[i:]).group(1)
    m = re.search(r"(?m)^" + ind + r"After Action=", part[i:])
    n = re.search(r"(?m)^" + ind + r"New Facing Angle", part[i:][m.start():])
    return i + m.start(), i + m.start() + n.start(), part[i + m.start():i + m.start() + n.start()]


def template(maps):
    """The stand-down, plus the damage script from a health block, which is what revokes the passage."""
    stand = B("CConditionalAction", [
        ("Try Action", exists(FLAG)),
        ("Succeed Action", ("CSetTargetTypeAction", [("Entity Name", "$Instigator"), ("Name To Target", ""), ("Valid Targets", "Scripted Custom 2")])),
        ("Fail Action", ""), ("Return failure if the TryAction failes", "0")]).rstrip()
    for z in maps.values():
        for part in parts(z):
            if "Node ID=1 nothing answers" in part:
                k = part.index("Node ID=1 nothing answers")
                s = part.index("Action=CSetDamagedScriptActionAction", k)
                block = part[s + len("Action="):balanced(part, s)]
                assert "Relay Name=Passage revoked" in block
                return wrap([stand, block])
    raise SystemExit("no template")


def parts(z):
    return re.findall(r"(?ms)^\t\tLevel Part=\w+\r\n\t\t\{\r\n.*?^\t\t\}", z)


def is_hujark(part):
    if "Activity=CGeneratorAI" not in part:
        return False
    if not re.search(r"Entity=[^\r\n]*(Swordsman|Shaman)", part):
        return False
    return not SKIP.search(re.search(r"\t\t\tName=([^\r\n]*)", part).group(1))


def wrap(items):
    return ("CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=" + str(len(items)) + CR +
            "".join("Action=" + a + CR for a in items) + "}" + CR + "}")


def fix_generator(part, tmpl):
    s, e, own = own_slot(part)
    body = own.strip()[len("After Action="):].strip()
    items = []
    if ("Valid Targets=" + WAR) not in own:
        items.append(B("CSetTargetTypeAction", [("Entity Name", "$Instigator"), ("Name To Target", ""), ("Valid Targets", WAR)]).rstrip())
    if "Categories to add=Scripted Custom 1" not in own:
        items.append(B("CAddCategoryAction", [("Target Name", "$Instigator"), ("Categories to add", "Scripted Custom 1")]).rstrip())
    if body:
        items.append(body)
    if not STANDS.search(own):
        items.append(tmpl)
    if not items or (len(items) == 1 and items[0] is body):
        return part
    return part[:s] + "After Action=" + wrap(items) + CR + part[e:]


def stand_down(z, name):
    """Add the retarget to a relay, whatever shape its action has."""
    i = z.index("\t\t\tName=" + name + CR)
    k = z.index("Activity=CRelayAI", i)
    s = z.index("Action=C", k)
    e = balanced(z, s)
    new = B("CSetTargetTypeAction", [("Entity Name", NAMES), ("Name To Target", ""), ("Valid Targets", "Scripted Custom 2")]).rstrip()
    return z[:s] + "Action=" + wrap([z[s + len("Action="):e], new]) + z[e:]


def seer(z):
    if z.count("Relay Name=" + KILL) > 4:
        return z
    i = z.index("\t\t\tName=NIS Relay 2" + CR)
    k = z.rindex("Name To Check For=" + FLAG, i, z.index("\r\n\t\t}", i))
    a = z.index("Item Count=3" + CR, k)
    assert a - k < 600
    return z[:a] + "Item Count=4" + CR + "Action=" + B(*relay(KILL)) + z[a + len("Item Count=3" + CR):]


def main():
    names = sorted(f for f in os.listdir(FX / D) if f.endswith(".zax"))
    maps = {f: lhbuild.read(D + f) for f in names}
    tmpl = template(maps)
    for f, z in maps.items():
        if NAMES in z:
            continue
        if f != SEER:
            for old in parts(z):
                if is_hujark(old):
                    z = z.replace(old, fix_generator(old, tmpl))
            assert "\t\t\tName=Passage revoked" + CR in z, f
            for name in ("Player sides with the Hujark", "Player buys safe passage", "Activate English generators", "Passage granted"):
                if "\t\t\tName=" + name + CR in z:
                    z = stand_down(z, name)
        else:
            z = seer(z)
        lhbuild.write_map(D + f, z)


if __name__ == "__main__":
    main()
