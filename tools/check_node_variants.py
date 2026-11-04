"""Find conversation variants that have drifted apart.

**The defect this exists for.** Farshad's return greeting is chosen by gender, and only the male
branch carried "Why were you fighting?" -- the sole route to `50 duel`, where Fixt hung his
duelling lesson. So no female Knight of Saladin could ever be taught. Every node resolved, every
requirement parsed, nothing pointed at a missing node, and `validate.py` was silent. The defect
was that **one of four entry points into a node could not reach it**, which is a reachability
question about a graph and nothing was asking it.

**The signal.** When a map picks between several `Node ID`s *in the same dialogue tree* from one
conditional chain, those nodes are variants of a single moment -- male/female, Inquisitor/not,
first meeting/return. A player sees exactly one of them. They should therefore offer the same
*destinations*, because a destination present in one and missing from another is content that
some characters can reach and others cannot, for reasons nobody chose.

Reply **text** legitimately differs (he calls you brother or sister). Reply **requirements**
legitimately differ. Where a reply *goes* is the thing that should match, so that is what is
compared.

**This is a survey, not a gate.** Vanilla drifted in plenty of places and most of it is harmless
or deliberate. It earns its keep by being run when a release adds a reply: if the node you
attached it to has variants, this says whether all of them can reach it.

Usage:
    python tools/check_node_variants.py            # only trees Fixt ships
    python tools/check_node_variants.py --all      # every tree, vanilla included
"""
import collections
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import zf, read, FX

SEP = re.compile(r"(?m)^-{20,}$")


def all_files():
    return sorted(set(zf.namelist())
                  | {"Resources/" + p.relative_to(FX / "Resources").as_posix()
                     for p in (FX / "Resources").rglob("*") if p.is_file()})


def tree_nodes(text):
    """node id -> list of destinations its replies point at."""
    out = {}
    for block in SEP.split(text.replace("\r\n", "\n")):
        m = re.match(r"\s*Node ID=(.+)", block)
        if not m:
            continue
        dests = [d.strip() for d in re.findall(r"^Go to node ID=(.*)$", block, re.M)]
        out[m.group(1).strip()] = [d for d in dests if d]
    return out


def selections(files):
    """(tree, frozenset(node ids)) that some map picks between in one conditional chain.

    A chain is recognised by proximity: `CDisplayDialogTreeAction`s naming the same tree, close
    together in one map, are the arms of a single if/else. 4000 characters is wide enough for the
    three-deep chains the game actually writes and narrow enough not to join unrelated triggers.
    """
    groups = collections.defaultdict(set)
    for n in files:
        if not n.endswith(".zax"):
            continue
        try:
            t = read(n).replace("\r\n", "\n")
        except Exception:
            continue
        # Group by the enclosing conditional, found by brace matching -- not by proximity.
        # Proximity grouped unrelated conversation states (a return greeting beside a quest
        # reaction) and produced 135 findings, nearly all noise. The arms of ONE if/else are
        # the real signal: the player takes exactly one of them at the same moment.
        lines = t.split("\n")
        starts = [i for i, l in enumerate(lines)
                  if l.strip() in ("Action=CIfAction", "Action=CConditionalAction",
                                   "Then=CIfAction", "Else=CIfAction",
                                   "Then=CConditionalAction", "Else=CConditionalAction")]
        claimed = set()
        for i in starts:
            if i in claimed:
                continue                      # an inner conditional: the outer one owns it
            depth, end = 0, None
            for j in range(i + 1, len(lines)):
                s = lines[j].strip()
                if s == "{":
                    depth += 1
                elif s == "}":
                    depth -= 1
                    if depth == 0:
                        end = j
                        break
            if end is None:
                continue
            claimed |= set(range(i, end + 1))
            block = "\n".join(lines[i:end + 1])
            by_tree = collections.defaultdict(set)
            for m in re.finditer(r"Dialog Tree File=([^\n]+)\n[ \t]*Node ID=([^\n]*)", block):
                node = m.group(2).strip()
                if node:
                    by_tree[m.group(1).strip()].add(node)
            # Only compare nodes sharing a leading number. The game numbers node IDs by
            # conversational position, so `3 Return Knight of Saladin Male`, `3 Retun ...
            # Sister` and `3 Return Dialogue` are one beat told three ways, while `1
            # Conversation Start`, `2 Return Dialogue angry` and `6 saved daughter` are
            # different beats that SHOULD offer different things. Without this the Woodcutter
            # alone produced four findings, none of them real.
            for tree, nodes in by_tree.items():
                beats = collections.defaultdict(set)
                for node in nodes:
                    m = re.match(r"(\d+)\b", node)
                    if m:
                        beats[m.group(1)].add(node)
                for _, same in beats.items():
                    if len(same) > 1:
                        groups[(tree, frozenset(same))].add(n.split("/")[-1])
    return groups


def main():
    everything = "--all" in sys.argv
    files = all_files()
    fixt_ships = {("Resources/" + p.relative_to(FX / "Resources").as_posix())
                  for p in (FX / "Resources").rglob("*") if p.is_file()}

    groups = selections(files)
    print("%d sets of nodes are chosen between by a map conditional\n" % len(groups))

    findings = 0
    for (tree, nodes), maps in sorted(groups.items(), key=lambda kv: str(kv[0])):
        rel = "Resources/" + tree + ".DialogTree"
        if rel not in files:
            continue
        if not everything and rel not in fixt_ships:
            continue
        try:
            nodemap = tree_nodes(read(rel))
        except Exception:
            continue
        present = {n: nodemap.get(n) for n in nodes if n in nodemap}
        if len(present) < 2:
            continue
        union = set()
        for d in present.values():
            union |= set(d)
        gaps = {n: sorted(union - set(d)) for n, d in present.items() if union - set(d)}
        if not gaps:
            continue
        findings += 1
        print("%s" % tree)
        print("   picked in: %s" % ", ".join(sorted(maps)))
        for n in sorted(present):
            miss = gaps.get(n)
            print("   %-38s %2d dest%s" % (n[:38], len(present[n]), "" if miss is None else ""))
            if miss:
                for d in miss:
                    print("        cannot reach: %s" % d)
        print()
    print("%d variant set%s differ in what they can reach%s"
          % (findings, "" if findings == 1 else "s",
             "" if everything else "  (--all to include vanilla-only trees)"))


if __name__ == "__main__":
    main()
