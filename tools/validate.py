"""Static validation for every file in the Lionheart Fixt mod tree.

  .DialogTree  - CDialogTree wrapper present and closed, brace balance, every
                 'Go to node ID' resolves (case-insensitively, which the engine
                 tolerates -- 244 vanilla links rely on it), every named
                 Requirement resolves to a real .can, and every embedded
                 Custom Action/Requirement object parses.
  .zax         - parses and round-trips, AND every map -> dialogue node
                 reference matches BYTE-EXACTLY. That last one is stricter on
                 purpose: the map-side lookup is exact and a miss is a hard
                 crash on map entry, not a silent failure. Vanilla node IDs
                 contain trailing spaces, so a reference that looks identical
                 can still be fatal -- which is exactly how the Goblin Warrens
                 crash shipped.
  everything else - parses with resource_format and round-trips byte-exact.

Also asserts the whole tree is CRLF and latin-1 clean.

Usage:
    python tools/validate.py [--tools <LionheartModTools>] [--vanilla <data.dat.vanilla.bak>]

Both default to their usual locations; override them if your checkout differs.
Exits non-zero on any problem, so it can gate a build.
"""
import argparse
import os
import re
import sys
import tempfile
import zipfile
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
args = ap.parse_args()

sys.path.insert(0, args.tools)
try:
    import resource_format as rf
except ImportError:
    sys.exit("cannot import resource_format from %r -- pass --tools" % args.tools)

F = REPO / "files"
Z = args.vanilla
if not Path(Z).exists():
    sys.exit("vanilla archive not found: %r -- pass --vanilla" % Z)

zf = zipfile.ZipFile(Z)
CANS = {Path(n).stem.lower() for n in zf.namelist()
        if n.lower().endswith(".can") and "/requirements/" in n.lower()}
CANS |= {Path(p).stem.lower() for p in F.rglob("*.can")}
CANPATHS = {n[len("Resources/"):-len(".can")].lower()
            for n in zf.namelist() if n.lower().endswith(".can")}
CANPATHS |= {str(p.relative_to(F / "Resources")).replace("\\", "/")[:-4].lower()
             for p in F.rglob("*.can")}

fails = []
LF = chr(10)


def check_dialogtree(p, raw):
    name = p.name
    if b"\n" in raw and raw.count(b"\r\n") != raw.count(b"\n"):
        fails.append(name + ": mixed line endings")
    t = raw.decode("latin-1").replace("\r\n", LF)

    if not t.startswith("CDialogTree" + LF + "{" + LF):
        fails.append(name + ": missing CDialogTree wrapper")
    if not t.rstrip().endswith("}"):
        fails.append(name + ": missing closing brace")
    if t.count(LF + "{") != t.count(LF + "}"):
        fails.append(name + ": brace imbalance")

    ids = [x.strip() for x in re.findall(r"^Node ID=(.*)$", t, re.M)]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        fails.append(name + ": duplicate node IDs " + repr(sorted(dupes)))
    low = {i.lower() for i in ids}

    for m in re.finditer(r"^Go to node ID=(.*)$", t, re.M):
        g = m.group(1).strip()
        if g and g.lower() not in low and g.lower() not in ("!none", "none"):
            fails.append(name + ": dangling target " + repr(g))

    for m in re.finditer(r"^Requirement=(.*)$", t, re.M):
        r = m.group(1).strip()
        if not r or r == "!None":
            continue
        if r.lower() in CANS or r.lower() in CANPATHS:
            continue
        fails.append(name + ": unresolved Requirement " + repr(r))

    replies = t.count(LF + "Reply Text=")
    gotos = t.count(LF + "Go to node ID=")
    if replies != gotos:
        fails.append(name + ": %d replies but %d goto lines" % (replies, gotos))

    # Every reply must be preceded by a blank line. Vanilla holds this without a single
    # exception -- 10915 replies, 0 violations -- and the parser needs it: without the
    # separator a reply is swallowed into the one before it, so its Custom Action never
    # runs. That shipped silently from 0.2.0 to 0.5 because helpers that reorder replies
    # rebuilt nodes by joining on a single newline. Caught in play, never by this file,
    # which is why it is now here.
    for m in re.finditer(LF + "Requirement=", t):
        if not t[:m.start()].endswith(LF):
            ctx = t[:m.start()].rsplit(LF + "Node ID=", 1)
            where = ctx[1].split(LF)[0].strip() if len(ctx) > 1 else "?"
            fails.append(name + ": reply not separated by a blank line, in node "
                         + repr(where))
            break

    for m in re.finditer(r"^(?:Custom Action|Custom Requirement)=(\w+)\n\{\n", t, re.M):
        start = m.end() - 2
        depth, i = 0, start
        while i < len(t):
            if t[i] == "{":
                depth += 1
            elif t[i] == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        try:
            rf.parse_resource_text(m.group(1) + LF + t[start:i + 1])
        except Exception as e:
            fails.append(name + ": embedded " + m.group(1) + " failed to parse: " + str(e))


