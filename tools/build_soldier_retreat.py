"""A wounded English soldier falls back to his druids, and comes back healed. Release 0.99.11.

The engine has a retreat and never uses it. CSkeletonAI registers `Retreat when` (+0xA4, "% Health or less"), a
`Retreat Start Action` (+0xA8) and a Retreat state, 3; the state setter (0x473b00) fires the start action on entering it,
but none of its 31 callers ever passes 3 and the tick (0x4726d0) has no case for it. So it is built here from parts that
are proven: `CAssignTemporaryTaskAction` pausing CSkeletonAI, which 0.98.0's draught does mid-fight and was played, and
Darsh's own `CGoToAI` walk, released by `CSendAIDoneMessage` to `$Trigger`, as vanilla's 18 walks end.

Where the druids hold the English, on Temple Initiate, Stone Chamber and the Antechamber of Lore, and in the Gate and
Temple District sieges: once each, below 30% health, while he is still hostile and a druid of his room lives, a soldier
breaks off, shouts, and runs to the nearest druid post. If a druid still lives when he gets there, he is healed for a
quarter of his health, and either way he goes back to the fight. A hit does not stop him, since a task holds until it
ends, so you can chase him down or let him go and meet him again. Kill the druids first and there is nowhere to run.

It rides in a timer the generator adds to each man, not in the can's damage slot, which the stand-down replaces. There
is no timed release: a second AI Done to a man already fighting again is untested, and CGoToAI tracks a failed path
itself. Each siege druid's generator shares the name `fight4`,
`fight5` or `fight8` with other parts, so a uniquely named rally marker stands on it; the Shrine's posts are named.

A rerun is a no-op.

    python tools/build_soldier_retreat.py
"""
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, if_action, multi
from build_shrine_druids import parts, pos
from build_shrine_repairs import register

S = "Levels/7 English Shrine/"
SIEGE = "Levels/6 Barcelona Attack/"
ROOMS = {S + "02 Temple Initiate.zax": "Temple", S + "03 Stone Chamber.zax": "Stone Chamber", S + "04 Antechamber of Lore.zax": "Antechamber",
         SIEGE + "Gate District Siege.zax": "Gate Siege", SIEGE + "Temple District Siege.zax": "Temple Siege"}
TREE = "Levels/6 Barcelona Attack/Dialog/Fixt Soldier Retreat"
LINES = [("1 fall back", "Fall back! To the druids!"), ("2 hurt", "I'm cut. Get me to the priests!"), ("3 hold them", "Hold them. I'll be back.")]
THRESHOLD, HEAL = "30", "0.25"


def name_of(x):
    m = re.search(r"(?m)^\t\t\tName=([^\r\n]*)", x)
    return m.group(1) if m else ""


def tree():
    p = FX / ("Resources/" + TREE + ".DialogTree")
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(lhbuild.tree("English Soldier", [lhbuild.node(n, t, []) for n, t in LINES]).encode("latin-1"))
    return "Resources/" + TREE + ".DialogTree"


