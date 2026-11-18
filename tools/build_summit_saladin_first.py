"""The Cathedral summit asks the Saladin question first, everywhere. Issue #16: "After joining the Templars and
progressing to the point where you set off for Montserrat and speak with Amir, you are transported to the cathedral.
A Templar starts speaking, but nothing happens".

`Church Interior.zax` decides the summit three times, each by which forcing object (`if templar`, `if saladin`, ...) is
active:

  * `Choose NIS Player` picks the scene. Since 0.80.1 it tests `if saladin` first, so the route just taken wins.
  * the walk `Done action` in `Lord Javier generator` starts the conversation once Javier reaches his mark;
  * `determine ending relay` picks how the scene ends.

The last two were left in vanilla's order, where Saladin is only the final `Else`. `if templar` is switched on when
Javier knights you (`450`/`455 made a knight`) and nothing switches it off. So a Templar who also passes the Djinn's
trial holds a Crescent perk, gets Amir's invitation (`400 next duty`), and arrives with both objects active: the
picker sets up the Saladin scene (Amir, Auric, the knights) and the dispatcher starts the Templar conversation inside
it. Javier speaks and nothing follows.

Both now test `if saladin` first, ahead of the vanilla chain, which is otherwise unchanged:
`Start Saladin NIS Conversation` and `End Saladin NIS Relay`, which already switches `if saladin` off again.

Map-side: a character who has not yet been to the Cathedral. A rerun is a no-op.

    python tools/build_summit_saladin_first.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, exists, if_action, relay
from build_shrine_repairs import register

MAP = "Levels/1 Barcelona/Church Interior.zax"
# (a relay only the dispatcher fires, the check its chain opens with, the Saladin relay to put first)
SITES = [("Start Templar NIS Conversation", "if inquisition", "Start Saladin NIS Conversation"),
         ("End Templar NIS Relay", "if dark wielder", "End Saladin NIS Relay")]


def chain_start(t, marker, first):
    """The `CIfAction` value that opens the dispatcher chain holding `Relay Name=<marker>`."""
    hits = [i for i in range(len(t)) if t.startswith("Relay Name=" + marker + lhbuild.CR, i)]
    hits = [i for i in hits if "Name To Check For=" + first in t[i - 4000:i]]
    assert len(hits) == 1, "%s: expected one dispatcher firing %r, found %d" % (MAP, marker, len(hits))
    k = t.rindex("Name To Check For=" + first, 0, hits[0])
    s = t.rindex("=CIfAction", 0, k) + 1
    assert lhbuild.balanced(t, s) > hits[0], "%s: %r is not inside the chain" % (MAP, marker)
    return s


def build():
    t = lhbuild.read(MAP)
    changed = False
    for marker, first, saladin in SITES:
        s = chain_start(t, marker, first)
        head = t[max(0, s - 400):s]
        if "Name To Check For=if saladin" in head and "Relay Name=" + saladin in t[s - 400:s + 200]:
            continue
        e = lhbuild.balanced(t, s)
        new = B(*if_action(exists("if saladin"), relay(saladin), t[s:e]))
        t = t[:s] + new.rstrip(lhbuild.CR) + t[e:]
        changed = True
    if changed:
        lhbuild.write_map(MAP, t)
        register([MAP])
    return changed


def main():
    print("summit saladin first:", build())


if __name__ == "__main__":
    main()
