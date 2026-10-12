"""Recorded voiceover sitting on dialogue nodes nothing in the game can reach.

This is `reachability.py` crossed with the voiceover corpus, and it exists because the
earlier voiceover sweep measured the wrong direction.

That sweep asked **"is every recording named after a node?"** -- 1,314 of 1,330 matched, so
it looked clean, and the 16 misses were chased to the end (see
`docs/unused-content.md`). It never asked the other question: **"can the player reach the
node a recording sits on?"** A line that was written, cast and performed, whose node is
spelled perfectly and which nothing can enter, passes the first test and fails the second.
There are 130-odd of those, and they are the strongest remaining leads in the game,
because recorded voiceover outranks every other signal: it means the line survived to the
studio.

Voiceover resolves as `<TreeName> VOs/<Node ID>.ogg` with no indirection, so the join is a
name match, folded for case, exactly as the engine does.

    python tools/vo_reach.py                 # the game as this mod leaves it
    python tools/vo_reach.py --as-shipped     # vanilla alone, ignoring files/
    python tools/vo_reach.py --min-kb 100     # only the substantial recordings

Entry points, and therefore reachability, are computed with **reachability.py's own**
`basename` / `enclosing_block` / `Node ID` logic rather than anything new. A hand-rolled
+-900-byte window around `Dialog Tree File=` was tried first and reported
`600 davinci stroll banter 7` as unwired when a map does open it -- which would have
documented a gap that is not there. Any change here belongs in both files.

The last column is the discriminator worth reading first. **Wired siblings** are nodes in
the same name family (`700 montaillou banter 4` -> `700 montaillou banter`) that a map
*does* open. Where a family has wired members and one dead one, the mechanism is already
placed and the entry for that one line was missed -- the cheapest class of repair there
is. Joan of Arc's five combat lines, of which one is wired, are the clearest case.
"""
import argparse
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
ap.add_argument("--tools", default=os.environ.get(
    "LIONHEART_TOOLS", str(REPO.parent / "LionheartModTools")))
ap.add_argument("--vanilla", default=os.environ.get("LIONHEART_VANILLA", DEFAULT_VANILLA))
ap.add_argument("--as-shipped", action="store_true",
                help="measure vanilla alone. Without this the mod's own files/ shadow the "
                     "archive, which is what keeps already-restored content out of the result")
ap.add_argument("--min-kb", type=int, default=0, help="omit recordings smaller than this")
ap.add_argument("--replies-only", action="store_true",
                help="only nodes carrying replies -- authored branches rather than barks")
args = ap.parse_args()

sys.path.insert(0, args.tools)
try:
    import dialogtree_format as dt
except ImportError:
    sys.exit("cannot import dialogtree_format from %r -- pass --tools" % args.tools)

if not Path(args.vanilla).exists():
    sys.exit("vanilla archive not found: %r -- pass --vanilla" % args.vanilla)
zf = zipfile.ZipFile(args.vanilla)
F = REPO / "files"

SCANNED = (".zax", ".dialogtree", ".can", ".txt")
TREE_EXT = ".dialogtree"
VO_DIR = " vos/"


def basename(tree_ref):
    """The key a `Dialog Tree File=` value resolves to -- see reachability.py."""
    name = tree_ref.strip().replace("\\", "/").split("/")[-1].lower()
    return name[:-len(TREE_EXT)] if name.endswith(TREE_EXT) else name


def enclosing_block(t, i):
    """Text of the innermost brace block containing offset `i` -- see reachability.py."""
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
                return t[j:k + 1]
        k += 1
    return t[j:]


TREE_REF = re.compile(r"Dialog Tree File=([^\r\n]*)")
NODE_REF = re.compile(r"(?:^|\n)[ \t]*(?:Starting )?Node ID=([^\r\n]*)")


def family(node_id):
    """`700 montaillou banter 4` -> `700 montaillou banter`, the name series it belongs to."""
    return re.sub(r"\s+\d+$", "", node_id.strip()).lower()


overlay = {}
if not args.as_shipped:
    for p in F.rglob("*"):
        if p.is_file() and p.suffix.lower() in SCANNED:
            overlay[p.relative_to(F).as_posix()] = p.read_bytes().decode("latin-1")


def corpus():
    seen = set()
    for name, text in overlay.items():
        seen.add(name.lower())
        yield name, text
    for name in zf.namelist():
        low = name.lower()
        if low.startswith("cache/") or not low.endswith(SCANNED) or low in seen:
            continue
        yield name, zf.read(name).decode("latin-1")


