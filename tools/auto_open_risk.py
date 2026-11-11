"""Destructive replies on conversations the player never asked for.

A `GetCloseThenTrigger` interaction specifier fires on PROXIMITY, so a conversation it opens can cost
the player something with one dismissive click. 0.57.4 lost the rotary gear that way. The check moved
to LionheartModTools (`auto_open_risk.py`), which explains the rule in full and carries vanilla's one
deliberate decision point, Relican's summoning ring, as a built-in default. This runs it on `files/`.

    python tools/auto_open_risk.py [--tools <LionheartModTools>]

Exits non-zero on a finding, so it can gate a release. Run it when adding a reply to anything a map
opens on its own.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _modtools  # noqa: E402

# Fixt's own deliberate decision points, beyond vanilla's: {(tree basename, node id), both lowered:
# why}. Add one only when the node's own text asks the question, the way Relican's ring does.
FIXT_ALLOWED = {}

if __name__ == "__main__":
    impl = _modtools.load("auto_open_risk", sys.argv, module="lionheart_modtools_auto_open_risk")
    if not Path(_modtools.vanilla()).exists():
        sys.exit("vanilla archive not found: %r -- set LIONHEART_VANILLA" % _modtools.vanilla())
    sys.exit(impl.run(_modtools.FILES, _modtools.vanilla(), FIXT_ALLOWED))
