"""The Doomed Plateau's war, made visible. 0.99.14, from the crypt-war review after the 0.99.12 playtest.

The review found the Crypt's two-sides design was written but not shown:

1. **The battle was one-way.** The horde targets `Player,Scripted Custom 2`, and of the knights only the intro detachment
   at the door wears `Scripted Custom 2`. The thirteen knights of the middle line hit the horde, and the horde walked past
   them to the player. They now wear the tag, by the intro knights' own `CAddCategoryAction`, so the horde fights them.
2. **The Revenant Sergeant could not do what its lines say.** It spawned on the horde's targets, about 780 units from the
   nearest knight and 5,150 from the nearest it could target. It now spawns on `Scripted Custom 2` only, at a horde spot
   458 units from the line, turns on the player at 66% beside its whistle, and narrows to the player alone at 33%.
3. **No map read the war tide.** Walk-in triggers at every way onto the Plateau, and on leaving the Bonecaller, read
   `Crypt War Tide` the way vanilla reads a scripting variable on a map (`CExpressionAction` on `$Instigator`). At +1 or
   more the line holds: three reserve knight generators come up at horde spots in front of it. At -1 or less it slips: the
   dead from the opened crypts arrive behind it, and the two forward-most knights fall, with the reserve if it came. Each
   fires once, with a combat-text line.
4. **The Bonecaller was behind the knights, and could not be spoken to.** It stood at (1864, 2555), on the keep side of the
   line and 5,738 units from the entry, and its talk specifier sat after the Boss Lich can's fight one, so a click fought
   it (the Rumjun Khan defect). It moves east to a horde spot behind its own army, holds its fire against the player,
   forgets the fight specifier before taking the talk one, and gets it back if the player strikes it. It hails the player
   on approach and now makes the offer itself.
5. **The undead had no recruiter.** A herald steps out of the dead past the door and asks the player to come and hear the
   Bonecaller. Accepting starts a truce: every undead on the map, and every one that spawns while it holds, drops the
   player from its targets and the Enemy category (so companions leave them alone too) and keeps fighting the knights.
   Striking any of them breaks it. Talking to the Bonecaller ends it, except by swearing to it, which makes it permanent.
6. **The Bonecaller moves the tide.** Releasing it is +1; swearing to it is -3, so swearing always loses the war whatever
   the corridors did. Swearing also sets a character-carried flag, `Fixt Sworn to the Bonecaller`, which the garrison's
   recruitment replies now read instead of the Plateau-only checker, so the knights in Retreat of Souls and the Garrison
   Camp refuse a sworn player too.

Built on in the same release, from play-reading the route:

7. **The dead answer a click** during the truce, as Sahar's stood-down minions do, instead of fighting.
8. **The knight at the door has never seen this.** While the truce holds, clicking him opens a challenge; most answers raise the
   alarm, which reaches Joan by the relay vanilla fires when you pick a fight with her.
9. **The truce lapses** at the knights' line for a player who never answered the Bonecaller, and the slip line names its cause.
10. **The bargain comes due** in the Burial Chamber, when a sworn player takes the Lance while the Bonecaller lives.
11. **Jehanne knows the oath**, and leaves the party if she is beside you when you swear.
12. **The oath follows you** into the Ante Chamber and the Burial Chamber.
13. **Clearing a captain wins ground**: +1 tide, and knights hold the spot when you walk away.

Map changes reach a game that has not entered the map; the dialogue changes reach any game.
A rerun is a no-op.

    python tools/build_crypt_front.py
"""
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH, multi, activate, deactivate, relay, exists, if_action, balanced
from build_shrine_druids import parts
from build_shrine_repairs import register
from build_crossroads_standard import forget_specifier, specifier

MAP = "Levels/4 Crypt/7 Doomed Plateau.zax"
TREE = "Resources/Levels/4 Crypt/Dialog/The Crypt Captains.DialogTree"
TREE_REF = "Levels/4 Crypt/Dialog/The Crypt Captains"
UT = "Resources/Levels/4 Crypt/Dialog/UndeadTemplar.DialogTree"
VARS = "Derived Character Attributes/Game Scripting Variables/"
TIDE = VARS + "Crypt War Tide"
SWORN = VARS + "Fixt Sworn to the Bonecaller"
BC_DEAD = VARS + "Fixt Bonecaller Destroyed"
HERALD_CAN = "Monster Cans/Fixt Captains/Undead/Bonecaller Herald"
HERALD_SRC = "Monster Cans/Undead/Greater Skeleton"
HERALD = "Bonecaller Herald"
BONECALLER = "Bonecaller"
TRUCE = "Fixt undead truce"
DEAD_NAME = "Plateau Dead"
BREACH = "Fixt breach dead"
FORWARD = "Knight Joan Forward"
RESERVE = "Knight Joan Reserve"
ENTRY = (7386, 4117)                 # From Retreat of Souls, where the kit's jump lands too
OTHER_ENTRIES = [(1625, 1993), (5037, 4570), (890, 3267)]  # From Misc Crypt 3, Misc Crypt 4, Ante Chamber
NIS_NAMES = ("Joan", "Ghoul Male attacking Joan")


# ---------------------------------------------------------------- small pieces
def name_of(x):
    m = re.search(r"(?m)^\t\t\tName=([^\r\n]*)", x)
    return m.group(1) if m else ""


def xy(x):
    a = re.search(r"(?m)^\t\t\tPosition X=(-?\d+)", x)
    b = re.search(r"(?m)^\t\t\tPosition Y=(-?\d+)", x)
    return (int(a.group(1)), int(b.group(1))) if a and b else None


def set_xy(x, p):
    x = re.sub(r"(?m)^(\t\t\tPosition X=)-?\d+", lambda m: m.group(1) + str(p[0]), x, count=1)
    return re.sub(r"(?m)^(\t\t\tPosition Y=)-?\d+", lambda m: m.group(1) + str(p[1]), x, count=1)


def rename_part(x, name):
    x = re.sub(r"(?m)^(\t\t\tName=)[^\r\n]*", lambda m: m.group(1) + name, x, count=1)
    return re.sub(r"(?m)^(\t\t\t\tComment=)[^\r\n]*", lambda m: m.group(1) + name, x, count=1)


def set_active(x, v):
    return re.sub(r"(?m)^(\t\t\tActive=)\d", lambda m: m.group(1) + v, x, count=1)


def new_name(x):
    m = re.search(r"New Name=([^\r\n]*)", x)
    return m.group(1) if m else None


def set_new_name(x, v):
    return re.sub(r"New Name=[^\r\n]*", "New Name=" + v, x, count=1)


def target(entity, vt):
    return ("CSetTargetTypeAction", [("Entity Name", entity), ("Name To Target", ""), ("Valid Targets", vt)])


def add_cat(who, cats):
    return ("CAddCategoryAction", [("Target Name", who), ("Categories to add", cats)])


def drop_enemy(who):
    return ("CRemoveCategoryAction", [("Target Name", who), ("Categories To Remove", "Enemy")])


def damaged(who, action):
    return ("CSetDamagedScriptActionAction", [("New Damaged Action", action), ("Target Name", who)])


