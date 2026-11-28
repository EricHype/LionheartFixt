"""Quests a player can start and never finish, and gates that wait on a state nothing sets.

Four of the sixteen defects `sibling_replies.py` found were quests: one copy of a reply that should
start, advance or finish a quest and did not. That pointed here. A quest is driven entirely by
actions scattered through dialogue, maps and cans:

    CActivateQuestStateAction        starts it, or moves it to a state      (Quest=, State=)
    CSetQuestSatusToCompletedAction  finishes it                            (Quest=)
    CSetQuestSatusToFailedAction     fails it                               (Quest=)
    CSetQuestSatusToFailedIfActiveAction                                    (Quest=)

and read by six checks (`CIsQuestStateTheCurrentStateAction`, `CWasQuestStateActivatedAction`,
`CWasQuestEverActivatedAction`, `CIsQuestCompletedAction`, `CIsQuestFailedAction`,
`CIsQuestStillCompleatableAction`). Nothing checks that those agree with each other or with the
quest files. This reports, for the game as Fixt leaves it:

  dangling   a Quest= that names no quest file, or a State= that is no state of its quest
  no-end     a quest something a player can reach starts, which nothing a player can reach ends
  dead-end   ... and its only completion or failure sits somewhere a player cannot reach
  dead-gate  a check waiting on a state that nothing reachable ever activates, so the reply or
             branch behind it never appears

**What "reachable" means here.** An action on a dialogue reply counts only when the reply's node
is reachable from the tree's first node or from a conversation that opens it -- `reachability.py`'s
rule, plus the link-rot finding that a node opened only as a balloon never offers its replies.
Balloon-only actions are kept apart as `balloon`, because whether a balloon runs its reply's
action is not established; nothing is concluded from them either way. Actions in maps, cans and
canned scripts count as reachable: telling a level part that is never switched on from one that is
is `deadparts.py`'s job, not this one's, so a map-only start or end is labelled `map` in the output
so it can be checked.

**A survey.** A quest that is meant to stay open (a standing order, a sub-quest whose parent ends
it) will show as no-end. Read the quest and its sources before calling anything broken.

    python tools/quest_reach.py                   # the game as this mod leaves it
    python tools/quest_reach.py --as-shipped       # vanilla alone
    python tools/quest_reach.py --quest "Lion Shield"
    python tools/quest_reach.py --csv quests.csv
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
ap.add_argument("--as-shipped", action="store_true", help="vanilla alone, ignoring files/")
ap.add_argument("--quest", default="", help="only quests whose path contains this (case-insensitive)")
ap.add_argument("--csv", help="also write every finding here")
ap.add_argument("--uses", action="store_true", help="with --quest: list every use of the matching quests")
args = ap.parse_args()

sys.path.insert(0, args.tools)
try:
    import dialogtree_format as dt
except ImportError:
    sys.exit("cannot import dialogtree_format from %r -- pass --tools" % args.tools)

zf = zipfile.ZipFile(args.vanilla)
SCANNED = (".zax", ".dialogtree", ".can", ".txt")
# Quest actions also live on items (picking up the Felgnash Sword sets its quest state from
# `Felgnash Sword.InventoryItem`), so actions are read from every text resource that names a quest,
# not from a list of extensions. Binary caches are skipped.
BINARY = (".ogg", ".wav", ".mp3", ".tga", ".bmp", ".png", ".jpg", ".mdl16", ".seq16", ".frm16", ".dds", ".fnt")
TREE_REF = re.compile(r"Dialog Tree File=([^\r\n]*)")
NODE_REF = re.compile(r"(?:^|\n)[ \t]*(?:Starting )?Node ID=([^\r\n]*)")

START = {"CActivateQuestStateAction"}
END = {"CSetQuestSatusToCompletedAction", "CSetQuestSatusToFailedAction", "CSetQuestSatusToFailedIfActiveAction"}
STATE_CHECK = {"CIsQuestStateTheCurrentStateAction", "CWasQuestStateActivatedAction"}
CHECK = STATE_CHECK | {"CWasQuestEverActivatedAction", "CIsQuestCompletedAction", "CIsQuestFailedAction",
                       "CIsQuestStillCompleatableAction"}
ALL = START | END | CHECK

corpus = {n.lower(): ("zip", n) for n in zf.namelist()}
if not args.as_shipped:
    F = REPO / "files"
    for p in F.rglob("*"):
        if p.is_file():
            corpus[p.relative_to(F).as_posix().lower()] = ("file", p)


def read(key):
    kind, where = corpus[key]
    return (where.read_bytes() if kind == "file" else zf.read(where)).decode("latin-1")


def shown(key):
    kind, where = corpus[key]
    return where if kind == "zip" else key


# ------------------------------------------------- reachability, as sibling_replies.py has it
def basename(tree_ref):
    name = tree_ref.strip().replace("\\", "/").split("/")[-1].lower()
    return name[:-len(".dialogtree")] if name.endswith(".dialogtree") else name


def enclosing_block(t, i):
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
    """basename -> ({ids a conversation opens}, {ids only a balloon opens})"""
    conv, ball = defaultdict(set), defaultdict(set)
    for key in corpus:
        if key.startswith("cache/") or not key.endswith(SCANNED):
            continue
        t = read(key)
        if "Dialog Tree File=" not in t:
            continue
        for m in TREE_REF.finditer(t):
            j, block = enclosing_block(t, m.start())
            head = t[max(0, j - 300):j].rstrip().splitlines()
            to = ball if head and "CDisplayDialogBalloonAction" in head[-1] else conv
            for nm in NODE_REF.finditer(block):
                to[basename(m.group(1))].add(dt.normalise_id(nm.group(1)))
    return conv, ball


def walk(tree, starts):
    by_id = {}
    for n in tree.nodes:
        by_id.setdefault(dt.normalise_id(n.node_id), n)
    seen, stack = set(), [s for s in starts if s in by_id]
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        stack += [g for g in (dt.normalise_id(r.goto) for r in by_id[cur].replies if r.goto) if g in by_id]
    return seen


# ------------------------------------------------------------------- quest actions
def quest_key(ref):
    r = ref.strip().replace("\\", "/").lower()
    if r in ("", "!none"):
        return None
    if not r.startswith("resources/"):
        r = "resources/" + r
    return r if r.endswith(".quest.txt") else r + ".quest.txt"


def actions_in(text):
    """(class, quest key, raw quest, state) for every quest action or check in a text."""
    out = []
    for m in re.finditer(r"=(C\w+)\r?\n", text):
        cls = m.group(1)
        if cls not in ALL:
            continue
        # Anchor on the action's own opening brace. Maps are tab-indented, so "one character past
        # the line" lands before the brace, and the enclosing block would be the parent's -- which
        # pins some other action's Quest= on this one. That bug reported four map-ended quests as
        # endless on the first run.
        brace = text.find("{", m.end())
        if brace < 0 or text[m.end():brace].strip():
            continue
        _, block = enclosing_block(text, brace + 1)
        nested = block.find("{", 1)
        if nested > 0:
            block = block[:nested]
        q = re.search(r"^\s*Quest=([^\r\n]*)", block, re.M)
        s = re.search(r"^\s*State=([^\r\n]*)", block, re.M)
        if q:
            out.append((cls, quest_key(q.group(1)), q.group(1).strip(), s.group(1).strip() if s else None))
    return out


def reply_text(node, r):
    return "\r\n".join(l for e in node.entries[r.start:r.end] for l in e.to_lines())


def main():
    quests = {}
    for key in corpus:
        if key.endswith(".quest.txt") and key.startswith("resources/levels/"):
            t = read(key)
            name = re.search(r"^\s*Name=([^\r\n]*)", t, re.M)
            parent = re.search(r"^\s*Sub-Quest of=([^\r\n]*)", t, re.M)
            quests[key] = dict(name=name.group(1).strip() if name else "?",
                               states=set(re.findall(r"^\s*ID=([^\r\n]*?)\s*$", t, re.M)),
                               parent=(parent.group(1).strip() if parent else ""))
    conv, ball = entry_points()
    # Requirement= names a requirement can by its stem; a can's checks matter only through the
    # replies that name it, so remember which replies do, and whether a player can choose them.
    req_users = defaultdict(list)
    uses = []  # (where-kind, file key, place, cls, quest key, raw, state)
    for key in sorted(corpus):
        if key.startswith("cache/") or key.endswith(BINARY) or key.endswith(".quest.txt") or "test" in key:
            continue
        t = read(key)
        if "Quest=" not in t:
            continue
        if not key.endswith(".dialogtree"):
            kind = "map" if key.endswith(".zax") else "item" if key.endswith(".inventoryitem") else "script"
            for a in actions_in(t):
                uses.append((kind, key, "", *a))
            continue
        tree = dt.parse(t)
        if not tree.nodes:
            continue
        b = basename(key)
        first = dt.normalise_id(tree.nodes[0].node_id)
        live = walk(tree, [first] + list(conv[b]))
        balloon = walk(tree, list(ball[b])) - live
        for n in tree.nodes:
            nid = dt.normalise_id(n.node_id)
            kind = "live" if nid in live else "balloon" if nid in balloon else "dead"
            for r in n.replies:
                for a in actions_in(reply_text(n, r)):
                    uses.append((kind, key, n.node_id.strip(), *a))
                req = r.requirement.strip()
                if req and req != "!None":
                    req_users[req.lower()].append((kind, key, n.node_id.strip(), " ".join(r.text.split())))
        # The tree root's own actions (Default Canceled Node Action and the like) run when the tree
        # is open, so they are live exactly when the tree is opened as a conversation.
        root = "\r\n".join(l for e in tree.header for l in e.to_lines())
        for a in actions_in(root):
            uses.append(("live" if b in conv else "dead", key, "(tree root)", *a))

    reachable = {"live", "map", "script", "item"}
    if args.uses:
        for kind, key, place, cls, qk, raw, state in sorted(uses, key=lambda u: (u[4] or "", u[3], u[1])):
            if args.quest.lower() in (raw or "").lower():
                print("%-8s %-38s %-9s %-44s [%s]" % (kind, cls[:38], state or "", shown(key).split("/")[-1][:44], place[:40]))
        return
    rows = []
    inert = [0]
    want = args.quest.lower()
    for kind, key, place, cls, qk, raw, state in uses:
        if want and want not in (raw or "").lower():
            continue
        if qk not in quests:
            rows.append(dict(finding="dangling", detail="no such quest", quest=raw, state=state or "",
                             cls=cls, where=kind, file=shown(key), place=place))
        elif state and cls in START | STATE_CHECK and state not in quests[qk]["states"]:
            rows.append(dict(finding="dangling", detail="no such state", quest=raw, state=state,
                             cls=cls, where=kind, file=shown(key), place=place))
    by_q = defaultdict(list)
    for u in uses:
        if u[4] in quests:
            by_q[u[4]].append(u)
    for qk, us in sorted(by_q.items()):
        if want and want not in qk:
            continue
        starts = [u for u in us if u[3] in START and u[0] in reachable]
        ends = [u for u in us if u[3] in END and u[0] in reachable]
        anyend = [u for u in us if u[3] in END]
        q = quests[qk]
        label = q["name"] + (" (sub-quest of %s)" % q["parent"] if q["parent"] not in ("", "!None") else "")
        wins = [u for u in ends if u[3] == "CSetQuestSatusToCompletedAction"]
        anywin = [u for u in us if u[3] == "CSetQuestSatusToCompletedAction"]
        if starts and not ends:
            finding = "dead-end" if anyend else "no-end"
            src = anyend if anyend else starts
            rows.append(dict(finding=finding, detail=label, quest=qk, state="",
                             cls="%d reachable start(s); ends only from: %s" % (len(starts), ",".join(sorted({u[0] for u in anyend})) or "nothing"),
                             where=",".join(sorted({u[0] for u in starts})), file=shown(src[0][1]), place=src[0][2]))
        elif starts and not wins:
            src = anywin if anywin else starts
            rows.append(dict(finding="no-win", detail=label, quest=qk, state="",
                             cls="%d reachable start(s); can only fail; completion %s" % (
                                 len(starts), "only from: " + ",".join(sorted({u[0] for u in anywin})) if anywin else "nowhere"),
                             where=",".join(sorted({u[0] for u in starts})), file=shown(src[0][1]), place=src[0][2]))
        set_live = {u[6] for u in us if u[3] in START and u[0] in reachable}
        for u in us:
            kind, key, place, cls, _, raw, state = u
            if not (cls in STATE_CHECK and kind in reachable and state in q["states"] and state not in set_live):
                continue
            set_any = sorted({v[0] for v in us if v[3] in START and v[6] == state})
            others = sorted({o for o in quests if o != qk and state in quests[o]["states"]})
            why = "state set only from: " + (",".join(set_any) or "nothing")
            if others:
                why += "; the same ID is a state of " + ", ".join(o.split("/")[-1][:-len(".quest.txt")] for o in others)
            if key.endswith(".can") and "/requirements/" in key:
                users = req_users[Path(key).stem.lower()]
                live = [x for x in users if x[0] == "live"]
                if not live:
                    inert[0] += 1
                    continue
                for _, tkey, node, text in live:
                    rows.append(dict(finding="dead-gate", detail=label, quest=qk, state=state, cls=cls,
                                     where=why, file=shown(tkey),
                                     place="%s: %r via %s" % (node, text[:50], Path(key).stem)))
                continue
            rows.append(dict(finding="dead-gate", detail=label, quest=qk, state=state, cls=cls,
                             where=why, file=shown(key), place=place))
    order = {"dangling": 0, "no-end": 1, "dead-end": 2, "no-win": 3, "dead-gate": 4}
    rows.sort(key=lambda r: (order[r["finding"]], r["quest"].lower(), r["file"], r["place"]))
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["finding"])
            w.writeheader()
            w.writerows(rows)
    last = None
    for r in rows:
        if r["finding"] != last:
            print("\n== %s" % r["finding"])
            last = r["finding"]
        print("  %s %s\n      %s [%s]  starts: %s\n      %s" % (
            r["quest"].split("/")[-1][:60], r["state"], r["file"].split("/")[-1][:50], r["place"][:40],
            r["where"], r["cls"] if r["finding"] != "dangling" else r["detail"] + " (" + r["cls"] + ")"))
    counts = defaultdict(int)
    for r in rows:
        counts[r["finding"]] += 1
    print("\n%d quests; %d uses; %s; %d more dead gates sit in requirement cans no reachable reply uses" % (
        len(quests), len(uses), ", ".join("%s %d" % (k, counts[k]) for k in order), inert[0]))


main()
