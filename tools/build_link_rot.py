"""Phase 1, finished: the dead replies a player can reach now go somewhere. See docs/link-rot.md.

Vanilla shipped 84 replies whose `Go to node ID` names no node in their tree (case-folded and
trimmed, the engine's rule). Choosing one advances to nothing. 13 went with earlier work; this
repairs the 48 of the remaining 71 that a player can actually choose, and leaves the 23 that no
one can reach, listed in INERT so the gate can hold the line on everything else.

Every target was decided by reading the tree, never by matching the node's number:

  * **retarget** where the tree already sends the same reply somewhere, or plainly meant to
    (`5 Goodbye.` -> `5 goodbye`, `10 goodbye` -> `10 goobye`);
  * **blank** -- end the conversation, vanilla's own shape in 2,263 replies -- where there is no
    plain goodbye to go to. The obvious candidate was wrong in every one of those trees: Iapetus's
    `100 Quest Goodbye` gives out his quest, the Surrey Vendor's `10 Fight baloon` is a fight, and
    the Rogue Inquisitor's `10 Goodbye` says *"You won't be leaving here alive!"* to a friend his
    own reply action has just let go.

No missing target has a recording, so nothing is restored from voiceover. Only `Go to node ID=`
lines change: no reply text, requirement or node ID. Dialogue-only, so it reaches a save already
in progress. A rerun is a no-op.

    python tools/build_link_rot.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR, DASH
from build_shrine_repairs import register

sys.path.insert(0, str(lhbuild.MODTOOLS))
import dialogtree_format as dt

B1 = "Resources/Levels/1 Barcelona/Dialog/"

# (tree, dead target, new target, replies expected, requirement to set or None)
FIXES = [
    (B1 + "Port District/Fish Monger.DialogTree", "5 Goodbye.", "5 goodbye", 1, None),
    (B1 + "Port District/Fish Monger.DialogTree", "I'll be leaving now.", "5 goodbye", 1, None),
    ("Resources/Levels/3 Montaillou/Dialog/fabrisse.DialogTree", "10 goodbye", "10 goobye", 2, None),
    (B1 + "Port District/shakespeare.dialogtree", "Shakespeare in love 3a", "2000 Shakespeare in love 3a", 1, None),
    # 60 Leaving and 200 boots send the same decline here.
    (B1 + "La Calle Perdida/MarcoPoloSpirit.DialogTree", "06 Goodbye forever", "06 Goodbye forever leaving", 1, None),
    # "I'll just be going." in the same nodes goes to 5 goodbye.
    (B1 + "Port District/Conspirator.DialogTree", "10 no thanks", "5 goodbye", 3, None),
    (B1 + "Port District/cortes.dialogtree", "5 goodbye", "10 goodbye", 1, None),
    # The melody starts at 1, and every wrong key returns there.
    (B1 + "Gate District/Viola Organista.DialogTree", "40 play the organ", "40 play the organ 1", 1, None),
    # 5 organ tuned sends the identical question to 60 name.
    (B1 + "Gate District/Viola Organista.DialogTree", "5 organista", "60 name", 1, None),
    # The same line elsewhere in his tree goes to 86 Speech skill, and the node's own note says
    # "Action work in progress=speech skill". This copy is gated on Barter 35 (a Custom
    # Requirement) rather than Speech 25; the gate is left as shipped.
    (B1 + "Gate District/Barcelona Vendor Sympathetic.DialogTree", "86 Speech solution", "86 Speech skill", 1, None),
    (B1 + "Port District/Inquisitor Port.DialogTree", "5 goodbye", "", 12, None),
    ("Resources/Levels/3 Montaillou/Dialog/ToulouseIapetus.DialogTree", "100 Goodbye", "", 16, None),
    ("Resources/Levels/6 Barcelona Attack/Dialog/Surrey Vendor.dialogtree", "10 goodbye", "", 2, None),
    # The reply's own CIfAction already lets a friend go or starts the fight; 3 Return Dialogue's
    # copy of "moving along" has a blank target for exactly that reason.
    ("Resources/Levels/Wilderness/Dialog/RogueInquisitor.DialogTree", "10 combat", "", 5, None),
]

# Left alone: on nodes nothing reaches, in trees nothing opens, or on nodes only ever shown as a
# balloon, whose replies are never offered (the maps chain those scenes themselves).
INERT = {
    ("bar patrons", "1500 drunk guy 3"): 3,
    ("shipsailorsonshipcanned", "200"): 2,
    ("cortes", "50 more info"): 2, ("cortes", "130 compromise"): 1, ("cortes", "140 no resolution"): 1,
    ("grandinquisitor", "400 nis montserrat directions"): 1, ("grandinquisitor", "400 crown of thorns"): 1,
    ("grandinquisitor", "400 relics explanation"): 1,
    ("inquisitorraphael", "238 leave for montserrat"): 1, ("inquisitorraphael", "500 sacred lance"): 1,
    ("inquisitorraphael", "400 nis dialogue 4"): 1,
    ("lordjavier", "400 nis dialogue 2"): 1,
    ("shylocke", "151 no resolution 2"): 1,
    ("shapeshifting daeva", "2 food"): 1, ("shapeshifting daeva trueform", "2 food"): 1,
    ("evilendingalldie", "10 your spirit speaks"): 1, ("goodendingallsurvive", "end dialogue"): 1,
    ("cervantes", "205 don quixote"): 1,
    ("pirate ghosts", "30 fight"): 1,
}
assert sum(INERT.values()) == 23 and sum(f[3] for f in FIXES) == 48


def dangling(text):
    tree = dt.parse(text)
    ids = {dt.normalise_id(n.node_id) for n in tree.nodes}
    return [r.goto for n in tree.nodes for r in n.replies if dt.normalise_id(r.goto) and dt.normalise_id(r.goto) not in ids]


def apply(text, dead, new, want, req):
    lines = text.split(CR)
    hits = [i for i, l in enumerate(lines)
            if l.startswith("Go to node ID=") and dt.normalise_id(l[len("Go to node ID="):]) == dt.normalise_id(dead)]
    if not hits:
        return text, 0
    assert len(hits) == want, (dead, len(hits), want)
    for i in hits:
        assert lines[i - 1].startswith("Reply Text="), (dead, lines[i - 1])
        lines[i] = "Go to node ID=" + new
        if req:
            assert lines[i - 2] == "Requirement=!None", (dead, lines[i - 2])
            lines[i - 2] = "Requirement=" + req
    return CR.join(lines), len(hits)


def main():
    by_tree = {}
    for f in FIXES:
        by_tree.setdefault(f[0], []).append(f)
    done, changed = [], 0
    for rel, fixes in by_tree.items():
        before = lhbuild.read(rel)
        t = before
        for _, dead, new, want, req in fixes:
            t, n = apply(t, dead, new, want, req)
            changed += n
        if t == before:
            continue
        a, b = dt.parse(before), dt.parse(t)
        assert len(a.nodes) == len(b.nodes)
        assert sum(len(n.replies) for n in a.nodes) == sum(len(n.replies) for n in b.nodes)
        assert t.count(CR) == before.count(CR) and "\n" not in t.replace(CR, "")
        stem = Path(rel).stem.lower()
        left = [g for g in dangling(t) if (stem, dt.normalise_id(g)) not in INERT]
        assert not left, (rel, left)
        new_file = not (lhbuild.FX / rel).exists()
        (lhbuild.FX / rel).parent.mkdir(parents=True, exist_ok=True)
        (lhbuild.FX / rel).write_bytes(t.encode("latin-1"))
        if new_file:
            done.append(rel)
    if done:
        register(done)
    print("link rot: %d replies repaired; new files: %s" % (changed, done))


if __name__ == "__main__":
    main()
