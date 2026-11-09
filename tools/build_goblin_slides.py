"""Two slides for any faction: what you did to the goblins, and what you did for them.

The Horde slides are for members, so a character who fought the goblins heard nothing at the end.

    The Khan, or the count    Khan slain, or Goblin Slayer, each with Butu's line if you touched it
    The dirty work            the woodcutter's eyes for Rakeb, Esteban for the patrol, or both

Everything reads from quest history and the perk except the Khan's death by anyone but Torquemada's
order. **The flag is in the generator and not in the can**, because `Goblin Khan Generator` sets a
destroyed script of its own and that replaces the can's, which is how the Lava Troll Hide stayed dead for
twenty releases. $Instigator in a death script is the corpse, so it goes through a for-each.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_goblin_slides.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, if_action, multi, relay
from build_inquisition_slides import ENDGAME, SLIDES, TITLES, VARS, flag, say, var_if, write_var

WARRENS = "Levels/Wilderness Maps/Goblin Warrens.zax"
KHAN = VARS + "Fixt Khan Slain"
SLAY = "Levels/1 Barcelona/Quests/Temple District/Slay the Goblin Khan"
POEMS = "Levels/Wilderness/Quests/Butu Khan's Poems"
HEIR = "Levels/Wilderness/Quests/The Goblin of Butu's Line"
EYES = "Levels/Wilderness/Quests/Bring the Woodcutter's Eyes to the Goblin Shaman"
ESTEBAN = "Levels/Wilderness/Quests/Kill Guard Esteban for the Goblin Patrol"
SPELLING = ["Resources/Levels/Wilderness/Dialog/GoblinKhan.DialogTree",
            "Resources/Levels/Wilderness/Dialog/Fixt Butu Heir.DialogTree",
            "Resources/Levels/Wilderness/Quests/Butu Khan's Poems.Quest.txt",
            "Resources/Levels/Wilderness/Quests/The Goblin of Butu's Line.Quest.txt"]

SLAIN = ("Plumdjum Khan had drawn plans for six winters when you killed him. He had called you morsel. The Horde was "
         "left with a cave full of shiny and a pile of maps nobody else could read. The tribes fought over the shiny "
         "and burned the maps for heat. The war he had planned came three generations late, and it was not the one "
         "he drew.")
COUNT = ("You killed goblins in such numbers that the tribes stopped counting you as a westerner and started counting "
         "you as weather. The Khan had a word for you. Mothers in Khara'Khorum used it at bedtime. The gates of "
         "Barcelona stayed quieter for it, and nobody there ever learned why.")
READ = ("You settled Butu Khan's poems with his line, and Hrargrub's goblins let you walk the east cave, and "
        "goblins who had never heard a verse sat down to listen.")
KILLED = ("You killed Hrargrub for the Khan, and Butu's line ended a second time. The Khan did not ask what he was "
          "called. Nobody else ever did.")
WOOD = ("You cut out the woodcutter's eyes and his liver for Rakeb. He had said they were beautiful. Nobody came looking. "
        "A woodcutter deep in a forest is not missed until someone needs firewood.")
ROAD = ("You killed Guard Esteban for the goblin patrol, and the road at the Crossroads belonged to the Horde. He had "
        "been paying travellers to thin them out. Soon nobody was paying. Then nobody was travelling.")

TEXT = {
    "900 order goblins khan": SLAIN,
    "900 order goblins khan poems": SLAIN + " " + READ,
    "900 order goblins khan heir": KILLED + " " + SLAIN,
    "900 order goblins count": COUNT,
    "900 order goblins count poems": COUNT + " " + READ,
    "900 order goblins count heir": COUNT + " " + KILLED,
    "900 order goblins poems": READ,
    "900 order goblins heir": KILLED,
    "900 order goblins eyes": WOOD,
    "900 order goblins esteban": ROAD,
    "900 order goblins eyes esteban": WOOD + " " + ROAD,
}


def slides():
    z = lhbuild.read(SLIDES)
    if "900 order goblins khan" in z:
        return
    add = ""
    for nid, text in TEXT.items():
        add += ("Node ID=" + nid + CR + "Text=" + text + CR + "Should Have Voiceover=1" + CR + CR +
                "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR +
                "Custom Action=" + B(*relay("Fixt order epilogue relay")) + "Is Default Reply=1" + CR + "-" * 60 + CR)
    key = "Node ID=900 order none" + CR
    assert z.count(key) == 1
    z = z.replace(key, add + key)
    assert z.count(CR) == z.count("\n")
    (FX / SLIDES).write_bytes(z.encode("latin-1"))


def state(quest, sid, then, els):
    return if_action(("CWasQuestStateActivatedAction", [("Quest", quest), ("State", sid)]), then, els)


def butu(prefix, skip):
    name = "900 order goblins" + (" " + prefix if prefix else "")
    plain = say(name) if prefix else skip
    return state(POEMS, "BTU8M3XV", say(name + " poems"), state(HEIR, "BTU2W6RJ", say(name + " heir"), plain))


def endgame():
    z = lhbuild.read(ENDGAME)
    if "900 order goblins khan" in z:
        return
    skip = relay("Fixt order epilogue relay")
    khan = butu("khan", skip)
    slayer = ("CIfExpressionAction", [
        ("If Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [
            ("Item Count", "1"), ("Perk To Check For", TITLES + "Goblin Slayer")]))])),
        ("Character to get attributes from", "Player1"), ("Then", butu("count", skip)), ("Else", butu("", skip))])
    fate = var_if(KHAN, khan, state(SLAY, "62VPSJUB", khan, slayer))
    errands = state(EYES, "3EUUJA40", state(ESTEBAN, "M3PZ9DLT", say("900 order goblins eyes esteban"), say("900 order goblins eyes")),
                    state(ESTEBAN, "M3PZ9DLT", say("900 order goblins esteban"), skip))
    k = z.index("Node ID=900 order savage heart betrayed")
    s = z.rindex("\t" * 7 + "Action=CIfAction", 0, k) + 7
    e = balanced(z, s)
    assert "900 order savage heart" in z[s:e]
    z = z[:e] + CR + "Action=" + B(*fate) + "Action=" + B(*errands).rstrip(CR) + z[e:]
    a = z.index("\t\t\tName=Fixt order epilogue relay" + CR)
    i = z.index("Item Count=29" + CR, a)
    assert i - a < 900
    z = z[:i] + "Item Count=31" + z[i + len("Item Count=29"):]
    lhbuild.write_map(ENDGAME, z)


def warrens():
    z = lhbuild.read(WARRENS)
    if "Fixt Khan Slain" in z:
        return
    a = z.index("\t\t\tName=Goblin Khan Generator" + CR)
    s = z.index("New Destroyed Action=CMultipleActionsAction", a)
    i = z.index("Item Count=6" + CR, s)
    assert i - s < 120
    new = B("CForEachPlayerAction", [("Action", flag(KHAN))])
    z = z[:i] + "Item Count=7" + CR + "Action=" + new + z[i + len("Item Count=6" + CR):]
    lhbuild.write_map(WARRENS, z)


def spelling():
    for rel in SPELLING:
        z = lhbuild.read(rel)
        if "Plumjum" in z:
            (FX / rel).write_bytes(z.replace("Plumjum", "Plumdjum").encode("latin-1"))


def main():
    write_var(KHAN, "Fixt Khan Slain", "1 means Plumdjum Khan is dead, whoever sent the player.")
    slides()
    endgame()
    warrens()
    spelling()


if __name__ == "__main__":
    main()
