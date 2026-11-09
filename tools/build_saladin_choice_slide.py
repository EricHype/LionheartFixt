"""A slide after the Saladin one, for the two forks every Knight of Saladin goes through.

Amir's second task is one-shot, the Shard of Dreams or a Sacred Scimitar, and Kabool then tests you by
intellect or by strength. The Saladin slides read neither. All four outcomes come from perks and quest
history, so they work on any save. Only the unasked Shard needs a variable, because that scene leaves no
quest behind it, and it is written from `216 the shard unasked`, whose one reply both entries reach.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_saladin_choice_slide.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, if_action, relay
from build_inquisition_slides import ENDGAME, SLIDES, VARS, flag, say, var_if, write_var

JAFAR = "Resources/Levels/1 Barcelona/Dialog/Gate District/Jafar.DialogTree"
UNASKED = VARS + "Fixt Shard Returned Unasked"
QUESTS = "Levels/1 Barcelona/Quests/Gate District/Knights Saladin Initiation/"
PERKS = "Perks/!NPC or Event Given Perks/"

BROUGHT = "You brought the Shard of Dreams out of the slavers' lair and put it in Amir's hands. "
FORGED = "Amir offered you a choice of tasks, and you took the sword. Eduardo forged it, you carried it back, and Amir handed it to you again. "
OFFER = "Then Kabool offered you the blade or your wits, and you "
ANYWAY = " You brought Amir the Shard anyway, and he paid you for it, because the order does not take a sacred thing as a gift."
WITS = ("chose your wits, with the blade at your side the whole time. He named you Scholar of the Crescent. The "
        "order found that very funny. Later it found it wise.")
BURNING = ("You took it into the Trial of Dreams and you won. Kabool said a second blade would be no gift, and he "
           "closed his hand around yours. When he opened it the steel was burning. It did not stop. The order still "
           "asks what became of it.")

TEXT = {
    "900 order saladin shard scholar": (
        BROUGHT + OFFER + "chose your wits. He named you Scholar of the Crescent, a great honor among the people of "
        "the east. The order has told that story for sixty years. It has never once told it as a fight."),
    "900 order saladin shard dervish": (
        BROUGHT + OFFER + "took the blade. You walked out of the Trial of Dreams with a Sacred Scimitar, forged in "
        "the image of Saladin's own. The order still teaches its novices how you fought. Few of them ever manage it."),
    "900 order saladin scimitar scholar": FORGED + OFFER + WITS,
    "900 order saladin scimitar dervish": FORGED + BURNING,
    "900 order saladin scimitar scholar unasked": FORGED + OFFER + WITS + ANYWAY,
    "900 order saladin scimitar dervish unasked": FORGED + BURNING + ANYWAY,
}


def slides():
    z = lhbuild.read(SLIDES)
    if "900 order saladin shard scholar" in z:
        return
    add = ""
    for nid, text in TEXT.items():
        add += ("Node ID=" + nid + CR + "Text=" + text + CR + "Should Have Voiceover=1" + CR + CR +
                "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR +
                "Custom Action=" + B(*relay("Fixt order epilogue relay")) + "Is Default Reply=1" + CR + "-" * 60 + CR)
    key = "Node ID=900 order wielder ring" + CR
    assert z.count(key) == 1
    z = z.replace(key, add + key)
    assert z.count(CR) == z.count("\n")
    (FX / SLIDES).write_bytes(z.encode("latin-1"))


def has_perk(perk, then, els):
    return ("CIfExpressionAction", [
        ("If Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [
            ("Item Count", "1"), ("Perk To Check For", PERKS + perk)]))])),
        ("Character to get attributes from", "Player1"), ("Then", then), ("Else", els)])


def completed(quest, then, els):
    return if_action(("CIsQuestCompletedAction", [("Quest", QUESTS + quest)]), then, els)


def path(trial):
    plain = say("900 order saladin scimitar " + trial)
    forged = var_if(UNASKED, say("900 order saladin scimitar " + trial + " unasked"), plain)
    return completed("Recover the Shard of Dreams", say("900 order saladin shard " + trial),
                     completed("Forge a Sacred Scimitar", forged, relay("Fixt order epilogue relay")))


def endgame():
    z = lhbuild.read(ENDGAME)
    if "900 order saladin shard scholar" in z:
        return
    skip = relay("Fixt order epilogue relay")
    action = ("CIfExpressionAction", [
        ("If Expression", ("CUseCannedExpressionExpression", [("Canned Expression", "Dialog/Requirements/Faction/Saladin IS")])),
        ("Character to get attributes from", "Player1"),
        ("Then", has_perk("Dervish of the Crescent", path("dervish"), has_perk("Scholar of the Crescent", path("scholar"), skip))),
        ("Else", skip)])
    k = z.index("Node ID=900 order saladin killer")
    s = z.rindex("Action=CIfExpressionAction", 0, k)
    e = balanced(z, s)
    assert "900 order saladin high" in z[s:e] and "900 order wielder" not in z[s:e]
    z = z[:e] + CR + "Action=" + B(*action).rstrip(CR) + z[e:]
    a = z.index("\t\t\tName=Fixt order epilogue relay" + CR)
    i = z.index("Item Count=27" + CR, a)
    assert i - a < 900
    z = z[:i] + "Item Count=28" + z[i + len("Item Count=27"):]
    lhbuild.write_map(ENDGAME, z)


def jafar():
    z = lhbuild.read(JAFAR)
    if "Fixt Shard Returned Unasked" in z:
        return
    i = z.index("Node ID=216 the shard unasked" + CR)
    old = "Reply Text=<Take the coin. Arguing would be worse.>" + CR + "Go to node ID=" + CR
    j = z.index(old, i)
    assert j - i < 1600 and z.count(old) == 1
    z = z[:j] + old + "Custom Action=" + B(*flag(UNASKED)) + z[j + len(old):]
    assert z.count(CR) == z.count("\n")
    (FX / JAFAR).write_bytes(z.encode("latin-1"))


def main():
    write_var(UNASKED, "Fixt Shard Returned Unasked", "1 means the player gave Amir the Shard of Dreams on the scimitar route.")
    slides()
    endgame()
    jafar()


if __name__ == "__main__":
    main()
