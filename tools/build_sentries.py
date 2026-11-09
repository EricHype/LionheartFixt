"""Sentries that raise the alarm. A probe on the Doomed Plateau first, the pattern for more after.

The engine has a working call for help that vanilla never fires: `CCallForReinforcementsAction` searches an oval of
`Max Distance` around its requester and pulls in every creature there that is idle, has `Respond to calls for
reinforcements=1`, and can target the requester's target (CSkeletonAI's message handler, 0x00472240). 88 of the 92
undead cans already listen. See docs/dormant-engine.md.

A listener sees 550, so a call of 500 reaches only creatures that have already seen the player. To wake a group that has
not, the call must reach past 550; the probe uses 800. The sentry fires it from a `CSkeletonTransition`, Once Per New
Target, Any to Attack, the hook vanilla uses 509 times for a creature's alert sound.

The sentry has to be beatable. Detection is the enemy's: `Max Distance` 550 and a 360 degree `Vision Cone` on nearly every
creature, with the Sneak skill as a chance to stay unseen. The player sees only as far as the fog of war is pushed back,
`380 - 25 for a helmet + a Perception bonus` (`Resurrect player.can`), 355 to 460, and creatures in the fog fade out, so a
stock creature at 550 always sees you first. The Deathwatch sees 355 and only 180 degrees (vanilla uses 90 on 145
creatures): a low-Perception character in a plain helmet is seen as it is seen, every other character sees it first, by up
to 135 units with a Farsight helmet (build_sight_helmets.py), and you can come at it from behind. It carries its own name,
so it can be picked out.

A sentry replaces its generator's spawn rather than adding to it: one Deathwatch where one to three undead stood.

The spot was chosen by walkable distance from the act's route (the re-score's path tracer): 37 units from the path, with
two listening groups 700 and 763 units off the path, inside the 800 oval of the sentry and beyond their own 550 sight of
it. The Bonecaller's cans stop listening, so no alarm can turn its conversation into a fight.

A rerun is a no-op.

    python tools/build_sentries.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, balanced, multi
from build_shrine_druids import parts, pos, replace_groups
from build_shrine_repairs import register

U = "Monster Cans/Undead/"
COPY = "Monster Cans/Fixt Sentry/"
# map, generator position, the sentry's tiers by mojo, display name, call radius
SPOTS = [("Levels/4 Crypt/7 Doomed Plateau.zax", (1903, 3084),
          [("14", U + "Skeleton"), ("18", U + "Skeleton Tough"), ("22", U + "Skeleton Super"), ("60", U + "Skeleton Super")],
          "Deathwatch", "800")]
SIGHT, CONE = "355", "180"
DEAF = [U + "Boss Lich", U + "Boss Lich Tough", U + "Boss Lich Super"]  # the Bonecaller


def alarm(name, radius):
    say = ("CPrintCombatTextAction", [("Text to print", "The " + name + " raises the alarm!"), ("Character to show text to", "Player1"),
                                      ("Emphasize", "1"), ("Suppress Duplicates", "0")])
    call = ("CCallForReinforcementsAction", [("Requester Name", "$Trigger"), ("Max Distance", radius)])
    return B("CSkeletonTransition", [("Trigger", "Once Per New Target"), ("From State", "Any"), ("To State", "Attack"),
                                     ("Action", multi([say, call])), ("IsDone", "0")]).rstrip()


def sentry_can(can, name, radius):
    new = COPY + can[len("Monster Cans/"):]
    rel = "Resources/" + new + ".can"
    if (lhbuild.FX / rel).exists():
        return new
    c = lhbuild.read("Resources/" + can + ".can")
    c, n = re.subn(r"User Assigned Name=[^\r\n]*", "User Assigned Name=" + name, c, count=1)
    assert n == 1
    k = c.index("Target Type=CEntityBehaviorStateSetClosestTarget")
    e = balanced(c, k)
    block = c[k:e]
    block, a = re.subn(r"(?m)^(\s*Max Distance=)[^\r\n]*", lambda m: m.group(1) + SIGHT, block, count=1)
    block, b = re.subn(r"(?m)^(\s*Vision Cone=)[^\r\n]*", lambda m: m.group(1) + CONE, block, count=1)
    assert a == b == 1
    c = c[:k] + block + c[e:]
    # the alarm, as the CSkeletonAI's first transition (vanilla writes Array Count here, not Item Count)
    t = c.index("Transition=Array")
    te = balanced(c, t)
    arr = c[t:te]
    m = re.search(r"Array Count=(\d+)", arr)
    close = arr.rindex(CR) + 2
    arr = arr[:close] + "Array Item=" + alarm(name, radius) + CR + arr[close:]
    arr = arr[:m.start()] + "Array Count=" + str(int(m.group(1)) + 1) + arr[m.end():]
    c = c[:t] + arr + c[te:]
    lhbuild.write_map(rel, c)
    register([rel])
    return new


def deafen():
    done = 0
    for can in DEAF:
        rel = "Resources/" + can + ".can"
        c = lhbuild.read(rel)
        c2 = c.replace("Respond to calls for reinforcements=1", "Respond to calls for reinforcements=0")
        if c2 != c:
            lhbuild.write_map(rel, c2)
            register([rel])
            done += 1
    return done


def groups_for(tiers):
    items = [("Group", ("CGeneratorAIGroup", [("Max Party Mojo", m), ("Quantity to generate min", "1"), ("Quantity to generate max", "1"),
                                              ("Things to Generate", ("Array", [("Item Count", "1"), ("Thing to Generate", ("CSpawnableCannedEntity", [("Weight", "1"), ("Entity", c)]))]))]))
             for m, c in tiers]
    return "Groups=" + B("Array", [("Item Count", str(len(items)))] + items).rstrip()


def place(rel, spot, tiers, name, radius):
    z = lhbuild.read(rel)
    if COPY in z:
        return 0
    gen = [x for x in parts(z) if "CGeneratorAI" in x and pos(x) == (float(spot[0]), float(spot[1]))]
    assert len(gen) == 1, (rel, spot)
    cans = [(m, sentry_can(c, name, radius)) for m, c in tiers]
    lhbuild.write_map(rel, z.replace(gen[0], replace_groups(gen[0], groups_for(cans)), 1))
    register([rel])
    return 1


def main():
    print("Bonecaller cans no longer listening:", deafen())
    for rel, spot, tiers, name, radius in SPOTS:
        print(rel.split("/")[-1], "sentries placed:", place(rel, spot, tiers, name, radius))


if __name__ == "__main__":
    main()
