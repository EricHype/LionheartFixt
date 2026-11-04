"""Give every greeting variant the Fixt replies its siblings already have.

Found by `tools/check_node_variants.py` and `triage_node_variants.py` after 0.93.3, which fixed
the same defect for Farshad: a conversation whose greeting is chosen by who you are, with content
hung on only some of the branches. The player sees one greeting and cannot tell that another
would have offered more.

**The hangover cure, 0.4.x, is cut off from several openings.** Both of its gates are quest
state -- `Fixt Hangover Asked`, `Fixt Hangover Has Root`, `Fixt Hangover Need Root` -- so the
replies can be copied to a sibling verbatim and the gate still does the work. Nothing here
changes when a reply appears, only who can see it.

    Herbalist   an Inquisitor or a Knight Templar could not start the cure at all
    weird woman four normal greetings would not sell the root

**Deliberately not touched.** `100 Weird Woman pissed return` is her refusing to deal with you
at all ("I will not tolerate you any more"); silence is the content there. And the Bar Patrons'
`1500` family looked like a finding but is a *state progression* with the drunk, not a set of
variants -- the cure hangs off `return after give gold` because that is the state it belongs to.
Both are reported by the survey and both are correct as they stand.

Usage: python tools/fix_variant_gaps.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import CR, FX, read

HERB = "Resources/Levels/1 Barcelona/Dialog/Gate District/Herbalist Dialogue.DialogTree"
WEIRD = "Resources/Levels/3 Montaillou/Dialog/weirdwoman.DialogTree"

# tree -> donor node -> (destinations to copy, target nodes)
WORK = [
    (HERB, "1 Conversation Start",
     ["1710 Fixt the nightshade", "1711 Fixt the cure brewed"],
     ["1 Conversation Start Inquisitor", "1 Conversation Start Knight Templar"]),
    (WEIRD, "01 Conversation Start",
     ["1720 Fixt the nightshade root"],
     ["03 Return Dialogue if Heard 50 AND shapechanged Beatrice",
      "05 Return Dialogue if Not Heard 50 AND shapechanged Beatrice",
      "5 Return if Inquisitor",
      "06 Return Destroyed Montaillou"]),
]


def node_span(text, node_id):
    start = text.index("Node ID=" + node_id + CR)
    nxt = text.find(CR + "-" * 20, start)
    return start, (nxt if nxt > start else len(text))


def reply_block(node_text, dest):
    """The single reply block routing to `dest`, taken verbatim."""
    line = "Go to node ID=" + dest + CR
    i = node_text.index(line)
    # rfind, not index: index would return the node's FIRST Requirement and swallow every
    # reply above this one. That shipped 18 replies into a 7-reply node in 0.93.3.
    j = node_text.rfind("Requirement=", 0, i)
    end = node_text.find(CR + CR, i)
    block = node_text[j:end if end > 0 else len(node_text)].rstrip(CR) + CR
    assert block.count("Reply Text=") == 1, \
        "block for %s holds %d replies" % (dest, block.count("Reply Text="))
    assert line in block
    return block


def insert(node_text, block):
    """Put the reply above a trailing default/exit reply, else append.

    **Every reply must be separated from its neighbours by a blank line.** The first version
    of this joined the new block straight onto the trailing default reply, and `validate.py`
    refused it -- the same "reply not separated by a blank line" defect that silently broke 47
    replies across three releases before Gate 0 learned to look for it. Both seams are built
    explicitly here rather than left to a join.
    """
    parts = re.split(r"(?=" + re.escape(CR) + "Requirement=)", node_text)
    last = parts[-1]
    body = block.rstrip(CR)
    if "Is Default Reply=1" in last or "Icon=Exit Icon" in last:
        head = node_text[:len(node_text) - len(last)].rstrip(CR)
        return head + CR + CR + body + CR + CR + last.lstrip(CR)
    return node_text.rstrip(CR) + CR + CR + body + CR


def main():
    total = 0
    for rel, donor, dests, targets in WORK:
        t = read(rel)
        assert t.count("\n") == t.count(CR), rel + " is not all-CRLF"
        d0, d1 = node_span(t, donor)
        donor_text = t[d0:d1]
        blocks = [reply_block(donor_text, d) for d in dests]

        changed = []
        for target in targets:
            if "Node ID=" + target + CR not in t:
                print("   !! %s: no such node" % target)
                continue
            s0, s1 = node_span(t, target)
            node = t[s0:s1]
            add = [b for b, d in zip(blocks, dests)
                   if ("Go to node ID=" + d + CR) not in node]
            if not add:
                continue
            for b in add:
                node = insert(node, b)
            t = t[:s0] + node + t[s1:]
            changed.append((target, len(add)))

        if not changed:
            print("%-26s nothing to do" % rel.split("/")[-1][:24])
            continue
        assert t.count("\n") == t.count(CR), rel + " lost CRLF"
        for d in dests:
            n = t.count("Go to node ID=" + d + CR)
            assert n >= 2, "%s is still reachable from only %d place(s)" % (d, n)
        (FX / rel).parent.mkdir(parents=True, exist_ok=True)
        (FX / rel).write_bytes(t.encode("latin-1"))
        print("%s" % rel.split("/")[-1])
        for target, n in changed:
            print("   +%d  %s" % (n, target))
            total += n
    print("\n%d replies restored" % total)


if __name__ == "__main__":
    main()
