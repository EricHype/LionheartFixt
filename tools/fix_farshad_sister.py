"""Give a female Knight of Saladin the two replies her brother gets.

Farshad's return greeting is chosen by gender, and only on one side of that branch:

    if Saladin Favored:
        if Male -> "3 Return Knight of Saladin Male"      <- 8 replies
        else    -> "3 Retun Knight of Saladin Sister"     <- 5 replies
    else        -> "3 Return Dialogue"                    <- 7 replies

The Sister node is missing **"Where are you from?"** and **"Why were you fighting?"**, both
present on the other three greetings. Vanilla shipped it that way; the typo in its node ID is
vanilla's too.

**That made Fixt's duelling lesson unreachable for every female Knight of Saladin.** The lesson
hangs off `50 duel`, and "Why were you fighting?" is the only route to it. The ordering is what
makes this bite rather than being a curiosity: you become Saladin Favored during the initiation
and Eduardo forges the scimitar as part of the same questline, so by the time the lesson's own
gate can pass you are always on a *return* greeting -- and for a woman that greeting is the one
with no way in. `1 Conversation Start` carries the reply, but that is long before you have the
blade.

Found from a bug report of "I talked to them and saw nothing", where the reporter blamed their
scimitar. The scimitar was innocent: the lesson accepts either quest blade.

**The lesson itself needs no change.** It lives on the shared `50 duel` node, so restoring the
route restores the lesson with it.

Not touched: the Male node also has a plain "Goodbye." that the Sister node lacks, and she
carries `Is Default Reply=1` on a different reply as a result. That is a cosmetic difference in
how the conversation exits, it works today, and moving a default reply is not worth the risk in
a repair aimed at a dead end.

Usage: python tools/fix_farshad_sister.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import CR, FX, read

REL = "Resources/Levels/1 Barcelona/Dialog/Gate District/saladinknightcan.DialogTree"
SISTER = "3 Retun Knight of Saladin Sister"          # vanilla's typo, kept
MALE = "3 Return Knight of Saladin Male"

RESTORE = [("Where are you from?", "20 persia"),
           ("Why were you fighting?", "50 duel")]


def node_bounds(text, node_id):
    """The slice of `text` holding one node, separator to separator."""
    start = text.index("Node ID=" + node_id + CR)
    nxt = text.find(CR + "-" * 20, start)
    assert nxt > start, "no separator after " + node_id
    return start, nxt


def main():
    t = read(REL)
    assert t.count("\n") == t.count(CR), "source is not all-CRLF"

    s0, s1 = node_bounds(t, SISTER)
    sister = t[s0:s1]
    m0, m1 = node_bounds(t, MALE)
    male = t[m0:m1]

    added = []
    for reply, dest in RESTORE:
        line = "Reply Text=" + reply + CR
        if line in sister:
            print("   already present: %s" % reply)
            continue
        # take the block verbatim from the male node, so the wording and routing match
        i = male.index(line)
        # rfind, not index. `index` returns the FIRST "Requirement=" in the node, so the
        # block would span every reply above the target one -- which shipped 18 replies into
        # a node that should hold 7, while the "did it land" assert still passed because the
        # wanted line was somewhere inside. The reply-count assert below is the real guard.
        j = male.rfind("Requirement=", 0, i)
        end = male.index(CR + CR, i)
        block = male[j:end] + CR + CR
        assert "Go to node ID=" + dest + CR in block, \
            "%r does not route to %s in the male node" % (reply, dest)
        assert block.count("Reply Text=") == 1, \
            "the block for %r carries %d replies" % (reply, block.count("Reply Text="))
        sister = sister.rstrip(CR) + CR + CR + block.rstrip(CR) + CR
        added.append(reply)

    if not added:
        print("nothing to do")
        return

    out = t[:s0] + sister + t[s1:]
    assert out.count("\n") == out.count(CR), "lost CRLF"
    # the restored replies must now exist on BOTH nodes, and nowhere else new
    for reply, dest in RESTORE:
        n0, n1 = node_bounds(out, SISTER)
        assert ("Reply Text=" + reply + CR) in out[n0:n1], reply + " did not land"
    assert out.count("Node ID=") == t.count("Node ID="), "node count changed"
    assert out.count("Is Default Reply=1") == t.count("Is Default Reply=1"), \
        "default-reply count changed"
    (FX / REL).parent.mkdir(parents=True, exist_ok=True)
    (FX / REL).write_bytes(out.encode("latin-1"))

    n0, n1 = node_bounds(out, SISTER)
    print("restored to the Sister node: %s" % ", ".join(added))
    print("   replies now: sister %d, male %d" % (
        out[n0:n1].count("Reply Text="), male.count("Reply Text=")))


if __name__ == "__main__":
    main()
