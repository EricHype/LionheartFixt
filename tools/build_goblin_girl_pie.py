"""The Goblin Girl goes away to bake the pie, and stops asking about the woodcutter once she has. Reported from play after
0.99.31: "goblin girl asks about the woodcutter again after I've given her the liver and gotten the pie", and then "when
the goblin girl goes to make the pie, it should fade to black before coming back to give you the pie".

**She asked again.** Her click in `Goblin Warrens` (`Goblin Girl Generator`, wired by Fixt in 988b7e0) picks her greeting
from the flags: once `Woodcutter Dead` is set it opens `200 Returning after killing the woodsman` on every visit, *"How
many innocents did you kill? Did you bring Rakeb the eyes? What did you bring me?"*. After the pie its liver reply is
gated off, and what is left is *"I pulverized him so thoroughly..."*, a lie about a liver she has just cooked, and the
rejection. The map is saved, so the fix goes through her tree:

- **Giving the pie swaps her click.** Both replies that hand it over (`225 Liver pie` and `227 momma's seasoning`) replace
  her `CAIInteractionSpecifier` with a copy of the map's own, one change made: once `Gave the Goblin Girl the Liver` is set
  it opens the new `205 after the pie`. Remove-then-add is vanilla's way to swap a click (`engine-notes.md`, "A click
  reads the first specifier").
- **A save that already has the pie** opens 200 once more. It now leads with *"I have your pie already, remember?"*, gated
  on the liver flag, which goes to 205 and makes the same swap. *"I pulverized him..."* is gated off once the liver is given.
- `205 after the pie` carries `290 follow 3`'s two replies verbatim, so she can still join or stay.

**The pie took no time.** `220 Liver` says *"Don't leave town, I'll be right back!"* and its one blank reply went straight
to `225 Liver pie`. Its design note asks for her to run off and come back. The reply now ends the conversation, holds the
scene (`CBeginNonInteractiveSequenceAction`), fades the screen down for two seconds and reopens her tree at 225, which is
vanilla's own way to pass the time a job takes: the blacksmith's Lionshield reply fades down and comes back with the
shield.

Both the swap and the reopen name this tree, and a tree that names its own file hangs the loader, so each goes through a
can.

A rerun is a no-op.

    python tools/build_goblin_girl_pie.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR
from build_shrine_repairs import register
from build_troll_choices import add_node, node_span, reply_start, VARS

TREE = "Resources/Levels/Wilderness/Dialog/GoblinGirl.DialogTree"
MAP = "Levels/Wilderness Maps/Goblin Warrens.zax"
TREE_REF = "Levels/Wilderness/Dialog/GoblinGirl"
SWAP_REF = "Common Objects and Scripts/Fixt Dialog Indirection/Goblin Girl after the pie"
BACK_REF = "Common Objects and Scripts/Fixt Dialog Indirection/Goblin Girl brings the pie"
SWAP_CAN, BACK_CAN = "Resources/" + SWAP_REF + ".can", "Resources/" + BACK_REF + ".can"
LIVER = VARS + "Gave the Goblin Girl the Liver"
NEW = "205 after the pie"
PIE_NODE = "225 Liver pie"
TEXT = ("You came back! Did you eat the pie yet? Momma keeps asking if you ate the pie. "
        "She asks it very nicely, which is not like momma at all.")
PIE = ("Custom Action=CUseCannedActionAction" + CR + "{" + CR +
       "Canned Object=Levels/Wilderness/Quests/Give the Liver Pie" + CR + "}" + CR)
PULVERIZED = "Reply Text=I'm sorry, I pulverized him so thoroughly that there just wasn't anything left." + CR
ALREADY = "I have your pie already, remember?"
TO_PIE = "Reply Text=" + CR + "Go to node ID=" + PIE_NODE + CR


def flat(s):
    return CR.join(l.lstrip("\t") for l in s.split(CR))


def use(ref):
    return "CUseCannedActionAction" + CR + "{" + CR + "Canned Object=" + ref + CR + "}" + CR


def liver(op, val):
    return (op + CR + "{" + CR + "Operand1=CVariableDerivedCharacterAttribute" + CR + "{" + CR + "Character Attribute=" + LIVER +
            CR + "}" + CR + "Operator=" + CR + "Operand2=CConstant" + CR + "{" + CR + "Constant Value=" + val + CR + "}" + CR + "}" + CR)


def specifier():
    """The map's click for her, flattened, with the after-the-pie greeting first."""
    z = lhbuild.read(MAP)
    g = z.index("\tName=Goblin Girl Generator" + CR)
    a = z.index("AI=CAIInteractionSpecifier" + CR, g)
    spec = flat(z[a + len("AI="):lhbuild.balanced(z, a)]) + CR
    k = spec.index("Action=CIfAction" + CR)
    assert spec[:k].endswith("Item Count=2" + CR) and "Node ID=200 Returning after killing the woodsman " + CR in spec
    old_if = spec[k + len("Action="):lhbuild.balanced(spec, k)] + CR
    new_if = ("CIfAction" + CR + "{" + CR + "If=CExpressionAction" + CR + "{" + CR + "Expression=" + liver("CIsGreaterThanOrEqual", "1") +
              "Character to get attributes from=$Instigator" + CR + "}" + CR +
              "Then=CDisplayDialogTreeAction" + CR + "{" + CR + "Dialog Tree File=" + TREE_REF + CR + "Node ID=" + NEW + CR +
              "Speaker=$trigger" + CR + "Player Being Spoken To=$Instigator" + CR + "}" + CR +
              "Else=" + old_if + "Return failure if the If failes=0" + CR + "}" + CR)
    return spec[:k] + "Action=" + new_if + spec[k + len("Action=") + len(old_if):]


