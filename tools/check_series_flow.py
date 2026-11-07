"""Fail the build on two faults every other gate passed, because both resolve every reference.

**A relay firing itself inline.** A series advances only after its step returns and a relay fires in the same call, so
a step that fires its own relay runs again until the stack gives out. Crossing a delay, or a balloon's or a walk's After
Action, is safe, because that runs later. Trigger Only Once blocks it too.

**A chained series with steps behind one that never continues.** A series that drives itself, by firing its own relay,
stops at the first step that neither fires that relay nor shows a conversation, so any step after it is dead. This found
the credits ahead of fifteen steps of slides. A series that something else steps through is not chained and is left alone.

Vanilla never does the first, so that rule covers every relay. Vanilla steps some series from outside while they also
fire themselves, so the second rule covers only relays Fixt named.

    python tools/check_series_flow.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild

FILES = Path(__file__).resolve().parent.parent / "files"
LATER = {"After Action", "Next Action", "Done action", "Stop Action", "Starting Action", "End Turn Action", "Action to execute After Effect"}


class N:
    __slots__ = ("cls", "kv")

    def __init__(self, c):
        self.cls = c
        self.kv = []


def parse(text):
    root = N("root")
    st = [root]
    pend = None
    for raw in text.split("\r\n"):
        l = raw.strip()
        if l == "{":
            n = N(pend[1] if pend else "")
            (pend[2] if pend else st[-1]).kv.append((pend[0] if pend else "", n))
            st.append(n)
            pend = None
            continue
        if pend:
            pend[2].kv.append((pend[0], pend[1]))
            pend = None
        if l == "}":
            if len(st) > 1:
                st.pop()
            continue
        if "=" in l:
            k, v = l.split("=", 1)
            if re.fullmatch(r"C[A-Za-z0-9]+|Array", v):
                pend = (k, v, st[-1])
            else:
                st[-1].kv.append((k, v))
    return root


def inline(n, name):
    """True if this action reaches a trigger of `name` without crossing anything that runs later."""
    if n.cls == "CTriggerRelayAction" and dict(n.kv).get("Relay Name") == name:
        return True
    return any(isinstance(v, N) and k not in LATER and inline(v, name) for k, v in n.kv)


def continues(n, name):
    """True if this action can hand on: a conversation, or firing the relay at any distance."""
    if n.cls == "CDisplayDialogTreeAction":
        return True
    if n.cls == "CTriggerRelayAction" and dict(n.kv).get("Relay Name") == name:
        return True
    return any(isinstance(v, N) and continues(v, name) for k, v in n.kv)


def fires(n, name):
    if n.cls == "CTriggerRelayAction" and dict(n.kv).get("Relay Name") == name:
        return True
    return any(isinstance(v, N) and fires(v, name) for k, v in n.kv)


def relays(root):
    def go(n, part):
        if n.cls == "CRelayAI":
            yield part, n
        for k, v in n.kv:
            if isinstance(v, N):
                yield from go(v, dict((a, b) for a, b in v.kv if not isinstance(b, N)).get("Name", part))

    yield from go(root, "")


def series_in(n):
    if n.cls == "CSeriesAction":
        yield n
    for k, v in n.kv:
        if isinstance(v, N):
            yield from series_in(v)


def check():
    bad = []
    for f in sorted(FILES.rglob("*.zax")):
        rel = f.relative_to(FILES).as_posix()
        root = parse(lhbuild.read(rel))
        for name, ai in relays(root):
            f_ = dict(ai.kv)
            act = f_.get("Action")
            if not name or not isinstance(act, N):
                continue
            if f_.get("Trigger Only Once") == "0" and inline(act, name):
                bad.append(f"{rel}: relay `{name}` fires itself inline, and will recurse until the stack overflows")
            for s in series_in(act):
                arr = dict(s.kv).get("Action")
                steps = [v for k, v in arr.kv if k == "Action" and isinstance(v, N)] if isinstance(arr, N) else []
                if not name.startswith("Fixt") or not any(fires(x, name) for x in steps):
                    continue
                last = max((i for i, x in enumerate(steps) if continues(x, name)), default=-1)
                for i, x in enumerate(steps[:last]):
                    if not continues(x, name):
                        bad.append(f"{rel}: relay `{name}` step {i + 1} does not continue, so steps {i + 2}-{len(steps)} are dead")
    return bad


def main():
    bad = check()
    for b in bad:
        print(" -", b)
    print(f"{len(bad)} series fault(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
