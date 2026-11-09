"""A slide after the Wielder one: what you did about Relican, whichever side you took.

The Wielder slides read rank and two perks. Everything else about the city's central quarrel ended
nowhere, and that includes the man Relican turned into a tree.

    Ruler, and a Wielder rank            you served him. Quinn and Leonardo each vary, and Brambles stays a tree
    `Hunt down Relican` completed        Cedric's route, with Brambles if you cured him
    refused the ring                     the game's own "No one here will know", with Brambles if you cured him
    Brambles cured, neither of those     Brambles alone

Only the refusal needed a variable. The ring's `No` reply fails the Dark initiation but leaves nothing the
end map can tell from never having been asked. These fire for any faction, because Brambles can be cured by
anyone. Using the ring without Relican's rank shows nothing here, because `900 order wielder ring` covers it.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_wielder_choice_slide.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, if_action, relay
from build_inquisition_slides import ENDGAME, SLIDES, TITLES, VARS, flag, say, var_if, write_var

RING = "Resources/Levels/1 Barcelona/Dialog/La Calle Perdida/Relican Summoning Ring.DialogTree"
REFUSED = VARS + "Fixt Ring Refused"
CALLE = "Levels/1 Barcelona/Quests/Calle Perdida/"
HUNT = CALLE + "Wielder Initiation Quests/Hunt down Relican"
CURE = CALLE + "Find the cure to restore Brambles"
QUINN = CALLE + "Wielder Initiation Quests/Convince Quinn the Herbalist to Join the Dark Wielders"
LEO = CALLE + "Wielder Initiation Quests/Convince DaVinci to Join the Dark Wielders"

CURED = ("You poured the potion on Brambles's roots. The tree split, and there was a man inside it, stiff in the "
         "legs and late for his grandchildren. ")
HUNTED = ("Cedric sent you after Relican, and you found the exile in the western forest and destroyed him. Nothing "
          "in La Calle Perdida marked it. The Wielders had cast him out once already, and they do not celebrate "
          "their own. Cedric heard your report and called you Wielder. ")
SLEPT = "The street slept well after that. Few of those sleeping there knew who to thank."
REFUSAL = ("Relican gave you a ring, and a city to use it on. You stood in La Calle Perdida with it burning in your "
           "hand, and you let it go. It shook itself to pieces, and something wailed as it went. Nobody in the "
           "hidden city ever knew how close it came. Cedric went on teaching. ")
QUIET = "You went back sometimes. You never told them."

DARK_QUINN = {"joined": "You bent Quinn the herbalist with your words, and he served Relican faithfully. ",
              "killed": "Quinn the herbalist refused, so you killed him. His shop in the Gate District stayed shut. ",
              "none": ""}
DARK_LEO = {"joined": "Leonardo gave you his word that he would not stand against Relican. He kept it, and he did not "
                      "forgive himself. ",
            "refused": "Leonardo asked you to turn back. He was the only one who ever did. ",
            "none": ""}


def dark(quinn, leo):
    return ("Relican made you a Dark Wielder, and he made you work for it. " + DARK_QUINN[quinn] + DARK_LEO[leo] +
            "Brambles stayed a tree. He creaked at you whenever you passed, and it could have been the wind. "
            "There was no one left in Barcelona who would say your name and his in the same breath.")


TEXT = {
    "900 order relican hunted": HUNTED + SLEPT,
    "900 order relican hunted cured": HUNTED + CURED + SLEPT,
    "900 order relican refused": REFUSAL + QUIET,
    "900 order relican refused cured": REFUSAL + CURED + QUIET,
    "900 order relican cured": ("Relican cursed a vitality potion, and Brambles stood rooted in La Calle Perdida for "
                                "years because of it. Quinn could not cure him. You took the cure from Relican himself. " +
                                CURED + "He thanked you and went to find them. The street has one less tree in it, and "
                                "nobody there has ever been sorry."),
}
for q in DARK_QUINN:
    for l in DARK_LEO:
        TEXT[f"900 order relican dark {q} {l}"] = dark(q, l)


def slides():
    z = lhbuild.read(SLIDES)
    if "900 order relican hunted" in z:
        return
    add = ""
    for nid, text in TEXT.items():
        add += ("Node ID=" + nid + CR + "Text=" + text + CR + "Should Have Voiceover=1" + CR + CR +
                "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR +
                "Custom Action=" + B(*relay("Fixt order epilogue relay")) + "Is Default Reply=1" + CR + "-" * 60 + CR)
    key = "Node ID=900 order horde traitor" + CR
    assert z.count(key) == 1
    z = z.replace(key, add + key)
    assert z.count(CR) == z.count("\n")
    (FX / SLIDES).write_bytes(z.encode("latin-1"))


def state(quest, sid, then, els):
    return if_action(("CWasQuestStateActivatedAction", [("Quest", quest), ("State", sid)]), then, els)


def done(quest, then, els):
    return if_action(("CIsQuestCompletedAction", [("Quest", quest)]), then, els)


def dark_for(quinn):
    return state(LEO, "RB4NW8TJ", say(f"900 order relican dark {quinn} joined"),
                 state(LEO, "ZH6PC3YF", say(f"900 order relican dark {quinn} refused"),
                       say(f"900 order relican dark {quinn} none")))


def endgame():
    z = lhbuild.read(ENDGAME)
    if "900 order relican hunted" in z:
        return
    skip = relay("Fixt order epilogue relay")
    served = ("CIfExpressionAction", [
        ("If Expression", ("CUseCannedExpressionExpression", [("Canned Expression", "Dialog/Requirements/Faction/Wielder IS")])),
        ("Character to get attributes from", "Player1"),
        ("Then", state(QUINN, "FPC9941A", dark_for("joined"), state(QUINN, "QQ2PE9WJ", dark_for("killed"), dark_for("none")))),
        ("Else", skip)])
    other = done(HUNT, done(CURE, say("900 order relican hunted cured"), say("900 order relican hunted")),
                 var_if(REFUSED, done(CURE, say("900 order relican refused cured"), say("900 order relican refused")),
                        done(CURE, say("900 order relican cured"), skip)))
    action = ("CIfExpressionAction", [
        ("If Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [
            ("Item Count", "1"), ("Perk To Check For", TITLES + "Ruler of Calle Perdida")]))])),
        ("Character to get attributes from", "Player1"), ("Then", served), ("Else", other)])
    k = z.index("Node ID=900 order wielder ring")
    s = z.rindex("Action=CIfExpressionAction", 0, k)
    e = balanced(z, s)
    assert "900 order wielder killer" in z[s:e] and "900 order horde" not in z[s:e]
    z = z[:e] + CR + "Action=" + B(*action).rstrip(CR) + z[e:]
    a = z.index("\t\t\tName=Fixt order epilogue relay" + CR)
    i = z.index("Item Count=28" + CR, a)
    assert i - a < 900
    z = z[:i] + "Item Count=29" + z[i + len("Item Count=28"):]
    lhbuild.write_map(ENDGAME, z)


def ring():
    z = lhbuild.read(RING)
    if "Fixt Ring Refused" in z:
        return
    i = z.index("Reply Text=No." + CR)
    j = z.index("Item Count=6" + CR, i)
    assert j - i < 120
    z = z[:j] + "Item Count=7" + CR + "Action=" + B(*flag(REFUSED)) + z[j + len("Item Count=6" + CR):]
    assert z.count(CR) == z.count("\n")
    (FX / RING).write_bytes(z.encode("latin-1"))


def main():
    write_var(REFUSED, "Fixt Ring Refused", "1 means the player refused to activate Relican's ring in La Calle Perdida.")
    slides()
    endgame()
    ring()


if __name__ == "__main__":
    main()