def say(text):
    return ("CPrintCombatTextAction", [("Text to print", text), ("Character to show text to", "Player1"),
                                       ("Emphasize", "1"), ("Suppress Duplicates", "0")])


def by_player():
    return ("CCheckCategoryAction", [("Target Name", "$Instigator"), ("Category to check for", "Player,Player Friend,Player Shot")])


def not_(a):
    return ("CNotAction", [("Action", a)])


def tide_is(cmp, value):
    return ("CExpressionAction", [("Expression", (cmp, [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", TIDE)])),
                                                         ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", value)]))])),
                                  ("Character to get attributes from", "$Instigator")])


def modify(attr, amount, why):
    """The corridor levers' own write, from 3 Misc Crypt 1."""
    return ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", why), ("Modification is permanent", "1"), ("Character to modify", "Player#1-9#"),
        ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", ("CConstant", [("Constant Value", amount)])), ("Modification amount is a percent", "0"),
            ("Allow Accumulation", "1"), ("Derived character attribute to modify", attr)]))])),
        ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])


def flat(action):
    return B(*action).rstrip()


def gen_after(x):
    """(start, end) of the generator's own After Action value. Balloons inside its AIs carry After Action too, so pin it
    by the key that follows: the generator's is followed by New Facing Angle."""
    for m in re.finditer(r"After Action=", x):
        v = m.end()
        line_end = x.index(CR, v)
        if x[v:line_end].strip():
            end = balanced(x, v)
        else:
            end = line_end
        if x[end:end + 200].lstrip().startswith("New Facing Angle="):
            return v, end
    raise AssertionError("no generator After Action in " + name_of(x))


def append_after(x, action):
    """Run `action` after whatever the generator already does to its spawn."""
    v, end = gen_after(x)
    cur = x[v:end]
    if not cur.strip():
        new = flat(action)
    elif cur.startswith("CMultipleActionsAction"):
        # last in the array, so it runs after (and overrides) what the generator already does; insert at the start of
        # the array's closing-brace line, never by rfind on a brace
        m = re.compile(r"Item Count=(\d+)\r\n").search(x, v)
        assert m and m.start() < end
        a = x.index("Action=Array", v)
        close = balanced(x, a) - 1
        assert x[close] == "}" and close < end
        line = x.rindex("\n", 0, close) + 1
        x = x[:line] + "Action=" + flat(action) + CR + x[line:]
        return x[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + x[m.end():]
    else:
        new = "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR + \
              "Action=" + cur.strip() + CR + "Action=" + flat(action) + CR + "}" + CR + "}"
    return x[:v] + new + x[end:]


def replace_after(x, action):
    v, end = gen_after(x)
    return x[:v] + flat(action) + x[end:]


def dist(a, b):
    return math.dist(a, b)


# ---------------------------------------------------------------- the map
def is_dead_gen(x):
    if "CGeneratorAI" not in x:
        return False
    ents = re.findall(r"Entity=([^\r\n]*)", x)
    # the Deathwatch lives under Fixt Sentry, and the ghoul clone generator by the door names $Instigator beside its cans
    if not ents or not all(re.match(r"Monster Cans/(Fixt Captains/|Fixt Sentry/)?Undead/", e) or e == "$Instigator" for e in ents) \
            or all(e == "$Instigator" for e in ents):
        return False
    nn = new_name(x) or ""
    return not nn.startswith(NIS_NAMES) and name_of(x) != "Fixt Bonecaller generator"


SEEK = ["130 the dead not us", "131 the dead that way", "132 the dead told not to"]
SWORN_LINES = ["135 the dead his now", "136 the dead the door", "137 the dead with you"]


def pick(nodes):
    return ("CRandomAction", [("Action", ("Array", [("Item Count", str(len(nodes)))] +
                                          [("Action", lhbuild.balloon(TREE_REF, n, "$trigger", "-80")) for n in nodes]))])


def dead_line():
    """What one of the dead says when clicked during the truce, the way Sahar's stood-down minions answer a click."""
    return if_action(exists("Fixt sworn to the Bonecaller"), pick(SWORN_LINES), pick(SEEK))


def talk_click(who):
    """A click reads only the first specifier, and every undead can's is the fight one, so forget it first."""
    return [forget_specifier(who), specifier(who, "GetCloseThenTalk", dead_line())]


def fight_click(who):
    return [forget_specifier(who), specifier(who, "GetCloseThenTriggerAndFight", "")]


def truce_spawn():
    """A spawn's script while the truce holds: the knights only, no Enemy category, a click that talks, and striking it
    breaks the truce."""
    return if_action(exists(TRUCE), multi([target("$Instigator", "Scripted Custom 2"), drop_enemy("$Instigator")] + talk_click("$Instigator")))


def breaks():
    return if_action(by_player(), if_action(exists(TRUCE), relay("Fixt truce breaks")))


