"""0.95.0: Torquemada can die, once Montserrat has made him expendable.

Run after `build_inquisitor_speech.py`, whose `120 combat` node this rewires.

He is AC 1000 / HP 10000, `Spell Immunity`, nine resistances at 100, and his chambers answer every
attack with jail, so raising his hit points would have changed nothing. The chambers' RESET relay runs
on every spawn point and is the one switch: once `Travel to Montaillou` has ever been activated it
clones a second generator holding a mortal copy, with none of the jail hooks.

    Before Montserrat   the speech, then jail. The cell line is skipped, it undercut the threat.
    After Montserrat    the speech, then the fight, guards included.
    In the cathedral    neither part exists, so the reply falls back to vanilla's combat message.

The titles are the record of his death. They are perks, so they reach the end slides from any act.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_torquemada.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, activate, balanced, deactivate, delay, exists, if_action, multi, relay

CHAMBERS = "Levels/1 Barcelona/Inquisition Chambers2.zax"
ENDGAME = "Levels/8 Alamut/END GAME Siege Map.zax"
TREE = "Resources/Levels/1 Barcelona/Dialog/Temple District/GrandInquisitor.DialogTree"
SLIDES = "Resources/Levels/8 Alamut/Dialog/Fixt Ending Slides.DialogTree"
TEMPLATES = "Levels/1 Barcelona/Character Templates/Temple District/"
CAN = "Resources/" + TEMPLATES + "Grand Inquisitor.can"
MORTAL_CAN = "Resources/" + TEMPLATES + "Grand Inquisitor Mortal.can"
RACE = "Resources/Races/NPCs/Grand Inquisitor.Race"
MORTAL_RACE = "Resources/Races/NPCs/Grand Inquisitor Mortal.Race"
TITLES = "Perks/!Event Title Perks/"
DARK = TITLES + "Dark Inquisitor"
BREAKER = TITLES + "Breaker of the Hammer"
KILLER = TITLES + "FACTION Inquisitor Killer"

MORTAL = "Fixt Torquemada is mortal"
DEAD = "Fixt Torquemada is dead"
FIGHT = "Fixt Torquemada fight"
GUARD = "Fixt Torquemada guard"
JAIL = "Grand Inquisitor Sends you to jail"
OLD_MAN_POLY = "Trigger cutscene with Old Man Poly"
SLIDE_TREE = "Levels/8 Alamut/Dialog/Fixt Ending Slides"
TEXT_DARK = ('The Inquisition entered the siege without a head. It came out with several. Torquemada died in '
             'his own chambers, and the Holy Office recorded it as a fever. The truth was worse: the hand '
             'that killed him still wore the mark. The cult on the plains had wanted this for years. You did '
             'it in an afternoon. His successors agreed on nothing, and the fires burned low. Within ten '
             'years, some cities stopped paying for the wood. No one ever named you. But the archive keeps a '
             'box with nothing written on it, and its keepers lower their voices.')
TEXT_BREAKER = ('The Inquisition entered the siege without a head. Barcelona would not rebuild under men who '
                'could not say who led them. Torquemada died in his own chambers, at the hand of someone who '
                'owed the Holy Office nothing. You walked out past what was left of his guards. His successors '
                'fought over his chair for years. The fires did not go out, but they burned low. Within ten '
                'years, some cities stopped paying for the wood. No one in those cities knew your name. The Holy '
                'Office did. It kept the page open.')


def write_tree(rel, text):
    assert text.count(CR) == text.count("\n"), rel + " lost its CRLF"
    (FX / rel).write_bytes(text.encode("latin-1"))


def write_raw(rel, text):
    (FX / rel).parent.mkdir(parents=True, exist_ok=True)
    (FX / rel).write_bytes(text.encode("latin-1"))


def swap(z, old, new, count=1):
    assert z.count(old) == count, (old[:70], z.count(old))
    return z.replace(old, new)


def perk_if(perk, then, els, who="Player1"):
    return ("CIfExpressionAction", [
        ("If Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [
            ("Item Count", "1"), ("Perk To Check For", perk)]))])),
        ("Character to get attributes from", who), ("Then", then), ("Else", els)])


def give(perk):
    return ("CGiveCharacterPerkAction", [("Character to give perk to", "$Instigator"), ("Perk to give", perk)])


def clone(source, used, facing="0.785398"):
    return multi([
        delay(0, ("CCloneAction", [("New Location", source), ("Copy Height", "0"), ("Random Location Delta", "0"),
                                   ("Warp Behavior", ""), ("Source Name", source), ("New Name", used),
                                   ("Set Facing Angle", "0"), ("New Facing Angle", facing)])),
        ("CDeleteAction", [("Target Name", used)])])


def to_combat(name):
    return multi([("CAddCategoryAction", [("Target Name", name), ("Categories to add", "Enemy")]),
                  ("CSetTargetTypeAction", [("Entity Name", name), ("Name To Target", ""),
                                            ("Valid Targets", "Player,Player Friend")]),
                  ("CGoToCombatAction", [("Enemy Name", name)])])


# ---- the mortal race and can ------------------------------------------------------------------

def mortal_race():
    r = lhbuild.read(RACE)
    r, n = re.subn(r"(\(AC\) Armor Class\s+Value To Preset=)1000", r"\g<1>225", r)
    assert n == 1
    r, n = re.subn(r"(\(HP\) Hit Points\s+Value To Preset=)10000", r"\g<1>260", r)
    assert n == 1
    # Elemental at the 50 every Inquisitor carries, the rest at 25. At 100 nothing could hurt him.
    r, n = re.subn(r"((?:Fire|Cold|Electrical) Damage Resistance\s+Value To Preset=)100", r"\g<1>50", r)
    assert n == 3, n
    r, n = re.subn(r"( Damage Resistance\s+Value To Preset=)100", r"\g<1>25", r)
    assert n >= 1
    assert "Value To Preset=100\r" not in r
    write_raw(MORTAL_RACE, r)


def mortal_can():
    z = lhbuild.read(CAN)
    z = swap(z, "Race=Races/NPCs/Grand Inquisitor" + CR, "Race=Races/NPCs/Grand Inquisitor Mortal" + CR)
    z = swap(z, "\t\tCategory=Spell Immunity" + CR, "\t\tCategory=" + CR)
    s = z.index("Destroyed Script Action=")
    e = balanced(z, s)
    was = z[s + len("Destroyed Script Action="):e]
    assert was.startswith("CConditionalAction") and "FACTION Inquisitor Killer" in was
    # $Instigator is the corpse in a death script, so everything for the player sits in a for-each.
    title = ("CIfExpressionAction", [
        ("If Expression", ("CUseCannedExpressionExpression", [("Canned Expression", "Dialog/Requirements/Faction/Inquisitor IS")])),
        ("Character to get attributes from", "$Instigator"), ("Then", give(DARK)), ("Else", give(BREAKER))])
    death = multi([
        ("CForEachPlayerAction", [("Action", multi([was, title]))]),
        ("CSetQuestSatusToFailedIfActiveAction", [("Quest", "Levels/1 Barcelona/Quests/Temple District/Inquisition Initiation Quests/Create a Rod of the Inquisitor")]),
        ("CSetQuestSatusToFailedIfActiveAction", [("Quest", "Levels/1 Barcelona/Quests/Temple District/Slay the Goblin Khan")]),
        activate(DEAD), deactivate(MORTAL), deactivate(OLD_MAN_POLY)])
    z = z[:s] + "Destroyed Script Action=" + B(*death) + z[e + len(CR):]
    lhbuild.write_map(MORTAL_CAN, z)


# ---- the chambers -----------------------------------------------------------------------------

def part_span(z, name):
    i = z.index("\t\t\tName=" + name + CR)
    s = z.rindex("\t\tLevel Part=", 0, i)
    e = z.index(CR + "\t\t}" + CR, i) + len(CR + "\t\t}" + CR)
    return s, e


def chambers():
    z = lhbuild.read(CHAMBERS)
    if MORTAL in z:
        return z
    # the mortal generator is his own, less everything that turned an attack into jail
    s, e = part_span(z, "Grand Inquisitor generator")
    gen = z[s:e]
    a = gen.index("After Action=CMultipleActionsAction")
    b = gen.index("New Facing Angle=1.48353")
    after = multi([
        ("CSetDamagedScriptActionAction", [("New Damaged Action", relay(FIGHT)), ("Target Name", "$Instigator")]),
        ("CAddAIAction", [("Target Name", "$Instigator"),
                          ("AI", ("CHandleMessageAI", [("Marked For Deletion", "0"), ("Publisher", ""),
                                                       ("Message To Handle", "GoToCombat"), ("Action", relay(FIGHT))])),
                          ("Delay Between Adds", "0")]),
        ("CAddCategoryAction", [("Target Name", "$Instigator"), ("Categories to add", "NonInteractiveSequence Actor")])])
    mortal_gen = gen[:a] + "After Action=" + B(*after) + gen[b:]
    mortal_gen = swap(mortal_gen, "\t\t\tName=Grand Inquisitor generator" + CR, "\t\t\tName=Fixt Mortal Inquisitor generator" + CR)
    mortal_gen = swap(mortal_gen, "Entity=" + TEMPLATES + "Grand Inquisitor" + CR, "Entity=" + TEMPLATES + "Grand Inquisitor Mortal" + CR)

    # every spawn point and the secret door already run this relay
    s, e = part_span(z, "RESET MAP for Invulnerable Grand Inquisitor")
    reset = z[s:e]
    a = reset.index("Action=CMultipleActionsAction")
    b = balanced(reset, a)
    old = reset[a + len("Action="):b]
    assert old.count("Target Name=" + JAIL) == 1 and old.count("Source Name=Grand Inquisitor generator") == 1
    pick = if_action(exists(DEAD), "", if_action(
        ("CWasQuestEverActivatedAction", [("Quest", "Levels/2 Montserrat/Quests/Travel to Montaillou and find Brother Michel")]),
        multi([activate(MORTAL), clone("Fixt Mortal Inquisitor generator", "Used Fixt Mortal Inquisitor Generator")]),
        multi([deactivate(MORTAL), clone("Grand Inquisitor generator", "Used Grand Inquisitor Generator")])))
    new = multi([activate(JAIL), activate(FIGHT), ("CDeleteAction", [("Target Name", "Grand Inquisitor")]),
                 ("CDeleteAction", [("Target Name", GUARD)]), pick])
    z = z[:s] + reset[:a] + "Action=" + B(*new).rstrip(CR) + reset[b:] + z[e:]

    fight = multi([
        # the chase poly fires on enemies and may be armed already, and his guards would trip it
        deactivate(FIGHT), deactivate(OLD_MAN_POLY), deactivate("Guard chasing player"),
        ("CRemoveAIAction", [("Target Name", "Grand Inquisitor"), ("AI", "CAIInteractionSpecifier"), ("Delay Between Removes", "0")]),
        to_combat("Grand Inquisitor"),
        clone("Fixt Torquemada guard generator 1", "Used Fixt Torquemada guard generator", "3.14159"),
        clone("Fixt Torquemada guard generator 2", "Used Fixt Torquemada guard generator", "3.14159")])
    guard_after = multi([("CAddCategoryAction", [("Target Name", "$Instigator"), ("Categories to add", "Enemy")]),
                         ("CSetTargetTypeAction", [("Entity Name", "$Instigator"), ("Name To Target", ""),
                                                   ("Valid Targets", "Player,Player Friend")]),
                         ("CGoToCombatAction", [("Enemy Name", "$Instigator")])])
    guard_can = TEMPLATES + "Inquisition Guard Generic"
    z = lhbuild.add_parts(z, [
        lhbuild.checker(MORTAL, 3395, 575), lhbuild.checker(DEAD, 3395, 590),
        lhbuild.relay_part(FIGHT, fight, 3395, 605, once="0"),
        lhbuild.generator("Fixt Torquemada guard generator 1", "0", guard_can, GUARD, guard_after, 3575, 603),
        lhbuild.generator("Fixt Torquemada guard generator 2", "0", guard_can, GUARD, guard_after, 3527, 583),
        mortal_gen.lstrip("\t")])
    return z


# ---- the conversation -------------------------------------------------------------------------

def conversation(z):
    if FIGHT in z:
        return z
    fallback = if_action(exists(JAIL), relay(JAIL), ("CGoToCombatAction", [("Enemy Name", "Grand Inquisitor")]))
    z = swap(z, "Death is the only penance for your crimes, heathen." + CR + "Should Have Voiceover=1" + CR + CR +
             "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR +
             "Custom Action=CGoToCombatAction" + CR + "{" + CR + "Enemy Name=Grand Inquisitor" + CR + "}" + CR,
             "Death is the only penance for your crimes, heathen." + CR + "Should Have Voiceover=1" + CR + CR +
             "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR +
             "Custom Action=" + B(*if_action(exists(MORTAL), relay(FIGHT), fallback)))
    challenge = ("Requirement=!None" + CR + "Custom Requirement=" + B("CActionExpression", [("Action", exists(MORTAL))]) +
                 "Reply Text=I have come to end you, Torquemada. Spain has burned enough." + CR +
                 "Go to node ID=120 combat" + CR + "Icon=Fight Icon" + CR + CR)
    for node in ["1 Conversation Start", "2 Irritated Return Dialogue", "3 Return Dialogue", "5 Favored Return"]:
        i = z.index("Node ID=" + node + CR)
        j = z.index("Should Have Voiceover=1" + CR + CR, i) + len("Should Have Voiceover=1" + CR + CR)
        assert z[j:].startswith("Requirement=") and j - i < 400
        z = z[:j] + challenge + z[j:]
    return z


# ---- the titles -------------------------------------------------------------------------------

def title(name, display, description):
    z = lhbuild.read("Resources/" + KILLER + ".Perk")
    z = swap(z, "Display Name=Enemy of the Inquisition", "Display Name=" + display)
    z = swap(z, "Description=TITLE PERK: You have slain an agent of the Inquisition.", "Description=TITLE PERK: " + description)
    write_raw("Resources/" + name + ".Perk", z)


# ---- the end slides ---------------------------------------------------------------------------

def slides(z):
    if "900 order inquisition dark" in z:
        return z
    i = z.index("Node ID=900 order inquisition" + CR)
    e = z.index("-" * 20, i)
    node = z[i:e]
    node = node[:node.index("Text=")] + "@" + node[node.index("Should Have Voiceover="):]
    add = ""
    for nid, text in (("900 order inquisition dark", TEXT_DARK), ("900 order inquisition broken", TEXT_BREAKER)):
        add += node.replace("Node ID=900 order inquisition" + CR, "Node ID=" + nid + CR).replace("@", "Text=" + text + CR) + "-" * 60 + CR
    return z[:i] + add + z[i:]


def endgame():
    z = lhbuild.read(ENDGAME)
    if "900 order inquisition dark" in z:
        return z
    say = lambda n: ("CDisplayDialogTreeAction", [("Dialog Tree File", SLIDE_TREE), ("Node ID", n),
                                                  ("Speaker", "Fake Talker for NIS"), ("Player Being Spoken To", "Player1")])
    k = z.index("Node ID=900 order inquisition exposer")
    s = z.rindex("Action=CIfExpressionAction", 0, k)
    e = balanced(z, s)
    inner = z[s + len("Action="):e]
    assert "900 order inquisition killer" in inner and "Fixt order epilogue relay" in inner
    wrap = perk_if(DARK, say("900 order inquisition dark"), perk_if(BREAKER, say("900 order inquisition broken"), inner))
    z = z[:s] + "Action=" + B(*wrap) + z[e + len(CR):]
    # a slide that can fire on a perk alone has to be excluded from the no-allegiance slide
    k = z.index("Node ID=900 order none")
    s = z.rindex("Else=CDisplayDialogTreeAction", 0, k)
    e = balanced(z, s)
    inner = z[s + len("Else="):e]
    wrap = perk_if(BREAKER, relay("Fixt order epilogue relay"), inner)
    return z[:s] + "Else=" + B(*wrap) + z[e + len(CR):]


def main():
    assert "Node ID=120 combat" + CR in lhbuild.read(TREE), "run build_inquisitor_speech.py first"
    if not (FX / MORTAL_RACE).exists():
        mortal_race()
    if not (FX / MORTAL_CAN).exists():
        mortal_can()
    title(DARK, "Dark Inquisitor", "You wore the mark of the Holy Office and killed Torquemada in his own chambers. "
                                   "The Inquisition calls it a fever. The cult on the plains would call it a beginning.")
    title(BREAKER, "Breaker of the Hammer", "You killed Tomas de Torquemada, the blessed hammer of heretics, in his own chambers, "
                                            "and walked out past his guards.")
    lhbuild.write_map(CHAMBERS, chambers())
    write_tree(TREE, conversation(lhbuild.read(TREE)))
    write_tree(SLIDES, slides(lhbuild.read(SLIDES)))
    lhbuild.write_map(ENDGAME, endgame())


if __name__ == "__main__":
    main()
