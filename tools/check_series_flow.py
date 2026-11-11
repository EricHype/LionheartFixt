"""Fail the build on two faults every other gate passed, because both resolve every reference.

**A relay firing itself inline.** A series advances only after its step returns and a relay fires in the same call, so
a step that fires its own relay runs again until the stack gives out. Crossing a delay, or a balloon's or a walk's After
Action, is safe, because that runs later. Trigger Only Once blocks it too.

**A chained series with steps behind one that never continues.** A series that drives itself, by firing its own relay,
stops at the first step that neither fires that relay nor shows a conversation, so any step after it is dead. This found
the credits ahead of fifteen steps of slides. A series that something else steps through is not chained and is left alone.

Vanilla never does the first, so that rule covers every relay. Vanilla steps some series from outside while they also
fire themselves, so the second rule covers only relays Fixt named.

The checks moved to LionheartModTools (`lhcheck.py`: series-flow and nameless-spawns); this runs them with Fixt's
settings from tools/_modtools.py. validate.py runs them too.

    python tools/check_series_flow.py [--tools <LionheartModTools>]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _modtools  # noqa: E402


def _ctx(argv=None):
    lhcheck = _modtools.load("lhcheck", argv)
    return lhcheck, lhcheck.Context(_modtools.FILES, _modtools.vanilla(), config=_modtools.fixt_config())


def check(argv=None):
    lhcheck, ctx = _ctx(argv)
    return lhcheck.check_series_flow(ctx)


def names(argv=None):
    """A script aimed at a name only a nameless spawn would bear reaches nobody. See build_spawn_names.py."""
    lhcheck, ctx = _ctx(argv)
    return lhcheck.check_nameless_spawns(ctx)


def main():
    lhcheck, ctx = _ctx(sys.argv)
    bad = lhcheck.check_series_flow(ctx) + lhcheck.check_nameless_spawns(ctx)
    for b in bad:
        print(" -", b)
    print(f"{len(bad)} series fault(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