def build_map():
    z = lhbuild.read(MAP)
    if "Name=" + TRUCE + CR in z:
        return 0
    P = parts(z)
    knights = [p for p in P if "Character Templates/Undead Templar" in p]
    knight_xy = [xy(p) for p in knights]
    dead_spots = [xy(p) for p in P if is_dead_gen(p) and xy(p)]
    any_spots = [xy(p) for p in P if "CGeneratorAI" in p and xy(p)]
    new = z

    def put(old, rep):
        nonlocal new
        assert new.count(old) == 1, name_of(old)
        new = new.replace(old, rep, 1)

    # --- where things go, from existing generator spots
    def kd(p):
        return min(dist(p, k) for k in knight_xy)
    fixt_spots = {xy(p) for p in P if name_of(p).startswith("Fixt")}
    dead_spots = sorted(set(dead_spots) - fixt_spots)
    any_spots = sorted(set(any_spots) - fixt_spots)
    # the Bonecaller stands behind its own horde: west of the door, toward the line, past the intro skirmish
    bc_spot = min((p for p in dead_spots if 1000 <= dist(p, ENTRY) <= 1800 and 5400 <= p[0] <= 6500 and kd(p) >= 900),
                  key=lambda p: dist(p, ENTRY))
    # the herald's ground is on the way there, clear of the door and of the Bonecaller
    arrive = min((p for p in any_spots if 400 <= dist(p, ENTRY) <= 900 and p[0] < ENTRY[0] and dist(p, bc_spot) >= 600),
                 key=lambda p: dist(p, bc_spot))
    herald_cands = [p for p in any_spots if 150 <= dist(p, arrive) <= 450 and dist(p, bc_spot) >= 450 and dist(p, bc_spot) < dist(arrive, bc_spot)]
    herald_spot = min(herald_cands, key=lambda p: dist(p, arrive)) if herald_cands else \
        (int(arrive[0] + (bc_spot[0] - arrive[0]) * 0.3), int(arrive[1] + (bc_spot[1] - arrive[1]) * 0.3))
    line = [k for k, p in zip(knight_xy, knights) if k[0] < 4000]
    line_centre = (int(sum(k[0] for k in line) / len(line)), int(sum(k[1] for k in line) / len(line)))
    sergeant_spot = (2060, 3323)
    assert min(dist(sergeant_spot, k) for k in line) < 550
    reserve_spots = sorted((p for p in dead_spots if 3700 <= p[0] <= 4700), key=lambda p: dist(p, (3900, 3250)))[:3]
    breach_spots = sorted((p for p in dead_spots if 1700 <= p[0] <= 2450 and dist(p, sergeant_spot) > 150), key=lambda p: dist(p, (2100, 3250)))[:3]
    assert len(reserve_spots) == 3 and len(breach_spots) == 3, (reserve_spots, breach_spots)

    # --- 1. the middle line wears the horde's target tag; two of it are named so the slip can take them
    middle = [p for p in knights if xy(p)[0] < 4000]
    assert len(middle) == 13, len(middle)
    plain = sorted((p for p in middle if new_name(p) == "Knight Joan" and "Valid Targets=Scripted Custom 1" in p
                    and "Dialog" not in name_of(p)), key=lambda p: -xy(p)[0])
    forward = plain[:2]
    for p in middle:
        q = append_after(p, add_cat("$Instigator", "Scripted Custom 2"))
        if p in forward:
            q = set_new_name(q, FORWARD)
        put(p, q)
    assert len(forward) == 2
    reserve_src = [q for q in parts(new) if xy(q) == xy(forward[0]) and new_name(q) == FORWARD][0]   # renamed below

    # the anger relay retargets the line by name; the two new names join it
    anger = [q for q in parts(new) if name_of(q) == "All Knights near Joan pissed at player"]
    assert len(anger) == 1
    a = anger[0]
    m = re.compile(r"Item Count=(\d+)\r\n").search(a, a.index("CMultipleActionsAction"))
    a2 = a[:m.start()] + "Item Count=" + str(int(m.group(1)) + 2) + CR + "Action=" + flat(target(FORWARD, "Player,Player Friend")) + CR + \
        "Action=" + flat(target(RESERVE, "Player,Player Friend")) + CR + a[m.end():]
    put(a, a2)

    # --- every undead generator: a list name, and the truce at spawn
    dead_names = set()
    for p in [q for q in parts(new) if is_dead_gen(q)]:
        q = p
        if not new_name(q):
            q = set_new_name(q, DEAD_NAME)
        dead_names.add(new_name(q))
        q = append_after(q, multi([truce_spawn(), damaged("$Instigator", breaks())]))
        if name_of(q) == "Fixt Sergeant generator":
            # 2. the Sergeant: the knights first, the player at 66%, only the player at 33%; none of it under the truce
            q, n = re.subn(r"(Entity Name=\$Instigator\r\n\s*Name To Target=\r\n\s*Valid Targets=)Player,Scripted Custom 2\r\n",
                           lambda m: m.group(1) + "Scripted Custom 2" + CR, q, count=1)
            assert n == 1
            i = q.index("Node ID=111 the sergeant rallies")
            k = q.rindex("CMultipleActionsAction", 0, i)
            m = re.compile(r"Item Count=(\d+)\r\n").search(q, k)
            q = q[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + "Action=" + flat(target("$Trigger", "Player,Scripted Custom 2")) + CR + q[m.end():]
            for node in ("Node ID=111 the sergeant rallies", "Node ID=112 the sergeant fixates"):
                i = q.index(node)
                k = q.rindex("What To Do=CHealthPercentThresholdTrigger", 0, i)
                j = q.index("Action=", k) + len("Action=")
                end = balanced(q, j)
                body = q[j:end]
                q = q[:j] + "CIfAction" + CR + "{" + CR + "If=" + flat(not_(exists(TRUCE))) + CR + "Then=" + body + CR + \
                    "Else=" + CR + "Return failure if the If failes=0" + CR + "}" + q[end:]
            q = set_xy(q, sergeant_spot)
        put(p, q)
    dead_names |= {BREACH}
    dead = sorted(dead_names)

    # --- 4. the Bonecaller: east, holds its fire, can be clicked, fights if struck
    bc = [q for q in parts(new) if name_of(q) == "Fixt Bonecaller generator"][0]
    talk = ("CDisplayDialogTreeAction", [("Dialog Tree File", TREE_REF), ("Node ID", "1 the bonecaller"), ("Speaker", "$trigger"),
                                         ("Player Being Spoken To", "$Instigator")])
    i = bc.index("AIs to Add=Array")
    q = bc[:i] + "AIs to Add=" + B("Array", [("Item Count", "0")]).rstrip() + bc[balanced(bc, i):]
    q = replace_after(q, multi([add_cat("$Instigator", "Scripted Custom 1"), target("$Instigator", "Scripted Custom 2"), drop_enemy("$Instigator"),
                                forget_specifier("$Instigator"), specifier("$Instigator", "GetCloseThenTalk", talk),
                                damaged("$Instigator", if_action(by_player(), relay("Fixt Bonecaller fights")))]))
    q = q.replace("Quantity to generate max=2", "Quantity to generate max=1")
    q = set_xy(q, bc_spot)
    put(bc, q)

    # --- the parts
    tx, ty = bc_spot
    turn_on = [target(n, "Scripted Custom 2") for n in dead] + [drop_enemy(n) for n in dead] + [a for n in dead for a in talk_click(n)]
    # the Sergeant goes back to the knights first; its own 66% trigger turns it on the player
    turn_off = [add_cat(n, "Enemy") for n in dead] + \
        [target(n, "Scripted Custom 2" if n == "Revenant Sergeant" else "Player,Scripted Custom 2") for n in dead] + \
        [a for n in dead for a in fight_click(n)]
    tide_check = multi([
        if_action(tide_is("CIsGreaterThanOrEqual", "1"), if_action(not_(exists("Fixt line held")), relay("Fixt the line holds"))),
        if_action(tide_is("CIsLessThanOrEqual", "-1"), if_action(not_(exists("Fixt line slipped")), relay("Fixt the line slips")))])
    herald_spawn = multi([target("$Instigator", ""), drop_enemy("$Instigator"), forget_specifier("$Instigator"),
                          ("CAddAIAction", [("Target Name", "$Instigator"), ("AI", specifier_part("GetCloseThenTrigger", lhbuild.dialog(TREE_REF, "200 the herald", "$trigger"), "120", "1")),
                                            ("Delay Between Adds", "0")]),
                          damaged("$Instigator", if_action(by_player(), relay("Fixt herald refused")))])
    reserve = []
    for n, s in enumerate(reserve_spots, 1):
        r = rename_part(set_active(set_xy(reserve_src, s), "0"), "Fixt reserve knights " + str(n))
        reserve.append(set_new_name(r, RESERVE).replace("\t\t" + "Level Part=", "Level Part=", 1) + CR)
    breach_src = [q for q in parts(new) if is_dead_gen(q) and name_of(q).startswith("Enemy to Create Crypt")][:3]
    breach = []
    for n, (src, s) in enumerate(zip(breach_src, breach_spots), 1):
        b = rename_part(set_active(set_xy(src, s), "0"), "Fixt breach " + str(n))
        b = set_new_name(b, BREACH)
        b = append_after(b, multi([add_cat("$Instigator", "Scripted Custom 1"), target("$Instigator", "Player,Scripted Custom 2")]))
        b = append_after(b, truce_spawn())   # the truce runs last, so it overrides the targets just set
        breach.append(b.replace("\t\t" + "Level Part=", "Level Part=", 1) + CR)
    herald = lhbuild.generator("Fixt herald generator", "0", HERALD_CAN, HERALD, herald_spawn, herald_spot[0], herald_spot[1])
    pain = [("CPainAction", [("Hit Points", "99999"), ("Damage Type", "Unavoidable"), ("Sound", "!None.wav"), ("Target", n)]) for n in (FORWARD, RESERVE)]
    hostile_herald = multi([activate("Fixt herald was refused"), target(HERALD, "Player,Scripted Custom 2"), add_cat(HERALD, "Enemy"), forget_specifier(HERALD),
                            specifier(HERALD, "GetCloseThenTriggerAndFight", "")])
    hostile_bc = multi([target(BONECALLER, "Player,Scripted Custom 2"), add_cat(BONECALLER, "Enemy"), forget_specifier(BONECALLER),
                        specifier(BONECALLER, "GetCloseThenTriggerAndFight", ""), relay("Fixt truce ends")])
    arrival = multi([if_action(not_(exists("Fixt herald met")), multi([
        activate("Fixt herald met"), activate("Fixt herald generator"),
        say("One of the dead steps out of the horde and comes towards you, an empty hand raised.")])), tide_check])
    hail = hail_when_heard()
    new_parts = [
        lhbuild.checker(TRUCE, tx, ty + 40), lhbuild.checker("Fixt herald met", tx + 20, ty + 40),
        lhbuild.checker("Fixt line held", tx + 40, ty + 40), lhbuild.checker("Fixt line slipped", tx + 60, ty + 40),
        lhbuild.checker("Fixt Bonecaller hailed", tx + 80, ty + 40), lhbuild.checker("Fixt herald was refused", tx + 100, ty + 40),
        lhbuild.relay_part("Fixt truce begins", multi([activate(TRUCE)] + turn_on +
                                                      [say("The dead let you pass. Do not strike them.")]), tx, ty + 60, once="0"),
        lhbuild.relay_part("Fixt truce ends", if_action(exists(TRUCE), multi([deactivate(TRUCE)] + turn_off +
                                                                          [say("The truce is over. The dead turn towards you.")])), tx + 20, ty + 60, once="0"),
        lhbuild.relay_part("Fixt truce breaks", if_action(exists(TRUCE), multi([deactivate(TRUCE)] + turn_off +
                                                                            [say("You struck one of the dead, and every one of them remembers what you are.")])), tx + 40, ty + 60, once="0"),
        lhbuild.relay_part("Fixt Bonecaller fights", hostile_bc, tx + 60, ty + 60),
        lhbuild.relay_part("Fixt herald refused", hostile_herald, tx + 80, ty + 60),
        lhbuild.relay_part("Fixt the line holds", multi([activate("Fixt line held")] + [activate("Fixt reserve knights " + str(n)) for n in (1, 2, 3)] +
                                                        [say("Knights come up from the rear of the keep and take the line forward.")]), tx, ty + 80),
        lhbuild.relay_part("Fixt the line slips", multi([activate("Fixt line slipped")] + [activate("Fixt breach " + str(n)) for n in (1, 2, 3)] + pain +
                                                        # the tide can fall by the corridors or by the oath, so the line says which
                                                        [if_action(exists("Fixt sworn to the Bonecaller"),
                                                                   say("The Bonecaller keeps its side of the bargain. Its dead come up behind the knights, and the line bends."),
                                                                   say("The dead come up through the galleries you opened, behind the knights, and the line bends."))]), tx + 20, ty + 80),
        lhbuild.relay_part("Fixt truce lapses", if_action(exists(TRUCE), if_action(not_(exists("Fixt sworn to the Bonecaller")), multi(
            [deactivate(TRUCE)] + turn_off + [say("You walked past him without a word, and the dead remember it.")]))), tx + 40, ty + 80, once="0"),
        herald,
        lhbuild.touch_oval("Fixt arrival watch", arrival, arrive[0], arrive[1], radius="200", once="0"),
        # wide enough to reach the herald's ground, so the call is heard where the truce is offered
        lhbuild.touch_oval("Fixt Bonecaller ground", hail, tx, ty, radius="650", once="0", exit_action=flat_tuple(tide_check),
                           repeat_action=hail, repeat_every="2"),   # the truce usually starts with the player already inside
    ] + [lhbuild.touch_oval("Fixt tide watch " + str(n), tide_check, *near_spot(any_spots, e), radius="180", once="0",
                            repeat_action=tide_check, repeat_every="2")
         for n, e in enumerate(OTHER_ENTRIES, 1)] + reserve + breach + \
        [lhbuild.touch_oval("Fixt truce lapse " + str(n), relay("Fixt truce lapses"), c[0], c[1], radius=r, once="0")
         for n, (c, r) in enumerate([(line_centre, "650"), ((line_centre[0] + 850, line_centre[1]), "400")], 1)]
    new = lhbuild.add_parts(new, new_parts)
    lhbuild.write_map(MAP, new)
    register([MAP])
    print("  Bonecaller", bc_spot, "| arrival", arrive, "| herald", herald_spot, "| reserve", reserve_spots, "| breach", breach_spots)
    print("  dead names:", dead)
    return 1


def flat_tuple(action):
    return action


def near_spot(spots, e):
    c = [p for p in spots if 150 <= dist(p, e) <= 600]
    p = min(c, key=lambda p: dist(p, e)) if c else (e[0] + 200, e[1])
    return p[0], p[1]


def specifier_part(kind, action, radius, once):
    return lhbuild.specifier(kind, action, radius=radius, once=once)


def balloon_once():
    """The Bonecaller calls the player over, once, while it still holds its fire."""
    return if_action(not_(exists("Fixt Bonecaller hailed")), multi([
        activate("Fixt Bonecaller hailed"),
        if_action(not_(exists("Fixt Bonecaller has turned")), if_action(not_(exists("Fixt sworn to the Bonecaller")),
                                                                         lhbuild.balloon(TREE_REF, "120 the bonecaller calls", BONECALLER, "-90")))]))


def hail_when_heard():
    return if_action(exists(TRUCE), balloon_once(), if_action(exists("Fixt herald was refused"), balloon_once()))


# ---------------------------------------------------------------- dialogue
NEW_NODES = [
    ("130 the dead not us", "Not us. Him. He is waiting.", []),
    ("131 the dead that way", "Go on. The one who raises us is that way.", []),
    ("132 the dead told not to", "We were told not to touch you. Do not make us.", []),
    ("135 the dead his now", "You are his now. Walk.", []),
    ("136 the dead the door", "The door. You promised him the door.", []),
    ("137 the dead with you", "Go on. We are with you.", []),
    ("120 the bonecaller calls", "Here, breathing one. I will not raise a hand to you, which is more than the hill will promise. Come and hear an offer.", []),
    ("15 the offer", "Then here it is. The knights hold a door, and behind it is the spear I was pointed at before you were born. Break the door "
                     "for me, and the dead will walk around you for as long as you are on this hill. Refuse, and you are one more thing that "
                     "breathes on a plateau of things that do not.", "OFFER"),
    ("16 then go", "Then go, and take the hill as you find it. I will not hold them back a second time.", []),
    ("200 the herald", "<A skeleton in the rags of a herald's tabard holds up an empty hand.> The one who raises us would speak with you. He waits "
                       "close by, behind his dead. Will you come and hear him? If you will, the dead will not lay a hand on you until you have.", "HERALD"),
    ("201 the herald steps aside", "<It lowers the hand and steps out of your way.> Then walk. They will not touch you. Do not touch them.", []),
    ("202 the herald turns", "<The hand closes.> Then you will meet him the other way.", []),
    ("210 the debt", "<The herald has come down after you, and the doorway behind it is full of the dead.> He kept his word. Not one of them "
                     "lifted a hand to you on that hill. Now the spear.", "DEBT"),
    ("211 he can wait", "<It looks at the spear for a long time.> He has waited two hundred years. He can wait for you. But he will always "
                        "know where you are.", []),
    ("212 a thing that breaks its word", "<The hand closes.> Then you are a thing that breaks its word, on a hill that has only ever held two "
                                         "kinds. Take it, then, if you can carry it out.", []),
]
DEBT_MAP = "Levels/4 Crypt/9 Burial Chamber.zax"
LANCE = "Inventory/Specific Item Cans/Quest Items/SACRED LANCE"
PLINTH = [4860, 3280, 5170, 3280, 5170, 3580, 4860, 3580, 4860, 3280]   # the polygon Jehanne's farewell already uses
PORTAL = (4770, 3540)


def build_debt():
    """The bargain comes due. A sworn player who walks off the plinth with the Lance meets the herald, which has followed
    them down; the oath is on the character, so this map can read it."""
    z = lhbuild.read(DEBT_MAP)
    if "Name=Fixt the debt comes due" + CR in z:
        return 0
    P = parts(z)
    sworn = ("CExpressionAction", [("Expression", ("CIsGreaterThanOrEqual", [
        ("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", SWORN)])), ("Operator", ""),
        ("Operand2", ("CConstant", [("Constant Value", "1")]))])), ("Character to get attributes from", "$Instigator")])
    has_lance = ("CActionCheckForInventoryItem", [("Who to give check", "$instigator"), ("Inventory Item To Check For", LANCE)])
    alive = ("CExpressionAction", [("Expression", ("CIsLessThan", [
        ("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", BC_DEAD)])), ("Operator", ""),
        ("Operand2", ("CConstant", [("Constant Value", "1")]))])), ("Character to get attributes from", "$Instigator")])
    due = if_action(not_(exists("Fixt debt called")), if_action(has_lance, if_action(sworn, if_action(alive, relay("Fixt the debt comes due")))))
    herald_spawn = multi([target("$Instigator", ""), drop_enemy("$Instigator"), forget_specifier("$Instigator"),
                          ("CAddAIAction", [("Target Name", "$Instigator"),
                                            ("AI", specifier_part("GetCloseThenTrigger", lhbuild.dialog(TREE_REF, "210 the debt", "$trigger"), "160", "1")),
                                            ("Delay Between Adds", "0")]),
                          damaged("$Instigator", if_action(by_player(), relay("Fixt the debt is refused")))])
    # the dead that come through the door: the chamber's own undead generators nearest the portal, copied and held back
    dead = sorted((p for p in P if is_dead_gen(p) and xy(p)), key=lambda p: dist(xy(p), PORTAL))[:3]
    assert len(dead) == 3
    wave = []
    for n, src in enumerate(dead, 1):
        w = rename_part(set_active(src, "0"), "Fixt debt " + str(n))
        w = set_new_name(w, "Fixt debt dead")
        w = append_after(w, multi([target("$Instigator", "Player,Player Friend"), add_cat("$Instigator", "Enemy")]))
        wave.append(w.replace("\t\t" + "Level Part=", "Level Part=", 1) + CR)
    refused = multi([target(HERALD, "Player,Player Friend"), add_cat(HERALD, "Enemy"), forget_specifier(HERALD),
                     specifier(HERALD, "GetCloseThenTriggerAndFight", "")] + [activate("Fixt debt " + str(n)) for n in (1, 2, 3)] +
                    [say("The dead come through the doorway after you. The Bonecaller has been refused.")])
    hx, hy = PORTAL[0] - 120, PORTAL[1] - 60
    new_parts = [
        lhbuild.checker("Fixt debt called", hx, hy + 40),
        lhbuild.relay_part("Fixt the debt comes due", multi([activate("Fixt debt called"), activate("Fixt debt herald generator"),
                                                            say("Something has followed you down from the hill.")]), hx + 20, hy + 40),
        lhbuild.relay_part("Fixt the debt is refused", refused, hx + 40, hy + 40),
        lhbuild.generator("Fixt debt herald generator", "0", HERALD_CAN, HERALD, herald_spawn, hx, hy),
        lhbuild.poly_part("Fixt the bargain watches the plinth", ("CTouchingPolygonTriggerAI",
                          lhbuild.trigger_fields("0", due, due, due, "1", "", "1")), PLINTH),
    ] + wave
    lhbuild.write_map(DEBT_MAP, lhbuild.add_parts(z, new_parts))
    register([DEBT_MAP])
    return 1


