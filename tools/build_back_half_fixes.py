"""Defects the 0.99.9 route re-score found in acts 6 to 8, and the Shrine's druid posts moved onto the path.

1. **The siege holds broke themselves (0.99.5).** Each siege's watch looked for its druids ten seconds after arrival, but
   every siege druid sits in a generator a trigger switches on later. So the watch found none, stood down the soldiers
   already there, and switched itself off, and killing the druids later did nothing. The watch now arms only once a
   druid has been seen alive, the two-phase shape `build_hamlet_raid.py` uses.
2. **Druids hidden among the Shrine's soldiers.** 0.19.0 swapped a passive "Druid" slot into almost every soldier
   generator, so those generators also spawn a Priest under the room's soldier name. The room's watch counts only
   `<Room> Druid`, so that priest was ignored, then stood down with a soldier's waking line. The Priest entries leave the
   soldier generators; the druid posts are the room's druids.
3. **The posts were off the path.** On Temple Initiate and Stone Chamber both posts stood 1,500 to 2,500 walk units from
   the shortest route, and the Antechamber's second stood beside the exit, so the hold paid only for clearing side rooms.
   One post per map moves to a generator spot on the route.
4. **Priest and Priestess tiers by mojo.** The swap placed tiers by a group's position in the file, not by its
   `Max Party Mojo`, so a 60-mojo group could hold the base Priestess and a 16-mojo one the Super. Every Priest and
   Priestess in the act now takes the tier of its group's mojo: below 23 base, below 40 Tough, else Super.
5. **The Knight of Saladin repeated himself.** 0.99.1's fact-check inserted its replacement sentences beside the old ones
   in nodes 22 and 23 instead of over them.
6. **The Old Man contradicted him.** 0.99.1 made the Knight's standing order "all the centuries since", and the Old Man's
   reply still said the order had "spent eighty of them waiting".
7. **Rumjun Khan could not be spoken to, and could not join.** His can's first specifier fights, and a click reads only
   the first, so the talk specifier his generator added was never read; clicking him attacked him. His spawn now forgets
   the fight specifier and leaves the Enemy category before taking the talk one. "Accompany me" led to a node with no
   action in vanilla too; it now makes him a Player Friend who fights the desert's enemies beside you.
8. **The dog whistle with no dogs.** The Assassin Master cans print "whistles, and guard dogs come running" and clone
   the dog source, but only act 8's maps hold one, so in the Slave Pits the line printed and nothing came. The summon now
   runs only where a map carries `Fixt assassin dogs here`, as vanilla gates the Summoner on its own checker.

A rerun is a no-op.

    python tools/build_back_half_fixes.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH, balanced, exists, if_action, multi, relay
from build_shrine_druids import parts, pos, groups
from build_shrine_repairs import register
from build_hamlet_raid import two_phase
from build_crossroads_standard import forget_specifier, specifier
import build_alamut

SIEGES = {"Levels/6 Barcelona Attack/Gate District Siege.zax": "Gate Siege",
          "Levels/6 Barcelona Attack/Temple District Siege.zax": "Temple Siege"}
SHRINE = "Levels/7 English Shrine/"
FRONT = {"02 Temple Initiate": "Temple", "03 Stone Chamber": "Stone Chamber", "04 Antechamber of Lore": "Antechamber"}
# post -> a generator spot on the shortest route (from the 0.99.9 re-score's path tracer)
MOVES = {"Fixt Temple druid post 2": (2214, 1784), "Fixt Stone Chamber druid post 1": (4099, 3455),
         "Fixt Antechamber druid post 2": (5697, 1520)}
E = "Monster Cans/English Enemies/"
SALADIN = "Resources/Levels/8 Alamut/Dialog/alamutknightsaladin.DialogTree"
OLDMAN = "Resources/Levels/8 Alamut/Dialog/OldMan.DialogTree"
KHAN_TREE = "Resources/Levels/Wilderness/Dialog/GoblinKhan.DialogTree"
SPRAWL = "Levels/8 Alamut/01 Desert Sprawl.zax"
RUMJUN = "Rumjun Khan"
DOGS_HERE = "Fixt assassin dogs here"
TEXT = {SALADIN: [
    ("It should sit badly in us both, brother of the Temple. If any coin of ours has gone to him, it should sit badly in us both. ",
     "If any coin of ours has gone to him, it should sit badly in us both, brother of the Temple. "),
    ("Twice, and both times the guard woke before the blade came down. Twice, and both times the guard woke before the blade came down. ",
     "Twice, and both times the guard woke before the blade came down. "),
    ("Finish what his guards began. Finish what his guards began.", "Finish what his guards began.")],
    OLDMAN: [("and has spent eighty of them waiting", "and has spent every year since waiting")]}


def name_of(x):
    m = re.search(r"(?m)^\t\t\tName=([^\r\n]*)", x)
    return m.group(1) if m else ""


def sieges():
    done = 0
    for rel, room in SIEGES.items():
        z = lhbuild.read(rel)
        watch = "Fixt " + room + " druid watch"
        if "Name=" + watch + " armed" + CR in z:
            continue
        old = [x for x in parts(z) if name_of(x) == watch]
        assert len(old) == 1, rel
        x, y = pos(old[0])
        z = z.replace(old[0] + CR, "", 1)
        z = lhbuild.add_parts(z, two_phase(watch, room + " Druid", relay("Fixt " + room + " druids fall"), int(x), int(y)))
        lhbuild.write_map(rel, z)
        register([rel])
        done += 1
    return done


def drop_things(x, unwanted):
    """Remove each `Thing to Generate` whose entity is unwanted, unless that would empty its group."""
    out = x
    for a, b in reversed(groups(x)):
        g = x[a:b]
        spans = []
        for m in re.finditer(r"(?m)^\t*Thing to Generate=", g):
            e = balanced(g, m.end())
            ent = re.search(r"Entity=([^\r\n]*)", g[m.end():e]).group(1)
            if unwanted(ent):
                spans.append((m.start(), e + 2))
        total = len(re.findall(r"(?m)^\t*Thing to Generate=", g))
        if not spans or len(spans) == total:
            continue
        for s, e in reversed(spans):
            g = g[:s] + g[e:]
        k = g.index("Things to Generate=Array")
        m = re.compile(r"Item Count=(\d+)").search(g, k)
        g = g[:m.start()] + "Item Count=" + str(int(m.group(1)) - len(spans)) + g[m.end():]
        out = out[:a] + g + out[b:]
    return out


def tier(mojo):
    return "" if mojo < 23 else " Tough" if mojo < 40 else " Super"


def retier(x):
    out = x
    for a, b in reversed(groups(x)):
        g = x[a:b]
        mojo = int(re.search(r"Max Party Mojo=(-?\d+)", g).group(1))
        g2 = re.sub(r"Entity=" + re.escape(E) + r"(Priestess|Priest)(?: Tough| Super)?\r\n",
                    lambda m: "Entity=" + E + m.group(1) + tier(mojo) + CR, g)
        out = out[:a] + g2 + out[b:]
    return out


def shrine():
    import glob
    report = {}
    for path in sorted(glob.glob(str(lhbuild.FX / SHRINE) + "/*.zax")):
        m = Path(path).stem
        rel = SHRINE + m + ".zax"
        z = lhbuild.read(rel)
        new = z
        room = FRONT.get(m)
        dropped = moved = 0
        for x in parts(z):
            if "CGeneratorAI" not in x:
                continue
            y = x
            if room and "New Name=" + room + " Soldier" + CR in y:
                y2 = drop_things(y, lambda e: e.startswith(E + "Priest"))
                dropped += y.count("Entity=" + E + "Priest") - y2.count("Entity=" + E + "Priest")
                y = y2
            y = retier(y)
            if name_of(y) in MOVES:
                px, py = MOVES[name_of(y)]
                if pos(y) != (float(px), float(py)):
                    y = re.sub(r"(?m)^(\t\t\tPosition X=)[^\r\n]*", lambda q: q.group(1) + str(px), y, count=1)
                    y = re.sub(r"(?m)^(\t\t\tPosition Y=)[^\r\n]*", lambda q: q.group(1) + str(py), y, count=1)
                    moved += 1
            if y != x:
                new = new.replace(x, y, 1)
        if new != z:
            lhbuild.write_map(rel, new)
            register([rel])
            report[m] = (dropped, moved)
    return report


def text():
    done = 0
    for rel, pairs in TEXT.items():
        t = lhbuild.read(rel)
        crlf = t.count(CR)
        new = t
        for old, fixed in pairs:
            if old in new:
                assert new.count(old) == 1, old
                new = new.replace(old, fixed)
        if new != t:
            assert new.count(CR) == crlf
            (lhbuild.FX / rel).write_bytes(new.encode("latin-1"))
            register([rel])
            done += 1
    return done


def rumjun():
    z = lhbuild.read(SPRAWL)
    gen = [x for x in parts(z) if name_of(x) == "Fixt Khan generator"]
    assert len(gen) == 1
    x = gen[0]
    changed = 0
    if "CRemoveAIAction" not in x:
        talk = ("CDisplayDialogTreeAction", [("Dialog Tree File", "Levels/Wilderness/Dialog/GoblinKhan"), ("Node ID", "500 Start in Persia"),
                                             ("Speaker", "$trigger"), ("Player Being Spoken To", "$Instigator")])
        spawn = multi([("CSetTargetTypeAction", [("Entity Name", "$Instigator"), ("Name To Target", ""), ("Valid Targets", "")]),
                       ("CRemoveCategoryAction", [("Target Name", "$Instigator"), ("Categories To Remove", "Enemy")]),
                       forget_specifier("$Instigator"),
                       specifier("$Instigator", "GetCloseThenTalk", talk)])
        i = x.index("AIs to Add=Array")
        y = x[:i] + "AIs to Add=" + B("Array", [("Item Count", "0")]).rstrip() + x[balanced(x, i):]
        k = y.index("After Action=")
        v = k + len("After Action=")
        y = y[:v] + B(*spawn).rstrip() + y[balanced(y, v):]
        z = z.replace(x, y, 1)
        lhbuild.write_map(SPRAWL, z)
        register([SPRAWL])
        changed += 1
    t = lhbuild.read(KHAN_TREE)
    blocks = t.split(DASH)
    for n, b in enumerate(blocks):
        if re.search(r"Node ID=501 Excellent\r\n", b) and "Custom Action=" not in b:
            join = multi([forget_specifier(RUMJUN),
                          ("COldBad_S_e_t__C_a_t_e_g_o_r_y_Action", [("Target Name", RUMJUN), ("New Category", "Player Friend,Goblin")]),
                          ("CSetTargetTypeAction", [("Entity Name", RUMJUN), ("Name To Target", ""), ("Valid Targets", "Enemy")])])
            k = b.index("Go to node ID=", b.index("Reply Text="))
            k = b.index(CR, k) + 2
            blocks[n] = b[:k] + "Custom Action=" + B(*join) + b[k:]
            new = DASH.join(blocks)
            assert new.count("\n") == new.count(CR)
            (lhbuild.FX / KHAN_TREE).write_bytes(new.encode("latin-1"))
            register([KHAN_TREE])
            changed += 1
    return changed


def dog_whistle():
    """Each master can summons only where a map says dogs are here."""
    done = 0
    clone_line = re.compile(r"Source Name=" + re.escape(build_alamut.DOG_SOURCE) + r"\r\n")
    for can in build_alamut.MASTERS:
        rel = "Resources/" + can + ".can"
        try:
            c = lhbuild.read(rel)
        except Exception:
            continue
        if build_alamut.DOG_SOURCE not in c or DOGS_HERE in c:
            continue
        m = clone_line.search(c)
        # the multi that holds the whistle line and the clone is the nearest CMultipleActionsAction above the clone
        a = c.rindex("CMultipleActionsAction", 0, m.start())
        e = balanced(c, a)
        assert "whistles, and guard dogs come running" in c[a:e]
        guarded = B(*if_action(exists(DOGS_HERE), ("CRawText", []))).rstrip()
        head, tail = guarded.split("CRawText", 1)
        tail = tail[balanced(tail, 0):]
        c = c[:a] + head + c[a:e] + tail + c[e:]
        lhbuild.write_map(rel, c)
        done += 1
    # Active, unlike lhbuild.checker(): an existence check sees only active parts, and this one is never switched on
    for mp in build_alamut.DOG_MAPS:
        rel = build_alamut.A + mp + ".zax"
        z = lhbuild.read(rel)
        here = [x for x in parts(z) if name_of(x) == DOGS_HERE]
        if not here:
            z = lhbuild.add_parts(z, [lhbuild.entity(DOGS_HERE, "1", [], "Editor/Checker", 40, 80, visible="1")])
        elif re.search(r"(?m)^\t\t\tActive=0", here[0]):
            z = z.replace(here[0], re.sub(r"(?m)^(\t\t\tActive=)0", r"\g<1>1", here[0], count=1), 1)
        else:
            continue
        lhbuild.write_map(rel, z)
        register([rel])
    return done


def main():
    print("siege watches made two-phase:", sieges())
    print("shrine maps (priests dropped, posts moved):", shrine())
    print("trees with repaired text:", text())
    print("rumjun edits:", rumjun())
    print("master cans with a guarded whistle:", dog_whistle())


if __name__ == "__main__":
    main()
