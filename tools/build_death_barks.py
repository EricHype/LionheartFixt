"""A goblin who barks on the blow that kills him says a dying line, not a fighting one. Reported from play after
0.99.22: "enemies playing their combat text when they get hit for the last time/die. I'm ok with them yelling on death, but
it should be death dialogue."

Every bark in the game is Fixt's, and the hurt barks ride `Damaged Script Action`, which also runs on the killing blow. So a
goblin could die shouting "Khan! Khan, it is winning!". The English soldiers do not have the bug: their fighting lines ride
`Shoot Completed`, their own swings, and their `Damaged Script Action` holds only the healing-draught line, which that hook
already skips at `CExpressionHealthPercent` 0. That same Fixt gate is the evidence that the creature's health has dropped by
the time the hook runs.

The bank of balloons in each hook is now wrapped: a `CDelayAction` of 0.1 seconds, then `CExpressionHealthPercent` of
`$trigger` below 1 picks a death bank, otherwise the same hurt bank as before. The delay is the frame-ordering idiom vanilla
uses in its own death hooks (all 13 of its `CDelayAction`s inside death hooks are 0 or 0.1), so the check reads the creature
after the hit has landed, whichever order the engine runs damage and the hook in. `Forget Trigger=0` keeps `$trigger`, and a
corpse stays an entity (the saves show `Category=Corpse,Goblin` bodies), so the balloon still has an anchor. The rate is
unchanged: the bank is still one entry of the hook's own random pick, so a death cry comes at the hurt bark's rate, not on
every death.

The goblin death lines are new nodes in `Fixt Goblin Barks`, in the same voice as the hurt lines beside them.

**Cortes and Cervantes** bark when hurt the same way, so a companion dying could shout "I need assistance!". Their hurt
banks get the same wrap, with three dying lines each in a new tree, `Levels/Fixt Death Barks`.

**Every other barking enemy** (soldiers, thieves, trolls, Snakebreed) barks only on its own swings, so nothing fires on the
blow that kills it, and a line from its last swing can still hang over the body; no action clears a balloon early. Asked for
after that: they say a dying line too. Their `Damaged Script Action` gains the same 0.1s check, then a 35% chance of a line
from `Fixt Death Barks`, placed 40 above the swing balloon so a lingering one never sits on the same point. Any hook already
there (the thieves' caltrops, the soldiers' draught, the troll boss's peace trigger) is kept and runs first. The damage slot
is the one to use: generators replace a spawn's `Destroyed Script Action` on 52 spawn sites of these families, and its
damage hook on 4, all goblins.

A rerun is a no-op.

    python tools/build_death_barks.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH
from build_shrine_repairs import register

GOBLIN_TREE = "Levels/Wilderness/Dialog/Fixt Goblin Barks"
DEATHS = {
    GOBLIN_TREE: [("200 death", "Not... the pot..."),
                  ("201 death", "Save the liver. Somebody save the liver."),
                  ("202 death", "Tell Grum he gets my share."),
                  ("203 death", "<He curls up small around the wound, and is still.>"),
                  ("204 death", "I was so hungry..."),
                  ("205 death", "Eat me quick, brothers. Before I spoil.")],
}

# everyone else's dying lines live in one new tree
DEATH_TREE = "Levels/Fixt Death Barks"
LINES = {
    "cortes": ["All that gold... and I never spent it.", "Not for so little. Not like this.",
               "<He grips his sword hilt, and does not let go of it.>"],
    "cervantes": ["Squire... finish the chapter for me.", "Every story ends, my friend. Even the good ones.",
                  "Write that I fought. Write it well."],
    "soldier": ["For... England...", "Saint George... I tried...", "Hold... the line...",
                "<He drops his blade and goes down.>", "Not here. Not so far from home.", "Sergeant... I cannot see you..."],
    "thief": ["Should have stayed in the alley...", "<He clutches at his purse as he falls.>", "Not... worth it...",
              "Tell the Guild... I paid my dues.", "Keep the coat, amigo.", "Nothing personal... was it?"],
    "troll": ["Rock... takes me back.", "<It sags like a rockslide, and is still.>", "One more dead Troll.",
              "Cold... cold now.", "Ore is... ours...", "<A long sound, like stone grinding to a stop.>"],
    "snake": ["The brood... remembersss...", "<It writhes, uncoils, and lies still.>", "Cold... ssso cold...",
              "Avenge me, my brood.", "The ssssting... was mine...", "Hssss... ssss..."],
}
NODES = {g: [(g + " " + str(i), x) for i, x in enumerate(xs, 1)] for g, xs in LINES.items()}
# companions bark when hurt, like goblins: their hurt bank gets the same wrap
COMPANIONS = {"Levels/1 Barcelona/Dialog/Port District/cortes": "cortes", "Levels/1 Barcelona/Dialog/Temple District/Cervantes": "cervantes"}
# these bark only on their own swings, so a dying one says nothing yet: the damage hook gains a death check
SWING = {"Levels/7 English Shrine/Dialog/Fixt Soldier Barks": "soldier", "Levels/Sewers/Dialog/Fixt Thief Barks": "thief",
         "Levels/Sewers/Dialog/Fixt Troll Barks": "troll", "Levels/Wilderness/Dialog/Fixt Snakebreed Barks": "snake"}
DEATH_CHANCE = "35"   # percent of deaths that get a line, for the families with no hurt bank to ride


def add_nodes(tree):
    rel = "Resources/" + tree + ".DialogTree"
    t = lhbuild.read(rel)
    if "Node ID=200 death" + CR in t:
        return 0
    assert t.endswith("Should Have Voiceover=0" + CR + "}" + CR), tree
    add = "".join(DASH + CR + "Node ID=" + n + CR + "Text=" + x + CR + "Should Have Voiceover=0" + CR for n, x in DEATHS[tree])
    t = t[:-len("}" + CR)] + add + "}" + CR
    (lhbuild.FX / rel).write_bytes(t.encode("latin-1"))
    register([rel])
    return len(DEATHS[tree])


def balloons_only(flat, s):
    """True when the CRandomAction at s holds nothing but dialogue balloons: a bark bank."""
    e = lhbuild.balanced(flat, s)
    inner = flat[flat.index("{", s) + 1:e]
    kids = re.findall(r"\r\nAction=(C\w+)\r\n", inner)
    depth_ok = [k for k in kids if k == "CDisplayDialogBalloonAction"]
    n = int(re.search(r"Item Count=(\d+)", inner).group(1))
    return kids and len(depth_ok) == n and all(k == "CDisplayDialogBalloonAction" for k in kids)


def death_bank(tree, nodes, anchor, offset):
    return ("CRandomAction", [("Action", ("Array", [("Item Count", str(len(nodes)))] + [
        ("Action", ("CDisplayDialogBalloonAction", [("Dialog Tree File", tree), ("Node ID", n), ("Name of Position", anchor),
                                                    ("Position Offset", offset), ("After Action", ""), ("Include In Log", "0")]))
        for n, _ in nodes]))])


DYING = ("CIsLessThan", [("Operand1", ("CExpressionHealthPercent", [])), ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "1")]))])


def wrap(flat, s, tree, nodes=None):
    e = lhbuild.balanced(flat, s)
    bank = flat[s:e] + CR
    first = re.search(r"Name of Position=([^\r\n]*)\r\nPosition Offset=([^\r\n]*)", bank)
    death = death_bank(tree, nodes or DEATHS[tree], first.group(1), first.group(2))
    dying = DYING
    pick = "CIfExpressionAction" + CR + "{" + CR + "If Expression=" + B(*dying) + "Character to get attributes from=$trigger" + CR + \
           "Then=" + B(*death) + "Else=" + bank + "}" + CR
    out = "CDelayAction" + CR + "{" + CR + "Next Action=" + pick + "Delay=0.1" + CR + "Plus or Minus=0" + CR + "Forget Trigger=0" + CR + "}"
    return flat[:s] + out + flat[e:]


def build_tree():
    rel = "Resources/" + DEATH_TREE + ".DialogTree"
    if (lhbuild.FX / rel).exists():
        return 0
    nodes = [lhbuild.node(n, x, []) for g in NODES for n, x in NODES[g]]
    (lhbuild.FX / rel).write_bytes(lhbuild.tree("Fixt Death Barks", nodes).encode("latin-1"))
    register([rel])
    return len(nodes)


def swing_death(t):
    """A death check for a creature that barks only when it swings: the same delayed health test as the wrap, then a chance."""
    m = re.search(r"(?m)^\t*Shoot Completed=C", t)
    if not m:
        return None
    shoot = t[m.start():lhbuild.balanced(t, m.start())]
    group = next((g for tr, g in SWING.items() if tr in shoot), None)
    if not group:
        return None
    anchor, off = re.search(r"Name of Position=([^\r\n]*)\r\n\t*Position Offset=([^\r\n]*)", shoot).groups()
    x, y = off.split(",")
    off = x + "," + "%.6f" % (float(y) - 40)   # above any swing balloon still showing, so the two never sit on one point
    chance = ("CIsLessThan", [("Operand1", ("CRandom", [("Operator", ""), ("Minimum", ("CConstant", [("Constant Value", "0")])),
                                                         ("Maximum", ("CConstant", [("Constant Value", "100")]))])),
                              ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", DEATH_CHANCE)]))])
    say = ("CIfExpressionAction", [("If Expression", chance), ("Character to get attributes from", anchor),
                                   ("Then", death_bank(DEATH_TREE, NODES[group], anchor, off)), ("Else", "")])
    pick = ("CIfExpressionAction", [("If Expression", DYING), ("Character to get attributes from", anchor), ("Then", say), ("Else", "")])
    return B("CDelayAction", [("Next Action", pick), ("Delay", "0.1"), ("Plus or Minus", "0"), ("Forget Trigger", "0")])


def build_swing(rel):
    t = lhbuild.read(rel)
    if DEATH_TREE in t:
        return 0
    check = swing_death(t)
    if not check:
        return 0
    slots = list(re.finditer(r"(?m)^(\t*)Damaged Script Action=([^\r\n]*)\r\n", t))
    assert len(slots) == 1, (rel, len(slots))
    m = slots[0]
    if m.group(2) == "":
        t = t[:m.start()] + m.group(1) + "Damaged Script Action=" + check + t[m.end():]
    else:
        e = lhbuild.balanced(t, m.start())
        old = re.sub(r"\r\n\t*", CR, t[m.start():e]).lstrip("\t")[len("Damaged Script Action="):] + CR
        both = "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR + \
               "Action=" + old + "Action=" + check + "}" + CR + "}" + CR
        t = t[:m.start()] + m.group(1) + "Damaged Script Action=" + both + t[e + len(CR):]
    lhbuild.write_map(rel, t)
    register([rel])
    return 1


def build_can(rel):
    t = lhbuild.read(rel)
    m = re.search(r"(?m)^\t*Damaged Script Action=C", t)
    if not m:
        return 0
    s0 = m.start()
    e0 = lhbuild.balanced(t, s0)
    hook = t[s0:e0]
    if "Node ID=200 death" in hook or DEATH_TREE in hook:
        return 0
    if GOBLIN_TREE in hook:
        tree, nodes = GOBLIN_TREE, None
    else:
        group = next((g for tr, g in COMPANIONS.items() if tr in hook), None)
        if not group:
            return 0
        tree, nodes = DEATH_TREE, NODES[group]
    flat = re.sub(r"\r\n\t*", CR, hook).lstrip("\t")
    banks = [k.start() + len("=") for k in re.finditer(r"=CRandomAction\r\n", flat) if balloons_only(flat, k.start() + 1)]
    assert banks, rel
    for s in reversed(banks):   # from the end, so earlier offsets stay valid
        flat = wrap(flat, s, tree, nodes)
    lead = re.match(r"\t*", t[s0:]).group(0)
    t = t[:s0] + lead + flat + t[e0:]
    lhbuild.write_map(rel, t)
    register([rel])
    return len(banks)


def main():
    print("death lines:", sum(add_nodes(tr) for tr in DEATHS), "goblin,", build_tree(), "others")
    cans = banks = swings = 0
    for p in sorted((lhbuild.FX / "Resources").rglob("*.can")):
        rel = p.relative_to(lhbuild.FX).as_posix()
        n = build_can(rel)
        cans += bool(n)
        banks += n
        swings += build_swing(rel)
    print("hurt banks wrapped:", banks, "in", cans, "cans | death checks added to swing barkers:", swings)


if __name__ == "__main__":
    main()