def tree_node(nid, text, replies):
    return lhbuild.node(nid, text, replies)


def build_tree():
    t = lhbuild.read(TREE)
    if "Node ID=15 the offer" + CR in t:
        return 0
    crlf_lines = t.count("\n")
    assert crlf_lines == t.count(CR)
    blocks = t.split(DASH)

    def edit(nid, fn):
        hits = [n for n, b in enumerate(blocks) if re.search(r"Node ID=" + re.escape(nid) + r"\r\n", b)]
        assert len(hits) == 1, nid
        blocks[hits[0]] = fn(blocks[hits[0]])

    fight = "Custom Action=CGoToCombatAction" + CR + "{" + CR + "Enemy Name=$Trigger" + CR + "}" + CR
    fight_relay = "Custom Action=" + B(*multi([relay("Fixt Bonecaller fights"), ("CGoToCombatAction", [("Enemy Name", "$Trigger")])]))

    def node1(b):
        k = b.index("Requirement=!None" + CR + "Reply Text=What are you?")
        offer = "Requirement=!None" + CR + "Reply Text=You said something that is not a sword. Name it." + CR + "Go to node ID=15 the offer" + CR + CR
        b = b[:k] + offer + b[k:]
        # the knights, Jehanne and the Old Man all count the siege in centuries
        old = "Reply Text=Ninety years of the same order."
        assert b.count(old) == 1
        b = b.replace(old, "Reply Text=Two hundred years of the same order.")
        assert b.count(fight) == 1
        return b.replace(fight, fight_relay)

    def node5(b):
        assert b.count(fight) == 1
        return b.replace(fight, fight_relay)

    def node10(b):
        assert b.count(fight) == 1
        return b.replace(fight, fight_relay)

    def node20(b):
        k = b.index("Custom Action=CMultipleActionsAction")
        m = re.compile(r"Item Count=(\d+)\r\n").search(b, k)
        add = [relay("Fixt truce ends"), modify(TIDE, "1", "Crypt war tide")]
        return b[:m.start()] + "Item Count=" + str(int(m.group(1)) + len(add)) + CR + "".join("Action=" + B(*a) for a in add) + b[m.end():]

    def node21(b):
        b = b.replace("New Category=Player Friend,Undead" + CR, "New Category=Player Friend,Scripted Custom 1,Undead" + CR)
        b = b.replace("Valid Targets=Undead" + CR, "Valid Targets=Scripted Custom 2" + CR)
        assert "Scripted Custom 1,Undead" in b and "Valid Targets=Scripted Custom 2" in b
        k = b.index("Custom Action=CMultipleActionsAction")
        m = re.compile(r"Item Count=(\d+)\r\n").search(b, k)
        add = [relay("Fixt truce begins"), modify(TIDE, "-3", "Crypt war tide"), modify(SWORN, "1", "Sworn to the Bonecaller")]
        return b[:m.start()] + "Item Count=" + str(int(m.group(1)) + len(add)) + CR + "".join("Action=" + B(*a) for a in add) + b[m.end():]

    edit("1 the bonecaller", node1)
    edit("5 the answer", node5)
    edit("10 bound", node10)
    edit("20 stands down", node20)
    edit("21 the bargain", node21)

    nodes = []
    for nid, text, kind in NEW_NODES:
        if kind == "OFFER":
            replies = [{"req": "Karma LESS 600", "text": "Keep your orders, then. I will open the keep for you, and you will owe me the spear.", "go": "21 the bargain"},
                       {"text": "There may be another way. Let me look at what binds you.", "go": "10 bound"},
                       {"text": "No.", "go": "16 then go", "action": relay("Fixt truce ends"), "default": True}]
        elif kind == "DEBT":
            replies = [{"req": "Speech moreequal 110", "text": "<Lie> He will have it, when I have finished what it is for. Tell him that.", "go": "211 he can wait"},
                       {"text": "The spear is mine. He was a fool to bargain with me.", "go": "212 a thing that breaks its word",
                        "action": relay("Fixt the debt is refused"), "default": True}]
        elif kind == "HERALD":
            replies = [{"text": "I will hear him.", "go": "201 the herald steps aside", "action": relay("Fixt truce begins")},
                       {"text": "No. Get out of my way.", "go": "202 the herald turns", "action": relay("Fixt herald refused"), "default": True}]
        else:
            replies = []
        nodes.append(tree_node(nid, text, replies))
    t2 = DASH.join(blocks)
    assert t2.endswith("}" + CR)
    t2 = t2[:-len("}" + CR)] + CR + DASH + CR + (CR + DASH + CR).join(nodes) + "}" + CR
    assert t2.count("\n") == t2.count(CR)
    (lhbuild.FX / TREE).write_bytes(t2.encode("latin-1"))
    register([TREE])
    return 1


