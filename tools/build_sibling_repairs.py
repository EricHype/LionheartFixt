"""Fifteen replies that did less than their identical twins now do the same. See docs/sibling-replies.md.

`tools/sibling_replies.py` groups a tree's replies by text and gate and reports the copies that
disagree. Read one by one, sixteen were defects: a copy that lacks the action every twin carries, or
ends the conversation where its twins go on. Fifteen are repaired here. The sixteenth, Jafar's
*"I will go to Montserrat"*, is not a defect after all: the one exit from where it leads activates
the same quest state, so the copy only skips activating it one line early.

Every repair makes the odd copy match its own twins in the same tree, so nothing here is new
behaviour:

  * **copy**: the twin's `Custom Action` block, byte for byte, onto the odd copy, which had none;
  * **retarget**: the odd copy's `Go to node ID` to where its twins go;
  * **Lord Javier**, the one that also removes: his first-meeting *"I would like to donate the
    thousand gold"* took 1000 gold itself and then went to `210 give gold`, which takes 1000 again.
    The return copies carry no action and pass through `520 before I accept`, the warning that no
    other faction will take you. The first-meeting copy now does the same: it charged twice and
    skipped the one warning the choice has.

The odd copy and its twin are named by node and exact text, and must share a gate, so a repair
cannot land on a lookalike. Only the named reply changes. Dialogue-only, so it reaches a save
already in progress. A rerun is a no-op.

    python tools/build_sibling_repairs.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR, DASH
from build_shrine_repairs import register

sys.path.insert(0, str(lhbuild.MODTOOLS))
import dialogtree_format as dt

B = "Resources/Levels/1 Barcelona/Dialog/"
M = "Resources/Levels/3 Montaillou/Dialog/"

# (id, tree, odd node, twin node, reply text, op, new target)
#   op "copy":   give the odd copy its twin's Custom Action
#   op "goto":   send the odd copy where its twin goes
#   op "javier": route through the twin's target and drop the odd copy's own action
REPAIRS = [
    ("S1", B + "Port District/shakespeare.dialogtree", "5 Return Dialogue 2", "3 Return Dialogue",
     "I convinced Shylocke to extend your debt.", "copy", None),
    ("S2", M + "ToulouseRhea.DialogTree", "15 Might makes right", "11 Morality 3",
     "Your philosophy sickens me.", "copy", None),
    ("S3", None, "200 a hell of a deal", "30 name",
     "You are a foul demon and worthy of a swift death, not freedom.", "goto", "50 Insult"),
    ("S4", None, "50 Linripper", "60 strategy",
     "How many goblins have you killed so far?", "goto", "70 goblin body count"),
    ("S5", B + "Gate District/Blacksmith.DialogTree", "07 what more", "01 Introduction Non-tainted Male",
     "I've been told you can forge a Lion Shield.", "copy", None),
    ("S6", B + "Gate District/GuardTomas.DialogTree", "15 Other Questions", "1 Conversation Start",
     "I have killed some goblins just around the bend there, apparently they were spying on Barcelona.", "copy", None),
    ("S7", B + "Gate District/GuardTomas.DialogTree", "15 Other Questions", "1 Conversation Start",
     "Someone has been murdered. The corpse is just to the east of the city gate.", "copy", None),
    ("S8", B + "Gate District/GuardTomas.DialogTree", "15 Other Questions", "1 Conversation Start",
     "There are goblins spying along the western wall of the city.", "copy", None),
    ("S9", None, "900 Toulouse", "900 Toulouse Return From Node 4",
     "Is Montaillou in danger?", "copy", None),
    ("S11", None, "35 Shell Game 2", "03 Return Dialogue if Heard 50",
     "You have the look of a witch. I think the Inquisition would want to have a word with you.", "copy", None),
    ("S12a", B + "Port District/Conspirator.DialogTree", "3 return no drink", "1 Conversation Start",
     "Yes, an ale would be nice.", "copy", None),
    ("S12b", B + "Port District/Conspirator.DialogTree", "3 return no drink", "1 Conversation Start",
     "The Serpent's Bile sounds good.", "copy", None),
    ("S12c", B + "Port District/Conspirator.DialogTree", "3 return no drink", "1 Conversation Start",
     "I'm not interested in drinking with *you*.", "copy", None),
    ("S13", B + "Port District/Fish Monger.DialogTree", "10 name", "3 Return Dialogue",
     "I have a vodyanoi skull to sell you.", "copy", None),
    ("S14", None, "23 The Wish Ending", "30 Efreet",
     "I will see what I can do.", "copy", None),
    ("S15", B + "Temple District/LordJavier.DialogTree", "1 Conversation Start", "3 Return Dialogue",
     "I would like to donate the thousand gold.", "javier", None),
    ("S16", B + "Gate District/Viola Organista.DialogTree", "5 organ already tuned", "5 organ tuned",
     "Goodbye.", "goto", None),
]

# Trees named by basename where the folder is not worth spelling out; resolved against the archive.
BY_NAME = {"S3": "demon", "S4": "bounty hunter", "S9": "mayor", "S11": "weirdwoman", "S14": "spirit council"}


def resolve(rid, rel):
    if rel:
        return rel
    want = BY_NAME[rid] + ".dialogtree"
    hits = [n for n in lhbuild.zf.namelist() if n.lower().endswith("/" + want)]
    assert len(hits) == 1, (rid, hits)
    return hits[0]


def norm(s):
    return " ".join(s.split())


def split_tree(t):
    """[(node id, [reply line-lists], head lines)] -- replies are the blank-line chunks led by Requirement=."""
    out = []
    for seg in t.split(CR + DASH + CR):
        chunks = seg.split(CR + CR)
        nid = next((l[len("Node ID="):] for l in chunks[0].split(CR) if l.startswith("Node ID=")), None)
        out.append((nid, chunks))
    return out


def top_level(lines):
    """Indices of lines at brace depth 0 (nothing in a DialogTree is indented, so depth is counted)."""
    depth, out = 0, []
    for i, l in enumerate(lines):
        s = l.strip()
        if s == "{":
            depth += 1
        elif s == "}":
            depth -= 1
        elif depth == 0:
            out.append(i)
    return out


def field(lines, key):
    return [i for i in top_level(lines) if lines[i].startswith(key + "=")]


def action_span(lines):
    """(start, end) of the top-level Custom Action, end exclusive, or None."""
    hit = field(lines, "Custom Action")
    if not hit:
        return None
    s = hit[0]
    if s + 1 >= len(lines) or lines[s + 1].strip() != "{":
        return s, s + 1
    depth, e = 0, s + 1
    while True:
        if lines[e].strip() == "{":
            depth += 1
        elif lines[e].strip() == "}":
            depth -= 1
            if depth == 0:
                return s, e + 1
        e += 1


def gate(lines):
    req = [lines[i] for i in field(lines, "Requirement")]
    c = field(lines, "Custom Requirement")
    creq = []
    if c:
        depth, e = 0, c[0] + 1
        creq = [lines[c[0]]]
        while e < len(lines):
            creq.append(lines[e])
            if lines[e].strip() == "{":
                depth += 1
            elif lines[e].strip() == "}":
                depth -= 1
                if depth == 0:
                    break
            e += 1
    return req, creq


def find(parts, node, text, like=None):
    """(part index, chunk index, lines) of the single reply with this text in this node -- and, for
    a twin, this gate: the Fish Monger's return node holds five skull replies under five gates."""
    hits = []
    for pi, (nid, chunks) in enumerate(parts):
        if nid is None or nid.strip() != node:
            continue
        for ci, ch in enumerate(chunks):
            lines = ch.split(CR)
            if lines[0].startswith("Requirement=") and any(
                    l.startswith("Reply Text=") and norm(l[len("Reply Text="):]) == norm(text) for l in lines):
                if like is None or gate(lines) == like:
                    hits.append((pi, ci, lines))
    assert len(hits) == 1, (node, text, len(hits))
    return hits[0]


