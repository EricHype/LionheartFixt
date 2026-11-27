"""Replies that say the same thing under the same gate, and do different things.

A tree often carries one reply in several nodes -- the same "Goodbye." on every menu, the same
"Yes, an ale would be nice." at the first meeting and on return. When the copies agree on text and
gate, they should agree on what they do. Two vanilla defects found while repairing the link rot
(docs/link-rot.md) had exactly this shape and no check could see either:

  * the Viola Organista's "Goodbye." at `5 organ already tuned` goes to `5 organ tuned`, the
    first-tuning greeting, while both other copies go to `5 goodbye`;
  * the Conspirator's "Yes, an ale would be nice." at `3 return no drink` goes to `10 take ale`
    like its twin at `1 Conversation Start`, but gives no ale and sets no `took drink`.

So: group a tree's replies by (text, gate) and report every group whose copies differ in target or
in action. **The gate is part of the key on purpose.** "Can you spare some coin" goes to one node
for a human and another for a tainted character, and that is the design, not a defect; copies that
differ in gate are never compared.

**A survey, and a noisy one.** A first meeting that pays and a return that does not can be the
point. What makes a row strong is an *outlier*: three or more copies, and exactly one disagrees.
Read both ends before believing any row, and use the tree's own majority as the default answer.

Only replies a player can choose are compared: on a node reachable from the tree's first node or
from a conversation that opens it. Entry points use reachability.py's own `basename` /
`enclosing_block` / `Node ID` logic, with one addition from the link-rot work: a node opened only
by `CDisplayDialogBalloonAction` is not an entry point, because a balloon never offers replies.

    python tools/sibling_replies.py                  # the game as this mod leaves it
    python tools/sibling_replies.py --as-shipped      # vanilla alone, ignoring files/
    python tools/sibling_replies.py --outliers        # only the strong rows
    python tools/sibling_replies.py --tree Conspirator
"""
import argparse
import csv
import os
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_VANILLA = os.path.join(
    "C:" + os.sep, "Program Files (x86)", "GOG Galaxy", "Games",
    "Lionheart - Legacy of the Crusader", "data.dat.vanilla.bak")

ap = argparse.ArgumentParser()
ap.add_argument("--tools", default=os.environ.get("LIONHEART_TOOLS", str(REPO.parent / "LionheartModTools")))
ap.add_argument("--vanilla", default=os.environ.get("LIONHEART_VANILLA", DEFAULT_VANILLA))
ap.add_argument("--as-shipped", action="store_true", help="measure vanilla alone, ignoring files/")
ap.add_argument("--outliers", action="store_true", help="only groups of 3+ where exactly one copy differs")
ap.add_argument("--tier", help="only outliers of these tiers, e.g. A or AB (see rank())")
ap.add_argument("--tree", default="", help="only trees whose path contains this (case-insensitive)")
ap.add_argument("--csv", help="also write every row here")
args = ap.parse_args()

sys.path.insert(0, args.tools)
try:
    import dialogtree_format as dt
except ImportError:
    sys.exit("cannot import dialogtree_format from %r -- pass --tools" % args.tools)

zf = zipfile.ZipFile(args.vanilla)
SCANNED = (".zax", ".dialogtree", ".can", ".txt")
TREE_REF = re.compile(r"Dialog Tree File=([^\r\n]*)")
NODE_REF = re.compile(r"(?:^|\n)[ \t]*(?:Starting )?Node ID=([^\r\n]*)")

# The archive with files/ shadowing it, keyed by lowercased path.
corpus = {n.lower(): ("zip", n) for n in zf.namelist()}
if not args.as_shipped:
    F = REPO / "files"
    for p in F.rglob("*"):
        if p.is_file():
            corpus[p.relative_to(F).as_posix().lower()] = ("file", p)


def read(key):
    kind, where = corpus[key]
    return (where.read_bytes() if kind == "file" else zf.read(where)).decode("latin-1")


def basename(tree_ref):
    """As reachability.py: basename, extension stripped, folded."""
    name = tree_ref.strip().replace("\\", "/").split("/")[-1].lower()
    return name[:-len(".dialogtree")] if name.endswith(".dialogtree") else name


def enclosing_block(t, i):
    """As reachability.py: text of the innermost brace block containing offset `i`."""
    depth, j = 0, i
    while j > 0:
        if t[j] == "}":
            depth += 1
        elif t[j] == "{":
            if depth == 0:
                break
            depth -= 1
        j -= 1
    depth, k = 0, j
    while k < len(t):
        if t[k] == "{":
            depth += 1
        elif t[k] == "}":
            depth -= 1
            if depth == 0:
                return j, t[j:k + 1]
        k += 1
    return j, t[j:]


def entry_points():
    """basename -> node ids a conversation (not a balloon) opens from outside the tree."""
    out = defaultdict(set)
    for key in corpus:
        if key.startswith("cache/") or not key.endswith(SCANNED):
            continue
        t = read(key)
        if "Dialog Tree File=" not in t:
            continue
        for m in TREE_REF.finditer(t):
            j, block = enclosing_block(t, m.start())
            head = t[max(0, j - 300):j].rstrip().splitlines()
            if head and "CDisplayDialogBalloonAction" in head[-1]:
                continue
            for nm in NODE_REF.finditer(block):
                out[basename(m.group(1))].add(dt.normalise_id(nm.group(1)))
    return out


def reachable(tree, entries):
    ids = [dt.normalise_id(n.node_id) for n in tree.nodes]
    by_id = {}
    for i, n in zip(ids, tree.nodes):
        by_id.setdefault(i, n)
    seen, stack = set(), [ids[0]] + [e for e in entries if e in by_id]
    while stack:
        cur = stack.pop()
        if cur in seen or cur not in by_id:
            continue
        seen.add(cur)
        stack += [dt.normalise_id(r.goto) for r in by_id[cur].replies if r.goto]
    return seen


