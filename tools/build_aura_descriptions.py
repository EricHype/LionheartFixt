"""The three aura additions say what they do. Asked for after a playtest confirmed the acid one firing from a wand.

`Acid Touch`, `Cold Zone` and `Lava Burn` read "Inflicts 2-7 points of acid damage to any enemy within melee range of the
character." That reads as a melee rider, and on a wand, which has no melee attack, it reads as broken. It is neither: each
is a `CPlugInBehaviorAddAIWhenSelected` holding a `CAIAreaOvalManager` that fires on its own timer at every enemy with HP
inside an oval of radius 110 (aspect 0.71) around the holder, whatever the holder is doing. Confirmed in play on a
`Wand of Greater Healing, Acid Touch`: acid-only hits of 5, 2, 6 and 6 on wasps, one tick catching two of them, and a kill.

Deepest Winter (`Armor/Cold Touch`), the armour aura, already said aura but only "periodically"; it fires every 6s.

So the descriptions now say aura, damage and interval, with the numbers read from the file's own trigger, never typed:

    Creates an aura that deals 2-7 acid damage to nearby enemies every 2 seconds.

Only items generated after install show it: an item's description is assembled when it is made and saved with it.

A rerun is a no-op.

    python tools/build_aura_descriptions.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from build_shrine_repairs import register

BASE = "Resources/Inventory/Inventory Additions/"
# (file, the sentence's opening). Deepest Winter keeps its own flavour and only gains the truth: its "periodically" is 6s
AURAS = [("Miscellaneous/UNIQUE/Acid Touch", "Creates an aura that deals"),
         ("Miscellaneous/UNIQUE/Cold Zone", "Creates an aura that deals"),
         ("Miscellaneous/UNIQUE/Lava Burn", "Creates an aura that deals"),
         ("Armor/Cold Touch", "A magical aura of frost emanates from this armor, dealing")]


def describe(t, opening):
    one = lambda pat: re.findall(pat, t, re.S)
    (every,) = one(r"Re Trigger Delay=CConstant\r\n\t*\{\r\n\t*Constant Value=([\d.]+)")
    (kind,) = one(r"Damage Type=Damage Types/(\w+)")
    amount = r"Damage Amount=CRandom\r\n\t*\{\r\n\t*Operator=\r\n\t*"
    fixed = one(amount + r"Minimum=CConstant\r\n\t*\{\r\n\t*Constant Value=(\d+)\r\n\t*\}\r\n\t*Maximum=CConstant\r\n\t*\{\r\n\t*Constant Value=(\d+)")
    if fixed:
        (lo, hi), = fixed
    else:   # Deepest Winter's damage scales with the item, so it keeps the engine's own %i[] placeholders
        assert len(one(amount + r"Minimum=CInventoryAdditionsNamedExpressionExpression")) == 1 and "Name=min" in t and "Name=max" in t
        lo, hi = "%i[min]", "%i[max]"
    assert "AI To Add=CAIAreaOvalManager" in t and "Trigger if Enemy=1" in t and "Trigger if Player=0" in t
    return "%s %s-%s %s damage to nearby enemies every %s seconds." % (opening, lo, hi, kind.lower(), every)


def main():
    changed = 0
    for name, opening in AURAS:
        rel = BASE + name + ".InventoryAddition"
        t = lhbuild.read(rel)
        new = describe(t, opening)
        old = re.search(r"\tDescription=([^\r\n]*)\r\n", t)
        if old.group(1) == new:
            continue
        assert t.count("\tDescription=") == 1, rel
        t = t[:old.start(1)] + new + t[old.end(1):]
        (lhbuild.FX / rel).write_bytes(t.encode("latin-1"))
        register([rel])
        changed += 1
        print(name + ": " + new)
    print("aura descriptions changed:", changed)


if __name__ == "__main__":
    main()
