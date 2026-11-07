"""The end slides can finish. Since 0.71.0 the epilogue relay could only have crashed or stopped short.

Found by adversarial review, read from the decompilation, never seen in play, because no character has reached the
credits on any of these builds.

* **It recursed.** A series advances only after its step returns (`0x56ffc0`), and a relay fires inline (`0x422c00`). A
  step with no slide fired its own relay from Else, so the same step ran again until the stack gave out. It was the only
  relay in the game that did this. The self-fires now sit in a 0.1 second delay, so they land after the advance.
* **It could not advance.** `CIfExpressionAction` returns false from Else (`0x58fe40`) and Require Success held the index,
  so the Else steps had to be let through. It is off.
* **Half of it was unreachable.** The credits were step 17 of 32 and fire nothing, so all fifteen steps of companion
  slides behind them never ran. The credits are now last.

A slide still advances through its own reply, or through the tree's Default Canceled Node Action on Escape.

`150 Final encounter` moves to the shaman: 0.97.3 made the guard and his English twin alive together, and a balloon
fails on two matches.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_epilogue_flow.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, delay, relay

ENDGAME = "Levels/8 Alamut/END GAME Siege Map.zax"
SEER = "Levels/5 Nostrodomus/05 Nostrodomus Demesne.zax"
RELAY = "Fixt order epilogue relay"
ITEM = "\t" * 7 + "Action="


def relay_span(z):
    i = z.index("\t\t\tName=" + RELAY + CR)
    return i, z.index("\r\n\t\t}", i)


def items(p):
    """The series' steps, as text spans. A step starts at the series' own indent."""
    a = p.index(CR, p.index("Item Count=", p.index("Action=CSeriesAction"))) + len(CR)
    b = p.index("When Done=", a)
    b = p.rindex("\t" * 6 + "}", a, b)
    starts = [m.start() for m in re.finditer(r"(?m)^" + ITEM + "C", p[a:b])]
    return a, b, [p[a + s:a + e] for s, e in zip(starts, starts[1:] + [b - a])]


def ending():
    z = lhbuild.read(ENDGAME)
    i, e = relay_span(z)
    p = z[i:e]
    if "Require Success To Advance=0" in p:
        return
    a, b, steps = items(p)
    assert len(steps) == 32, len(steps)
    credits = [s for s in steps if "CShowCreditsAction" in s]
    assert len(credits) == 1 and steps.index(credits[0]) == 16
    steps.remove(credits[0])
    steps.append(credits[0])
    p = p[:a] + "".join(steps) + p[b:]

    fire = re.compile(r"CTriggerRelayAction\r\n\s*\{\r\n\s*Relay Name=" + RELAY + r"\r\n\s*\}")
    p, n = fire.subn(lambda m: B(*delay("0.1", relay(RELAY))).rstrip(), p)
    assert n == 53, n
    k = p.rindex("Require Success To Advance=1")
    p = p[:k] + "Require Success To Advance=0" + p[k + len("Require Success To Advance=1"):]
    assert p.count("Require Success To Advance=1") == 0
    lhbuild.write_map(ENDGAME, z[:i] + p + z[e:])


def seer():
    z = lhbuild.read(SEER)
    k = z.index("Node ID=150 Final encounter" + CR)
    old = "Name of Position=Hujark Guard"
    n = z.find(old, k, k + 200)
    if n < 0:
        return
    lhbuild.write_map(SEER, z[:n] + "Name of Position=Hujark Shaman" + z[n + len(old):])


def main():
    ending()
    seer()


if __name__ == "__main__":
    main()
