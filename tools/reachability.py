"""Find dialogue nodes nothing in the game can reach.

A node is reachable if you can arrive at it by following `Go to node ID` from an entry
point. Entry points are:

  * the first node in the file -- the conventional default start, and
  * any node named by a `Dialog Tree File=` / `Node ID=` pair anywhere in the corpus.

Two details in that second rule are what make this correct rather than approximately
correct, and both were got wrong on the first attempt:

  * **Those two fields sit in the same brace block in either order.** A forward-only scan
    of the N bytes after `Dialog Tree File=` misses every block that names the node first,
    and then reports live balloon nodes as orphans. The block is delimited properly here.
  * **`.can` files open dialogue too.** Character templates carry
    `CDisplayDialogTreeAction` of their own -- 10+ of them in the shipped game, including
    `Inquisition Guard Generic` and `Brother Michel`. Scanning only `.zax` and
    `.DialogTree` invents orphans in exactly the trees most worth reading.

Node IDs match case-insensitively with surrounding whitespace trimmed, which is what the
engine does -- see `dialogtree_format.normalise_id`. Comparing exactly reports 369 shipped
replies as broken, including the goodbye of the first NPC in the game.

Two modes:

    python tools/reachability.py
        Gate mode. Checks the trees this mod ships and fails on any node that is
        unreachable *and* is either new or was reachable in vanilla. Vanilla's own
        orphans are tolerated -- a Fixt tree is usually a shipped tree with nodes spliced
        in, and it should not have to inherit the blame for what it copied. Exits
        non-zero on a problem, so it can gate a build.

    python tools/reachability.py --survey "Port District"
        Survey mode. Reports unreachable nodes in the *shipped* game under any path
        matching the argument, newest question first: what did the developers write and
        never connect? Pass "" for the whole game. This is how 0.6.0 was scoped.

Survey mode reads the whole archive and takes about a minute; gate mode reads only what
it needs to resolve the mod's own trees.
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
ap.add_argument("--vanilla", default=os.environ.get(
    "LIONHEART_VANILLA", DEFAULT_VANILLA))
ap.add_argument("--survey", metavar="PATH_FRAGMENT",
                help="report unreachable nodes in the shipped game instead of gating "
                     "the mod; matches tree paths case-insensitively, '' means all")
ap.add_argument("--all-nodes", action="store_true",
                help="survey: list every unreachable node, not just those with replies")
ap.add_argument("--with-mod", action="store_true",
                help="survey: measure the game as this mod leaves it, not as it shipped. "
                     "Without this a survey re-reports content Fixt has already "
                     "restored, which reads like a discovery and is not one")
args = ap.parse_args()

sys.path.insert(0, args.tools)
try:
    import dialogtree_format as dt
except ImportError:
    sys.exit("cannot import dialogtree_format from %r -- pass --tools" % args.tools)

F = REPO / "files"
if not Path(args.vanilla).exists():
    sys.exit("vanilla archive not found: %r -- pass --vanilla" % args.vanilla)
zf = zipfile.ZipFile(args.vanilla)

# Anything that can carry a CDisplayDialogTreeAction or CDisplayDialogBalloonAction.
SCANNED = (".zax", ".dialogtree", ".can", ".txt")
TREE_EXT = ".dialogtree"


def basename(tree_ref):
    """The key a `Dialog Tree File=` value resolves to.

    Matched on basename rather than full path: the corpus writes these with mixed
    separators and inconsistent leading segments, and no two shipped trees share a
    basename.

    The extension is stripped because **the two sides spell it differently**. A map says
    `Dialog Tree File=Levels/1 Barcelona/Dialog/Port District/Distressed Sailor`, with no
    extension at all, while the file on disk is `Distressed Sailor.DialogTree`. Keying one
    side with the extension and the other without silently finds zero entry points, and
    then every node a map opens directly looks orphaned -- which is a failure that reads
    like a discovery.
    """
    name = tree_ref.strip().replace("\\", "/").split("/")[-1].lower()
    return name[:-len(TREE_EXT)] if name.endswith(TREE_EXT) else name


def enclosing_block(t, i):
    """Text of the innermost brace block containing offset `i`."""
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


def entry_points(sources):
    """basename -> {normalised node id} named from outside the trees themselves."""
    out = defaultdict(set)
    for text in sources:
        if "Dialog Tree File=" not in text:
            continue
        for m in TREE_REF.finditer(text):
            key = basename(m.group(1))
            block = enclosing_block(text, m.start())
            for nm in NODE_REF.finditer(block):
                out[key].add(dt.normalise_id(nm.group(1)))
    return out


def corpus_texts(overlay):
    """Every scannable file, with `overlay` (path -> text) shadowing the archive.

    The overlay is how a mod's edited map replaces the shipped one rather than being
    unioned with it. Unioning would hide a link this mod had *removed*.
    """
    seen = set()
    for name, text in overlay.items():
        seen.add(name.lower())
        yield text
    for name in zf.namelist():
        low = name.lower()
        if low.startswith("cache/") or not low.endswith(SCANNED) or low in seen:
            continue
        yield zf.read(name).decode("latin-1")


def unreachable(tree, entries):
    """Nodes of `tree` not reachable from its first node or any id in `entries`."""
    if not tree.nodes:
        return []
    ids = [dt.normalise_id(n.node_id) for n in tree.nodes]
    by_id = {}
    for i, n in zip(ids, tree.nodes):
        by_id.setdefault(i, n)          # duplicate ids: the first one wins, as the engine does

    seen, stack = set(), [ids[0]] + [e for e in entries if e in by_id]
    while stack:
        cur = stack.pop()
        if cur in seen or cur not in by_id:
            continue
        seen.add(cur)
        for r in by_id[cur].replies:
            g = dt.normalise_id(r.goto)
            if g and g not in seen:
                stack.append(g)
    return [n for i, n in zip(ids, tree.nodes) if i not in seen]


def show(node):
    text = " ".join(node.text.split())
    return "%-42s %d replies  %s" % ("[" + node.node_id + "]", len(node.replies),
                                     text[:90])


# ---------------------------------------------------------------- survey mode
if args.survey is not None:
    want = args.survey.lower()
    survey_overlay = {}
    if args.with_mod:
        for p in sorted(F.rglob("*")):
            if p.is_file() and p.suffix.lower() in SCANNED:
                survey_overlay[p.relative_to(F).as_posix()] = \
                    p.read_bytes().decode("latin-1")
    by_lower = {k.lower(): v for k, v in survey_overlay.items()}
    entries = entry_points(corpus_texts(survey_overlay))
    trees = sorted(n for n in zf.namelist()
                   if n.lower().endswith(TREE_EXT) and want in n.lower())
    if not trees:
        sys.exit("no shipped dialogue trees match %r" % args.survey)
    if args.with_mod:
        print("surveying the game as this mod leaves it (%d file(s) overlaid)"
              % len(survey_overlay))

    total_nodes = total_orphans = total_with_replies = 0
    for name in trees:
        # read our edited copy of the tree when we ship one, so nodes this mod has
        # already spliced in are counted as present
        text = by_lower.get(name.lower())
        tree = dt.parse(text if text is not None
                        else zf.read(name).decode("latin-1"))
        orphans = unreachable(tree, entries[basename(name)])
        total_nodes += len(tree.nodes)
        total_orphans += len(orphans)
        withreplies = [n for n in orphans if n.replies]
        total_with_replies += len(withreplies)
        listed = orphans if args.all_nodes else withreplies
        if not listed:
            continue
        print("\n=== %s" % Path(name).name)
        print("    %d nodes, %d unreachable (%d carry replies)"
              % (len(tree.nodes), len(orphans), len(withreplies)))
        for n in listed:
            print("    " + show(n))

    print("\n%d trees, %d nodes, %d unreachable, %d of those carry replies."
          % (len(trees), total_nodes, total_orphans, total_with_replies))
    print("Nodes with no replies are usually balloons and combat barks fired straight "
          "from a map.\nThe ones carrying replies are where authored branches are.")
    if not args.all_nodes:
        print("Pass --all-nodes to see the rest.")
    sys.exit(0)

# ------------------------------------------------------------------ gate mode
mod_trees = sorted(F.rglob("*.DialogTree")) + sorted(F.rglob("*.dialogtree"))
mod_trees = sorted({p.resolve() for p in mod_trees})
if not mod_trees:
    print("no dialogue trees in the mod tree -- nothing to check")
    sys.exit(0)

overlay = {}
for p in sorted(F.rglob("*")):
    if p.is_file() and p.suffix.lower() in SCANNED:
        overlay[p.relative_to(F).as_posix()] = p.read_bytes().decode("latin-1")

entries = entry_points(corpus_texts(overlay))
VANILLA = {basename(n): n for n in zf.namelist()
           if n.lower().endswith(TREE_EXT)}

fails = []
tolerated = 0
for p in mod_trees:
    key = basename(p.name)
    tree = dt.parse(p.read_bytes().decode("latin-1"))
    orphans = unreachable(tree, entries[key])
    if not orphans:
        continue

    # What was already unreachable in the shipped tree is not this mod's to answer for.
    inherited = set()
    if key in VANILLA:
        base = dt.parse(zf.read(VANILLA[key]).decode("latin-1"))
        inherited = {dt.normalise_id(n.node_id)
                     for n in unreachable(base, entries[key])}

    for n in orphans:
        if dt.normalise_id(n.node_id) in inherited:
            tolerated += 1
            continue
        fails.append("%s: node %r is unreachable -- nothing links to it and no map "
                     "opens it" % (p.name, n.node_id.strip()))

print("checked %d dialogue tree(s)%s"
      % (len(mod_trees),
         "; tolerated %d node(s) already orphaned in vanilla" % tolerated
         if tolerated else ""))
if fails:
    print("\n%d PROBLEM(S):" % len(fails))
    for f in fails:
        print("   -", f)
    sys.exit(1)
print("every node this mod adds is reachable")
