"""Read Lionheart's saves and character file, so a playtest can be checked instead of remembered.

Moved to LionheartModTools (`savecheck.py`), which documents both formats; nothing in it was Fixt's.
This forwards to it with the same arguments, and re-exports its functions so `import savecheck`
(tools/check_save_additions.py does) keeps working.

    python tools/savecheck.py save latest               # map, player, ranks, variables, layers
    python tools/savecheck.py character                 # the starting character
    python tools/savecheck.py snapshot before-bishop --save latest
    python tools/savecheck.py diff before-bishop
    python tools/savecheck.py grep "Goblin Khan" --save latest
    python tools/savecheck.py dump latest -o out

The mod tools are found from --tools DIR, $LIONHEART_TOOLS, or ../LionheartModTools.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _modtools  # noqa: E402

_impl = _modtools.load("savecheck", sys.argv if __name__ == "__main__" else None,
                       module="lionheart_modtools_savecheck")
globals().update(_modtools.public(_impl))

if __name__ == "__main__":
    sys.exit(_impl.main())
