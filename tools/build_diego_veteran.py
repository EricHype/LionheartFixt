"""Bishop Diego fights like the veteran he is. Reported: "when we fight inquisitor diego on the plains, he's very weak. We
fold him in a few hits, does that match the fiction of him being a veteran dark inquisitor hunter?"

He does not. `Races/NPCs/Inquisitor Diego` is a companion's build at character level 1: 35 HP, 45 AC, Celestial Smite 30.
Every spawn on the Plains is harder to hit than he is (a plain goblin has 100 AC, a gray wolf 80), and the rogue Dark
Inquisitors he hunts have more of both (40 HP, 60 AC).

The fight starts from one reply, *"The Dark Inquisitors have asked me to kill you..."*, in `3 Return Dialogue`, whose
action was `CGoToCombatAction` on `$Trigger`. It now first gives `$Trigger`, the same Diego, a permanent modifier:

  * HP +65 (100, a Greater Skeleton Super's);
  * AC +105 (150, a Goblin Super's);
  * Celestial Smite +40 (70).

Only that reply carries it, so Diego as a companion is unchanged. Tree only, so every save that has not had the fight. A
rerun is a no-op.

    python tools/build_diego_veteran.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

TREE = "Resources/Levels/Wilderness/Dialog/Diego.DialogTree"
TAG = "Fixt veteran inquisitor"
OLD = "Custom Action=CGoToCombatAction" + CR + "{" + CR + "Enemy Name=$Trigger" + CR + "}" + CR
KILL = "Reply Text=The Dark Inquisitors have asked me to kill you and I am here to do just that!" + CR
DA = "Derived Character Attributes/"


def derived(attr, n):
    return ("Modifier", ("CCharacterModifierDerivedAttribute", [
        ("Modification Amount", ("CConstant", [("Constant Value", str(n))])), ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "0"), ("Derived character attribute to modify", DA + attr)]))


def skill(sk, n):
    return ("Modifier", ("CCharacterModifierSkill", [
        ("Modification Amount", ("CConstant", [("Constant Value", str(n))])), ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "0"), ("Skill to modify", "Skills/" + sk)]))


def veteran():
    return ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", TAG), ("Modification is permanent", "1"), ("Character to modify", "$Trigger"),
        ("Modifiers", ("Array", [("Item Count", "3"), derived("(HP) Hit Points", 65), derived("(AC) Armor Class", 105),
                                 skill("Magic Divine/Offensive/Celestial Smite", 40)])),
        ("OPTIONAL Duration", ""), ("Expression Context", "$Trigger")])


def main():
    t = lhbuild.read(TREE)
    if TAG in t:
        print("diego veteran: []")
        return
    k = t.index(KILL)
    a = t.index("Custom Action=", k)
    assert t.count(OLD) == 1 and t.index(OLD) == a and t.count(KILL) == 1
    fight = ("CGoToCombatAction", [("Enemy Name", "$Trigger")])
    t = t[:a] + "Custom Action=" + B(*lhbuild.multi([veteran(), fight])) + t[a + len(OLD):]
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    register([TREE])
    print("diego veteran:", [TREE])


if __name__ == "__main__":
    main()
