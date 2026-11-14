"""Fernand keeps up with the party at a walk. Requested after 0.99.18.

Walk speed is `Walk Magic Speed Multiplier` x `Base Animation Speed Multiplier` x sneak x encumbrance, and the base
multiplier scales Action Points (5 + AG/2) from 5.5..10 onto 1..2. Fernand's race gives him AG 3, so he walks at 1.22x,
against Grace's 1.44x (AG 5) and a typical hero's 1.55x-1.78x (AG 6-8): he fell behind just walking around, and the
engine's catch-up run was the only thing bringing him back. How a companion follows is compiled into the exe, so the fix
is speed, not pathing.

`Walk Magic Speed Multiplier` is the walk-only stat that armour lowers (full plate -0.15, plate mail -0.10, hauberk -0.05).
A permanent +0.2 on it puts Fernand at about 1.42x, level with Grace, and leaves his AG, Action Points and attack speed
alone. Raising AG would also have sped up his attacks.

It is granted by `Fixt Companion Joined/Distressed Sailor`, which his tree runs on every join and rejoin, so it reaches a
save where he is already recruited the next time he is asked to walk with you. `Fixt Fernand Stride` on Player1 makes it
once only: a permanent modifier granted on every rejoin would stack for ever.

A rerun is a no-op.

    python tools/build_fernand_stride.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, if_action, exists, multi
from build_shrine_repairs import register

JOINED = "Resources/Common Objects and Scripts/Fixt Companion Joined/Distressed Sailor.can"
GUARD = "Fixt Fernand Stride"
GUARD_DCA = "Resources/Derived Character Attributes/Game Scripting Variables/" + GUARD + ".DerivedCharacterAttribute"
FERNAND = "Distressed Sailor"
BONUS = "0.2"


def modifier(who, permanent, attr, amount, description=""):
    return ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", description), ("Modification is permanent", permanent), ("Character to modify", who),
        ("Modifiers", [("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", ("CConstant", [("Constant Value", amount)])), ("Modification amount is a percent", "0"),
            ("Allow Accumulation", "1"), ("Derived character attribute to modify", "Derived Character Attributes/" + attr)]))]),
        ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])


def stride():
    grant = multi([modifier(FERNAND, "1", "Speed/Walk Magic Speed Multiplier", BONUS, "Fixt Fernand stride"),
                   modifier("Player1", "0", "Game Scripting Variables/" + GUARD, "1")])
    return ("CIfExpressionAction", [
        ("If Expression", ("CIsEqualTo", [
            ("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", "Derived Character Attributes/Game Scripting Variables/" + GUARD)])),
            ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "0")]))])),
        ("Character to get attributes from", "Player1"),
        ("Then", if_action(exists(FERNAND), grant)),
        ("Else", "")])


def build_guard():
    if (lhbuild.FX / GUARD_DCA).exists():
        return 0
    t = lhbuild.read("Resources/Derived Character Attributes/Game Scripting Variables/Fixt Companion Grace.DerivedCharacterAttribute")
    t = t.replace("Fixt Companion Grace", GUARD)
    t = re.sub(r"Description=[^\r\n]*", "Description=1 once Fernand has been given his walking pace (tools/build_fernand_stride.py).", t)
    (lhbuild.FX / GUARD_DCA).write_bytes(t.encode("latin-1"))
    register([GUARD_DCA])
    return 1


def build_joined():
    t = lhbuild.read(JOINED)
    if GUARD in t:
        return 0
    flat = CR.join(line.lstrip("\t") for line in t.split(CR))
    assert flat.count("Item Count=3" + CR) == 1
    flat = flat.replace("Item Count=3" + CR, "Item Count=4" + CR, 1)
    anchor = "Canned Object=Common Objects and Scripts/Fixt Companion Health Install" + CR + "}" + CR
    assert flat.count(anchor) == 1
    flat = flat.replace(anchor, anchor + "Action=" + B(*stride()), 1)
    lhbuild.write_map(JOINED, flat)
    register([JOINED])
    return 1


def main():
    print("guard:", build_guard(), "| joined:", build_joined())


if __name__ == "__main__":
    main()