UT_REF = "Levels/4 Crypt/Dialog/UndeadTemplar"
DOOR = "Knight Intro Talker"
ARMS = "Fixt garrison takes up arms"
DOOR_NODES = [
    ("300 the dead let you walk", "<His sword is up before you are close.> Stand there. I watched you come up through that gallery, and not one "
                                  "of them lifted a hand to you. I have held this line for two hundred years and I have never once seen that. What "
                                  "are you, and what did they promise you? Answer carefully. If I call this line to arms, the Lady will hear it.", "DOOR"),
    ("301 an envoy", "Then you are his envoy until you have, and his envoys do not stand in this line. <He raises his voice.> To arms! The dead "
                     "have sent us a guest!", []),
    ("302 fools", "<He does not lower the sword.> Then they are fools, or you are. Stay where I can see you, and keep away from the Lady.", []),
    ("303 they do not part", "<His eyes go to the dead behind you, and back to you.> They do not part for nothing. To arms!", []),
    ("304 go then", "Go, then. And do not come back to this line while they are still letting you walk.", []),
    ("305 watch that one", "The dead are letting it walk! Watch that one!", []),
]


def build_door_tree():
    """The knight at the door, clicked while the truce holds: suspicion, and most answers end in a fight."""
    t = lhbuild.read(UT)
    if "Node ID=300 the dead let you walk" + CR in t:
        return 0
    nodes = []
    for nid, text, kind in DOOR_NODES:
        replies = []
        if kind == "DOOR":
            replies = [{"req": "Speech moreequal 100", "text": "<Lie> They took me for one of their own. I let them.", "go": "302 fools"},
                       {"text": "Their master wants to bargain. I have not answered him.", "go": "301 an envoy", "action": relay(ARMS)},
                       {"text": "I owe them nothing, and I owe you less.", "go": "303 they do not part", "action": relay(ARMS)},
                       {"text": "I will go.", "go": "304 go then", "default": True}]
        nodes.append(tree_node(nid, text, replies))
    assert t.endswith("}" + CR)
    t2 = t[:-len("}" + CR)] + CR + DASH + CR + (CR + DASH + CR).join(nodes) + "}" + CR
    assert t2.count("\n") == t2.count(CR)
    (lhbuild.FX / UT).write_bytes(t2.encode("latin-1"))
    register([UT])
    return 1


