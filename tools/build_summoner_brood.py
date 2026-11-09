"""The Snakebreed Summoners of Montserrat summon, and their brood dies with them. Release 8 of the post-0.99 plan.

Act 2 fields 40 Snakebreed Summoners, inside the Grove's and the abbey's first level's `Snakebreed` generators. The can's
summon branch fires only where the map holds `snakebreed summoning enabled` and clones `Snakebreed Summoner Clone
Generator`, and neither map held either, so every one of them cast at nothing. Each map now has both. The source is
vanilla's own from `02 Clan of the Hand A`, with its sixty-second expiry kept, but it calls the summoner's brood, the plain
and venom snakebreed at the map's own mojo bands, not that source's goblins, ogres and titans.

**Death dispels.** Every summon on a map carries one name, `Summoned Snakebreed`, so the engine cannot tell whose is whose.
The rule is therefore per map: when a Summoner dies, every snakebreed summoned on that map unravels with it. The others
summon again, so it rewards killing the caster first without emptying the room. It sits in the can's death effect slot,
which no generator overrides, and act 5's two summoner sources take the same name so the rule holds there too.

The summons are added to every stand-down list on the two maps that names the plain `Snakebreed`, so Sahar's ring and
the parley reach them. Druid Council Level 2 is left alone: its only Summoner is Sahar.

A rerun is a no-op.

    python tools/build_summoner_brood.py
"""
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, balanced, exists, if_action, multi
from build_shrine_druids import replace_groups, setting
from build_shrine_repairs import register

MAPS = ["Levels/2 Montserrat/01 Grove Exterior.zax", "Levels/2 Montserrat/02 Druid Council Level1.zax"]
ACT5 = ["Levels/5 Nostrodomus/02 Clan of the Hand A.zax", "Levels/5 Nostrodomus/04 Clan of the Skull B.zax"]
CANS = ["Resources/Monster Cans/Snakebreed Summoner" + t + ".can" for t in ("", " Tough", " Super")]
SOURCE = "Snakebreed Summoner Clone Generator"
CHECKER = "snakebreed summoning enabled"
BROOD = "Summoned Snakebreed"
S = "Monster Cans/Snakebreed"
TIERS = [("8", [S, S + " Venom"]), ("18", [S + " Tough", S + " Venom Tough"]), ("40", [S + " Super", S + " Venom Super"]), ("60", [S + " Super", S + " Venom Super"])]
UNRAVEL = "The summoner dies, and the brood it called unravels with it."


def brood_groups():
    items = [("Group", ("CGeneratorAIGroup", [("Max Party Mojo", m), ("Quantity to generate min", "1"), ("Quantity to generate max", "1"),
                                              ("Things to Generate", ("Array", [("Item Count", str(len(cs)))] + [
                                                  ("Thing to Generate", ("CSpawnableCannedEntity", [("Weight", "1"), ("Entity", c)])) for c in cs]))]))
             for m, cs in TIERS]
    return "Groups=" + B("Array", [("Item Count", str(len(items)))] + items).rstrip()


def vanilla_part(name):
    t = zipfile.ZipFile(lhbuild.VANILLA).read("Levels/5 Nostrodomus/02 Clan of the Hand A.zax").decode("latin-1")
    i = t.index("\t\t\tName=" + name + CR)
    a = t.rindex("Level Part=", 0, i)
    return t[a:balanced(t, a)]


def source():
    x = replace_groups(vanilla_part(SOURCE), brood_groups())
    return setting(x, "New Name", BROOD) + CR


def checker():
    return vanilla_part(CHECKER) + CR


def stand_down_lists(z):
    """Every name list on the map that holds the plain `Snakebreed` takes the brood too. Alive-checks are left alone."""
    def add(m):
        names = [n.strip() for n in m.group(2).split(",")]
        if "Snakebreed" not in names or BROOD in names:
            return m.group(0)
        return m.group(1) + m.group(2) + ", " + BROOD
    new = re.sub(r"(?m)^(\s*(?:Target Name|Entity Name)=)([^\r\n]*)", add, z)
    return new, new.count(", " + BROOD) - z.count(", " + BROOD)


def maps():
    out = []
    for rel in MAPS:
        z = lhbuild.read(rel)
        if "\t\t\tName=" + SOURCE + CR in z:
            out.append((rel.split("/")[-1], 0))
            continue
        z, n = stand_down_lists(z)
        lhbuild.write_map(rel, lhbuild.add_parts(z, [source(), checker()]))
        register([rel])
        out.append((rel.split("/")[-1], n))
    for rel in ACT5:
        z = lhbuild.read(rel)
        i = z.index("\t\t\tName=" + SOURCE + CR)
        a = z.rindex("\t\tLevel Part=", 0, i)
        e = balanced(z, a + 2)
        part = z[a:e]
        if "New Name=" + BROOD + CR in part:
            continue
        lhbuild.write_map(rel, z[:a] + setting(part, "New Name", BROOD) + z[e:])
        register([rel])
    return out


def cans():
    done = 0
    dispel = if_action(exists(BROOD), multi([
        ("CPrintCombatTextAction", [("Text to print", UNRAVEL), ("Character to show text to", "Player1"), ("Emphasize", "0"), ("Suppress Duplicates", "1")]),
        ("CPlaySoundAction", [("Sound", "Spells/Monster Summon.ogg"), ("Position", "$Trigger"), ("Multiplayer", "Heard by all players")]),
        ("CDeleteAction", [("Target Name", BROOD)])]))
    for rel in CANS:
        c = lhbuild.read(rel)
        if BROOD in c:
            continue
        k = c.index("Destroyed Effect Action=")
        v = k + len("Destroyed Effect Action=")
        e = balanced(c, v)
        new = "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR + "Action=" + c[v:e] + CR + \
              "Action=" + B(*dispel) + "}" + CR + "}"
        lhbuild.write_map(rel, c[:v] + new + c[e:])
        register([rel])
        done += 1
    return done


def main():
    print("summoner cans that dispel:", cans())
    for m, n in maps():
        print(m, "stand-down lists widened:", n)


if __name__ == "__main__":
    main()
