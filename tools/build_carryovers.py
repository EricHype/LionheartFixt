"""Two choices that now reach later acts, not just the end slides. Release 3 of the post-0.99 plan.

The plan had four. Two failed the data: the only Hujark-like enemies in Alamut are the Old Man's summoned Cursed Elf shamans,
part of his fight, and nothing in act 5's dialogue mentions Sahar, Montserrat or the snakebreed. These two the game supports.

**The standard.** Break it at the Crossroads Siege and two of the archer groups on the road to England have deserted: they
stand aside and talk. Read from `Fixt Standard Broken` when the road is first visited, so it reaches a save that broke the
standard before installing, as long as it has not yet walked the road.

**The Khan.** Kill him and the Horde's bands fight with less heart afterwards: each goblin attacks slower, and the log says why.
Become his Champion and the bands keep their distance instead. Read when each map with a band is first visited. The Khan's
death had two records, `Fixt Khan Slain` from the Warrens and `Fixt Goblin Khan Dead` from act 8's gate; this keeps the first
and points everything at it.

A rerun is a no-op.

    python tools/build_carryovers.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balloon, delay, if_action, multi
from build_inquisition_slides import VARS, var_if
from build_shrine_repairs import register
from build_crossroads_standard import forget_specifier, specifier

ROAD = "Levels/6 Barcelona Attack/Crossroads to England map.zax"
BROKEN = VARS + "Fixt Standard Broken"
DESERTERS = "English Deserter"
TREE = "Levels/6 Barcelona Attack/Dialog/Fixt Deserters"
LINES = [("1 word", "Word came up the road from the crossroads. We heard, and we stopped."),
         ("2 priests", "The druid priests did this to us. They are waiting for you up the road."),
         ("3 home", "We are going home. Nobody here is going to stop you."),
         ("4 shrine", "Whatever is in that shrine, it wanted us. Take care it does not want you.")]
KHAN = VARS + "Fixt Khan Slain"
OLD_KHAN = VARS + "Fixt Goblin Khan Dead"
CHAMPION = "Perks/!Event Title Perks/Goblin Champion"
BANDS = ["Lake", "Plains", "Woodcutter Forest", "Barcelona Coast"]
BAND = "Horde Goblin"
GENERIC = ["Goblin Lake map", "Goblin upper right near node"]  # existing band names; quest-named goblins are left alone
HEARTLESS = "Without their Khan, the goblins here fight with less heart."
DISTANCE = "The goblins here know the Khan's Champion, and keep their distance."


def parts(z):
    return re.findall(r"(?ms)^\t\tLevel Part=\w+\r\n\t\t\{\r\n.*?^\t\t\}", z)


def once_on_arrival(name, action):
    timer = ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""),
                                       ("Action", multi([action, ("CDeactivateAction", [("Target Name", name)])])),
                                       ("Delay Between Actions", "600"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "3")])
    return lhbuild.entity(name, "1", [timer], "Editor/Position Marker", 100, 60)


def stand_aside(names, talk):
    out = [("CSetTargetTypeAction", [("Entity Name", names), ("Name To Target", ""), ("Valid Targets", "")]),
           ("CRemoveCategoryAction", [("Target Name", names), ("Categories To Remove", "Enemy")])]
    if talk:
        out += [forget_specifier(names), specifier(names, "GetCloseThenTalk", talk)]
    return out


def deserters():
    p = FX / ("Resources/" + TREE + ".DialogTree")
    if not p.exists():
        t = "CDialogTree" + CR + "{" + CR + "Name=English Deserter" + CR + "Portrait=!None" + CR + "Should Have Voiceovers=0" + CR + "Default Canceled Node Action=" + CR
        for n, x in LINES:
            t += "-" * 60 + CR + lhbuild.node(n, x, [])
        p.write_bytes((t + "}" + CR).encode("latin-1"))
    register(["Resources/" + TREE + ".DialogTree"])
    z = lhbuild.read(ROAD)
    if "New Name=" + DESERTERS + CR in z:
        return
    archers = [x for x in parts(z) if "CGeneratorAI" in x and re.search(r"(?m)^\t\t\tActive=1", x) and not re.search(r"New Name=[^\r\n]", x)
               and re.findall(r"Entity=([^\r\n]*)", x) and all(" Bow" in e for e in re.findall(r"Entity=([^\r\n]*)", x))]
    assert len(archers) >= 2, len(archers)
    new = z
    for x in archers[:2]:
        new = new.replace(x, re.sub(r"New Name=\r\n", "New Name=" + DESERTERS + CR, x, count=1))
    talk = ("CRandomAction", [("Action", ("Array", [("Item Count", str(len(LINES)))] + [("Action", balloon(TREE, n, "$trigger", "-80")) for n, _ in LINES]))])
    act = var_if(BROKEN, multi(stand_aside(DESERTERS, talk)), "")
    lhbuild.write_map(ROAD, lhbuild.add_parts(new, [once_on_arrival("Fixt the deserters", act)]))
    register([ROAD])


def khan_record():
    """One record of the Khan's death: act 8's gate and the Goblin King can point at Fixt Khan Slain."""
    for rel in ("Levels/8 Alamut/01 Desert Sprawl.zax", "Resources/Levels/Wilderness/Character Templates/Goblin King.can"):
        t = lhbuild.read(rel)
        if OLD_KHAN in t:
            lhbuild.write_map(rel, t.replace(OLD_KHAN, KHAN))
    old = FX / ("Resources/" + OLD_KHAN + ".DerivedCharacterAttribute")
    if old.exists():
        old.unlink()
        mods = FX.parent / "mod.json"
        text = mods.read_bytes().decode("utf8")
        nl = "\r\n" if "\r\n" in text else "\n"
        line = '    "Resources/' + OLD_KHAN + '.DerivedCharacterAttribute",' + nl
        if line in text:
            mods.write_bytes(text.replace(line, "").encode("utf8"))
    b = Path(__file__).resolve().parent / "build_alamut.py"
    s = b.read_bytes().decode("utf8")
    if 'KHAN_DEAD = VARS + "Fixt Goblin Khan Dead"' in s:
        b.write_bytes(s.replace('KHAN_DEAD = VARS + "Fixt Goblin Khan Dead"', 'KHAN_DEAD = VARS + "Fixt Khan Slain"  # one record of his death; see build_carryovers.py').encode("utf8"))


def bands():
    def slower():
        mod = ("CAddCharacterModifierToCharacterAction", [
            ("Modifier Description", ""), ("Modification is permanent", "1"), ("Character to modify", "$Trigger"),
            ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
                ("Modification Amount", ("CConstant", [("Constant Value", "-0.2")])), ("Modification amount is a percent", "0"),
                ("Allow Accumulation", "0"), ("Derived character attribute to modify", "Derived Character Attributes/Speed/Base Animation Speed Multiplier")]))])),
            ("OPTIONAL Duration", ""), ("Expression Context", "$Trigger")])
        once = ("CSeriesAction", [("Action", [("Action", mod), ("Action", ("CSucceedAction", [("Action", "")]))]),
                                  ("When Done", "Repeat Last Action"), ("Require Success To Advance", "0"), ("Next Action Index", "0")])
        return ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", once),
                                          ("Delay Between Actions", "600"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "0")])

    def note(text):
        return ("CPrintCombatTextAction", [("Text to print", text), ("Character to show text to", "Player1"), ("Emphasize", "0"), ("Suppress Duplicates", "1")])
    champion = ("CExpressionAction", [("Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [("Item Count", "1"), ("Perk To Check For", CHAMPION)]))])),
                                  ("Character to get attributes from", "Player1")])
    done = 0
    for m in BANDS:
        rel = "Levels/Wilderness Maps/" + m + ".zax"
        z = lhbuild.read(rel)
        if "Fixt the Horde's heart" in z:
            continue
        new = z
        for x in parts(z):
            e = re.findall(r"Entity=([^\r\n]*)", x)
            if "CGeneratorAI" in x and e and all(i.startswith("Monster Cans/Mongol Goblin") and "Shaman" not in i for i in e) and re.search(r"New Name=\r\n", x):
                new = new.replace(x, re.sub(r"New Name=\r\n", "New Name=" + BAND + CR, x, count=1))
                done += 1
        names = [n for n in [BAND] + GENERIC if "New Name=" + n + CR in new]
        if not names:
            continue
        BANDS_HERE = ", ".join(names)
        heartless = multi([("CAddAIAction", [("Target Name", BANDS_HERE), ("AI", slower()), ("Delay Between Adds", "0")]), note(HEARTLESS)])
        act = if_action(champion, multi(stand_aside(BANDS_HERE, "") + [note(DISTANCE)]), var_if(KHAN, heartless, ""))
        lhbuild.write_map(rel, lhbuild.add_parts(new, [once_on_arrival("Fixt the Horde's heart", act)]))
        register([rel])
    return done


def main():
    deserters()
    khan_record()
    print(bands(), "goblin generators carry the Horde's name")


if __name__ == "__main__":
    main()