def flat(lines):
    """An embedded object as one comparable string: whitespace folded, blank lines dropped."""
    return " ".join(" ".join(l.split()) for l in lines if l.strip())


def gate(r):
    return (r.requirement.strip(), flat(r.block_for("Custom Requirement")))


def action(r):
    head = (r._get("Custom Action") or "").strip()
    return (head + " " + flat(r.block_for("Custom Action"))).strip()


def classes(a):
    return ",".join(sorted(set(re.findall(r"\b(C[A-Z]\w+Action)\b", a)))) or "-"


VARIANT = re.compile(r"tainted|feral|human|male|female|inquisit|sylvant|demokin|good|bad|angry|accept|return", re.I)


def rank(odd_node, odd, majority):
    """How an outlier differs from its twins, and how much that is worth reading.

    The direction is the signal. A copy that *lacks* what its twins do, or ends where they go on,
    is the shape of both defects this tool was built from. A copy that does *more* is usually a
    first-time flag ("Action work in progress=(Set Know James)"). A different target from a
    node named for a race, gender or standing is usually that variant's own branch."""
    (og, oa), (mg, ma) = odd, majority
    oc, mc = set(re.findall(r"\bC[A-Z]\w+", oa)), set(re.findall(r"\bC[A-Z]\w+", ma))
    variant = bool(VARIANT.search(odd_node)) and og != mg
    if og == mg and ma and (not oa or oc < mc):
        return "A", "lacks its twins' action"
    if mg and not og and not oa:
        return "A", "ends where its twins go on"
    if og != mg and not variant:
        return "B", "goes elsewhere"
    if og == mg and oa and not ma:
        return "C", "does more than its twins"
    return "C", "variant branch" if variant else "differs in action"


def main():
    entries = entry_points()
    rows = []
    trees = sorted(k for k in corpus if k.endswith(".dialogtree") and "test" not in k and args.tree.lower() in k)
    for key in trees:
        tree = dt.parse(read(key))
        if not tree.nodes:
            continue
        live = reachable(tree, entries[basename(key)])
        groups = defaultdict(list)
        for n in tree.nodes:
            if dt.normalise_id(n.node_id) not in live:
                continue
            for i, r in enumerate(n.replies, 1):
                text = " ".join(r.text.split())
                if text:
                    groups[(text.lower(), gate(r))].append(("%s#%d" % (n.node_id.strip(), i), r, text))
        for (_, g), copies in groups.items():
            if len(copies) < 2:
                continue
            does = [(dt.normalise_id(r.goto), action(r)) for _, r, _ in copies]
            kinds = set(does)
            if len(kinds) < 2:
                continue
            counts = defaultdict(int)
            for d in does:
                counts[d] += 1
            majority = max(counts.values())
            outlier = len(copies) >= 3 and majority == len(copies) - 1
            targets = {d[0] for d in does}
            acts = {d[1] for d in does}
            kind = "target+action" if len(targets) > 1 and len(acts) > 1 else "target" if len(targets) > 1 else "action"
            tier, why = "-", ""
            if outlier:
                maj = max(counts, key=counts.get)
                oi = next(i for i, d in enumerate(does) if counts[d] == 1)
                tier, why = rank(copies[oi][0], does[oi], maj)
            for (nid, r, text), d in zip(copies, does):
                rows.append(dict(
                    tree=key.split("/")[-1][:-len(".dialogtree")], path=corpus[key][1] if corpus[key][0] == "zip" else key,
                    fixt="yes" if corpus[key][0] == "file" else "no", text=text, gate=" & ".join(x for x in g if x and x != "!None") or "-",
                    kind=kind, strength="outlier" if outlier else "split", tier=tier, why=why, copies=len(copies),
                    odd="ODD" if outlier and counts[d] == 1 else "", node=nid, goto=r.goto or "(ends)",
                    actions=classes(d[1])))
    if args.outliers:
        rows = [r for r in rows if r["strength"] == "outlier"]
    if args.tier:
        rows = [r for r in rows if r["tier"] in args.tier.upper()]
    rows.sort(key=lambda r: (r["tier"] if r["tier"] != "-" else "Z", r["tree"], r["text"]))
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["tree"])
            w.writeheader()
            w.writerows(rows)
    last = None
    for r in rows:
        head = (r["tree"], r["text"], r["gate"])
        if head != last:
            print("\n%s%s  [%s, %s, %d copies%s]\n  %r  gate: %s" % (
                (r["tier"] + ": " + r["why"] + " -- ") if r["tier"] != "-" else "",
                r["tree"], r["kind"], r["strength"], r["copies"], ", Fixt" if r["fixt"] == "yes" else "",
                r["text"][:90], r["gate"][:80]))
            last = head
        print("   %-3s %-40s -> %-36s %s" % (r["odd"], "[" + r["node"][:38] + "]", r["goto"][:36], r["actions"]))
    groups = {(r["tree"], r["text"], r["gate"]) for r in rows}
    strong = {(r["tree"], r["text"], r["gate"]) for r in rows if r["strength"] == "outlier"}
    tiers = defaultdict(set)
    for r in rows:
        tiers[r["tier"]].add((r["tree"], r["text"], r["gate"]))
    print("\n%d groups in %d trees; %d are outliers (A %d, B %d, C %d)" % (
        len(groups), len({g[0] for g in groups}), len(strong),
        len(tiers["A"]), len(tiers["B"]), len(tiers["C"])))


main()
