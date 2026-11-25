"""Ravine Cave East decides whose cave it is when you arrive, and the Khan's goblins know his friends. Reported: "Seeing
the goblins swap out was jarring and not at all expected, it happened after i was already fighting the kahn's goblins
(which why were they hostile to me?)".

0.31.0 handed the cave to Butu's line after Montserrat with a touch trigger at the Scar Ravine spawn: deactivate and
delete the Khan's goblins, activate Butu's posts. But the Khan's generators are active in the map, so they spawn on
load, and the trigger fires only once the player walks into its 320 radius (the hut entrance has no trigger at all).
The player fought the Khan's goblins, then watched them vanish and red ones appear. And those goblins never read
goblin standing: vanilla placed plain hostile Mongol goblins here, 0.30.0 named them `Khan Goblins`, and a Champion was
attacked by his own Khan's raiders.

  * **Nothing of the Khan's spawns until the cave has decided.** All 13 of his generators and the three arguers start
    inactive. Both spawn points (`Start Here`, `From GoblinHut1`) run the decision as the party arrives: after
    Montserrat, `Butu takeover` (once, as before); otherwise `Fixt Khan goblins arrive` (once), which activates the Khan's
    side. The old touch trigger stays as a harmless fallback: the takeover relay runs only once.
  * **The Khan's goblins keep the peace with his friends.** On that first arrival, a character the Horde counts as
    its own (`Goblin Horde IS`: Chum, Blooded or Champion, not Traitor) lights `Fixt Khan goblins at peace`. Every
    goblin the Khan's generators spawn while it is lit has its targets blanked and `Enemy` removed, and its damaged
    script set, as vanilla's Mongol Camp does, to `Fixt Khan goblins turn`: strike one and the whole cave turns,
    targets and `Enemy` restored, the checker put out.

Map edits: a `Ravine Cave East` not yet entered. A rerun is a no-op.

    python tools/build_ravine_cave_arrival.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, relay, activate, deactivate, if_action, multi
from build_shrine_repairs import register

MAP = "Levels/Wilderness Maps/Ravine Cave East.zax"
KHAN_NAMES = ["Khan Goblins", "Goblin Cave Post", "Drubjub", "Wumjup", "Lumgrub"]
KHAN_GENERATORS = ["Goblin Generator", "Goblin archer Generator", "Goblin archer", "Drubjub Generator", "Wumjup Generator",
                   "Lumgrub Generator"]
SPAWNS = ["Start Here", "From GoblinHut1"]
PEACE = "Fixt Khan goblins at peace"
ARRIVE = "Fixt Khan goblins arrive"
TURN = "Fixt Khan goblins turn"
MONTSERRAT = ["Levels/1 Barcelona/Quests/Calle Perdida/Go to Montserrat and seek out the Crown of Thorns",
              "Levels/1 Barcelona/Quests/Calle Perdida/Go to Montserrat and protect the Crown of Thorns",
              "Levels/1 Barcelona/Quests/Temple District/Ensure safety of Monserrat Relics"]


def parts(z):
    starts = [m.start() + len(CR) for m in re.finditer(r"\r\n\t\tLevel Part=", z)]
    for s in starts:
        yield s, lhbuild.balanced(z, s)


def name_of(p):
    m = re.search(r"\r\n\t\t\tName=([^\r]*)\r\n", p)
    return m.group(1) if m else ""


def targets(name, valid):
    return ("CSetTargetTypeAction", [("Entity Name", name), ("Name To Target", ""), ("Valid Targets", valid)])


PACIFY = if_action(("CCheckExistenceAction", [("Name To Check For", PEACE), ("Desired Minimum Count", "1")]), multi([
    targets("$Instigator", ""),
    ("CRemoveCategoryAction", [("Target Name", "$Instigator"), ("Categories To Remove", "Enemy")]),
    ("CSetDamagedScriptActionAction", [("New Damaged Action", relay(TURN)), ("Target Name", "$Instigator")])]))

TURN_ACTION = multi([deactivate(PEACE)] +
                    [targets(n, "Player,Player Friend") for n in KHAN_NAMES] +
                    [("CAddCategoryAction", [("Target Name", n), ("Categories to add", "Enemy")]) for n in KHAN_NAMES])

FRIEND = ("CExpressionAction", [("Expression", ("CUseCannedExpressionExpression", [
    ("Canned Expression", "Dialog/Requirements/Faction/Goblin Horde IS")])), ("Character to get attributes from", "Player1")])

ARRIVE_ACTION = multi([if_action(FRIEND, activate(PEACE))] + [activate(g) for g in KHAN_GENERATORS])

DECIDE = ("CConditionalAction", [
    ("Try Action", ("COrAction", [("Action", ("Array", [("Item Count", str(len(MONTSERRAT)))] +
                                              [("Action", ("CWasQuestEverActivatedAction", [("Quest", q)])) for q in MONTSERRAT])),
                                  ("Early Exit", "1")])),
    ("Succeed Action", relay("Butu takeover")),
    ("Fail Action", relay(ARRIVE)),
    ("Return failure if the TryAction failes", "0")])


def build():
    z = lhbuild.read(MAP)
    if "Name=" + ARRIVE + CR in z:
        return []
    out, last, gens, pacified, spawns = [], 0, 0, 0, 0
    for s, e in parts(z):
        p = z[s:e]
        name = name_of(p)
        if "Activity=CGeneratorAI" in p and name in KHAN_GENERATORS:
            assert p.count("\r\n\t\t\tActive=1\r\n") == 1, name
            p = p.replace("\r\n\t\t\tActive=1\r\n", "\r\n\t\t\tActive=0\r\n")
            gens += 1
            m = re.search(r"New Name=([^\r]*)\r\n", p)
            if m and m.group(1) in KHAN_NAMES:
                a = p.index("After Action=", m.end())
                v = a + len("After Action=")
                if p.startswith(CR, v):
                    p = p[:v] + B(*PACIFY) + p[v + len(CR):]
                else:
                    ve = lhbuild.balanced(p, v)
                    old = p[v:ve] + CR
                    p = p[:v] + "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR + \
                        "Action=" + old + "Action=" + B(*PACIFY) + "}" + CR + "}" + CR + p[ve + len(CR):]
                pacified += 1
        elif "Activity=CSpawnPointAI" in p and name in SPAWNS:
            assert "Per Party Spawn Action=" + CR in p, name
            p = p.replace("Per Party Spawn Action=" + CR, "Per Party Spawn Action=" + B(*DECIDE), 1)
            spawns += 1
        out.append(z[last:s] + p)
        last = e
    out.append(z[last:])
    z = "".join(out)
    assert (gens, pacified, spawns) == (16, 16, 2), (gens, pacified, spawns)
    z = lhbuild.add_parts(z, [
        lhbuild.checker(PEACE, 1400, 1700),
        lhbuild.relay_part(ARRIVE, ARRIVE_ACTION, 1420, 1700),
        lhbuild.relay_part(TURN, TURN_ACTION, 1440, 1700)])
    lhbuild.write_map(MAP, z)
    return [MAP]


def main():
    done = build()
    if done:
        register(done)
    print("ravine cave arrival:", done)


if __name__ == "__main__":
    main()
