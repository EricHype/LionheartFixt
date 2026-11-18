"""Point creature weapons at clips their models have. Issue #15: "Bonewalker" flickering into GRANNY MODEL on the
Doomed Plateau, "the one that looks human ... while he is attacking".

A weapon's `CPlugInBehaviorPlaySequence{Sequence Name=X}` plays the model's clips whose `Short Name` starts with X:
vanilla's `Attack` plays `Attack01`/`Attack02`, its `AttackOneHanded` plays `AttackOneHanded01`/`02`. Name no clip and
the engine draws its "GRANNY MODEL" placeholder for the swing. The strike itself is a trigger inside the clip
(`Strike Current Target` in `OneHandedSwing_01.ANIMATION.TXT`), so a swing with no clip may land no hit either.

  * **The Bonecaller** (`Monster Cans/Undead/Boss Lich*.can`, three tiers, Fixt 0.21.0) wears the vanilla `Boss Lich`
    model, which no vanilla creature ever used and whose swings alone in the game are named `OneHandedSwing_01`/`_02`.
    The can was given the ghouls' `Attack`. Now `OneHandedSwing`, both swings at random as the can already asks.
  * **The Hujark General** (`5 Nostrodomus/Character Templates/Hujark General.can`, vanilla) wears `ShamanGreater`,
    which has no melee clip at all, under a melee weapon playing `AttackOneHanded`. Now `SpellCast`, the model's only
    attacking clip. It carries no strike trigger, so whether his blow lands is no worse than before; the placeholder
    is gone. Vanilla's own `Spellcast` weapons (the Wielders) are gestures with no damage, so there is no precedent
    for which way that goes.

`seq_sweep` over every Fixt can found these four and no others. Can edits, so they reach creatures spawned after
install. A rerun is a no-op.

    python tools/build_attack_clips.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR, T
from build_shrine_repairs import register

LICH = [f"Resources/Monster Cans/Undead/Boss Lich{t}.can" for t in ("", " Tough", " Super")]
GENERAL = "Resources/Levels/5 Nostrodomus/Character Templates/Hujark General.can"
EDITS = [(rel, "Attack", "OneHandedSwing") for rel in LICH] + [(GENERAL, "AttackOneHanded", "SpellCast")]


def build():
    done = []
    for rel, old, new in EDITS:
        t = lhbuild.read(rel)
        o, n = T + "Sequence Name=" + old + CR, T + "Sequence Name=" + new + CR
        if t.count(n) == 1 and o not in t:
            continue
        assert t.count(o) == 1, "%s: expected one weapon sequence %s" % (rel, old)
        i = t.index(o)
        assert "CPlugInBehaviorPlaySequence" in t[i - 300:i], "%s: %s is not a weapon sequence" % (rel, old)
        (lhbuild.FX / rel).write_bytes(t.replace(o, n, 1).encode("latin-1"))
        done.append(rel)
    if done:
        register(done)
    return len(done)


def main():
    print("attack clips:", build())


if __name__ == "__main__":
    main()
