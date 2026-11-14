"""Caltrops land near the thief, not under it. Reported from play after the 0.99.20 model: "it shows up directly under the
thief who drops it, usually while they are standing still."

Every one of the 57 cans that lays a patch (0.35.0's 48 assassins and thieves, and the nine Montserrat and Assassin Master
cans 0.35.x added) creates `Fixt Caltrops Entity` at `$Trigger` with `Random Location Delta=0`. It is laid the first time
the thief is hurt, which is almost always in melee, so it appeared exactly under a thief standing still to fight.

Now it scatters within 80 of the thief, the most common non-zero `Random Location Delta` in vanilla (32 of its 66), so the patch lands somewhere in the fight around the thief. It still only hurts players,
on the 1.25 second tick, so a patch that lands under you still gives you a beat to step off.

A rerun is a no-op.

    python tools/build_caltrops_scatter.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from build_shrine_repairs import register

CREATE = "Canned Entity to Create=Common Objects and Scripts/Fixt Caltrops Entity"
DELTA = "80"
EXPECTED = 57


def main():
    changed = seen = 0
    for p in sorted(lhbuild.FX.rglob("*.can")):
        rel = str(p.relative_to(lhbuild.FX)).replace("\\", "/")
        t = lhbuild.read(rel)
        if CREATE not in t:
            continue
        seen += 1
        assert t.count(CREATE) == 1, rel
        k = t.index(CREATE)
        s = t.rindex("CCreateEntityFromCanAction", 0, k)
        block = t[s:k]
        if "Random Location Delta=" + DELTA + "\r\n" in block:
            continue
        assert block.count("Random Location Delta=0\r\n") == 1, rel
        t = t[:s] + block.replace("Random Location Delta=0\r\n", "Random Location Delta=" + DELTA + "\r\n") + t[k:]
        p.write_bytes(t.encode("latin-1"))
        register([rel])
        changed += 1
    assert seen == EXPECTED, seen
    print("caltrop layers:", seen, "| scattered now:", changed)


if __name__ == "__main__":
    main()