def build_door_map():
    """The door knight's click reads the truce; the truce, when it starts, is seen from the door."""
    z = lhbuild.read(MAP)
    if "Name=" + ARMS + CR in z:
        return 0
    p = [x for x in parts(z) if name_of(x) == "Adds Dialog knight beginning"]
    assert len(p) == 1
    x = p[0]
    k = x.index("Interaction Type=Interaction Specifiers/GetCloseThenTalk")
    j = x.index("Action=", k) + len("Action=")
    assert x[j:].startswith("CRandomAction")
    end = balanced(x, j)
    y = x[:j] + "CIfAction" + CR + "{" + CR + "If=" + flat(exists(TRUCE)) + CR + "Then=" + flat(lhbuild.dialog(UT_REF, "300 the dead let you walk", "$trigger")) + CR + \
        "Else=" + x[j:end] + CR + "Return failure if the If failes=0" + CR + "}" + x[end:]
    z = z.replace(x, y, 1)
    # the vanilla relay that sets the door's knights on the player when one is struck
    # the alarm reaches the Lady: the second relay is the one vanilla fires when you choose combat with Joan herself
    arms = lhbuild.relay_part(ARMS, multi([relay("Make Knights at Level Start attack"), relay("Joan Player chose combat in dialog"),
                                           say("The alarm goes up the line. The knights, and the Lady with them, take up arms against you.")]), 7300, 4100)
    seen = lhbuild.relay_part("Fixt the door sees the truce", if_action(("CIsAliveAction", [("Name To Check For", DOOR), ("Desired Minimum Count", "1")]),
                                                                       lhbuild.balloon(UT_REF, "305 watch that one", DOOR, "-75")), 7320, 4100)
    z = lhbuild.add_parts(z, [arms, seen])
    # the truce's first start is seen from the door
    b = [q for q in parts(z) if name_of(q) == "Fixt truce begins"][0]
    m = re.compile(r"Item Count=(\d+)\r\n").search(b, b.index("CMultipleActionsAction"))
    b2 = b[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + "Action=" + flat(relay("Fixt the door sees the truce")) + CR + b[m.end():]
    z = z.replace(b, b2, 1)
    lhbuild.write_map(MAP, z)
    register([MAP])
    return 1


def build_garrison_gate():
    t = lhbuild.read(UT)
    old = flat(("CCheckExistenceAction", [("Name To Check For", "Fixt sworn to the Bonecaller"), ("Desired Minimum Count", "1")]))
    if t.count(old) == 0:
        return 0
    assert t.count(old) == 3, t.count(old)
    sworn = flat(("CExpressionAction", [("Expression", ("CIsGreaterThanOrEqual", [
        ("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", SWORN)])), ("Operator", ""),
        ("Operand2", ("CConstant", [("Constant Value", "1")]))])), ("Character to get attributes from", "$Instigator")]))
    n = t.count(CR)
    t2 = t.replace(old, sworn)
    assert t2.count("\n") == t2.count(CR)
    (lhbuild.FX / UT).write_bytes(t2.encode("latin-1"))
    register([UT])
    return 1


