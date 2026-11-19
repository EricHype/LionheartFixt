"""Goblin standing follows the title perks, not the faction. A user report: "My character in the quicksave is goblin
champion ... but can't get the quest to attack esteban at the crossroads from the goblin".

The Horde's ranks were Fixt factions (`Factions/Goblin Chum`, `Blooded`, `Champion`, 0.1.0), each adding its number to
`Uber Perks/Goblin Rank`, and every Horde gate read that number. A character holds one `Faction=`, and assigning another
withdraws the old package, rank included (0.9.0, "One faction, one rank"). The save: `Faction=Factions/Wielder Mage`,
`Wielder Rank=1`, no Goblin Rank at all, and all three goblin title perks. Joining the Wielders had quietly taken the
Champion out of the Horde, and every gate read 0. The other way round was worse: `Advance Goblin Rank` assigned the goblin
faction with no test, so serving the Horde after swearing to an order replaced the order.

0.9.0 settled the same fault for Saladin by gating on the Crescent perks, which survive faction changes. Same here:

  * `Goblin Horde IS` / `Midlevel` / `Highlevel`: Chum, Blooded or Champion / Blooded or Champion / Champion, each AND
    NOT `Goblin Traitor`. `Goblin Horde NOT` is NOT `IS`. `Fixt Goblin Slayer In The Horde` reads the same test.
  * `Advance Goblin Rank` picks the next tier from the perks (none -> Chum -> Blooded -> Champion -> nothing) and assigns
    the tier's faction, with its bonuses, only to a character sworn to no order (Templar, Inquisition, Wielder and
    Saladin rank all 0, vanilla's own cans). A sworn character gains the title. `Join Butus Line` the same, Champion ->
    Fallen Champion, any other title -> Bad Blood, none -> Foe. The 2026-11-18 import guard around both is kept.
  * The Khan's three Everlasting rewards gave vanilla's Champion perk *and* one ladder step, so the title read Champion
    while the rank read 1 or 2. They now dispatch `Name Goblin Champion`: the same import guard, the Champion faction if
    sworn to no order, and the Champion perk, which vanilla gives here regardless.
  * The Warrens' Khan greeting read the rank directly; it reads `Goblin Horde Highlevel`.

The cans and the tree reach every save. The Warrens greeting is map-side. Imported titles now carry their standing, which
the 2026-11-18 decision ("keeps the title and bonuses it carried") already implies. A rerun is a no-op.

    python tools/build_goblin_standing_by_title.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register
from build_goblin_rank_guard import CONDITION, SET_FLAG, has_perk, any_of

REQ = "Resources/Dialog/Requirements/Faction/"
GATES = {"Goblin Horde IS": ["Goblin Chum", "Goblin Blooded", "Goblin Champion"],
         "Goblin Horde Midlevel": ["Goblin Blooded", "Goblin Champion"],
         "Goblin Horde Highlevel": ["Goblin Champion"]}
SLAYER = "Resources/Dialog/Requirements/Fixt Goblin Slayer In The Horde.can"
LADDER = "Resources/Levels/Wilderness/Quests/Advance Goblin Rank.can"
BUTU = "Resources/Levels/Wilderness/Quests/Join Butus Line.can"
CHAMPION = "Resources/Levels/Wilderness/Quests/Name Goblin Champion.can"
KHAN = "Resources/Levels/Wilderness/Dialog/GoblinKhan.DialogTree"
WARRENS = "Levels/Wilderness Maps/Goblin Warrens.zax"
TITLE = "Perks/!Event Title Perks/"
ORDERS = ["Templar NOT", "Inquisitor NOT", "Saladin NOT", "Wielder NOT"]


# ------------------------------------------------------------- expressions (the Saladin Favored can's own idiom)
def perk_expr(p):
    return ("CHasPerkExpression", [("Perks To Check For", ("Array", [("Item Count", "1"), ("Perk To Check For", TITLE + p)]))])


def bin_op(cls, items):
    out = items[0]
    for nxt in items[1:]:
        out = (cls, [("Operand1", out), ("Operator", ""), ("Operand2", nxt)])
    return out


def standing(perks):
    return bin_op("CAND", [bin_op("COR", [perk_expr(p) for p in perks]),
                           ("CExpressionNot", [("Operand1", perk_expr("Goblin Traitor"))])])


def canned_file(obj):
    return B("CCannedObject", [("Object", obj), ("Use", "Shared Global Instance")])


# ------------------------------------------------------------- actions
def expr_action(expr):
    return ("CExpressionAction", [("Expression", expr), ("Character to get attributes from", "$Instigator")])


NO_ORDER = ("CAndAction", [("Action", ("Array", [("Item Count", str(len(ORDERS)))] + [
    ("Action", expr_action(("CUseCannedExpressionExpression", [("Canned Expression", "Dialog/Requirements/Faction/" + o)])))
    for o in ORDERS])), ("Early Exit", "0")])


def if_(cond, then, els=""):
    return ("CIfAction", [("If", cond), ("Then", then), ("Else", els), ("Return failure if the If failes", "0")])


def multi(items):
    return ("CMultipleActionsAction", [("Action", ("Array", [("Item Count", str(len(items)))] + [("Action", i) for i in items]))])


def tier(faction, perk):
    return multi([if_(NO_ORDER, ("CAssignFactionToCharacterAction", [("Faction To Assign", "Factions/" + faction),
                                                                      ("Character To assign", "$Instigator")])),
                  ("CGiveCharacterPerkAction", [("Character to give perk to", "$Instigator"), ("Perk to give", TITLE + perk)])])


def lacks(perks):
    return ("CNotAction", [("Action", any_of([has_perk(p) for p in perks]))])


LADDER_BODY = if_(lacks(["Goblin Chum", "Goblin Blooded", "Goblin Champion"]), tier("Goblin Chum", "Goblin Chum"),
                  if_(lacks(["Goblin Blooded", "Goblin Champion"]), tier("Goblin Blooded", "Goblin Blooded"),
                      if_(lacks(["Goblin Champion"]), tier("Goblin Champion", "Goblin Champion"))))
BUTU_BODY = if_(has_perk("Goblin Champion"), tier("Goblin Traitor - Fallen Champion", "Goblin Traitor"),
                if_(any_of([has_perk("Goblin Chum"), has_perk("Goblin Blooded")]), tier("Goblin Traitor - Bad Blood", "Goblin Traitor"),
                    tier("Goblin Traitor - Foe", "Goblin Traitor")))
CHAMPION_BODY = if_(CONDITION, multi([SET_FLAG, tier("Goblin Champion", "Goblin Champion")]),
                    ("CGiveCharacterPerkAction", [("Character to give perk to", "$Instigator"), ("Perk to give", TITLE + "Goblin Champion")]))


# ------------------------------------------------------------- builders
def write(rel, text):
    lhbuild.write_map(rel, text)  # resource_format restores canonical indentation for any resource
    return rel


def gates():
    done = []
    for name, perks in GATES.items():
        rel = REQ + name + ".can"
        if "CHasPerkExpression" not in lhbuild.read(rel):
            done.append(write(rel, canned_file(standing(perks))))
    rel = REQ + "Goblin Horde NOT.can"
    if "CHasPerkExpression" not in lhbuild.read(rel):
        done.append(write(rel, canned_file(("CExpressionNot", [("Operand1", standing(GATES["Goblin Horde IS"]))]))))
    t = lhbuild.read(SLAYER)
    if "Uber Perks/Goblin Rank" in t:
        s = t.index("Operand2=", t.index("Goblin Slayer")) + len("Operand2=")
        e = lhbuild.balanced(t, s)
        assert "Uber Perks/Goblin Rank" in t[s:e]
        done.append(write(SLAYER, t[:s] + B(*standing(GATES["Goblin Horde IS"])).rstrip(CR) + t[e:]))
    return done


def ladder(rel, body):
    """Replace the rank-reading ladder that sits after the import guard's flag in the guard's Then."""
    t = lhbuild.read(rel)
    if "Uber Perks/Goblin Rank" not in t:
        return []
    k = t.index("Fixt Goblin Ladder This Game", t.index("Then=CMultipleActionsAction"))
    s = t.index("Action=CIfAction", k) + len("Action=")
    e = lhbuild.balanced(t, s)
    assert "Uber Perks/Goblin Rank" in t[s:e] and "Uber Perks/Goblin Rank" not in t[e:], rel
    return [write(rel, t[:s] + B(*body).rstrip(CR) + t[e:])]


def champion_can():
    if (lhbuild.FX / CHAMPION).exists():
        return []
    return [write(CHAMPION, canned_file(CHAMPION_BODY))]


def khan():
    p = lhbuild.FX / KHAN
    t = lhbuild.read(KHAN)
    perk = ("Action=CGiveCharacterPerkAction" + CR + "{" + CR + "Character to give perk to=$Instigator" + CR +
            "Perk to give=" + TITLE + "Goblin Champion" + CR + "}" + CR)
    if t.count(perk) == 0:
        return []
    assert t.count(perk) == 3, "%s: expected vanilla's three Champion grants" % KHAN
    while perk in t:
        i = t.index(perk)
        a = t.rindex("Custom Action=CMultipleActionsAction" + CR, 0, i)
        e = lhbuild.balanced(t, a)
        blk = t[a:e]
        old_can = "Canned Object=Levels/Wilderness/Quests/Advance Goblin Rank" + CR
        assert blk.count(old_can) == 1 and blk.count(perk) == 1, KHAN
        n = int(blk.split("Item Count=", 1)[1].split(CR, 1)[0])
        blk = blk.replace(perk, "").replace(old_can, "Canned Object=Levels/Wilderness/Quests/Name Goblin Champion" + CR)
        blk = blk.replace("Item Count=%d" % n + CR, "Item Count=%d" % (n - 1) + CR, 1)
        t = t[:a] + blk + t[e:]
    p.write_bytes(t.encode("latin-1"))
    return [KHAN]


def warrens():
    t = lhbuild.read(WARRENS)
    i = t.index("Node ID=06 The Champion Returns")
    s = t.rindex("If=CAndAction", 0, i)
    k = t.index("Action=CExpressionAction", s) + len("Action=")
    e = lhbuild.balanced(t, k)
    if "Uber Perks/Goblin Rank" not in t[k:e]:
        return []
    assert e < i and "Constant Value=2" in t[k:e]
    new = expr_action(("CUseCannedExpressionExpression", [("Canned Expression", "Dialog/Requirements/Faction/Goblin Horde Highlevel")]))
    lhbuild.write_map(WARRENS, t[:k] + B(*new).rstrip(CR) + t[e:])
    return [WARRENS]


def main():
    done = gates() + ladder(LADDER, LADDER_BODY) + ladder(BUTU, BUTU_BODY) + champion_can() + khan() + warrens()
    if done:
        register(done)
    print("goblin standing by title:", len(done), "files")
    for d in done:
        print("  ", d)


if __name__ == "__main__":
    main()
