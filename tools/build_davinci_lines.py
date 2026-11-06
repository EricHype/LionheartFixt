"""The last four of DaVinci's unreachable recordings, each put where the scene already leaves room for it.

* `320 general surly response 3` closes the rudeness chain. Being rude to him a second time now gets it, from a flag
  either insult sets. Only the insult that can repeat needs the fork.
* `400 touch machines` replaces the second use of `400 davinci machine warning`. The quake's third step is the one that
  repeats forever and burns you, so "No! Not that button!" there was always the wrong line for a repeat offender.
* `800 davinci travel banter` plays on `davinci enters barcelona`, the one-shot trigger that fires when the player steps
  through the open portcullis and sends him in after them, so the player is always there to hear it. The existence
  check is there because that trigger can also fire on a later visit.
* `2030 give crossbow` is not a lost hand-over: vanilla's `710 found lens` already says it. The line goes to the one
  completion that has no voice, the rotary gear, ahead of Fixt's silent `902`, whose own "There" is cut to match.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_davinci_lines.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balloon, exists, if_action
from build_inquisition_slides import VARS, flag, write_var

TREE_PATH = "Levels/1 Barcelona/Dialog/Gate District/DaVinciBarcelona"
TREE = "Resources/" + TREE_PATH + ".DialogTree"
WORKSHOP = "Levels/1 Barcelona/DaVinci Workshop interior.zax"
GATE = "Levels/1 Barcelona/Gate District.zax"
REBUKED = VARS + "Fixt DaVinci Rebuked"
GEAR = "902 Fixt the gear fitted"
OLD_GEAR_TEXT = "Si, that is the profile! Hold the lamp. There - you feel that? <He sits back on his heels, delighted.> It will turn now."
NEW_GEAR_TEXT = "<He sits back on his heels, delighted.> Si, that is the profile! You feel that? It will turn now."


def rebuked_is(n):
    return B("CIsEqualTo", [
        ("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", REBUKED)])),
        ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", str(n))]))])


def tree():
    z = lhbuild.read(TREE)
    if "Go to node ID=320 general surly response 3" in z:
        return
    head = "Requirement=!None" + CR
    said = "Reply Text=And what makes you think that I want your *help*, old one?" + CR
    old = head + said + "Go to node ID=320 general surly response" + CR
    assert z.count(old) == 1
    new = (head + "Custom Requirement=" + rebuked_is(0) + said + "Go to node ID=320 general surly response" + CR +
           "Custom Action=" + B(*flag(REBUKED)) + CR +
           head + "Custom Requirement=" + rebuked_is(1) + said + "Go to node ID=320 general surly response 3" + CR)
    z = z.replace(old, new)
    old = "Go to node ID=320 general surly response 2" + CR
    assert z.count(old) == 1
    z = z.replace(old, old + "Custom Action=" + B(*flag(REBUKED)))

    old = "Go to node ID=" + GEAR + CR
    assert z.count(old) == 2
    z = z.replace(old, "Go to node ID=2030 give crossbow" + CR)
    old = "Node ID=2030 give crossbow" + CR + "Text=Ah! There! It is complete." + CR + "Should Have Voiceover=1" + CR
    assert z.count(old) == 1
    z = z.replace(old, old + CR + "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + GEAR + CR + "Is Default Reply=1" + CR)
    assert z.count(OLD_GEAR_TEXT) == 1
    z = z.replace(OLD_GEAR_TEXT, NEW_GEAR_TEXT)
    assert z.count(CR) == z.count("\n")
    (FX / TREE).write_bytes(z.encode("latin-1"))


def workshop():
    z = lhbuild.read(WORKSHOP)
    if "Node ID=400 touch machines" in z:
        return
    key = "Node ID=400 davinci machine warning" + CR
    i = z.index("\t\t\tName=machine quake" + CR)
    first = z.index(key, i)
    second = z.index(key, first + 1)
    assert z.index("When Done=Repeat Last Action", second) - second < 1300
    lhbuild.write_map(WORKSHOP, z[:second] + "Node ID=400 touch machines" + CR + z[second + len(key):])


def gate():
    z = lhbuild.read(GATE)
    if "Node ID=800 davinci travel banter" in z:
        return
    i = z.index("\t\t\tName=davinci enters barcelona" + CR)
    j = z.index("Enter Action=CMultipleActionsAction", i)
    k = z.index("Item Count=4" + CR, j)
    assert k - j < 200
    add = "Action=" + B(*if_action(exists("DaVinci"), balloon(TREE_PATH, "800 davinci travel banter", "DaVinci", "-80")))
    z = z[:k] + "Item Count=5" + CR + add + z[k + len("Item Count=4" + CR):]
    lhbuild.write_map(GATE, z)


def main():
    write_var(REBUKED, "Fixt DaVinci Rebuked", "1 means DaVinci has already reprimanded the player once for rudeness.")
    tree()
    workshop()
    gate()


if __name__ == "__main__":
    main()
