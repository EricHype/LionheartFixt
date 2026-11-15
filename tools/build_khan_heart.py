"""The Khan's death, and his Champion's standing, reach the goblins as they spawn. Found while fixing the war leaders.

`tools/build_carryovers.py` put a marker, `Fixt the Horde's heart`, on the Lake, the Plains, Woodcutter Forest and the
Barcelona Coast. Three seconds after the map loads it either stood every Horde band aside (the Khan's Champion) or, if the
Khan was slain, added each band goblin a `CRepeatTimerTriggerAI` holding a permanent -0.2 `Base Animation Speed Multiplier`
on `$Trigger`, and then switched itself off. Both reach only goblins that exist three seconds in. A `CGeneratorAI` does not
generate when the map loads; it waits for the player. The proof is in the saves: on a Lake the player has walked,
`Fixt Lake Band 1 war leader` has still never generated. So a band out of range on arrival was never slowed and never stood
aside, and the war leader watchers failed the same way (`tools/build_goblin_leader_death.py`).

So both now happen at spawn. Every generator the marker named gets an `After Action` that runs on the goblin it has just
made, `$Instigator`, the same reference vanilla's own `After Action=CSetDestroyedScriptActionAction{Target Name=$Instigator}`
uses on 28 Woodcutter generators:

* the Khan's Champion: that goblin stands aside, with the marker's own pacifier (`CSetTargetTypeAction` with no targets and
  `CRemoveCategoryAction Enemy`);
* otherwise, the Khan slain: that goblin takes the -0.2, by name, not through a timer AI.

An `After Action` already there (vanilla's `monster counter` death script, the war leader's death script) is kept and runs
first, inside a `CMultipleActionsAction`. The marker keeps only its line on arrival, *"Without their Khan, the goblins here
fight with less heart."* or the Champion's, because that is about the map and is right on arrival.

Run after `build_carryovers.py`, `build_goblin_leaders.py` and `build_goblin_leader_death.py`. **Reach:** a visited map is
frozen into the save with its generators, so maps not yet entered, and new games. A rerun is a no-op.

    python tools/build_khan_heart.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register
from build_carryovers import BANDS, KHAN, CHAMPION, HEARTLESS, DISTANCE, once_on_arrival
from build_inquisition_slides import var_if

MARKER = "Fixt the Horde's heart"
TAG = "without the Khan"
ME = "$Instigator"


def note(text):
    return ("CPrintCombatTextAction", [("Text to print", text), ("Character to show text to", "Player1"), ("Emphasize", "0"), ("Suppress Duplicates", "1")])


def champion():
    return ("CExpressionAction", [("Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [("Item Count", "1"), ("Perk To Check For", CHAMPION)]))])),
                                  ("Character to get attributes from", "Player1")])


def on_spawn():
    aside = lhbuild.multi([("CSetTargetTypeAction", [("Entity Name", ME), ("Name To Target", ""), ("Valid Targets", "")]),
                           ("CRemoveCategoryAction", [("Target Name", ME), ("Categories To Remove", "Enemy")])])
    slower = ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", TAG), ("Modification is permanent", "1"), ("Character to modify", ME),
        ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", ("CConstant", [("Constant Value", "-0.2")])), ("Modification amount is a percent", "0"),
            ("Allow Accumulation", "0"), ("Derived character attribute to modify", "Derived Character Attributes/Speed/Base Animation Speed Multiplier")]))])),
        ("OPTIONAL Duration", ""), ("Expression Context", ME)])
    return lhbuild.if_action(champion(), aside, var_if(KHAN, slower, ""))


def part_bounds(z, i):
    s = z.rindex("\t\tLevel Part=", 0, i)
    return s, lhbuild.balanced(z, s)


def build(map_name):
    rel = "Levels/Wilderness Maps/" + map_name + ".zax"
    z = lhbuild.read(rel)
    if "Modifier Description=" + TAG + CR in z:
        return 0
    s, e = part_bounds(z, z.index("\t\t\tName=" + MARKER + CR))
    names = [n.strip() for n in re.search(r"Target Name=(Horde Goblin[^\r\n]*)", z[s:e]).group(1).split(",")]
    # the marker keeps its line, and only its line
    arrival = once_on_arrival(MARKER, lhbuild.if_action(champion(), note(DISTANCE), var_if(KHAN, note(HEARTLESS), "")))
    z = z[:s] + z[e + len(CR):]
    effect = B(*on_spawn())
    done = 0
    for part in re.findall(r"(?ms)^\t\tLevel Part=\w+\r\n\t\t\{\r\n.*?^\t\t\}", z):
        nn = re.findall(r"New Name=([^\r\n]*)", part)
        if "CGeneratorAI" not in part or not nn or nn[0] not in names:
            continue
        a = re.search(r"(?m)^\t*After Action=([^\r\n]*)\r\n", part)
        if a.group(1) == "":
            new = part[:a.start()] + "After Action=" + effect + part[a.end():]
        else:
            b = lhbuild.balanced(part, a.start())
            old = re.sub(r"\r\n\t*", CR, part[a.start():b]).lstrip("\t")[len("After Action="):] + CR
            both = "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR + \
                   "Action=" + old + "Action=" + effect + "}" + CR + "}" + CR
            new = part[:a.start()] + "After Action=" + both + part[b + len(CR):]
        assert z.count(part) == 1
        z = z.replace(part, new)
        done += 1
    assert done >= 2, (map_name, done)
    lhbuild.write_map(rel, lhbuild.add_parts(z, [arrival]))
    register([rel])
    return done


def main():
    for m in BANDS:
        print(m, build(m), "generators apply the Khan at spawn")


if __name__ == "__main__":
    main()
