"""The Inquisition slides in the game's rhythm, and a slide for what you did about the Dark Inquisitors.

Run after `build_torquemada.py`. Vanilla dialogue averages 10.2 words a sentence and the slides, pitched
at New Vegas in 0.71.0, averaged 21.4. The four rewrites keep every particular and change the rhythm.

The cult slide follows the Inquisition's own, for anyone who dealt with them, whatever their faction.

    destroyed, Torquemada dead       ended dead      he and the cult went to the same hand
    destroyed, Torquemada told       ended told      `It will not be written down`, and it was not
    destroyed                        ended
    you killed Diego for them        served
    the same, Torquemada dead        inherited       the job they wanted most

Destroyed outranks served: taking their money and then killing them leaves no cult to prosper. It reads a
new variable written by the relay all five report to, or state `E711FKUT`, so a character who finished
the quest before this variable existed still counts. A character who did none of this sees no slide.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_inquisition_slides.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, if_action, multi, relay

SLIDES = "Resources/Levels/8 Alamut/Dialog/Fixt Ending Slides.DialogTree"
ENDGAME = "Levels/8 Alamut/END GAME Siege Map.zax"
PLAINS = "Levels/Wilderness Maps/Plains.zax"
TREE = "Resources/Levels/1 Barcelona/Dialog/Temple District/GrandInquisitor.DialogTree"
VARS = "Derived Character Attributes/Game Scripting Variables/"
DESTROYED = VARS + "Fixt Dark Inquisitors Destroyed"
TOLD = VARS + "Fixt Told Torquemada of the Cult"
SLIDE_TREE = "Levels/8 Alamut/Dialog/Fixt Ending Slides"
TITLES = "Perks/!Event Title Perks/"

REWRITES = {
    "900 order inquisition exposer": (
        "The Inquisition came out of the siege with its command intact, and the city handed it the rebuilding. "
        "Part of that standing was your doing. You told them where La Calle Perdida was, and your directions "
        "were good, because you had been inside it as a friend. The Holy Office took the quarter apart in nine "
        "days. It spent thirty years cataloguing what it found. The men who did the work were promoted on your "
        "word. The pyres were lit in the plaza where the markets had been, and the cities paid for the wood."),
    "900 order inquisition killer": (
        "The Inquisition came out of the siege with its command intact, and the city handed it the rebuilding. "
        "You had worn its mark and you had killed its own. The Holy Office keeps careful records of a name "
        "entered twice. Its fires burned on through the peace as they had through the war, because a frightened "
        "city asks its inquisitors for more work, not less. The cities paid for the wood. Nothing was ever "
        "charged against you. But there were four towns between Barcelona and the coast that you never entered "
        "again, and you knew all four names."),
    "900 order inquisition high": (
        "The Inquisition came out of the siege with its command intact, and the city handed it the rebuilding. "
        "You had risen high in the Holy Office, high enough that the work reached you as paper. You signed what "
        "other men carried out. Its fires burned on through the peace as they had through the war, because a "
        "frightened city asks its inquisitors for more work, not less. The cities paid for the wood. Your "
        "signature was on enough of it that the archive gave you a box of your own."),
    "900 order inquisition": (
        "The Inquisition came out of the siege with its command intact, and the city handed it the rebuilding. "
        "You had worn its mark and done its work. For a few years the mark was worth more than the work had "
        "been. It opened doors in the new Barcelona. Then it went on opening doors you no longer wanted to walk "
        "through. Its fires burned on through the peace as they had through the war, and the cities paid for "
        "the wood. You stopped wearing the mark in the third year. Nobody ever asked you why."),
}

CULT = {
    "900 order cult ended": (
        "The Dark Inquisitors did not survive you. You found them on the northern plains and you ended what they "
        "were doing there. Their habits were burned where they lay. The shepherds brought their flocks back "
        "within the year. Nobody in Barcelona asked what had happened, because nobody in Barcelona wanted the "
        "answer. The Holy Office went on saying that such men had never been its own. You knew better. You had "
        "seen the habits."),
    "900 order cult told": (
        "The Dark Inquisitors did not survive you. You found them on the northern plains, you ended them, and "
        "you told Torquemada to his face. He paid you and he kept his word. It was never written down. The Holy "
        "Office holds no record of the cult, or the habits, or the men who wore them. Within a generation you "
        "were the last who knew. He had called it rot from inside the house. The house stayed standing, and "
        "nobody ever looked for the rest."),
    "900 order cult ended dead": (
        "You ended the Dark Inquisitors on the plains, and you ended Torquemada in his own chambers. The Holy "
        "Office lost its heretics and its head to the same hand. It could not praise you for the first without "
        "naming you for the second. So it did neither. Both entries were struck from the record. In the archive, "
        "the two pages sit side by side with nothing written on them."),
    "900 order cult served": (
        "The Dark Inquisitors paid what they promised. Bishop Diego was dead on the south road, and nobody was "
        "left to write letters about them. They grew. Their habits spread from the northern plains to the hill "
        "towns, and then to parishes that had never heard the name. Within ten years it was hard to say where "
        "the cult stopped and the Holy Office began. Some of them knew your name. They said it the way the "
        "faithful say a saint's."),
    "900 order cult inherited": (
        "The Dark Inquisitors paid you for Bishop Diego. Nobody paid you for Torquemada, though it was the job "
        "they wanted most. The Holy Office was still fighting over his chair when they came down from the "
        "plains, in good habits, with good letters. There was no honest bishop left to read them. Within a "
        "generation the chair was theirs, and few could have said when it changed. The fires had burned low. "
        "They burned again, and no city was asked to pay for the wood."),
}


def flag(path):
    return ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", ""), ("Modification is permanent", "0"), ("Character to modify", "$Instigator"),
        ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", ("CConstant", [("Constant Value", "1")])),
            ("Modification amount is a percent", "0"), ("Allow Accumulation", "0"),
            ("Derived character attribute to modify", path)]))])),
        ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])


def write_var(path, short, description):
    z = lhbuild.read("Resources/" + VARS + "Fixt Cathedral Summit Done.DerivedCharacterAttribute")
    z = z.replace("Fixt Cathedral Summit Done", short)
    z = z.replace("0 means the Cathedral summit with Lord Javier has not run yet.", description)
    p = FX / ("Resources/" + path + ".DerivedCharacterAttribute")
    p.write_bytes(z.encode("latin-1"))


def say(node):
    return ("CDisplayDialogTreeAction", [("Dialog Tree File", SLIDE_TREE), ("Node ID", node),
                                         ("Speaker", "Fake Talker for NIS"), ("Player Being Spoken To", "Player1")])


def perk_if(perk, then, els):
    return ("CIfExpressionAction", [
        ("If Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [
            ("Item Count", "1"), ("Perk To Check For", TITLES + perk)]))])),
        ("Character to get attributes from", "Player1"), ("Then", then), ("Else", els)])


def var_if(path, then, els):
    return ("CIfExpressionAction", [
        ("If Expression", ("CIsGreaterThan", [
            ("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", path)])),
            ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "0")]))])),
        ("Character to get attributes from", "Player1"), ("Then", then), ("Else", els)])


def state_if(quest, state, then, els):
    return if_action(("CWasQuestStateActivatedAction", [("Quest", quest), ("State", state)]), then, els)


def dead_if(then, els):
    return perk_if("Dark Inquisitor", then, perk_if("Breaker of the Hammer", then, els))


def slides():
    z = lhbuild.read(SLIDES)
    if "900 order cult ended" in z:
        return
    for nid, text in REWRITES.items():
        z, n = re.subn(r"(Node ID=" + nid + r"\r\nText=)[^\r\n]*", lambda m: m.group(1) + text, z)
        assert n == 1, nid
    add = ""
    for nid, text in CULT.items():
        add += ("Node ID=" + nid + CR + "Text=" + text + CR + "Should Have Voiceover=1" + CR + CR +
                "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR +
                "Custom Action=" + B(*relay("Fixt order epilogue relay")) + "Is Default Reply=1" + CR + "-" * 60 + CR)
    key = "Node ID=900 order saladin killer" + CR
    assert z.count(key) == 1
    z = z.replace(key, add + key)
    assert z.count(CR) == z.count("\n")
    (FX / SLIDES).write_bytes(z.encode("latin-1"))


def endgame():
    z = lhbuild.read(ENDGAME)
    if "900 order cult ended" in z:
        return
    ended = dead_if(say("900 order cult ended dead"), var_if(TOLD, say("900 order cult told"), say("900 order cult ended")))
    served = state_if("Levels/Wilderness/Quests/Eliminate Bishop Diego", "AS4T5BB5",
                      dead_if(say("900 order cult inherited"), say("900 order cult served")),
                      relay("Fixt order epilogue relay"))
    cult = var_if(DESTROYED, ended, state_if("Levels/Wilderness/Quests/Bring the Rogue Inquisitors to Justice", "E711FKUT", ended, served))
    k = z.index("Node ID=900 order inquisition dark")
    s = z.rindex("Action=CIfExpressionAction", 0, k)
    e = balanced(z, s)
    z = z[:e] + CR + "Action=" + B(*cult).rstrip(CR) + z[e:]
    a = z.index("\t\t\tName=Fixt order epilogue relay" + CR)
    i = z.index("Item Count=25" + CR, a)
    assert i - a < 900, i - a
    z = z[:i] + "Item Count=26" + z[i + len("Item Count=25"):]
    lhbuild.write_map(ENDGAME, z)


def plains():
    z = lhbuild.read(PLAINS)
    if "Fixt Dark Inquisitors Destroyed" in z:
        return
    a = z.index("\t\t\tName=Killed all of the Rogue Inquisitors" + CR)
    i = z.index("Quest=Levels/Wilderness/Quests/Bring the Rogue Inquisitors to Justice", a)
    s = z.rindex("Action=CIfAction", 0, i)
    e = balanced(z, s)
    assert z[a:s].count("Action=" + CR) == 3
    inner = z[s + len("Action="):e]
    # the fifth death of the five. A relay's $Instigator is not the player, so this goes through a for-each.
    new = multi([("CForEachPlayerAction", [("Action", flag(DESTROYED))]), inner])
    z = z[:s] + "Action=" + B(*new) + z[e + len(CR):]
    lhbuild.write_map(PLAINS, z)


def tree():
    z = lhbuild.read(TREE)
    if "Fixt Told Torquemada of the Cult" in z:
        return
    i = z.index("Node ID=413 rogue inquisitors" + CR)
    j = z.index("Item Count=3" + CR, i)
    assert j - i < 800
    z = z[:j] + "Item Count=4" + CR + "Action=" + B(*flag(TOLD)) + z[j + len("Item Count=3" + CR):]
    assert z.count(CR) == z.count("\n")
    (FX / TREE).write_bytes(z.encode("latin-1"))


def main():
    write_var(DESTROYED, "Fixt Dark Inquisitors Destroyed", "1 means all five Dark Inquisitors on the plains are dead.")
    write_var(TOLD, "Fixt Told Torquemada of the Cult", "1 means the player reported the Dark Inquisitors to Torquemada.")
    slides()
    endgame()
    plains()
    tree()


if __name__ == "__main__":
    main()
