"""Half the English packs of the Hujark war stay home. Issue #15: "When choosing to side with the Hurjak, there are too
many NPCs fighting which makes the noise too loud (... 20+ NPCs screaming, especially annoying in the cave itself)".

0.17.0 placed the act's never-deployed English army (`Monster Cans/English in Caverns of Nostrodomus/`) by twinning
every Hujark generator with an English one at the same spot, `Active=0`, switched on by name (`English Generator`)
only when the player sides with the Hujark. Counted as enemies of the player that was a swap, as its notes said. But
every spot then spawned two packs, the Hujark and the English twin, and since 0.97.3 gave the Hujark the English as
targets, both fight: twice vanilla's bodies per encounter, every one shouting and dying aloud.

Most twins spawn a single soldier at the tiers act 5 plays at (party mojo about 26, the `Max Party Mojo=30` row), so
halving pack sizes would only have cut 27% there. Instead, every other `English Generator` twin on each map is renamed
`Fixt English Generator held back`, so the by-name activation never reaches it and it stays off. At mojo 30 the
English go from 144 to about 76 bodies across the act (-47%); the fights that remain are full-size, and alternate
Hujark camps simply stand guard.

Left alone: `05 Nostrodomus Demesne`, whose single twin is part of the seer's scene; the `English voice Generator`s,
which belong to the English route; and every vanilla English generator (none uses the `English in Caverns` roster).
The renamed parts are referenced by nothing else -- the only references to `English Generator` are the activations.

Nothing changes on the English route or the neutral one, where the twins never spawn. A map edit, so it reaches act 5
maps not yet entered. A rerun is a no-op.

    python tools/build_hujark_war_thinning.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR
from build_shrine_repairs import register

D = "Levels/5 Nostrodomus/"
MAPS = ["01 Heart Entrance", "02 Clan of the Hand A", "03 Tourniquet of Pain", "04 Clan of the Skull B",
        "07 Cave 2", "08 Cave 3", "09 Cave 4", "10 Cave 5"]
ROSTER = "Entity=Monster Cans/English in Caverns of Nostrodomus/"
LIVE = "\t\t\tName=English Generator" + CR
HELD = "\t\t\tName=Fixt English Generator held back" + CR


def thin(z):
    parts = re.findall(r"(?ms)^\t\tLevel Part=\w+\r\n\t\t\{\r\n.*?^\t\t\}", z)
    twins = [p for p in parts if "CGeneratorAI" in p and ROSTER in p and (LIVE in p or HELD in p)]
    if any(HELD in p for p in twins):
        return z, 0, len(twins)
    held = 0
    for i, p in enumerate(twins):
        if i % 2 == 1:
            assert p.count(LIVE) == 1 and z.count(p) == 1
            z = z.replace(p, p.replace(LIVE, HELD, 1))
            held += 1
    return z, held, len(twins)


def main():
    touched = []
    for mp in MAPS:
        rel = D + mp + ".zax"
        z0 = lhbuild.read(rel)
        z, held, n = thin(z0)
        if z != z0:
            lhbuild.write_map(rel, z)
            touched.append(rel)
        print("  %s: %d of %d twins held back" % (mp, held, n))
    if touched:
        register(touched)


if __name__ == "__main__":
    main()
