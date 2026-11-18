"""A peaceful Enchanter opens the way out of his ether plane. Issue #15: "When talking to the wizard in the trapped
ether plane if you ask him to join you and Relican you cannot exit without killing him."

The plane's only exit is `Teleporter Crystal`, and only the relay `Power the crystal to leave` arms it (it adds the
crystal's teleporter specifier, plays a sound and relocates it). In play two things fire that relay: Marco's portal
relay, which Marco's tree switches off on the route that leads to the Enchanter, and the Enchanter's death. A third,
a part named `warp`, is an inactive debug switch nothing references.

The non-lethal endings, `45 Barter 3` and `59 Winner`, fire `Pacify Enchanter in Dialog`, which calms him and opens
his return dialogue, and never arms the crystal. His own line in `59 Winner` promises it: "Very well. I shall see if I
can open the portal by talking to the spirits." Fixt's pact (0.39.0, `71 Fixt Pact 2`) branches off the pacified
state, so it inherited the trap. This is vanilla's bug, and the pact made it more likely to be hit.

`Pacify Enchanter in Dialog` now fires `Power the crystal to leave` as well, so the barter, the contest and the pact
all leave a way out. Killing him afterwards fires the relay a second time, which is harmless: the relay part's own
Trigger Only Once means the crystal is armed once.

A map edit, so it reaches a save that has not yet entered the plane. A rerun is a no-op.

    python tools/build_ether_exit.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR, balanced
from build_shrine_repairs import into_relay, register

MAP = "Levels/1 Barcelona/TrappedEtherPlane.zax"
PACIFY = "Pacify Enchanter in Dialog"
POWER = "Power the crystal to leave"


def build():
    z = lhbuild.read(MAP)
    i = z.index("\t\t\tName=" + PACIFY + CR)
    s = z.rindex("Level Part=", 0, i)
    part = z[s:balanced(z, s)]
    if "Relay Name=" + POWER + CR in part:
        return 0
    assert z.count("\t\t\tName=" + POWER + CR) == 1, "the power relay is not unique"
    z = into_relay(z, PACIFY, "Action=" + lhbuild.B(*lhbuild.relay(POWER)), 1)
    lhbuild.write_map(MAP, z)
    register([MAP])
    return 1


def main():
    print("ether exit:", build())


if __name__ == "__main__":
    main()
