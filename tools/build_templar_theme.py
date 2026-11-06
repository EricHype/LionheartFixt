"""Javier's knighting plays the Templars' own theme, the only faction theme the game never used.

Inquisition, Wielders and Saladin all hear theirs when they advance, and the Templars heard nothing. The cue goes
on the six replies that enter `450 made a knight`, as Cedric's does on the reply entering `130 initiated`, so it
starts under the line rather than after it. A reply's actions fire as it is taken, which is why it is not on the
node's own reply. A rerun is a no-op.

    python tools/build_templar_theme.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX

TREE = "Resources/Levels/1 Barcelona/Dialog/Temple District/LordJavier.DialogTree"
THEME = "1 Barcelona/MX_FACT_KNIGHTTEMPLAR1.ogg"
ENTRY = re.compile(r"(Go to node ID=450 made a knight\r\nCustom Action=CMultipleActionsAction\r\n\{\r\nAction=Array\r\n\{\r\nItem Count=)(\d+)\r\n")


def main():
    z = lhbuild.read(TREE)
    if THEME in z:
        return
    cue = "Action=" + B("CMixInSongAndPlayAmbientTrackAction", [("Song To Mix In", THEME)])
    z, n = ENTRY.subn(lambda m: m.group(1) + str(int(m.group(2)) + 1) + CR + cue, z)
    assert n == 6, n
    assert z.count(CR) == z.count("\n")
    (FX / TREE).write_bytes(z.encode("latin-1"))


if __name__ == "__main__":
    main()