def tree_node_ids(tree_path):
    """Exact node IDs of a tree, preferring the mod copy over vanilla."""
    raw = None
    for suffix in (".DialogTree", ".dialogtree"):
        local = F / ("Resources/" + tree_path + suffix)
        if local.exists():
            raw = local.read_bytes()
            break
    if raw is None:
        want = ("Resources/" + tree_path + ".dialogtree").lower()
        hit = None
        for n in zf.namelist():
            if n.lower() == want:
                hit = n
                break
        if hit is None:
            return None
        raw = zf.read(hit)
    txt = raw.decode("latin-1").replace("\r\n", LF)
    return [m.group(1) for m in re.finditer(r"^Node ID=(.*)$", txt, re.M)]


def check_map_node_refs(p, raw):
    z = raw.decode("latin-1").replace("\r\n", LF)
    pattern = (r"(?:CDisplayDialogTreeAction|CDisplayDialogBalloonAction)\s*\n"
               r"\s*\{(.*?)\n\s*\}")
    for m in re.finditer(pattern, z, re.S):
        body = m.group(1)
        f = re.search(r"Dialog Tree File=([^\n]*)", body)
        n = re.search(r"Node ID=([^\n]*)", body)
        if not (f and n):
            continue
        tree = f.group(1).strip()
        want = n.group(1)          # deliberately NOT stripped
        ids = tree_node_ids(tree)
        if ids is None:
            fails.append(p.name + ": dialogue tree not found: " + tree)
        elif want not in ids:
            near = [x for x in ids if x.strip().lower() == want.strip().lower()]
            why = ("tree has " + repr(near[0])) if near else "no such node"
            fails.append(p.name + ": CRASH -- exact node ref " + repr(want) +
                         " into " + tree.split("/")[-1] + " (" + why + ")")


def check_resource(p, raw):
    try:
        node = rf.parse_resource_text(raw.decode("latin-1"))
    except Exception as e:
        fails.append(p.name + ": parse failed: " + str(e))
        return
    tmp = Path(tempfile.gettempdir()) / "_rf_check.txt"
    rf.write_resource_file(node, tmp)
    if tmp.read_bytes() != raw:
        fails.append(p.name + ": not in canonical engine formatting")


# Binary payloads -- icon art, sprites, audio, models. They are shipped verbatim and are
# not resource text, so the grammar and line-ending checks do not apply to them. Every
# other extension is checked, so a new *text* type cannot slip through by being unlisted.
BINARY = {".mdl16", ".frm16", ".ogg", ".wav", ".gr2", ".way", ".bmp", ".tga", ".png"}

files = sorted(p for p in F.rglob("*") if p.is_file())
binary = 0
for p in files:
    raw = p.read_bytes()
    if p.suffix.lower() in BINARY:
        binary += 1
        if len(raw) == 0:
            fails.append(p.name + ": binary payload is empty")
        continue
    try:
        raw.decode("latin-1").encode("latin-1")
    except Exception:
        fails.append(p.name + ": not latin-1 clean")
    if p.suffix.lower() == ".dialogtree":
        check_dialogtree(p, raw)
    else:
        check_resource(p, raw)
        if p.suffix.lower() == ".zax":
            check_map_node_refs(p, raw)

# Every state of every quest this mod defines must be set by something, somewhere.
# A state that is only ever *read* is a quest that can be offered and accepted but never
# actually starts -- so its turn-in, gated on that state, never appears. Two of Quinn's
# three reagent errands shipped in 0.4.0 that way: the reply that offers them carried the
# Custom Requirement deciding whether to show it, and no Custom Action to activate it.
# Both were uncompletable, and one of them gated the peaceful route to a lava troll hide.
# Caught in play three releases later, so it lives here now.
# .can and .zax are tab-indented; DialogTrees are flat. Allow both, or this silently
# fails to see any activation that lives outside a conversation.
SET_STATE = re.compile(r"CActivateQuestStateAction[ \t]*\n[ \t]*\{[ \t]*\n"
                       r"[ \t]*Quest=([^\n]*)\n[ \t]*State=([^\n]*)")
activated = set()
for p in files:
    if p.suffix.lower() in BINARY:
        continue
    t = p.read_bytes().decode("latin-1").replace("\r\n", LF)
    for m in SET_STATE.finditer(t):
        activated.add((m.group(1).strip().lower(), m.group(2).strip()))
for q in F.rglob("*.Quest.txt"):
    rel = q.as_posix().split("/Resources/", 1)
    if len(rel) != 2:
        continue
    qpath = rel[1][:-len(".Quest.txt")].lower()
    qt = q.read_bytes().decode("latin-1").replace("\r\n", LF)
    for s in re.findall(r"^\s*ID=(.*)$", qt, re.M):
        s = s.strip()
        if s and (qpath, s) not in activated:
            fails.append(q.name + ": state " + repr(s)
                         + " is never activated -- the quest can be offered but never starts")

print("checked %d files (%d binary payloads skipped)" % (len(files), binary))
if fails:
    print("\n%d PROBLEM(S):" % len(fails))
    for f in fails:
        print("   -", f)
    sys.exit(1)
print("all checks passed")
