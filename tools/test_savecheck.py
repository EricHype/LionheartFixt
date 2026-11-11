"""Hold savecheck against whatever saves are on this machine.

Moved to LionheartModTools as tests/test_savecheck.py; this runs it.

    python tools/test_savecheck.py [--tools <LionheartModTools>]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _modtools  # noqa: E402

if __name__ == "__main__":
    t = _modtools.load("tests/test_savecheck", sys.argv, module="lionheart_modtools_test_savecheck")
    sys.exit(t.main())
