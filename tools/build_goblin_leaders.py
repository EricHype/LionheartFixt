"""Goblin bands have war leaders, and lose heart when he falls. Release 6 of the post-0.99 plan.

The maintainer's correction stands behind this one: goblins are led by warriors and the Khan, not by their shamans. The plan
named the vanilla Patrol Leader can, but that is a weak goblin (38 XP) and already the Crossroads' named NPC. The hat goblins
are what this project's own notes call the goblin officer (`Goblin Striker`, 94 to 186 XP, their own hat model), so the war
leader is a copy of each hat tier with its own display name, `Goblin War Leader`, and nothing else changed.

On the Lake, the Plains, Woodcutter Forest and the Barcelona Coast, the two Horde bands farthest apart each take a band name
and get a war leader beside them. When he falls, his band loses heart: every goblin of it attacks slower, permanently, and the
log says why. It stacks with the Khan's death, and the Khan carryover's lists take the new band names so the Champion's
stand-aside still covers them.

A rerun is a no-op.

    python tools/build_goblin_leaders.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, if_action, multi
from build_shrine_repairs import register
from build_shrine_druids import replace_groups, pos

MAPS = {"Lake": "Lake", "Plains": "Plains", "Woodcutter Forest": "Woodcutter", "Barcelona Coast": "Coast"}
HAT = "Monster Cans/Mongol Goblin Hat"
LEADER_CAN = "Levels/Wilderness/Character Templates/Fixt Goblin War Leader"
TIERS = ["", " Tough", " Super", " Super"]
LEADER = "Goblin War Leader"
LOST_HEART = "Their war leader is dead, and the goblins around him lose heart."


def parts(z):
    return re.findall(r"(?ms)^\t\tLevel Part=\w+\r\n\t\t\{\r\n.*?^\t\t\}", z)


def leader_cans():
    for t in ("", " Tough", " Super"):
        rel = "Resources/" + LEADER_CAN + t + ".can"
        p = FX / rel
        if p.exists():
            continue
        c = lhbuild.read("Resources/" + HAT + t + ".can")
        c, n = re.subn(r"User Assigned Name=Goblin Striker", "User Assigned Name=" + LEADER, c)
        assert n >= 1
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(c.encode("latin-1"))
        register([rel])


def leader_groups():
    def group(mojo, can):
        return ("Group", ("CGeneratorAIGroup", [("Max Party Mojo", mojo), ("Quantity to generate min", "1"), ("Quantity to generate max", "1"),
                                                ("Things to Generate", ("Array", [("Item Count", "1"), ("Thing to Generate", ("CSpawnableCannedEntity", [("Weight", "1"), ("Entity", can)]))]))]))
    items = [group(m, LEADER_CAN + t) for m, t in zip(("16", "23", "40", "60"), TIERS)]
    return "Groups=" + B("Array", [("Item Count", str(len(items)))] + items).rstrip()


def heartless(band):
    mod = ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", "lost heart"), ("Modification is permanent", "1"), ("Character to modify", "$Trigger"),
        ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", ("CConstant", [("Constant Value", "-0.25")])), ("Modification amount is a percent", "0"),
            ("Allow Accumulation", "0"), ("Derived character attribute to modify", "Derived Character Attributes/Speed/Base Animation Speed Multiplier")]))])),
        ("OPTIONAL Duration", ""), ("Expression Context", "$Trigger")])
    once = ("CSeriesAction", [("Action", [("Action", mod), ("Action", ("CSucceedAction", [("Action", "")]))]),
                              ("When Done", "Repeat Last Action"), ("Require Success To Advance", "0"), ("Next Action Index", "0")])
    ai = ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", once),
                                    ("Delay Between Actions", "600"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "0")])
    return ("CAddAIAction", [("Target Name", band), ("AI", ai), ("Delay Between Adds", "0")])


def build(map_name, short):
    rel = "Levels/Wilderness Maps/" + map_name + ".zax"
    z = lhbuild.read(rel)
    if "New Name=" + short + " Band 1" + CR in z:
        return 0
    bands = [x for x in parts(z) if "CGeneratorAI" in x and "New Name=Horde Goblin" + CR in x]
    if len(bands) < 2:
        return 0
    a = max(bands, key=len)
    b = max((x for x in bands if x is not a), key=lambda x: (pos(x)[0] - pos(a)[0]) ** 2 + (pos(x)[1] - pos(a)[1]) ** 2)
    new = z
    extra = []
    for n, x in enumerate((a, b), 1):
        band = short + " Band " + str(n)
        new = new.replace(x, x.replace("New Name=Horde Goblin" + CR, "New Name=" + band + CR, 1))
        g = replace_groups(x, leader_groups())
        g = g.replace("New Name=Horde Goblin" + CR, "New Name=" + band + " Leader" + CR, 1)
        g = re.sub(r"(?m)^(\t\t\t)Name=[^\r\n]*", lambda m: m.group(1) + "Name=Fixt " + band + " war leader", g, count=1)
        g = re.sub(r"(?m)^(\t\t\t)Active=\d", lambda m: m.group(1) + "Active=1", g, count=1)
        extra.append(g.replace("\t\tLevel Part=", "Level Part=", 1) + CR)
        watch = "Fixt " + band + " heart"
        fell = if_action(("CNotAction", [("Action", ("CIsAliveAction", [("Name To Check For", band + " Leader"), ("Desired Minimum Count", "1")]))]),
                         multi([heartless(band), ("CPrintCombatTextAction", [("Text to print", LOST_HEART), ("Character to show text to", "Player1"),
                                                                            ("Emphasize", "0"), ("Suppress Duplicates", "0")]),
                                ("CDeactivateAction", [("Target Name", watch)])]))
        timer = ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", fell),
                                           ("Delay Between Actions", "2"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "10")])
        px, py = pos(x)
        extra.append(lhbuild.entity(watch, "1", [timer], "Editor/Position Marker", px, py + 40))
    # the Khan carryover's lists, so his death and his Champion still reach these bands
    new = re.sub(r"((?:Target Name|Entity Name)=)Horde Goblin(?=[,\r])", lambda m: m.group(1) + "Horde Goblin, " + short + " Band 1, " + short + " Band 2, " + short + " Band 1 Leader, " + short + " Band 2 Leader", new)
    lhbuild.write_map(rel, lhbuild.add_parts(new, extra))
    register([rel])
    return 2


def main():
    leader_cans()
    for m, short in MAPS.items():
        print(m, build(m, short), "war leaders")


if __name__ == "__main__":
    main()
