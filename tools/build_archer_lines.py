"""Archers who hold their ground. A probe on Temple Initiate first, the pattern for wider use after.

Every vanilla bow can's attack AI, `CNormalAttackAI`, closes to `Minimum Attack Distance=350`, so an archer drifts in
until it stands in the melee. The engine's own label for 0 on that field is "Do not move while attacking" (the tick skips
its movement branch, `0x00457570`), and 202 vanilla cans write it that way. An archer set to it stands, turns and
shoots, and keeps CNormalAttackAI's protection against a shot being cut off. Out of its attack range (`Max Dist`) the
skeleton still pursues, so it holds only while it can reach you. See docs/dormant-engine.md.

A can is shared by every map that spawns it, so the holding archers are copies, `Monster Cans/Fixt Holding/...`, that
differ from their originals in that one field and nothing else, display name included. They replace the originals only
in the generators listed here.

The probe: the two bow generators that sit on Temple Initiate's route (117 and 136 walk units from it), in front of the
melee group at 1737,2368.

A rerun is a no-op.

    python tools/build_archer_lines.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR
from build_shrine_druids import parts, pos
from build_shrine_repairs import register

HOLD = "Do not move while attacking"
COPY = "Monster Cans/Fixt Holding/"
# map -> generator positions whose archers hold
LINES = {"Levels/7 English Shrine/02 Temple Initiate.zax": [(1795, 2104), (2214, 1784)]}


def holding(can):
    """The copy's path, written once: the original with its one Minimum Attack Distance set to hold."""
    new = COPY + can[len("Monster Cans/"):]
    rel = "Resources/" + new + ".can"
    p = lhbuild.FX / rel
    if not p.exists():
        c = lhbuild.read("Resources/" + can + ".can")
        c, n = re.subn(r"(?m)^(\s*Minimum Attack Distance=)[^\r\n]*", lambda m: m.group(1) + HOLD, c)
        assert n == 1, can
        lhbuild.write_map(rel, c)
        register([rel])
    return new


def build(rel, spots):
    z = lhbuild.read(rel)
    new = z
    swapped = 0
    for x in parts(z):
        if "CGeneratorAI" not in x or pos(x) not in [(float(a), float(b)) for a, b in spots]:
            continue
        ents = sorted(set(re.findall(r"Entity=(Monster Cans/[^\r\n]*Bow[^\r\n]*)", x)))
        ents = [e for e in ents if not e.startswith(COPY)]
        if not ents:
            continue
        y = x
        for e in ents:
            y = y.replace("Entity=" + e + CR, "Entity=" + holding(e) + CR)
        new = new.replace(x, y, 1)
        swapped += len(ents)
    if new != z:
        lhbuild.write_map(rel, new)
        register([rel])
    return swapped


def main():
    for rel, spots in LINES.items():
        print(rel.split("/")[-1], build(rel, spots), "bow cans swapped for holding copies")


if __name__ == "__main__":
    main()
