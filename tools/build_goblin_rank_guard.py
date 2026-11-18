"""An imported goblin title keeps what it carried and climbs no further. Issue #15: "The goblin ranks can be acquired
indefinitely by exporting character and doing any quest for goblins, and the bonuses would stack (i could get goblin
chum rank 3)".

`Advance Goblin Rank.can` climbs the ladder on `Uber Perks/Goblin Rank` alone: 0 gives Chum, 1 Blooded, 2 Champion,
each by assigning a faction (`Factions/Goblin *`) whose permanent modifiers hold the running bonuses and bump the rank,
plus a title perk. `Join Butus Line.can`, the traitor branch, reads the same attribute. The design leans on the engine
withdrawing the old faction's package when the next is assigned. An exported character keeps its perks and permanent
modifiers but not its faction (a live save holds `Faction=Factions/Goblin Chum`; the exported `.RPG` does not), so in a
new game nothing is withdrawn and each grant lands on top of what was carried. Which numbers come back exactly needs an
export test; the guard below does not depend on it.

Decided 2026-11-18: an imported title holder keeps the title and bonuses it carried, and gains no further rank.

Both cans' whole ladder is now wrapped in one more test: the character holds **no** goblin title perk (Chum, Blooded,
Champion or Traitor), **or** this game's own flag is set. The flag is a new scripting variable, `Fixt Goblin Ladder
This Game`, cloned from vanilla's `Relican Dead` with `Include in character Import and Export=0`, so it resets in every
new game, and each pass through the guard sets it. A character climbing in its own game always passes; an imported
title holder never does. The perk test is one `CHasPerkExpression` per perk joined with `COrAction`, because no vanilla
use shows whether a multi-entry perk array means any or all.

A can edit, so it reaches every save the next time a goblin service completes. A rerun is a no-op.

    python tools/build_goblin_rank_guard.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

CANS = ["Resources/Levels/Wilderness/Quests/Advance Goblin Rank.can",
        "Resources/Levels/Wilderness/Quests/Join Butus Line.can"]
FLAG_REL = "Resources/Derived Character Attributes/Game Scripting Variables/Fixt Goblin Ladder This Game.DerivedCharacterAttribute"
FLAG = "Derived Character Attributes/Game Scripting Variables/Fixt Goblin Ladder This Game"
TEMPLATE = "Resources/Derived Character Attributes/Game Scripting Variables/Relican Dead.DerivedCharacterAttribute"
TITLES = ["Goblin Chum", "Goblin Blooded", "Goblin Champion", "Goblin Traitor"]
MARK = "Character Attribute=" + FLAG + CR


def has_perk(p):
    return ("CExpressionAction", [
        ("Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [
            ("Item Count", "1"), ("Perk To Check For", "Perks/!Event Title Perks/" + p)]))])),
        ("Character to get attributes from", "$Instigator")])


def any_of(items):
    return ("COrAction", [("Action", ("Array", [("Item Count", str(len(items)))] + [("Action", i) for i in items]))])


CONDITION = any_of([
    ("CNotAction", [("Action", any_of([has_perk(p) for p in TITLES]))]),
    ("CExpressionAction", [
        ("Expression", ("CIsGreaterThan", [
            ("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", FLAG)])),
            ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "0")]))])),
        ("Character to get attributes from", "$Instigator")]),
])
SET_FLAG = ("CAddCharacterModifierToCharacterAction", [
    ("Modifier Description", ""), ("Modification is permanent", "1"), ("Character to modify", "$Instigator"),
    ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
        ("Modification Amount", ("CConstant", [("Constant Value", "1")])),
        ("Modification amount is a percent", "0"), ("Allow Accumulation", "0"),
        ("Derived character attribute to modify", FLAG)]))])),
    ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])


def flag_file():
    if (lhbuild.FX / FLAG_REL).exists():
        return 0
    t = lhbuild.read(TEMPLATE)
    assert "Include in character Import and Export=0" + CR in t and t.count("Short Name=Relican Dead" + CR) == 1
    t = t.replace("Short Name=Relican Dead" + CR, "Short Name=Fixt Goblin Ladder This Game" + CR)
    t = t.replace("Description=0 Means he is not dead.  1 Means he is dead." + CR,
                  "Description=Set by the first goblin rank earned in this game. Not exported, so an imported goblin title cannot climb again." + CR)
    assert "Fixt Goblin Ladder This Game" in t and "Relican" not in t
    p = lhbuild.FX / FLAG_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(t.encode("latin-1"))
    return 1


def guard(rel):
    t = lhbuild.read(rel)
    if MARK in t:
        return 0
    k = t.index("\tObject=")
    s = k + len("\tObject=")
    e = lhbuild.balanced(t, s)
    old = t[s:e]
    assert old.startswith("CIfAction") and "Goblin Rank" in old, rel
    cond = B(*CONDITION).rstrip(CR)
    then = ("CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR +
            "Action=" + B(*SET_FLAG) + "Action=" + old + CR + "}" + CR + "}")
    new = ("CIfAction" + CR + "{" + CR + "If=" + cond + CR + "Then=" + then + CR + "Else=" + CR +
           "Return failure if the If failes=0" + CR + "}")
    lhbuild.write_map(rel, t[:s] + new + t[e:])
    return 1


def main():
    made = flag_file()
    done = [rel for rel in CANS if guard(rel)]
    register(([FLAG_REL] if made else []) + done)
    print("goblin rank guard: flag", made, "cans", len(done))


if __name__ == "__main__":
    main()
