"""Hints for the systems a player could miss. Release 2 of the post-0.99 plan.

The maintainer's rule for these: show, do not instruct. A hint says what the player would notice, never what to do about it.

* The druids' hold: a journal entry on the first visit to Temple Initiate says the soldiers seem spellbound, and Sir Roger
  says the same if he is with you. It is a sub-quest of the act's own quest, so the parent's state is never touched.
* The draught: a soldier who reaches for one shows <Reaches for a potion> over his head, so the moment can be seen.
* The valve: the line about it belongs to whoever finds it, so it plays when the search reveals the valve, not before.

Persuasion needs no entry: a player who can talk a dragon down will see the option. A rerun is a no-op.

    python tools/build_hints.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, delay, if_action, multi
from build_shrine_repairs import register

SHRINE_Q = "Levels/7 English Shrine/Quests/Stop the Druids"
HOLD_Q = "Levels/7 English Shrine/Quests/Fixt The Spellbound Soldiers"
HOLD_ID = "FXHOLD01"
HOLD_NAME = "The Spellbound Soldiers"
HOLD_TEXT = "The English soldiers in the shrine fight with blank faces, as though spellbound. Their druid priests stand among them."
TEMPLE = "Levels/7 English Shrine/02 Temple Initiate.zax"
COMPANIONS = "Levels/7 English Shrine/Dialog/Fixt Shrine Companions"
ROGER = ("20 roger spellbound", "Look at their eyes, Lionheart. These are not men following orders. Something has hold of them.")
SOLDIER_TREE = "Levels/7 English Shrine/Dialog/Fixt Soldier Barks"
POTION = ("90 reaches for a potion", "<Reaches for a potion>")
ACID = "Levels/8 Alamut/05 Acid Wash.zax"
ACID_TREE = "Levels/8 Alamut/Dialog/The Acid Wash"
VALVE = ("6 the valve", "Behind a loose stone at the foot of the wall, a hand valve, its wheel worn bright by somebody's palm.")


def add_node(tree, nid, text):
    p = FX / ("Resources/" + tree + ".DialogTree")
    t = p.read_bytes().decode("latin-1")
    if "Node ID=" + nid + CR in t:
        return
    end = t.rindex("}")
    p.write_bytes((t[:end] + "-" * 60 + CR + lhbuild.node(nid, text, []) + t[end:]).encode("latin-1"))


def journal():
    p = FX / ("Resources/" + HOLD_Q + ".Quest.txt")
    if not p.exists():
        q = ("CQuestDefinition" + CR + "{" + CR + "\tName=" + HOLD_NAME + CR + "\tStates=Array" + CR + "\t{" + CR + "\t\tItem Count=1" + CR +
             "\t\tState=CQuestStateDefinition" + CR + "\t\t{" + CR + "\t\t\tText=" + HOLD_TEXT + CR + "\t\t\tID=" + HOLD_ID + CR + "\t\t}" + CR +
             "\t}" + CR + "\tSub-Quest of=" + SHRINE_Q + CR + "}" + CR)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(q.encode("latin-1"))
    register(["Resources/" + HOLD_Q + ".Quest.txt"])
    add_node(COMPANIONS, *ROGER)
    z = lhbuild.read(TEMPLE)
    name = "Fixt spellbound hint"
    if "Name=" + name + CR in z:
        return
    alive = ("CIsAliveAction", [("Name To Check For", "Sir Roger Templeton"), ("Desired Minimum Count", "1")])
    steps = [("CActivateQuestStateAction", [("Quest", HOLD_Q), ("State", HOLD_ID)]),
             delay("2", if_action(alive, lhbuild.balloon(COMPANIONS, ROGER[0], "Sir Roger Templeton", "-80"))),
             ("CDeactivateAction", [("Target Name", name)])]
    timer = ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", multi(steps)),
                                       ("Delay Between Actions", "600"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "4")])
    lhbuild.write_map(TEMPLE, lhbuild.add_parts(z, [lhbuild.entity(name, "1", [timer], "Editor/Position Marker", 80, 60)]))


def potion():
    """Beside the draught's start, in each of the 12 cans: a balloon on the man himself."""
    add_node(SOLDIER_TREE, *POTION)
    say = ("CDisplayDialogBalloonAction", [("Dialog Tree File", SOLDIER_TREE), ("Node ID", POTION[0]), ("Name of Position", "$Trigger"),
                                          ("Position Offset", "0.000000,-80.000000"), ("After Action", ""), ("Include In Log", "0")])
    for f in sorted((FX / "Resources/Monster Cans/English Enemies").glob("Soldier[34]*.can")):
        rel = f.relative_to(FX).as_posix()
        c = lhbuild.read(rel)
        if POTION[0] in c:
            continue
        k = c.index("Categories to add=Scripted Custom 2")
        a = c.rindex("Action=CAddCategoryAction", 0, k)
        s = c.rindex(CR, 0, a) + len(CR)
        arr = c.rindex("Item Count=", 0, a)
        m = re.match(r"Item Count=(\d+)", c[arr:])
        c = c[:arr] + "Item Count=" + str(int(m.group(1)) + 1) + c[arr + m.end():]
        s = c.index("Action=CAddCategoryAction", arr)
        c = c[:s] + "Action=" + B(*say) + c[s:]
        lhbuild.write_map(rel, c)


def valve():
    add_node(ACID_TREE, *VALVE)
    z = lhbuild.read(ACID)
    i = z.index("\t\t\tName=Fixt the sluice valve" + CR)
    a = z.rindex("Level Part=", 0, i)
    e = balanced(z, a)
    p = z[a:e]
    if VALVE[0] in p:
        return
    r = p.index("Reveal Action=CMultipleActionsAction")
    m = re.compile(r"Item Count=(\d+)\r\n").search(p, r)
    say = lhbuild.balloon(ACID_TREE, VALVE[0], "$Trigger", "-60")
    q = p[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + "Action=" + B(*say) + p[m.end():]
    lhbuild.write_map(ACID, z[:a] + q + z[e:])


def main():
    journal()
    potion()
    valve()
    print("hints in")


if __name__ == "__main__":
    main()