def build_cans():
    if (lhbuild.FX / SWAP_CAN).exists():
        return 0
    swap = ("CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR +
            "Action=CRemoveAIAction" + CR + "{" + CR + "Target Name=Goblin Girl" + CR + "AI=CAIInteractionSpecifier" + CR +
            "Delay Between Removes=0" + CR + "}" + CR +
            "Action=CAddAIAction" + CR + "{" + CR + "Target Name=Goblin Girl" + CR + "AI=" + specifier() +
            "Delay Between Adds=0" + CR + "}" + CR + "}" + CR + "}" + CR)
    back = ("CDisplayDialogTreeAction" + CR + "{" + CR + "Dialog Tree File=" + TREE_REF + CR + "Node ID=" + PIE_NODE + CR +
            "Speaker=Goblin Girl" + CR + "Player Being Spoken To=Player1" + CR + "}" + CR)
    for path, obj in ((SWAP_CAN, swap), (BACK_CAN, back)):
        lhbuild.write_map(path, "CCannedObject" + CR + "{" + CR + "Object=" + obj + "}" + CR)
    register([SWAP_CAN, BACK_CAN])
    return 2


def away():
    """220's reply: she goes off to bake, the screen fades, and she comes back with the pie."""
    return ("Reply Text=" + CR + "Go to node ID=" + CR +
            "Custom Action=CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=4" + CR +
            "Action=CBeginNonInteractiveSequenceAction" + CR + "{" + CR + "Options=CNonInteractiveSequence" + CR + "{" + CR +
            "Pause Characters=1" + CR + "Disable Player Controls=1" + CR + "Can Fast Forward=1" + CR + "}" + CR + "}" + CR +
            "Action=CFadeScreenDownAction" + CR + "{" + CR + "Time Until Auto Fade Up=2" + CR + "}" + CR +
            "Action=CDelayAction" + CR + "{" + CR + "Next Action=CEndNonInteractiveSequenceAction" + CR + "{" + CR + "}" + CR +
            "Delay=2.01" + CR + "Plus or Minus=0" + CR + "Forget Trigger=0" + CR + "}" + CR +
            "Action=CDelayAction" + CR + "{" + CR + "Next Action=" + use(BACK_REF) +
            "Delay=2" + CR + "Plus or Minus=0" + CR + "Forget Trigger=0" + CR + "}" + CR +
            "}" + CR + "}" + CR + "Is Default Reply=1" + CR)


def build_tree():
    t = lhbuild.read(TREE)
    if "Node ID=" + NEW + CR in t:
        return 0
    # the pie hand-overs swap her click
    assert t.count(PIE) == 2, t.count(PIE)
    t = t.replace(PIE, "Custom Action=CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR +
                  "Action=" + use("Levels/Wilderness/Quests/Give the Liver Pie") + "Action=" + use(SWAP_REF) + "}" + CR + "}" + CR)
    # 220: away to bake, and back
    i, j = node_span(t, "220 Liver")
    blk = t[i:j]
    assert blk.count(TO_PIE) == 1 and blk.count("Reply Text=") == 1 and "Is Default Reply" not in blk
    t = t[:i] + blk.replace(TO_PIE, away()) + t[j:]
    # node 200: a way out for a save that already has the pie, and no lie about the liver
    i, j = node_span(t, "200 Returning after killing the woodsman ")
    blk = t[i:j]
    assert blk.count(PULVERIZED) == 1 and blk.count("Reply Text=") == 3
    blk = blk.replace("Requirement=!None" + CR + PULVERIZED,
                      "Requirement=!None" + CR + "Custom Requirement=" + liver("CIsLessThan", "1") + PULVERIZED)
    first = blk.index(CR + CR + "Requirement=") + len(CR + CR)
    out = ("Requirement=!None" + CR + "Custom Requirement=" + liver("CIsGreaterThanOrEqual", "1") +
           "Reply Text=" + ALREADY + CR + "Go to node ID=" + NEW + CR + "Custom Action=" + use(SWAP_REF) + CR)
    t = t[:i] + blk[:first] + out + blk[first:] + t[j:]
    # 205 takes 290's two replies
    a, b = node_span(t, "290 follow 3")
    k = reply_start(t, "290 follow 3", "Stay with your momma.")
    replies = t[k:b].rstrip(CR) + CR
    assert replies.count("Reply Text=") == 2 and "CSetCompanionAction" in replies
    t = add_node(t, NEW, TEXT, [replies])
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    register([TREE])
    return 1


def main():
    print("cans:", build_cans(), "| tree:", build_tree())


if __name__ == "__main__":
    main()
