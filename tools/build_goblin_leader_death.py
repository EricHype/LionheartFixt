"""A band loses heart when its war leader dies, and shows it. Reported from play after 0.99.22: "it shows that goblins have
lost their warleader and I haven't even seen the goblins yet", then "I didn't see impact on the goblins".

**The false alarm.** 0.99.x (`tools/build_goblin_leaders.py`) watched each leader with a `CRepeatTimerTriggerAI` on a marker:
ten seconds after the map loads, then every two, `NOT CIsAliveAction(<band> Leader)` fired the penalty and the line and
deactivated the marker. But a `CGeneratorAI` does not generate when the map loads; it waits for the player. Entering a map
far from a band, the leader did not exist yet, the watcher read him as dead, printed the line, and switched itself off, so
the real death later did nothing. Shown by a save pair: `warleaderdeadornot` has `Woodcutter Band 2 Leader` alive and
fighting while that band's watcher is already off (countdown frozen at 1.98889 in both saves), and in the later quicksave he
is dead and the band never lost heart. So the watcher goes, and the leader carries his own death: each leader generator's
`After Action` is a `CSetDestroyedScriptActionAction`, which can only run when he dies.

**The penalty that never showed.** It was a `CRepeatTimerTriggerAI` added to every band goblin, holding a modifier on
`$Trigger`. The two Coast goblins that received it had run it (`Next Action Index=1`) and carried no speed modifier. They
were corpses by the save, so whether `$Trigger` or death refused it is not proven, and it does not need to be: the modifier
now names the band directly. `CAddCharacterModifierToCharacterAction` resolves its `Character to modify` into a list of
every match and applies to each (`0x488980` -> `0x41f150`, which loops the list calling vtable `+0x84`), so naming the band
reaches every goblin in it, the same broadcast `CSetTargetTypeAction` showed in the Troll Pit.

**What his death does now**, in this order:

1. vanilla's `monster counter` relay first, where the slot already held it (Woodcutter Forest);
2. **the band breaks off**: `CSetTargetTypeAction` with no valid targets and `CRemoveCategoryAction Enemy` on the band, the
   Champion stand-aside's own pacifier, so they stop fighting and companions stop chasing them;
3. **a permanent -0.25 `Base Animation Speed Multiplier`** on the band, the stat vanilla's Speed potion raises, so they move
   and swing slower for good;
4. the line, *"Their war leader is dead, and the goblins around him lose heart."*;
5. activate `Fixt <band> rally`, a dormant marker that six seconds later gives them back `Valid Targets=Player,Player Friend`
   and `Enemy`, exactly what every band can carries, and deactivates itself. It skips the rally for the Khan's Champion, whose
   bands the stand-aside already holds off, so it never turns them hostile. An inactive entity's timer does not run (the old
   watcher's frozen countdown), so it counts its six seconds from the death.

XP and drops are untouched: they live in the leader can's `Destroyed Effect Action`, a separate slot the generator does not
set (the war leader cans' `Destroyed Script Action` is empty).

**Reach:** a map already visited is frozen into the save with its generators and markers, so this fixes maps a character
has not entered yet, and new games. Run it after `build_goblin_leaders.py` and before `build_khan_heart.py`, which wraps the
death script this writes.

A rerun is a no-op.

    python tools/build_goblin_leader_death.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register
from build_goblin_leaders import MAPS, LOST_HEART
from build_shrine_druids import pos

RELAY = "After Action=CSetDestroyedScriptActionAction" + CR
BREAK_OFF = "6"
HOSTILE = "Player,Player Friend"
CHAMPION = "Perks/!Event Title Perks/Goblin Champion"


def part_of(z, name_line):
    i = z.index(name_line)
    s = z.rindex("\t\tLevel Part=", 0, i)
    return s, lhbuild.balanced(z, s)


def targets(band, valid):
    return ("CSetTargetTypeAction", [("Entity Name", band), ("Name To Target", ""), ("Valid Targets", valid)])


def slow(band):
    return ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", "lost heart"), ("Modification is permanent", "1"), ("Character to modify", band),
        ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", ("CConstant", [("Constant Value", "-0.25")])), ("Modification amount is a percent", "0"),
            ("Allow Accumulation", "0"), ("Derived character attribute to modify", "Derived Character Attributes/Speed/Base Animation Speed Multiplier")]))])),
        ("OPTIONAL Duration", ""), ("Expression Context", "Player1")])


def rally(band):
    champion = ("CExpressionAction", [("Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [("Item Count", "1"), ("Perk To Check For", CHAMPION)]))])),
                                      ("Character to get attributes from", "Player1")])
    back = lhbuild.multi([targets(band, HOSTILE), ("CAddCategoryAction", [("Target Name", band), ("Categories to add", "Enemy")])])
    act = lhbuild.multi([lhbuild.if_action(champion, "", back), lhbuild.deactivate("Fixt " + band + " rally")])
    return ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", act),
                                      ("Delay Between Actions", "600"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", BREAK_OFF)])


def death(band, keep):
    acts = ([keep] if keep else []) + [
        targets(band, ""), ("CRemoveCategoryAction", [("Target Name", band), ("Categories To Remove", "Enemy")]),
        slow(band),
        ("CPrintCombatTextAction", [("Text to print", LOST_HEART), ("Character to show text to", "Player1"), ("Emphasize", "0"), ("Suppress Duplicates", "0")]),
        lhbuild.activate("Fixt " + band + " rally")]
    return B("CSetDestroyedScriptActionAction", [("New Destroyed Action", lhbuild.multi(acts)), ("Target Name", "$Instigator")])


def build(map_name, short):
    rel = "Levels/Wilderness Maps/" + map_name + ".zax"
    z = lhbuild.read(rel)
    if "Name=Fixt " + short + " Band 1 heart" + CR not in z:
        return 0
    markers = []
    for n in (1, 2):
        band = short + " Band " + str(n)
        # the watcher marker goes; nothing but its own CDeactivateAction names it. Its place holds the rally marker
        s, e = part_of(z, "\t\t\tName=Fixt " + band + " heart" + CR)
        assert z.count("Fixt " + band + " heart") == 2, band
        x, y = pos(z[s:e])
        z = z[:s] + z[e + len(CR):]
        markers.append(lhbuild.entity("Fixt " + band + " rally", "0", [rally(band)], "Editor/Position Marker", x, y))
        s, e = part_of(z, "\t\t\tName=Fixt " + band + " war leader" + CR)
        p = z[s:e]
        a = re.search(r"(?m)^(\t*)After Action=([^\r\n]*)\r\n", p)
        if a.group(2) == "":
            keep, end = None, a.end()
        else:
            assert a.group(2) == "CSetDestroyedScriptActionAction", (band, a.group(2))
            b = lhbuild.balanced(p, a.start())
            old = re.sub(r"\r\n\t*", CR, p[a.start():b]).lstrip("\t")
            assert old == (RELAY + "{" + CR + "New Destroyed Action=CTriggerRelayAction" + CR + "{" + CR + "Relay Name=monster counter" + CR +
                           "}" + CR + "Target Name=$Instigator" + CR + "}"), (band, old)
            keep, end = ("CTriggerRelayAction", [("Relay Name", "monster counter")]), b + len(CR)
        p = p[:a.start()] + "After Action=" + death(band, keep) + p[end:]
        z = z[:s] + p + z[e:]
    z = lhbuild.add_parts(z, markers)
    assert LOST_HEART in z and short + " Band 1 heart" not in z and short + " Band 2 heart" not in z
    lhbuild.write_map(rel, z)
    register([rel])
    return 2


def main():
    for m, short in MAPS.items():
        print(m, build(m, short), "leaders now carry their own death")


if __name__ == "__main__":
    main()
