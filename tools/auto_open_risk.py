"""Destructive replies on conversations the player never asked for.

A `GetCloseThenTrigger` interaction specifier fires on PROXIMITY. The conversation opens by itself
as the player walks past, so any reply on that node can be taken by one dismissive click. 0.57.4
put `(fit the rotary gear into the turret ring)` -- with `CActionRemoveInventoryItem` on it -- as the
FIRST reply of the siege tank's examine node, which a map opens at radius 200. The next player to
walk into the chamber lost the quest item on entry, and because the item was gone the hand-over
scene could never play either. One click, two features destroyed.

THE RULE THIS ENFORCES: a node opened by an auto-firing specifier must not carry a reply that
removes an item, takes money, hurts the player or completes a quest -- unless the node's own text
ASKS THE QUESTION, so the click is a decision rather than a dismissal.

Vanilla has exactly one of those, and it is the model: `Relican Summoning Ring / 01 Conversation
Start` opens by itself and its text reads *"Do you wish to activate the ring and bring destruction
onto La Calle Perdida?"*, with the removal behind "Yes." It is allow-listed by name below, with the
reason, rather than by a pattern match on question marks.

    python tools/auto_open_risk.py

Exits non-zero on a finding, so it can gate a release. It is a separate tool rather than a
validate.py check because it reads every map in the archive, which validate's 30 seconds cannot
absorb -- run it when adding a reply to anything a map opens on its own.
"""
import os
import re
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_VANILLA = os.path.join(
    "C:" + os.sep, "Program Files (x86)", "GOG Galaxy", "Games",
    "Lionheart - Legacy of the Crusader", "data.dat.vanilla.bak")
VANILLA = Path(os.environ.get("LIONHEART_VANILLA", DEFAULT_VANILLA))
F = REPO / "files"
if not VANILLA.exists():
    sys.exit("vanilla archive not found: %r -- set LIONHEART_VANILLA" % str(VANILLA))
zf = zipfile.ZipFile(VANILLA)

# Fires without the player choosing to talk. GetCloseThenTalk is NOT in this list: a greeting is
# the player walking up to somebody, and vanilla hangs ordinary conversations on it.
AUTO = re.compile(r"Interaction Type=Interaction Specifiers/(GetCloseThenTrigger\w*)")
COSTLY = re.compile(r"CActionRemoveInventoryItem|CTakeMoneyAction|CPainAction|"
                    r"CSetQuestSatusToCompletedAction")

# Deliberate decision points: the node's own text asks, so the reply is an answer.
ALLOWED = {
    ("relican summoning ring", "01 conversation start"):
        "its text asks 'Do you wish to activate the ring and bring destruction onto La Calle"
        " Perdida?' and the removal sits behind Yes.",
}

SCANNED = (".zax", ".can")


def corpus():
    """Every map and can, with files/ shadowing the archive."""
    seen = set()
    for p in sorted(F.rglob("*")):
        if p.is_file() and p.suffix.lower() in SCANNED:
            rel = p.relative_to(F).as_posix()
            seen.add(rel.lower())
            yield rel, p.read_bytes().decode("latin-1")
    for n in zf.namelist():
        low = n.lower()
        if low.startswith("cache/") or not low.endswith(SCANNED) or low in seen:
            continue
        yield n, zf.read(n).decode("latin-1")


def tree_text(basename):
    """A tree by basename, files/ first."""
    for p in F.rglob("*.DialogTree"):
        if p.name[:-11].lower() == basename:
            return p.read_bytes().decode("latin-1"), True
    for n in zf.namelist():
        if n.lower().endswith(".dialogtree") and n.rsplit("/", 1)[-1][:-11].lower() == basename:
            return zf.read(n).decode("latin-1"), False
    return None, False


pairs = {}
for rel, text in corpus():
    if "Interaction Specifiers/GetCloseThenTrigger" not in text:
        continue
    for m in AUTO.finditer(text):
        seg = text[m.start():m.start() + 2500]
        tm = re.search(r"Dialog Tree File=([^\r\n]*)", seg)
        nm = re.search(r"Node ID=([^\r\n]*)", seg)
        if not (tm and nm):
            continue
        key = (tm.group(1).strip().rsplit("/", 1)[-1].lower(), nm.group(1).strip())
        pairs.setdefault(key, set()).add(rel.rsplit("/", 1)[-1])

print("%d (tree, node) pair(s) are opened by an auto-firing specifier" % len(pairs))

problems = []
for (basename, node), where in sorted(pairs.items()):
    text, is_ours = tree_text(basename)
    if text is None:
        continue
    m = re.search(r"^Node ID=" + re.escape(node) + r"\r?$", text, re.M)
    if not m:
        continue
    end = text.find("\r\n" + "-" * 60 + "\r\n", m.start())
    seg = text[m.start():end if end > 0 else len(text)]
    hit = COSTLY.search(seg)
    if not hit:
        continue
    why = ALLOWED.get((basename, node.lower()))
    if why:
        print("   allowed: %-26s %-30s %s" % (basename, node[:30], why[:60]))
        continue
    problems.append((basename, node, sorted(where), hit.group(0), is_ours))

if problems:
    print("\n%d PROBLEM(S): a conversation the player did not ask for can cost them something"
          % len(problems))
    for basename, node, where, what, is_ours in problems:
        print("   - %s / %r opened from %s carries %s%s"
              % (basename, node, ", ".join(where), what,
                 "  [THIS MOD SHIPS THAT TREE]" if is_ours else ""))
    print("\n   Put the costly reply behind a second, deliberate click, or make the node's own"
          "\n   text ask the question the way Relican's ring does.")
    sys.exit(1)
print("no auto-opened conversation can cost the player anything")
