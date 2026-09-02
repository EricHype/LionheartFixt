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

# Every Model= an entity names must exist as art, or the game dies on map entry with a
# "Fatal Not Found Error" naming the model and the map. That is a hard crash, not a
# silent failure -- and it shipped in 0.5.0, from a chest placed with the invented path
# "Environments/Misc/Chest/Chest A". Nothing else here would have caught it: the file
# parsed, round-tripped byte-exact, deployed byte-identical, and passed every other gate.
MODELS = {n[len("Cache/Models/"):-len(".mdl16")].lower()
          for n in zf.namelist()
          if n.lower().startswith("cache/models/") and n.lower().endswith(".mdl16")}
MODELS |= {str(p.relative_to(F / "Cache" / "Models")).replace("\\", "/")[:-len(".mdl16")].lower()
           for p in (F / "Cache" / "Models").rglob("*.mdl16")} \
    if (F / "Cache" / "Models").exists() else set()
# Editor/* markers are placeholders the editor draws and the engine ignores, and the
# empty value and !Unknown Model are both legal "no art" spellings.
MODEL_OK = {"", "!unknown model"}

# `Cur Sequence` has to name an animation the model actually has, and the failure is the
# same fatal crash with the same dialog -- 0.5.0 shipped a chest set to "Idle" when the
# chest models only have Closed/Open/Opening. Rather than parse sequence tables out of
# the .mdl16, take the pairs vanilla itself uses: 200 shipped maps are a better authority
# on which sequence goes with which model than anything inferred.
SEQ_RE = re.compile(r"Model=([^\r\n]+)\r\n(?:[^\r\n]*\r\n){0,12}?[ \t]*Cur Sequence=([^\r\n]*)")
VANILLA_SEQ = {}
for _n in zf.namelist():
    if not _n.lower().endswith(".zax"):
        continue
    for _m in SEQ_RE.finditer(zf.read(_n).decode("latin-1")):
        VANILLA_SEQ.setdefault(_m.group(1).strip().lower(), set()).add(_m.group(2).strip())

fails = []
LF = chr(10)


_VANILLA_DANGLING = {}


def vanilla_dangling(p):
    """Dangling `Go to node ID` targets in the SHIPPED copy of this same tree.

    Empty for a tree this mod authored, which is the point: only inherited breakage is
    excused, never breakage in something we wrote.
    """
    rel = p.relative_to(F).as_posix()
    if rel in _VANILLA_DANGLING:
        return _VANILLA_DANGLING[rel]
    out = set()
    try:
        v = zf.read(rel).decode("latin-1").replace("\r\n", LF)
    except KeyError:
        pass
    else:
        ids = {x.strip().lower() for x in re.findall(r"^Node ID=(.*)$", v, re.M)}
        for m in re.finditer(r"^Go to node ID=(.*)$", v, re.M):
            g = m.group(1).strip().lower()
            if g and g not in ids and g not in ("!none", "none"):
                out.add(g)
    _VANILLA_DANGLING[rel] = out
    return out


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

    # A Fixt dialogue tree is almost always a *shipped* tree with nodes spliced into it,
    # so it inherits whatever was already broken -- `Fish Monger` alone ships four dead
    # `Go to node ID=` targets, and `Bar Patrons` ships three more in a branch nothing can
    # reach. Reporting those says nothing about this mod and drowns out the ones it would
    # actually introduce, so they are tolerated exactly the way reachability.py tolerates
    # nodes already orphaned in vanilla: compare against the shipped copy of the same file
    # and report only what is new. A tree we author from scratch has no vanilla
    # counterpart, so every dangling target in it is still reported.
    inherited = vanilla_dangling(p)
    for m in re.finditer(r"^Go to node ID=(.*)$", t, re.M):
        g = m.group(1).strip()
        if g and g.lower() not in low and g.lower() not in ("!none", "none"):
            if g.lower() in inherited:
                continue
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