def walk(dest, druid):
    """Darsh's walk-off, sent to a post. On arrival: a quarter of his health if a druid still lives, then back to the fight."""
    z = lhbuild.read("Levels/2 Montserrat/01 Grove Exterior.zax")
    i = z.index("\t\t\tName=Darsh Leaves for Good" + CR)
    s = z.index("Action=CAssignTemporaryTaskAction", i)
    t = z[s + len("Action="):balanced(z, s)]
    t = re.sub(r"(\n\s*)Target=Darsh\r", lambda m: m.group(1) + "Target=$Trigger" + CR, t)
    t = t.replace("Destination=Companion goto spot for deletion", "Destination=" + dest)
    heal = ("CGiveHealthToCharacterAction", [("Character to give health to", "$Trigger"), ("Amount of health to give", ("CMultiply", [
        ("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", "Derived Character Attributes/(HP) Hit Points")])),
        ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", HEAL)]))])), ("Expression Context", "$Trigger")])
    done = multi([if_action(("CIsAliveAction", [("Name To Check For", druid), ("Desired Minimum Count", "1")]), heal),
                  ("CSendAIDoneMessage", [("Target", "$Trigger")])])
    a = t.index("Done action=CDeleteAction")
    t = t[:a] + "Done action=" + B(*done).rstrip() + t[balanced(t, a):]
    t = t.replace("Suppress can't assign error=0", "Suppress can't assign error=1")
    assert "Darsh" not in t and "Move Behavior=CEntityBehaviorMoveToPos" in t and "Original AI Type=CSkeletonAI" in t
    return t


def watcher(dest, druid):
    def hp(cmp, v):
        return ("CExpressionAction", [("Expression", (cmp, [("Operand1", ("CExpressionHealthPercent", [])), ("Operator", ""),
                                                            ("Operand2", ("CConstant", [("Constant Value", v)]))])), ("Character to get attributes from", "$Trigger")])
    shout = ("CRandomAction", [("Action", ("Array", [("Item Count", str(len(LINES)))] + [
        ("Action", ("CDisplayDialogBalloonAction", [("Dialog Tree File", TREE), ("Node ID", n), ("Name of Position", "$Trigger"),
                                                   ("Position Offset", "0.000000,-80.000000"), ("After Action", ""), ("Include In Log", "0")])) for n, _ in LINES]))])
    go = multi([shout, ("CFixtWalk", [])])
    once = ("CSeriesAction", [("Action", [("Action", go), ("Action", ("CSucceedAction", [("Action", "")]))]),
                              ("When Done", "Repeat Last Action"), ("Require Success To Advance", "1"), ("Next Action Index", "0")])
    hostile = ("CCheckCategoryAction", [("Target Name", "$Trigger"), ("Category to check for", "Enemy")])
    druids = ("CIsAliveAction", [("Name To Check For", druid), ("Desired Minimum Count", "1")])
    cond = if_action(hp("CIsLessThanOrEqual", THRESHOLD), if_action(hp("CIsGreaterThan", "0"), if_action(hostile, if_action(druids, once))))
    ai = B("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", cond),
                                     ("Delay Between Actions", "1"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "2")])
    task = walk(dest, druid)
    k = ai.index("CFixtWalk")
    return ai[:k] + task + ai[balanced(ai, k):]


def add_ai(x, ai):
    """Append to the generator's own `AIs to Add`, at the closing brace's line start, and bump its count."""
    i = x.index("AIs to Add=Array")
    e = balanced(x, i)
    block = x[i:e]
    k = block.rindex(CR) + 2
    block = block[:k] + "AI=" + ai.rstrip() + CR + block[k:]
    m = re.compile(r"Item Count=(\d+)").search(block)
    block = block[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + block[m.end():]
    return x[:i] + block + x[e:]


def build(rel, room):
    z = lhbuild.read(rel)
    if "Dialog Tree File=" + TREE + CR in z:
        return 0, 0
    soldier, druid = room + " Soldier", room + " Druid"
    posts = [(name_of(x), pos(x)) for x in parts(z) if re.fullmatch(r"Fixt " + re.escape(room) + r" druid post \d", name_of(x))]
    new = z
    extra = []
    if not posts:
        # a siege: its druids sit in generators whose names other parts share, so stand a unique marker on each
        # not the `Fixed Dead Body Generator`s 0.99.5 also named: they lay out corpses
        live = [x for x in parts(z) if "New Name=" + druid + CR in x and name_of(x) != "Fixed Dead Body Generator"]
        for n, x in enumerate(live, 1):
            name = "Fixt " + room + " rally " + str(n)
            px, py = pos(x)
            extra.append(lhbuild.entity(name, "1", [], "Editor/Position Marker", int(px), int(py)))
            posts.append((name, (px, py)))
    assert posts, rel
    men = 0
    for x in parts(z):
        if "CGeneratorAI" not in x or "New Name=" + soldier + CR not in x:
            continue
        sx, sy = pos(x)
        dest = min(posts, key=lambda p: math.hypot(p[1][0] - sx, (p[1][1] - sy) * 1.4))[0]
        new = new.replace(x, add_ai(x, watcher(dest, druid)), 1)
        men += 1
    if extra:
        new = lhbuild.add_parts(new, extra)
    lhbuild.write_map(rel, new)
    register([rel])
    return men, len(posts)


def main():
    register([tree()])
    for rel, room in ROOMS.items():
        men, posts = build(rel, room)
        print(rel.split("/")[-1], men, "soldier generators fall back to", posts, "posts")


if __name__ == "__main__":
    main()
