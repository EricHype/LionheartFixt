"""The dream's yellow crystal does not fail a trial you have already passed. Issue #16: "I killed all enemies one by one,
after I finished and I was teleported the game forced me to do it one more time to pass the trial."

The yellow crystal in `Dream Djinni Map` is the only way out of the dream (Kabool's `300 start physical test 2`: "run to
the yellow crystal and invoke its power to end the dream"). Vanilla's crystal always records a failure: it activates
`failed dream djinn` in the Gate District and sets `Pass the Trial of Dreams` to `XFEDCK28`. Neither `160`/`161 pass
combat` nor the riddles' `150 pass trials` takes a winner home, so a winner walks out through the crystal and is
recorded as having failed: Amir (`3 Return Dialogue`, `600 ready to resume`) reads `failed dream djinn` and sends them
back. The riddle route's `Pass 3 Relay` deactivates `failed dream djinn`, and the crystal switches it straight back on.

The crystal's two failure actions now run only when `RHAGYW4H` (passed, set by `150`, `160` and `161`) was never
activated. It still wakes you and clears the arena either way. And the combat win (`Completed Physical Trial`) now
clears an earlier failure the way the riddle win does, deactivating `failed dream djinn` in the Gate District, so a
character who failed once and then won the fight is not still read as failed. Map-side: a dream not yet entered. A
rerun is a no-op.

    python tools/build_djinn_crystal_after_pass.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

MAP = "Levels/1 Barcelona/Dream Djinni Map.zax"
QUEST = "Levels/1 Barcelona/Quests/Gate District/Knights Saladin Initiation/Pass the Trial of Dreams"
MARK = "State=RHAGYW4H"


def build():
    t = lhbuild.read(MAP)
    k = t.index("Model=Environments/Misc/SmallCrystalRocks/RokYellow2")
    s = t.rindex("\t\tLevel Part=", 0, k)
    part = t[s:k]
    if MARK in part:
        return False
    a = part.index("Action=COtherMapAction")
    assert "Target Name=failed dream djinn" in part[a:a + 400]
    ae = lhbuild.balanced(part, a + len("Action=")) + len(CR)
    b = part.index("Action=CIfAction", ae)
    assert part[ae:b].strip() == "" and "State=XFEDCK28" in part[b:b + 900]
    be = lhbuild.balanced(part, b + len("Action=")) + len(CR)
    fail = part[a:be]
    passed = B("CWasQuestStateActivatedAction", [("Quest", QUEST), ("State", "RHAGYW4H")])
    guard = ("Action=CIfAction" + CR + "{" + CR + "If=CNotAction" + CR + "{" + CR + "Action=" + passed + "}" + CR +
             "Then=CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR + fail + "}" + CR + "}" + CR +
             "Else=" + CR + "Return failure if the If failes=0" + CR + "}" + CR)
    # the enclosing array loses one item (two folded into one)
    head = part[:a]
    n_at = head.rindex("Item Count=")
    n = int(head[n_at + len("Item Count="):head.index(CR, n_at)])
    head = head[:n_at] + "Item Count=%d" % (n - 1) + head[head.index(CR, n_at):]
    t = t[:s] + head + guard + part[be:] + t[k:]
    # the combat win clears an earlier failure, as the riddle win's `Pass 3 Relay` does
    r = t.index("			Name=Completed Physical Trial" + CR)
    m = t.index("Action=CMultipleActionsAction", r) + len("Action=")
    ic = t.index("Item Count=", m)
    n = int(t[ic + len("Item Count="):t.index(CR, ic)])
    clear = B("COtherMapAction", [("Action", ("CDeactivateAction", [("Target Name", "failed dream djinn")])),
                                  ("Other Map Name", "1 Barcelona/Gate District")])
    t = t[:ic] + "Item Count=%d" % (n + 1) + CR + "Action=" + clear + t[t.index(CR, ic) + len(CR):]
    lhbuild.write_map(MAP, t)
    register([MAP])
    return True


def main():
    print("djinn crystal after pass:", build())


if __name__ == "__main__":
    main()
