"""The Wasp Queen is called the Wasp Queen. Asked: "the wasp queen is still called "cursed wasp" in the quick status
description".

0.11.0 cloned her can from the cursed wasp and named her only on the generator (`New Name=Wasp Queen` in
`4 Animal Cave.zax`). `New Name` is the script name; the name the game displays (quick status, the combat log) is the
can's `User Assigned Name`, which stayed `Cursed Wasp`. It is now `Wasp Queen`.

A can edit: a Queen spawned after install, so a `4 Animal Cave` not yet entered. A rerun is a no-op.

    python tools/build_wasp_queen_name.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR

CAN = "Resources/Monster Cans/Animals/Wasp Queen.can"
OLD = "User Assigned Name=Cursed Wasp" + CR
NEW = "User Assigned Name=Wasp Queen" + CR


def build():
    t = lhbuild.read(CAN)
    if NEW in t:
        return False
    assert t.count(OLD) == 1
    (lhbuild.FX / CAN).write_bytes(t.replace(OLD, NEW).encode("latin-1"))
    return True


def main():
    print("wasp queen name:", build())


if __name__ == "__main__":
    main()
