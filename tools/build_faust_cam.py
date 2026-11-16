"""The camera shows the Daeva of Pain's whole speech when Faust frees it. A vanilla bug, reported from play after 0.99.28: "the
camera doesn't move up enough to read the hover text above the daeva".

When Faust frees the Daeva in `Inquisition Pit3`, the camera goes to `Faust Cam` at (2813,631), between him (spawned at
(2728,657)) and the Daeva (`Move To Spot1 Demon`, (2980,577)). Faust's one line shows there. The Daeva then answers with
`301 Pan Free Demon`, a 230-character balloon anchored 110 pixels above it, which grows upward past the top of the screen.
The first two lines were lost.

The marker moves up 100 pixels, to (2813,531). The attractor centres the view on its owner's position (`0x4ab080` to
`0x61c230`), and map positions are background pixels, so the whole view moves up 100. Faust, now 126 below centre, and his
balloon stay on screen. Nothing else names the marker's position. This reaches an Inquisition Pit3 not yet entered.

A rerun is a no-op.

    python tools/build_faust_cam.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR
from build_shrine_repairs import register

MAP = "Levels/1 Barcelona/Inquisition Pit3.zax"
OLD = "Position X=2813" + CR + "\t\t\tPosition Y=631" + CR
NEW = "Position X=2813" + CR + "\t\t\tPosition Y=531" + CR


def build():
    z = lhbuild.read(MAP)
    a = z.index("\t\t\tName=Faust Cam" + CR)
    e = lhbuild.balanced(z, z.rindex("{", 0, a))
    blk = z[a:e]
    if NEW in blk:
        return 0
    assert blk.count(OLD) == 1 and "Model=Editor/Camera Attractor" in blk
    z = z[:a] + blk.replace(OLD, NEW) + z[e:]
    lhbuild.write_map(MAP, z)
    register([MAP])
    return 1


def main():
    print("faust cam:", build())


if __name__ == "__main__":
    main()
