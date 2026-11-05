"""Torquemada's speech before he fights you, which lost its node and kept its recording.

Vanilla's `30 admit tainted` has a reply going to `120 combat`, a node that does not exist, and
`GrandInquisitor VOs/120 combat.ogg` is 14.6 seconds of that speech. The text is the author's
transcript of the recording. The node takes the shape of `13 Really Angry Combat Greeting` and
`110 Defy`, so the line plays and a blank reply starts the fight. The action therefore moves off the
player's reply, where it would have started the fight before he spoke.

All four replies that say "You are the one who will burn, Inquisitor" and start this fight go through
it. `100 renounce` carries the same reply text and sends you to jail instead, which is not a fight, so
it is left alone.

Each edit asserts what it replaces, so a rerun is a no-op.

    python tools/build_inquisitor_speech.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR, FX

TREE = "Resources/Levels/1 Barcelona/Dialog/Temple District/GrandInquisitor.DialogTree"
SPEECH = ("Silence! You will know why the guilty fear me as the blessed hammer of heretics. "
          "Death is the only penance for your crimes, heathen.")
FIGHT = ("Custom Action=CGoToCombatAction" + CR + "{" + CR + "Enemy Name=Grand Inquisitor" + CR + "}" + CR)
REPLY = "Reply Text=You are the one who will burn, Inquisitor." + CR


def main():
    z = lhbuild.read(TREE)
    if "Node ID=120 combat" + CR in z:
        return
    blank = REPLY + "Go to node ID=" + CR + FIGHT + "Icon=Fight Icon" + CR
    dangling = REPLY + "Go to node ID=120 combat" + CR + FIGHT + "Icon=Fight Icon" + CR
    wired = REPLY + "Go to node ID=120 combat" + CR + "Icon=Fight Icon" + CR
    assert z.count(blank) == 3 and z.count(dangling) == 1, (z.count(blank), z.count(dangling))
    z = z.replace(blank, wired).replace(dangling, wired)

    node = ("Node ID=120 combat" + CR + "Text=" + SPEECH + CR + "Should Have Voiceover=1" + CR + CR +
            "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR + FIGHT +
            "Is Default Reply=1" + CR + "-" * 60 + CR)
    before = "Node ID=200 trial" + CR
    assert z.count(before) == 1
    z = z.replace(before, node + before)
    assert z.count(CR) == z.count("\n")
    (FX / TREE).write_bytes(z.encode("latin-1"))


if __name__ == "__main__":
    main()