def check_models(p, raw):
    """Every Model= names art that exists. A miss is a fatal crash on map entry."""
    seen = set()
    for m in re.finditer(r"^\s*Model=(.*)$", raw.decode("latin-1"), re.M):
        v = m.group(1).strip()
        low = v.lower()
        if low in MODEL_OK or low.startswith("editor/") or low in seen:
            continue
        seen.add(low)
        if low not in MODELS:
            fails.append(p.name + ": CRASH -- Model=" + repr(v)
                         + " does not exist; the engine dies on map entry")
    # Only pairs this mod introduces are judged; a pair already in the vanilla copy of
    # the same map is the game's own business even if it looks odd.
    rel = "Levels/" + p.as_posix().split("/files/Levels/", 1)[-1]
    try:
        vanilla_same_map = zf.read(rel).decode("latin-1")
    except KeyError:
        vanilla_same_map = ""
    for m in SEQ_RE.finditer(raw.decode("latin-1")):
        mod, seq = m.group(1).strip(), m.group(2).strip()
        if mod.lower().startswith("editor/") or mod.lower() in MODEL_OK:
            continue
        if SEQ_RE.search(vanilla_same_map) and re.search(
                re.escape("Model=" + mod) + r"\r\n(?:[^\r\n]*\r\n){0,12}?[ \t]*Cur Sequence="
                + re.escape(seq), vanilla_same_map):
            continue
        known = VANILLA_SEQ.get(mod.lower())
        if known and seq not in known:
            fails.append(p.name + ": CRASH -- Cur Sequence=" + repr(seq) + " on Model="
                         + repr(mod) + "; vanilla uses " + repr(sorted(known)))


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
            check_models(p, raw)

# Every state of every quest this mod defines must be set by something, somewhere.
# A state that is only ever *read* is a quest that can be offered and accepted but never
# actually starts -- so its turn-in, gated on that state, never appears. Two of Quinn's
# three reagent errands shipped in 0.4.0 that way: the reply that offers them carried the
# Custom Requirement deciding whether to show it, and no Custom Action to activate it.
# Both were uncompletable, and one of them gated the peaceful route to a lava troll hide.
# Caught in play three releases later, so it lives here now.
# .can and .zax are tab-indented; DialogTrees are flat. Allow both, or this silently
# fails to see any activation that lives outside a conversation.
#
# The activation does not have to live in *our* files. As soon as this mod ships an
# edited copy of a shipped quest -- 0.6.0's `help distressed sailor` is the first -- the
# states it inherits are activated by vanilla maps we do not ship, and scanning only the
# mod tree reports every one of them as dead. So the vanilla archive is scanned too, with
# our own files shadowing their archive counterparts rather than being unioned with them:
# unioning would hide an activation this mod had deliberately *removed*.
SET_STATE = re.compile(r"CActivateQuestStateAction[ \t]*\n[ \t]*\{[ \t]*\n"
                       r"[ \t]*Quest=([^\n]*)\n[ \t]*State=([^\n]*)")
SCANNED_FOR_STATES = (".zax", ".dialogtree", ".can", ".txt")
activated = set()


def collect_activations(text):
    for m in SET_STATE.finditer(text):
        activated.add((m.group(1).strip().lower(), m.group(2).strip()))


ours = set()
for p in files:
    if p.suffix.lower() in BINARY:
        continue
    ours.add(p.relative_to(F).as_posix().lower())
    collect_activations(p.read_bytes().decode("latin-1").replace("\r\n", LF))
for name in zf.namelist():
    low = name.lower()
    if low.startswith("cache/") or not low.endswith(SCANNED_FOR_STATES):
        continue
    if low in ours:                      # our edited copy already contributed
        continue
    collect_activations(zf.read(name).decode("latin-1").replace("\r\n", LF))

for q in F.rglob("*.Quest.txt"):
    rel = q.as_posix().split("/Resources/", 1)
    if len(rel) != 2:
        continue
    qpath = rel[1][:-len(".Quest.txt")].lower()
    qt = q.read_bytes().decode("latin-1").replace("\r\n", LF)
    ids = [s.strip() for s in re.findall(r"^\s*ID=(.*)$", qt, re.M)]

    # The array's declared length must match what follows it. A `.zax` tolerates a wrong
    # `Item Count` in some places because the reader walks braces, but a quest's state
    # array is read as a counted list: declare too few and the tail is silently dropped,
    # which presents as a quest whose log never advances past a certain step.
    m = re.search(r"States=Array\s*\n\s*\{\s*\n\s*Item Count=(\d+)", qt)
    if not m:
        fails.append(q.name + ": no States=Array with an Item Count")
    elif int(m.group(1)) != len(ids):
        fails.append(q.name + ": Item Count=%s but %d State entries"
                     % (m.group(1), len(ids)))

    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        fails.append(q.name + ": duplicate state IDs " + repr(dupes))
    for s in ids:
        if not re.fullmatch(r"[A-Z0-9]{8}", s):
            fails.append(q.name + ": state ID " + repr(s)
                         + " is not 8 uppercase alphanumerics")

    for s in ids:
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
