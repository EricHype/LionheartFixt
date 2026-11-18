"""Montserrat's assassins pay XP. Issue #15: "The assassins killed at Monserrat do not give XP".

A kill pays through the can's death action, `CGiveExperiencePointsToAllPlayersAction{Get XP Frome=$Trigger}`, and the
amount comes from the entity's own top-level `Dynamic Properties { Experience Points=N }`. 644 of vanilla's 656
walking cans that award XP carry it. The three `Montserrat Assassin` tiers are 0.10.0 clones of `Assasin EarlyLevels`,
one of the dozen that do not, so every kill paid 0. The 0.10.0 note "counts unchanged, so XP unchanged" was wrong.

Each tier now carries `Experience Points=152`, Snakebreed Venom's figure, the toughest of the snakebreed fought in the
same invasion. Vanilla uses one number across a family's tiers (Snakebreed 111/111/111, Assassin Bow 775/775/775), so
the three tiers match.

`Wounded Assassin` is left at 0 on purpose: he lies in the hall pleading for his life, and killing him should not pay
like a fight.

A can edit, so it reaches creatures spawned after install. A rerun is a no-op.

    python tools/build_montserrat_assassin_xp.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR, T
from build_shrine_repairs import register

XP = "152"
CANS = [f"Resources/Levels/2 Montserrat/Character Templates/Montserrat Assassin{t}.can" for t in ("", " Tough", " Super")]
OLD = T * 2 + "Dynamic Properties=1" + CR + T * 2 + "{" + CR + T * 3 + "Comment=Assassin can" + CR + T * 2 + "}" + CR
NEW = (T * 2 + "Dynamic Properties=2" + CR + T * 2 + "{" + CR + T * 3 + "Comment=Assassin can" + CR +
       T * 3 + "Experience Points=" + XP + CR + T * 2 + "}" + CR)


def build():
    done = []
    for rel in CANS:
        t = lhbuild.read(rel)
        head = t[:400]
        if NEW in head:
            continue
        assert head.count(OLD) == 1, "%s: unexpected Dynamic Properties" % rel
        t = t.replace(OLD, NEW, 1)
        (lhbuild.FX / rel).write_bytes(t.encode("latin-1"))
        done.append(rel)
    if done:
        register(done)
    return len(done)


def main():
    print("montserrat assassin xp:", build())


if __name__ == "__main__":
    main()
