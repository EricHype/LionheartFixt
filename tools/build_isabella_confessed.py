"""Isabella does not wait at the Shrine after she has confessed. Issue #15: "After doing peaceful route with Isabella
(where she turns herself in) she waits for you at the entrance before you meet sir roger templeton and attacks you
saying Spain lost the sea battle".

In Barcelona there are two ways to see her arrested: report her to the Duke, or persuade her to confess (Speech 40,
`310 against england` -> `210 isabella turns herself in`). Both set the Morales quest to `QF4BLH9V` ("tell the spirit
of Captain Morales"). Only the Duke route also activates `Captain Isabella fled` in `01 Outside Shrine`, and that
checker is the one thing the Shrine's three spawn calls test before activating `Grace generator`. So a player who got
her to confess found her at the Shrine anyway, and her click, which checks only for the keep-her-secret state
`JMBN5402`, fell through to `500 arrive in england isabella hates you` and a fight. Fixt made the Shrine encounter
reachable in 0.19.0 and its three-way outcome table never considered the confession.

Each spawn call's Fail branch is now wrapped in `CWasQuestStateActivatedAction{QF4BLH9V}`, with an empty Succeed: if
she was ever arrested, by either route, she does not spawn. "Was activated" rather than "is current", because the
quest completes when the player tells the ghost. `QF4BLH9V` is set nowhere else: the Duke's tree, the confession relay
in `Port District.zax`, and two copies of an inactive debug entity on the Barcelona Coast named `warp` that nothing
activates.

A map edit, so it reaches a save that has not yet entered `01 Outside Shrine`. A rerun is a no-op.

    python tools/build_isabella_confessed.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

MAP = "Levels/7 English Shrine/01 Outside Shrine.zax"
QUEST = "Levels/Wilderness/Quests/Solve the Murder of Captain Morales"
ARRESTED = "QF4BLH9V"
CHECK = "Name To Check For=Captain Isabella fled" + CR


def build():
    z = lhbuild.read(MAP)
    sites, k = [], 0
    while True:
        k = z.find(CHECK, k)
        if k < 0:
            break
        sites.append(k)
        k += 1
    assert len(sites) == 3, len(sites)
    done = 0
    for c in reversed(sites):
        # the CConditionalAction that holds this existence check
        s = z.rindex("CConditionalAction", 0, c)
        e = lhbuild.balanced(z, s)
        blk = z[s:e]
        assert blk.index(CHECK) == c - s, "the check is not this conditional's own"
        if "State=" + ARRESTED in blk:
            continue
        f = blk.index("Fail Action=CActivateAction")
        fs = f + len("Fail Action=")
        fe = lhbuild.balanced(blk, fs)
        inner = blk[fs:fe]
        assert "Target Name=Grace generator" + CR in inner, inner
        wrapped = B("CConditionalAction", [
            ("Try Action", ("CWasQuestStateActivatedAction", [("Quest", QUEST), ("State", ARRESTED)])),
            ("Succeed Action", ""),
            ("Fail Action", "@INNER@"),
            ("Return failure if the TryAction failes", "0")])
        wrapped = wrapped.replace("Fail Action=@INNER@" + CR, "Fail Action=" + inner + CR)
        blk = blk[:fs] + wrapped.rstrip(CR) + blk[fe:]
        z = z[:s] + blk + z[e:]
        done += 1
    if done:
        assert done == 3, done
        lhbuild.write_map(MAP, z)
        register([MAP])
    return done


def main():
    print("isabella confessed:", build())


if __name__ == "__main__":
    main()
