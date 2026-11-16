"""Renaldo, the Sylvant in the stocks in Inquisition Pit3, keeps his questions when you come back. Reported from play after
0.99.29: "I had to leave the conversation due to nearby enemies attacking and the second chat with him only gave me one
option".

The map opens `1 Conversation Start` on the first click and, once his brother's quest is active (either stage), every
later click opens `3 Return Dialogue With Quest`. That node held only the two quest replies, *"I'm still looking for your
brother..."* and *"Your brother sent me to free you."*, gated on the two stages, so exactly one ever shows. A player who
left the first conversation early lost the rest of it: who he is, the Eastern Knights, why he is locked up, and the
ribs.

The node now carries node 1's other five replies after the quest one, copied verbatim, so it offers what the first
conversation did. The copied Goodbye drops its default flag, so Escape behaves as before. A tree, so every save.

A rerun is a no-op.

    python tools/build_renaldo_return.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR
from build_shrine_repairs import register
from build_troll_choices import node_span, reply_start

TREE = "Resources/Levels/1 Barcelona/Dialog/Temple District/Man in Stocks in Prison.DialogTree"
FIRST, RETURN = "1 Conversation Start", "3 Return Dialogue With Quest"
FROM = "Eastern Knights?"
MARK = "Reply Text=Why are you locked up like this?" + CR


def build():
    t = lhbuild.read(TREE)
    i, j = node_span(t, RETURN)
    if MARK in t[i:j]:
        return 0
    a, b = node_span(t, FIRST)
    k = reply_start(t, FIRST, FROM)
    copied = t[k:b].rstrip(CR) + CR
    assert copied.count("Reply Text=") == 5 and "Custom Requirement" not in copied, copied
    assert copied.count("Is Default Reply=1" + CR) == 1
    copied = copied.replace("Is Default Reply=1" + CR, "")
    body = t[i:j].rstrip(CR) + CR
    assert body.count("Reply Text=") == 2
    t = t[:i] + body + CR + copied + t[j:]
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    register([TREE])
    return 1


def main():
    print("renaldo:", build())


if __name__ == "__main__":
    main()
