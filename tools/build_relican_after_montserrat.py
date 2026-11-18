"""Relican still talks after the Montserrat task. Issue #15: "After finishing the last quest for dark wielders and
unlocking Monserrat, you cannot talk to Relican anymore."

`Relican Clone Generator` in `Calle Perdida.zax` gives its `Relican` a click that branches on the Montserrat quest
(`Go to Montserrat and seek out the Crown of Thorns`). Once that was ever activated, the click showed node `40 dark
wielder task 4` as a balloon with `Name of Position=Lord Relican`, and nothing in the map has that name (the spawn is
`Relican`), so it showed nothing. Vanilla's bug, identical in the shipped map. It costs Fixt more than vanilla:
`5 Return Dialogue` holds Fixt's report-backs (Leonardo, the Sceptre shell), and they went with it.

The Then branch is now the same `CDisplayDialogTreeAction` to `5 Return Dialogue` the click uses before Montserrat.
"Tell me more about the tasks" in that node still recaps the relics.

Reopening the hub exposes one reply vanilla never had to survive: "Let us talk about the events that transpired in the
Church." It completes `Enter Inquisitor's House and Learn about Relics` and pays `Find out Info From Knights Relican XP`,
gated only on its state `4XUQR7B3` being current, which completion leaves current. So it would repeat, XP and all. It
now also needs the quest not completed, in the CNotAction form vanilla uses.

Reach: the tree gate reaches every save. The click lives on a spawned creature, so it reaches only a save whose
Relican has not spawned yet -- a game that has not reached La Calle Perdida. A save already past it keeps the silent
click.

A rerun is a no-op.

    python tools/build_relican_after_montserrat.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

MAP = "Levels/1 Barcelona/Calle Perdida.zax"
TREE = "Resources/Levels/1 Barcelona/Dialog/La Calle Perdida/Lord Relican.DialogTree"
RELICAN_TREE = "Levels/1 Barcelona/Dialog/La Calle Perdida/Lord Relican"
CHURCH_QUEST = "Levels/1 Barcelona/Quests/Calle Perdida/Wielder Initiation Quests/Enter Inquisitor's House and Learn about Relics"
CHURCH_REPLY = "Reply Text=Let us talk about the events that transpired in the Church." + CR
BROKEN = "Name of Position=Lord Relican" + CR


def fix_click():
    z = lhbuild.read(MAP)
    g = z.index("\t\t\tName=Relican Clone Generator" + CR)
    s = z.rindex("Level Part=", 0, g)
    e = lhbuild.balanced(z, s)
    blk = z[s:e]
    if BROKEN not in blk:
        return 0
    assert blk.count(BROKEN) == 1
    t = blk.index("Then=CDisplayDialogBalloonAction")
    ts = t + len("Then=")
    te = lhbuild.balanced(blk, ts)
    old = blk[ts:te]
    assert "Node ID=40 dark wielder task 4" + CR in old and BROKEN in old, old
    assert "Go to Montserrat and seek out the Crown of Thorns" in blk[:t][-400:], "not the Montserrat branch"
    new = B("CDisplayDialogTreeAction", [("Dialog Tree File", RELICAN_TREE), ("Node ID", "5 Return Dialogue"),
                                        ("Speaker", "$trigger"), ("Player Being Spoken To", "$Instigator")])
    blk = blk[:ts] + new.rstrip(CR) + blk[te:]
    z = z[:s] + blk + z[e:]
    lhbuild.write_map(MAP, z)
    register([MAP])
    return 1


def gate_church():
    t = lhbuild.read(TREE)
    gate = ("Custom Requirement=CActionExpression" + CR + "{" + CR + "Action=CNotAction" + CR + "{" + CR +
            "Action=CIsQuestCompletedAction" + CR + "{" + CR + "Quest=" + CHURCH_QUEST + CR + "}" + CR + "}" + CR +
            "}" + CR)
    if gate + CHURCH_REPLY in t:
        return 0
    assert t.count(CHURCH_REPLY) == 1
    i = t.index(CHURCH_REPLY)
    # the reply's Requirement is an inline expression block that ends with the line before the reply text
    assert t[:i].endswith("}" + CR) and "State=4XUQR7B3" in t[i - 300:i], "unexpected Church requirement"
    n0 = t.count(CR)
    t = t[:i] + gate + t[i:]
    assert t.count(CR) == n0 + gate.count(CR)
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    register([TREE])
    return 1


def main():
    print("relican after montserrat: click", fix_click(), "church gate", gate_church())


if __name__ == "__main__":
    main()
