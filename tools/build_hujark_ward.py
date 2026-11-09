"""The Hujark acolytes ward their warriors. Release 4 of the post-0.99 plan, the first enemy role.

Act 5 is the largest repeat of the late game: 200-odd Hujark warrior generators against about 40 of acolytes. Huko says
the Hujark work magic "out of the ground and out of the blood", and the shamans are `Hujark Acolyte`, in generators of their
own, so the role was the game's before it was ours.

While any acolyte on a map lives, every warrior there is warded: each refreshes a short armour bonus every four seconds, so
the ward lapses by itself within seconds of the last acolyte dying and nothing has to be taken off. The log says so on
arrival and when it breaks. A map's names are its own, so `Hujark Acolyte` alive on one map wards only that map.

Warriors keep the names Fixt's ally and safe-conduct scripts already aim at; a nameless warrior generator takes its first
can's display name, as `build_spawn_names.py` does. On the allied routes the warriors are not hostile, so the ward does nothing.

A rerun is a no-op.

    python tools/build_hujark_ward.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR, FX, if_action, multi
from build_shrine_repairs import register

ACT = "Levels/5 Nostrodomus/"
MAPS = ["01 Heart Entrance", "02 Clan of the Hand A", "03 Tourniquet of Pain", "04 Clan of the Skull B",
        "07 Cave 2", "08 Cave 3", "09 Cave 4", "10 Cave 5"]
ACOLYTE = "Hujark Acolyte"
WARD_LINE = "The Hujark acolytes here are chanting, and a ward hangs over their warriors."
BROKEN_LINE = "The last acolyte falls, and the ward over the Hujark warriors breaks."


def parts(z):
    return re.findall(r"(?ms)^\t\tLevel Part=\w+\r\n\t\t\{\r\n.*?^\t\t\}", z)


def entities(x):
    return [e.split("/")[-1] for e in re.findall(r"Entity=([^\r\n]*)", x)]


def display(x):
    for e in re.findall(r"Entity=([^\r\n]*)", x):
        try:
            u = re.findall(r"User Assigned Name=([^\r\n]*)", lhbuild.read("Resources/" + e + ".can"))
        except Exception:
            continue
        if u and u[0]:
            return u[0]
    return ""


def ward_ai():
    """On each warrior: every four seconds, while an acolyte lives here, a six-second armour bonus."""
    bonus = ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", "Hujark ward"), ("Modification is permanent", "0"), ("Character to modify", "$Trigger"),
        ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", ("CConstant", [("Constant Value", "20")])), ("Modification amount is a percent", "1"),
            ("Allow Accumulation", "0"), ("Derived character attribute to modify", "Derived Character Attributes/(AC) Armor Class")]))])),
        ("OPTIONAL Duration", ("CConstant", [("Constant Value", "6")])), ("Expression Context", "$Trigger")])
    alive = ("CIsAliveAction", [("Name To Check For", ACOLYTE), ("Desired Minimum Count", "1")])
    return ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", if_action(alive, bonus)),
                                      ("Delay Between Actions", "4"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "1")])


def note(text):
    return ("CPrintCombatTextAction", [("Text to print", text), ("Character to show text to", "Player1"), ("Emphasize", "0"), ("Suppress Duplicates", "1")])


def build(rel):
    z = lhbuild.read(rel)
    if "Name=Fixt the Hujark ward" + CR in z:
        return 0, ""
    new = z
    warriors = set()
    acolytes = 0
    for x in parts(z):
        if "CGeneratorAI" not in x:
            continue
        e = entities(x)
        full = re.findall(r"Entity=([^\r\n]*)", x)
        # Only the Hujark's own cans: act 5's English invaders are `Nos Soldier`, and must not be warded.
        if not e or not all(f.startswith("Monster Cans/Cursed Elves/") for f in full):
            continue
        nn = re.search(r"New Name=([^\r\n]*)", x)
        if all("Shaman" in i for i in e):
            acolytes += 1
            if nn and not nn.group(1):
                new = new.replace(x, re.sub(r"New Name=\r\n", "New Name=" + ACOLYTE + CR, x, count=1))
        else:
            name = nn.group(1) if nn else ""
            if "voice" in name.lower():  # balloon anchors, not fighters
                continue
            if not name:
                name = display(x)
                if not name:
                    continue
                new = new.replace(x, re.sub(r"New Name=\r\n", "New Name=" + name + CR, x, count=1))
            warriors.add(name)
    if not acolytes or not warriors:
        return 0, ""
    names = ", ".join(sorted(warriors))
    start = multi([("CAddAIAction", [("Target Name", names), ("AI", ward_ai()), ("Delay Between Adds", "0")]), note(WARD_LINE)])
    timer = ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""),
                                       ("Action", multi([start, ("CDeactivateAction", [("Target Name", "Fixt the Hujark ward")])])),
                                       ("Delay Between Actions", "600"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "3")])
    gone = if_action(("CNotAction", [("Action", ("CIsAliveAction", [("Name To Check For", ACOLYTE), ("Desired Minimum Count", "1")]))]),
                     multi([note(BROKEN_LINE), ("CDeactivateAction", [("Target Name", "Fixt the Hujark ward watch")])]))
    watch = ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", gone),
                                       ("Delay Between Actions", "2"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "10")])
    new = lhbuild.add_parts(new, [lhbuild.entity("Fixt the Hujark ward", "1", [timer], "Editor/Position Marker", 120, 60),
                                  lhbuild.entity("Fixt the Hujark ward watch", "1", [watch], "Editor/Position Marker", 140, 60)])
    lhbuild.write_map(rel, new)
    register([rel])
    return acolytes, names


def main():
    for m in MAPS:
        n, names = build(ACT + m + ".zax")
        print(m, n, "acolyte generators;", names[:120])


if __name__ == "__main__":
    main()