def build_files():
    done = 0
    rel = "Resources/" + SWORN + ".DerivedCharacterAttribute"
    if not (lhbuild.FX / rel).exists():
        t = lhbuild.read("Resources/" + TIDE + ".DerivedCharacterAttribute")
        assert t.count("Crypt War Tide") == 2
        lhbuild.write_map(rel, t.replace("Crypt War Tide", "Fixt Sworn to the Bonecaller"))
        register([rel])
        done += 1
    rel = "Resources/" + BC_DEAD + ".DerivedCharacterAttribute"
    if not (lhbuild.FX / rel).exists():
        t = lhbuild.read("Resources/" + TIDE + ".DerivedCharacterAttribute")
        lhbuild.write_map(rel, t.replace("Crypt War Tide", "Fixt Bonecaller Destroyed"))
        register([rel])
        done += 1
    rel = "Resources/" + HERALD_CAN + ".can"
    if not (lhbuild.FX / rel).exists():
        t = lhbuild.read("Resources/" + HERALD_SRC + ".can")
        t, n = re.subn(r"User Assigned Name=[^\r\n]*", "User Assigned Name=Herald of the Bonecaller", t, count=1)
        assert n == 1
        lhbuild.write_map(rel, t)
        register([rel])
        done += 1
    return done


# ---------------------------------------------------------------- the knights claim a captain's ground
CLAIMS = {"Fixt Bonewright generator": "Bonewright", "Fixt Sergeant generator": "Sergeant", "Fixt Bonecaller generator": "Bonecaller"}
CLAIM_KNIGHT = "Knight Claim"