def repair(t, rid, odd_node, twin_node, text, op, new):
    parts = split_tree(t)
    pi, ci, odd = find(parts, odd_node, text)
    _, _, twin = find(parts, twin_node, text, like=gate(odd))
    g = field(odd, "Go to node ID")[0]
    twin_goto = twin[field(twin, "Go to node ID")[0]]
    twin_act = action_span(twin)
    if op == "copy":
        want = twin[twin_act[0]:twin_act[1]]
        have = action_span(odd)
        if have and odd[have[0]:have[1]] == want:
            return t, 0
        assert have is None, (rid, "odd copy already carries a different action")
        k = g + 1
        while k < len(odd) and odd[k].startswith("Action work in progress="):
            k += 1
        odd = odd[:k] + want + odd[k:]
    elif op == "goto":
        target = "Go to node ID=" + new if new else twin_goto
        if odd[g] == target:
            return t, 0
        assert dt.normalise_id(odd[g][len("Go to node ID="):]) != dt.normalise_id(target[len("Go to node ID="):])
        odd[g] = target
    elif op == "javier":
        assert twin_act is None and twin_goto == "Go to node ID=520 before I accept"
        if odd[g] == twin_goto and action_span(odd) is None:
            return t, 0
        assert odd[g] == "Go to node ID=210 give gold"
        s, e = action_span(odd)
        body = CR.join(odd[s:e])
        assert "CTakeMoneyAction" in body and "Value to take=1000" in body
        odd[g] = twin_goto
        odd = odd[:s] + odd[e:]
    parts[pi][1][ci] = CR.join(odd)
    return (CR + DASH + CR).join((CR + CR).join(chunks) for _, chunks in parts), 1


def main():
    by_tree = {}
    for r in REPAIRS:
        by_tree.setdefault(resolve(r[0], r[1]), []).append(r)
    touched, done = [], []
    for rel, reps in by_tree.items():
        before = lhbuild.read(rel)
        assert (CR + DASH + CR).join((CR + CR).join(c) for _, c in split_tree(before)) == before
        t = before
        for rid, _, odd_node, twin_node, text, op, new in reps:
            t, n = repair(t, rid, odd_node, twin_node, text, op, new)
            if n:
                done.append(rid)
        if t == before:
            continue
        a, b = dt.parse(before), dt.parse(t)
        assert len(a.nodes) == len(b.nodes)
        assert [len(n.replies) for n in a.nodes] == [len(n.replies) for n in b.nodes]
        assert "\n" not in t.replace(CR, "")
        ids = {dt.normalise_id(n.node_id) for n in b.nodes}
        assert all(not r.goto or dt.normalise_id(r.goto) in ids for n in b.nodes for r in n.replies
                   if any(norm(r.text) == norm(x[4]) for x in reps)), rel
        p = lhbuild.FX / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(t.encode("latin-1"))
    # Every repaired tree, not just the ones created this run: a run that stops part-way has
    # already written some, and register() skips what mod.json lists.
    touched = [rel for rel in by_tree if (lhbuild.FX / rel).exists()]
    register(touched)
    print("sibling repairs: %s" % (done or "none"))


if __name__ == "__main__":
    main()
