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

The death lines are new nodes in `Fixt Goblin Barks`, in the same voice as the hurt lines beside them.

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


def wrap(flat, s, tree):
    e = lhbuild.balanced(flat, s)
    bank = flat[s:e] + CR
    first = re.search(r"Name of Position=([^\r\n]*)\r\nPosition Offset=([^\r\n]*)", bank)
    death = ("CRandomAction", [("Action", ("Array", [("Item Count", str(len(DEATHS[tree])))] + [
        ("Action", ("CDisplayDialogBalloonAction", [("Dialog Tree File", tree), ("Node ID", n), ("Name of Position", first.group(1)),
                                                    ("Position Offset", first.group(2)), ("After Action", ""), ("Include In Log", "0")]))
        for n, _ in DEATHS[tree]]))])
    dying = ("CIsLessThan", [("Operand1", ("CExpressionHealthPercent", [])), ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "1")]))])
    pick = "CIfExpressionAction" + CR + "{" + CR + "If Expression=" + B(*dying) + "Character to get attributes from=$trigger" + CR + \
           "Then=" + B(*death) + "Else=" + bank + "}" + CR
    out = "CDelayAction" + CR + "{" + CR + "Next Action=" + pick + "Delay=0.1" + CR + "Plus or Minus=0" + CR + "Forget Trigger=0" + CR + "}"
    return flat[:s] + out + flat[e:]


def build_can(rel):
    t = lhbuild.read(rel)
    m = re.search(r"(?m)^\t*Damaged Script Action=C", t)
    if not m:
        return 0
    s0 = m.start()
    e0 = lhbuild.balanced(t, s0)
    hook = t[s0:e0]
    if "Node ID=200 death" in hook:
        return 0
    if GOBLIN_TREE not in hook:
        return 0
    tree = GOBLIN_TREE
    flat = re.sub(r"\r\n\t*", CR, hook).lstrip("\t")
    banks = [k.start() + len("=") for k in re.finditer(r"=CRandomAction\r\n", flat) if balloons_only(flat, k.start() + 1)]
    assert banks, rel
    for s in reversed(banks):   # from the end, so earlier offsets stay valid
        flat = wrap(flat, s, tree)
    lead = re.match(r"\t*", t[s0:]).group(0)
    t = t[:s0] + lead + flat + t[e0:]
    lhbuild.write_map(rel, t)
    register([rel])
    return len(banks)


def main():
    print("death lines:", sum(add_nodes(tr) for tr in DEATHS))
    cans = banks = 0
    for p in sorted((lhbuild.FX / "Resources").rglob("*.can")):
        n = build_can(p.relative_to(lhbuild.FX).as_posix())
        cans += bool(n)
        banks += n
    print("cans:", cans, "| banks wrapped:", banks)


if __name__ == "__main__":
    main()
