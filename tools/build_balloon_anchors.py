"""Barks that could never play, because their anchor named a crowd.

A balloon's Name of Position takes exactly one match and draws nothing on two (`0x41ef10`), unlike Target Name, which
broadcasts. Two of Fixt's own lines named a whole family.

* `Sewer Stash / 2 caught` named `Sewer Thief`, and 8 to 10 stand in those maps. The stash itself is the speaker's
  $Trigger, so the shout now comes from where the player is caught.
* `Ogre Canned / 40 charm broken` named `Ogre`. A timer goes on every ogre and fires a one-shot relay, so the first to
  tick says it, on $Trigger.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_balloon_anchors.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, balanced, balloon, relay

SEWERS = ("Levels/Sewers/01 Sewer Main Entrance.zax", "Levels/Sewers/02 Thieves Congregation.zax")
OGRES = ("Levels/Wilderness Maps/Mountain Pass.zax", "Levels/Wilderness Maps/Ogre Cave.zax", "Levels/Wilderness Maps/Ogre Sprawl.zax")
VOICE = "Fixt the charm voice"


def sewers():
    for rel in SEWERS:
        z = lhbuild.read(rel)
        new, n = re.subn(r"(Node ID=2 caught\r\n\s*Name of Position=)Sewer Thief", r"\1$Trigger", z)
        if n:
            lhbuild.write_map(rel, new)


def ogres():
    timer = ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", relay(VOICE)),
                                       ("Delay Between Actions", "1"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "1")])
    add = ("CAddAIAction", [("Target Name", "Ogre"), ("AI", timer), ("Delay Between Adds", "0")])
    say = balloon("Levels/Wilderness/Dialog/Ogre Canned", "40 charm broken", "$Trigger", "-60")
    for rel in OGRES:
        z = lhbuild.read(rel)
        if VOICE in z:
            continue
        k = z.index("Node ID=40 charm broken")
        s = z.rindex("Then=CDelayAction", 0, k)
        e = balanced(z, s)
        assert k < e and "Name of Position=Ogre" + CR in z[s:e]
        z = z[:s] + "Then=" + B(*add).rstrip() + z[e:]
        lhbuild.write_map(rel, lhbuild.add_parts(z, [lhbuild.relay_part(VOICE, say, 60, 60)]))


def main():
    sewers()
    ogres()


if __name__ == "__main__":
    main()