def build_claims():
    """Clearing a captain is a win for the garrison, so it moves the war tide +1, and the knights taking its ground is how the
    player sees it: when they walk away from where it stood, knights come up and hold the spot. Not for a sworn player, and
    not for the Bonecaller once it has been released (that already paid +1)."""
    z = lhbuild.read(MAP)
    if "Name=Fixt claim Bonewright" + CR in z:
        return 0
    P = parts(z)
    src = [q for q in P if "Character Templates/Undead Templar" in q and new_name(q) == FORWARD][0]
    tide_check = multi([
        if_action(tide_is("CIsGreaterThanOrEqual", "1"), if_action(not_(exists("Fixt line held")), relay("Fixt the line holds"))),
        if_action(tide_is("CIsLessThanOrEqual", "-1"), if_action(not_(exists("Fixt line slipped")), relay("Fixt the line slips")))])
    new_parts = []
    new = z
    for gen, short in CLAIMS.items():
        p = [q for q in parts(new) if name_of(q) == gen][0]
        x, y = xy(p)
        fallen, claimed, ground = "Fixt " + short + " fallen", "Fixt " + short + " claimed", "Fixt claim " + short
        guard = not_(exists("Fixt sworn to the Bonecaller"))
        death = if_action(guard, multi([activate(fallen), activate(ground), modify(TIDE, "1", "Crypt war tide")]))
        if short == "Bonecaller":
            death = multi([if_action(not_(exists("Fixt Bonecaller has turned")), death), modify(BC_DEAD, "1", "Bonecaller destroyed")])
        if "CSetDestroyedScriptActionAction" in p:
            k = p.index("New Destroyed Action=CMultipleActionsAction")
            m = re.compile(r"Item Count=(\d+)\r\n").search(p, k)
            q = p[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + "Action=" + flat(death) + CR + p[m.end():]
        else:
            q = append_after(p, ("CSetDestroyedScriptActionAction", [("New Destroyed Action", death), ("Target Name", "$Instigator")]))
        new = new.replace(p, q, 1)
        knights = []
        for n, (dx, dy) in enumerate([(-40, 0), (40, 20)], 1):
            k = rename_part(set_active(set_xy(src, (x + dx, y + dy)), "0"), "Fixt claim knights " + short + " " + str(n))
            knights.append(set_new_name(k, CLAIM_KNIGHT).replace("\t\t" + "Level Part=", "Level Part=", 1) + CR)
        walk_away = if_action(exists(fallen), if_action(not_(exists(claimed)), multi(
            [activate(claimed)] + [activate("Fixt claim knights " + short + " " + str(n)) for n in (1, 2)] +
            [say("Knights come up behind you and stand where the " + ("Revenant Sergeant" if short == "Sergeant" else short) +
                 " fell. This ground is held."), tide_check])))
        new_parts += [lhbuild.checker(fallen, x, y + 60), lhbuild.checker(claimed, x + 20, y + 60),
                      lhbuild.touch_oval(ground, "", x, y, radius="300", once="0", exit_action=walk_away, active="0")] + knights
    new = lhbuild.add_parts(new, new_parts)
    lhbuild.write_map(MAP, new)
    register([MAP])
    return 1


# ---------------------------------------------------------------- Jehanne knows the oath
JOAN_TREE = "Resources/Levels/4 Crypt/Dialog/JoanofArc.DialogTree"
JOAN_OPENERS = ["1 Conversation Start", "3 Return Dialogue Likes Player", "3 Return Dialogue Hate Player"]
JOAN_NODES = [
    ("700 the oath", "<Her sword is out before you speak.> You smell of him. For two hundred years that thing has sent my own knights' "
                     "dead up this hill against us, and you have given it your word. I will not ask what it promised you. Go back to it, or draw.", "OATH"),
    ("701 then go", "Then go. And if I see you inside my line, I will not be the one who speaks first.", []),
]


def build_joan_tree():
    t = lhbuild.read(JOAN_TREE)
    if "Node ID=700 the oath" + CR in t:
        return 0
    nodes = []
    for nid, text, kind in JOAN_NODES:
        replies = []
        if kind == "OATH":
            replies = [{"text": "Then we draw.", "go": "", "action": relay("Joan Player chose combat in dialog"), "icon": "Fight Icon"},
                       {"text": "I am going.", "go": "701 then go", "default": True}]
        nodes.append(tree_node(nid, text, replies))
    assert t.endswith("}" + CR)
    t2 = t[:-len("}" + CR)] + CR + DASH + CR + (CR + DASH + CR).join(nodes) + "}" + CR
    assert t2.count("\n") == t2.count(CR)
    (lhbuild.FX / JOAN_TREE).write_bytes(t2.encode("latin-1"))
    register([JOAN_TREE])
    return 1


def build_joan_map():
    """Every way Jehanne's conversation opens on the Plateau reads the oath first."""
    z = lhbuild.read(MAP)
    if "Node ID=700 the oath" in z:
        return 0
    for node in JOAN_OPENERS:
        key = "Dialog Tree File=Levels/4 Crypt/Dialog/JoanofArc" + CR
        hits = [m.start() for m in re.finditer(re.escape("Node ID=" + node) + r"\r\n", z)]
        hits = [h for h in hits if z.rfind(key, 0, h) > z.rfind("Action", 0, z.rfind(key, 0, h)) - 40]
        assert len(hits) == 1, (node, len(hits))
        h = hits[0]
        s = z.rindex("CDisplayDialogTreeAction", 0, h)
        e = balanced(z, s)
        orig = z[s:e]
        oath = orig.replace("Node ID=" + node + CR, "Node ID=700 the oath" + CR, 1)
        z = z[:s] + "CIfAction" + CR + "{" + CR + "If=" + flat(exists("Fixt sworn to the Bonecaller")) + CR + "Then=" + oath + CR + \
            "Else=" + orig + CR + "Return failure if the If failes=0" + CR + "}" + z[e:]
    lhbuild.write_map(MAP, z)
    register([MAP])
    return 1


def build_joan_leaves():
    """Swearing with Jehanne beside you: she leaves and turns on you, by the relay vanilla wrote for exactly that."""
    t = lhbuild.read(TREE)
    if "Name To Check For=Joan is a companion" in t:
        return 0
    blocks = t.split(DASH)
    hits = [n for n, b in enumerate(blocks) if re.search(r"Node ID=21 the bargain\r\n", b)]
    assert len(hits) == 1
    b = blocks[hits[0]]
    k = b.index("Custom Action=CMultipleActionsAction")
    m = re.compile(r"Item Count=(\d+)\r\n").search(b, k)
    leave = if_action(exists("Joan is a companion"), relay("Joan leaves party and attacks player"))
    blocks[hits[0]] = b[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + "Action=" + B(*leave) + b[m.end():]
    t2 = DASH.join(blocks)
    assert t2.count("\n") == t2.count(CR)
    (lhbuild.FX / TREE).write_bytes(t2.encode("latin-1"))
    register([TREE])
    return 1


# ---------------------------------------------------------------- the oath beyond the Plateau
OATH_MAPS = {"Levels/4 Crypt/8 Ante Chamber.zax": ("Ante Dead", [(5182, 5083), (4013, 3381)]),
             "Levels/4 Crypt/9 Burial Chamber.zax": ("Chamber Dead", [(2101, 1683), (3989, 3825)])}
OATH_SKIP = ("Fixt debt dead", HERALD)


def build_oath_map(rel, dead_name, entries):
    entries = sorted(set(entries) | {xy(q) for q in parts(lhbuild.read(rel)) if "CSpawnPointAI" in q and xy(q)})
    """A sworn player's dead follow the oath off the hill. The oath is on the character, so an entry trigger reads it and
    switches on a map-local checker that spawn scripts can test; striking one, or refusing the debt, breaks it here."""
    z = lhbuild.read(rel)
    if "Name=Fixt oath honoured" + CR in z:
        return 0
    new = z
    names = set()
    honoured = "Fixt oath honoured"
    calm = multi([target("$Instigator", ""), drop_enemy("$Instigator"), forget_specifier("$Instigator"),
                  specifier("$Instigator", "GetCloseThenTalk", pick(SWORN_LINES))])
    hit = if_action(by_player(), if_action(exists(honoured), relay("Fixt oath breaks")))
    for p in [q for q in parts(z) if is_dead_gen(q) and (new_name(q) or "") not in OATH_SKIP]:
        q = p
        if not new_name(q):
            q = set_new_name(q, dead_name)
        names.add(new_name(q))
        q = append_after(q, multi([if_action(exists(honoured), calm), damaged("$Instigator", hit)]))
        assert new.count(p) == 1
        new = new.replace(p, q, 1)
    names = sorted(names)
    on = [a for n in names for a in (target(n, ""), drop_enemy(n), forget_specifier(n), specifier(n, "GetCloseThenTalk", pick(SWORN_LINES)))]
    off = [a for n in names for a in (add_cat(n, "Enemy"), target(n, "Player,Player Friend"), forget_specifier(n),
                                      specifier(n, "GetCloseThenTriggerAndFight", ""))]
    sworn = ("CExpressionAction", [("Expression", ("CIsGreaterThanOrEqual", [
        ("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", SWORN)])), ("Operator", ""),
        ("Operand2", ("CConstant", [("Constant Value", "1")]))])), ("Character to get attributes from", "$Instigator")])
    enter = if_action(sworn, if_action(not_(exists(honoured)), if_action(not_(exists("Fixt oath broken")), relay("Fixt the oath is honoured"))))
    x, y = entries[0]
    new_parts = [
        lhbuild.checker(honoured, x, y + 40), lhbuild.checker("Fixt oath broken", x + 20, y + 40),
        lhbuild.relay_part("Fixt the oath is honoured", multi([activate(honoured)] + on +
                                                              [say("The dead here know whose word you carry. They let you pass.")]), x + 40, y + 40),
        lhbuild.relay_part("Fixt oath breaks", if_action(exists(honoured), multi([deactivate(honoured), activate("Fixt oath broken")] + off +
                                                                              [say("The oath is broken. The dead here turn on you.")])), x + 60, y + 40, once="0"),
    ] + [lhbuild.touch_oval("Fixt oath watch " + str(n), enter, ex, ey, radius="300", once="0", repeat_action=enter, repeat_every="2")
         for n, (ex, ey) in enumerate(entries, 1)]
    new = lhbuild.add_parts(new, new_parts)
    if "Name=Fixt the debt is refused" + CR in new:
        # refusing the debt breaks the oath for the chamber's own dead too
        r = [q for q in parts(new) if name_of(q) == "Fixt the debt is refused"][0]
        m = re.compile(r"Item Count=(\d+)\r\n").search(r, r.index("CMultipleActionsAction"))
        r2 = r[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + "Action=" + flat(relay("Fixt oath breaks")) + CR + r[m.end():]
        new = new.replace(r, r2, 1)
    lhbuild.write_map(rel, new)
    register([rel])
    print("  ", rel.split("/")[-1], "dead:", names)
    return 1


def main():
    print("files:", build_files())
    print("map:", build_map())
    print("tree:", build_tree(), "| garrison gate:", build_garrison_gate())
    print("door: tree", build_door_tree(), "| map", build_door_map())
    print("debt:", build_debt())
    print("Jehanne: tree", build_joan_tree(), "| map", build_joan_map(), "| leaves", build_joan_leaves())
    print("oath:", [build_oath_map(rel, n, e) for rel, (n, e) in OATH_MAPS.items()])
    print("claims:", build_claims())


if __name__ == "__main__":
    main()
