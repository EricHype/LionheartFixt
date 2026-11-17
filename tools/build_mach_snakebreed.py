"""Machiavelli's quest completes whichever snakebreed dies last. Reported from play after 0.99.30: "after killing all the
snakebreed in machiavelli's house he still asks us to kill them / doesn't progress to the next step".

The quest moves on only through `Swap Mach Dialogue`, a relay that does nothing while any `Assassin` lives and otherwise
gives Machiavelli his `200 Saved Machiavelli Return Greeting` and the reward. In vanilla, all four `Assassin Generator`s
spawned `Monster Cans/Assassin Machiavelli`, and that can fires the relay from its `Destroyed Effect Action`, so the
last death always fired it. 0.46.0 gave the ambush real stats by pointing three of the generators at shipped Snakebreed
cans (`Snakebreed` twice and `Snakebreed Venom`). Those cans fire nothing on death. So the relay ran only when the leader
died, and if any other snakebreed outlived the leader the quest stuck on `255 help me` for good.

Each of the three generators now sets the relay as its spawn's `Destroyed Script Action`, in the `After Action` slot,
with `Target Name=$Instigator`. That is the pattern `Machiavelli generator` in this map already uses, and the one
`05 Troll Pit` uses for its kill counter. The Snakebreed cans leave that slot blank (their barks and drops are in
`Destroyed Effect Action`), so nothing is overwritten. The leader's can is untouched.

This reaches a save that has not yet entered the House of Ilk. A save already stuck in the house cannot be reached:
the map is saved, and Machiavelli's click there is a reply-less balloon.

A rerun is a no-op.

    python tools/build_mach_snakebreed.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

MAP = "Levels/1 Barcelona/House of Ilk map.zax"
RELAY = "Swap Mach Dialogue"
SNAKES = ("Entity=Monster Cans/Snakebreed" + CR, "Entity=Monster Cans/Snakebreed Venom" + CR)
SET = B("CSetDestroyedScriptActionAction", [("New Destroyed Action", lhbuild.relay(RELAY)), ("Target Name", "$Instigator")])


def build():
    z = lhbuild.read(MAP)
    starts, k = [], 0
    while True:
        k = z.find("\tName=Assassin Generator" + CR, k)
        if k < 0:
            break
        starts.append(k)
        k += 1
    assert len(starts) == 4, len(starts)
    done = 0
    for a in reversed(starts):
        s = z.rindex("{", 0, a)
        e = lhbuild.balanced(z, s)
        blk = z[s:e]
        if not any(x in blk for x in SNAKES):
            assert "Entity=Monster Cans/Assassin Machiavelli" + CR in blk
            continue
        if "Relay Name=" + RELAY in blk:
            continue
        assert blk.count("After Action=" + CR) == 1, blk.count("After Action=" + CR)
        blk = blk.replace("After Action=" + CR, "After Action=" + SET, 1)
        z = z[:s] + blk + z[e:]
        done += 1
    if done:
        assert done == 3, done
        lhbuild.write_map(MAP, z)
        register([MAP])
    return done


def main():
    print("mach snakebreed:", build())


if __name__ == "__main__":
    main()