entries, trees = defaultdict(set), {}
for name, text in corpus():
    if name.lower().endswith(TREE_EXT):
        trees[name] = text
    if "Dialog Tree File=" not in text:
        continue
    for m in TREE_REF.finditer(text):
        key = basename(m.group(1))
        block = enclosing_block(text, m.start())
        for nm in NODE_REF.finditer(block):
            entries[key].add(dt.normalise_id(nm.group(1)))

# `<TreeName> VOs/<Node ID>.ogg`, keyed by folder stem so it joins on the tree basename.
vo = defaultdict(dict)
for name in zf.namelist():
    low = name.lower()
    if low.endswith(".ogg") and VO_DIR in low:
        folder, base = name.rsplit("/", 1)
        vo[folder.rsplit("/", 1)[-1][:-4].strip().lower()][base[:-4].lower()] = \
            zf.getinfo(name).file_size

rows, parsed, total_nodes = [], 0, 0
for path, text in sorted(trees.items()):
    key = basename(path)
    try:
        tree = dt.parse(text)
    except Exception as exc:                                   # a tree we cannot read is a
        print("!! parse failed %s: %s" % (path, exc))          # finding, not something to
        continue                                               # swallow
    if not tree.nodes:
        continue
    parsed += 1
    total_nodes += len(tree.nodes)
    ids = [dt.normalise_id(n.node_id) for n in tree.nodes]
    by_id = {}
    for i, n in zip(ids, tree.nodes):
        by_id.setdefault(i, n)        # duplicate ids: the first wins, as the engine does

    seen, stack = set(), [ids[0]] + [e for e in entries[key] if e in by_id]
    while stack:
        cur = stack.pop()
        if cur in seen or cur not in by_id:
            continue
        seen.add(cur)
        for r in by_id[cur].replies:
            g = dt.normalise_id(r.goto)
            if g and g not in seen:
                stack.append(g)

    recs = vo.get(key, {})
    wired = defaultdict(list)
    for i, n in zip(ids, tree.nodes):
        if i in entries[key]:
            wired[family(n.node_id)].append(n.node_id.strip())
    for i, n in zip(ids, tree.nodes):
        if i in seen:
            continue
        size = recs.get(n.node_id.strip().lower())
        if not size or size / 1024 < args.min_kb:
            continue
        if args.replies_only and not n.replies:
            continue
        rows.append(dict(tree=key, node=n.node_id.strip(), kb=size / 1024,
                         replies=len(n.replies),
                         siblings=sorted(wired.get(family(n.node_id), []))))

mode = "as shipped" if args.as_shipped else "as this mod leaves it (%d file(s) overlaid)" % len(overlay)
print("voiceover on unreachable nodes, %s\n" % mode)
print("%d tree(s), %d node(s), %d recording(s) in %d paired folder(s)"
      % (parsed, total_nodes, sum(len(v) for v in vo.values()), len(vo)))
print("\n*** %d unreachable node(s) carry a recording: %.2f MB across %d tree(s)"
      % (len(rows), sum(r["kb"] for r in rows) / 1024, len({r["tree"] for r in rows})))
print("    %d of those carry replies, which is where authored branches are"
      % sum(1 for r in rows if r["replies"]))

by_tree = defaultdict(list)
for r in rows:
    by_tree[r["tree"]].append(r)
print("\n%-32s %5s %8s %8s" % ("tree", "nodes", "MB", "w/replies"))
for t, v in sorted(by_tree.items(), key=lambda x: -sum(r["kb"] for r in x[1])):
    print("%-32s %5d %8.2f %8d"
          % (t, len(v), sum(r["kb"] for r in v) / 1024, sum(1 for r in v if r["replies"])))

sib = [r for r in rows if r["siblings"]]
if sib:
    print("\n--- a name sibling is already opened by a map: the mechanism is placed and one "
          "entry was missed (%d node(s), %.2f MB)" % (len(sib), sum(r["kb"] for r in sib) / 1024))
    for r in sorted(sib, key=lambda r: -r["kb"]):
        print("  %6.0f KB %2dr  %s / %s" % (r["kb"], r["replies"], r["tree"], r["node"]))
        print("               wired: %s" % ", ".join(r["siblings"]))

print("\n--- every unreachable recording, largest first")
for r in sorted(rows, key=lambda r: -r["kb"]):
    print("  %6.0f KB %2dr  %s / %s" % (r["kb"], r["replies"], r["tree"], r["node"]))

print("\nA recording here means the line was written, cast and performed. Classify before "
      "building:\nfilename drift, unreachable branch, or superseded draft -- see the orphan "
      "taxonomy in\ndocs/unused-content.md. Nodes with no replies are usually barks and "
      "balloons, which need a\ntrigger placed in a map rather than a reply written.")
