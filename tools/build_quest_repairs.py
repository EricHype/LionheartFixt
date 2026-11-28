"""Three quests that could not end, or a step nobody could take. See docs/quest-reach.md.

`tools/quest_reach.py` reads every quest action in the game against the quest files and against what
a player can reach. Read one by one, three findings are defects with a repair the game itself shows:

  * **Q1, the road to Galileo (vanilla).** Cedric and the Inquisition Pit set state `J5WOL4C2` on
    *Bind Spirit to Rod*, and Galileo's own opening and return lines check it there. Two requirement
    cans check the same ID on *Initiation Quest for the Wielders* -- which has a state of that ID,
    and nothing ever sets it. So Galileo's three mid-conversation copies of *"Cedric told me to seek
    you out to obtain a spirit for my wand"* never appeared, and the Prisoner Wielder's *"I'm looking
    for Galileo."* never appeared in any game: all four of its copies use the broken can. Both cans
    now name *Bind Spirit to Rod*.
  * **Q2, Travel to Montserrat (Fixt).** In vanilla every line that starts it was unreachable. Fixt's
    Jafar work made three of them reachable, and nothing completes it, so a Knight of Saladin carried
    it to the Temple District siege, which fails it. Every other faction's Montserrat quest completes
    in the same four replies -- Brother Montgomerie's two at `50 Bro michelle`, and Sahar's at
    `50 her word` and `60 the ring is on your hand` -- so it now completes there too.
  * **Q3, Obtain Darkwood from the Wilderness (vanilla).** Darkwood Cave starts it and nothing ends it,
    so it sat open until the siege failed it. The Darkwood's own pickup already advances both
    factions' rod quests; it now completes this one as well.

Q2 and Q3 add a completion, guarded by `CWasQuestEverActivatedAction`, so a player who never had the
quest gets no journal entry for it. A rerun is a no-op.

    python tools/build_quest_repairs.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR, DASH
from build_shrine_repairs import register

sys.path.insert(0, str(lhbuild.MODTOOLS))
import dialogtree_format as dt
import resource_format

REQ = "Resources/Levels/1 Barcelona/Dialog/Temple District/Requirements/"
CANS = [REQ + "Galileo Player on quest to get spirit wand.can", REQ + "Prisoner Wielder Player looking for Galileo.can"]
WRONG = "Quest=Levels/1 Barcelona/Quests/Calle Perdida/Wielder Initiation Quests/Initiation Quest for the Wielders"
RIGHT = "Quest=Levels/1 Barcelona/Quests/Calle Perdida/Wielder Initiation Quests/Bind Spirit to Rod"

TRAVEL = "Levels/1 Barcelona/Quests/Gate District/Knights Saladin Initiation/Travel to Montserrat"
MONT = "Resources/Levels/2 Montserrat/Dialog/"
# (tree, node, reply text start) -- the four replies that complete the other factions' Montserrat quests
TRAVEL_AT = [
    (MONT + "Brother Montgomerie.DialogTree", "50 Bro michelle", "It's about time you perished."),
    (MONT + "Brother Montgomerie.DialogTree", "50 Bro michelle", "I will find Brother Michel. Rest now, warrior."),
    (MONT + "Sahar.DialogTree", "50 her word", "<Take the ring.>"),
    (MONT + "Sahar.DialogTree", "60 the ring is on your hand", "Which road north?"),
]

DARKWOOD_ITEM = "Resources/Inventory/Specific Item Cans/Quest Items/Darkwood.InventoryItem"
DARKWOOD = "Levels/1 Barcelona/Quests/Temple District/Obtain Darkwood from the Wilderness"


def guarded_complete(quest, indent=""):
    """CIfAction: complete `quest` only if it was ever started. Lines without the leading 'Action='."""
    t = indent
    lines = ["CIfAction", "{",
             "\tIf=CWasQuestEverActivatedAction", "\t{", "\t\tQuest=" + quest, "\t}",
             "\tThen=CSetQuestSatusToCompletedAction", "\t{", "\t\tQuest=" + quest, "\t}",
             "\tElse=", "\tReturn failure if the If failes=0", "}"]
    if indent is None:
        return [l.replace("\t", "") for l in lines]
    return [t + l if i else l for i, l in enumerate(lines)]


def q1():
    done = []
    for rel in CANS:
        t = lhbuild.read(rel)
        if RIGHT in t:
            continue
        lines = t.split(CR)
        hit = [i for i, l in enumerate(lines) if l.strip() == WRONG]
        assert len(hit) == 1, (rel, len(hit))
        i = hit[0]
        lines[i] = lines[i][:len(lines[i]) - len(lines[i].lstrip())] + RIGHT
        assert "State=J5WOL4C2" in lines[i + 1]
        new = CR.join(lines)
        assert resource_format.parse_resource_text(new).to_text() == new
        (lhbuild.FX / rel).parent.mkdir(parents=True, exist_ok=True)
        (lhbuild.FX / rel).write_bytes(new.encode("latin-1"))
        done.append(rel)
    return done


def q2():
    done = []
    by_tree = {}
    for rel, node, start in TRAVEL_AT:
        by_tree.setdefault(rel, []).append((node, start))
    action = ["Action=" + guarded_complete(TRAVEL, None)[0]] + guarded_complete(TRAVEL, None)[1:]
    for rel, reps in by_tree.items():
        before = lhbuild.read(rel)
        segs = before.split(CR + DASH + CR)
        for node, start in reps:
            si = [i for i, s in enumerate(segs) if s.split(CR, 1)[0] == "Node ID=" + node or
                  ("Node ID=" + node + CR) in s.split(CR + CR)[0] + CR]
            assert len(si) == 1, (rel, node, si)
            chunks = segs[si[0]].split(CR + CR)
            ci = [i for i, c in enumerate(chunks) if c.startswith("Requirement=") and
                  any(l.startswith("Reply Text=" + start) for l in c.split(CR))]
            assert len(ci) == 1, (rel, node, start, ci)
            lines = chunks[ci[0]].split(CR)
            if any(l == "Quest=" + TRAVEL for l in lines):
                continue
            a = lines.index("Custom Action=CMultipleActionsAction")
            assert lines[a + 1:a + 4] == ["{", "Action=Array", "{"] and lines[a + 4].startswith("Item Count=")
            n = int(lines[a + 4][len("Item Count="):])
            lines[a + 4] = "Item Count=%d" % (n + 1)
            lines[a + 5:a + 5] = action
            chunks[ci[0]] = CR.join(lines)
            segs[si[0]] = (CR + CR).join(chunks)
        t = (CR + DASH + CR).join(segs)
        if t == before:
            continue
        a, b = dt.parse(before), dt.parse(t)
        assert [len(n.replies) for n in a.nodes] == [len(n.replies) for n in b.nodes]
        assert "\n" not in t.replace(CR, "")
        (lhbuild.FX / rel).write_bytes(t.encode("latin-1"))
        done.append(rel)
    return done


def q3():
    rel = DARKWOOD_ITEM
    t = lhbuild.read(rel)
    if "Quest=" + DARKWOOD in t:
        return []
    lines = t.split(CR)
    p = [i for i, l in enumerate(lines) if l.strip() == "Pick Up Action=CMultipleActionsAction"]
    assert len(p) == 1
    i = p[0]
    assert lines[i + 1].strip() == "{" and lines[i + 2].strip() == "Action=Array" and lines[i + 3].strip() == "{"
    assert lines[i + 4].strip().startswith("Item Count=")
    ind = lines[i + 4][:len(lines[i + 4]) - len(lines[i + 4].lstrip())]
    n = int(lines[i + 4].strip()[len("Item Count="):])
    assert lines[i + 5] == ind + "Action=CIfAction", "the first item is the rod-quest CIfAction this clones"
    lines[i + 4] = ind + "Item Count=%d" % (n + 1)
    block = guarded_complete(DARKWOOD, ind)
    lines[i + 5:i + 5] = [ind + "Action=" + block[0]] + block[1:]
    new = CR.join(lines)
    assert resource_format.parse_resource_text(new).to_text() == new
    (lhbuild.FX / rel).parent.mkdir(parents=True, exist_ok=True)
    (lhbuild.FX / rel).write_bytes(new.encode("latin-1"))
    return [rel]


def main():
    done = q1() + q2() + q3()
    register([rel for rel in CANS + [r for r, _, _ in TRAVEL_AT] + [DARKWOOD_ITEM] if (lhbuild.FX / rel).exists()])
    print("quest repairs:", done or "none")


if __name__ == "__main__":
    main()
