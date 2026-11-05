"""A slide after the Templar one, for a Templar who freed the Doomed Knights: what became of the shield.

The Crypt and the shield chain were real choices that the Templar slides never read. Six slides by three
shield outcomes would be eighteen variants, so this is one slide of its own, as the cult's is.

    `Release the Doomed Knights` completed, Templar       900 order templar relic
    the same, and Sir Roger handed you the Aegis          900 order templar aegis

The Aegis cannot be read from the inventory, because it can be sold, so `70 the relic` writes a variable.
That reply already holds an action array and exits through `10 accept`, which is left exactly as it is,
because the greeting fires inside a non-interactive sequence.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_templar_shield_slide.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, if_action, relay
from build_inquisition_slides import ENDGAME, SLIDES, VARS, flag, say, var_if, write_var

ROGER = "Resources/Levels/7 English Shrine/Dialog/SirRoger.DialogTree"
AEGIS = VARS + "Fixt Aegis Received"
QUEST = "Levels/4 Crypt/Quests/Release the Doomed Knights from their torment"

TEXT = {
    "900 order templar relic": (
        "You forged the Lion Shield as an initiate. You carried it out of the Crypt changed, with an old cross on "
        "it and the lion gone faint beneath. Two hundred years of damned knights had gone free to put it there. "
        "No chapter roll records why. When you were gone it went back to the order. They hung it in a hall, and "
        "nobody there could say whose it had been."),
    "900 order templar aegis": (
        "You forged the Lion Shield as an initiate, and you carried it out of the Crypt with an old cross on it. "
        "Two hundred years of damned knights had gone free to put it there. Sir Roger saw what it was and took it "
        "from you, because a relic is a thing the order lays on tombs. He gave you the Aegis, and you carried that "
        "to the end. The order keeps both now. It tells the story of the second. Nobody there can tell you who "
        "the first one was for."),
}


def slides():
    z = lhbuild.read(SLIDES)
    if "900 order templar relic" in z:
        return
    add = ""
    for nid, text in TEXT.items():
        add += ("Node ID=" + nid + CR + "Text=" + text + CR + "Should Have Voiceover=1" + CR + CR +
                "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR +
                "Custom Action=" + B(*relay("Fixt order epilogue relay")) + "Is Default Reply=1" + CR + "-" * 60 + CR)
    key = "Node ID=900 order inquisition exposer" + CR
    assert z.count(key) == 1
    z = z.replace(key, add + key)
    assert z.count(CR) == z.count("\n")
    (FX / SLIDES).write_bytes(z.encode("latin-1"))


def endgame():
    z = lhbuild.read(ENDGAME)
    if "900 order templar relic" in z:
        return
    skip = relay("Fixt order epilogue relay")
    chosen = var_if(AEGIS, say("900 order templar aegis"), say("900 order templar relic"))
    action = ("CIfExpressionAction", [
        ("If Expression", ("CUseCannedExpressionExpression", [("Canned Expression", "Dialog/Requirements/Faction/Templar IS")])),
        ("Character to get attributes from", "Player1"),
        ("Then", if_action(("CIsQuestCompletedAction", [("Quest", QUEST)]), chosen, skip)),
        ("Else", skip)])
    a = z.index("\t\t\tName=Fixt order epilogue relay" + CR)
    i = z.index("Item Count=26" + CR, a)
    assert i - a < 900
    s = z.index("Action=CIfAction", i)
    assert s - i < 40
    e = balanced(z, s)
    assert "900 order templar knelt killer" in z[s:e]
    z = z[:e] + CR + "Action=" + B(*action).rstrip(CR) + z[e:]
    z = z[:i] + "Item Count=27" + z[i + len("Item Count=26"):]
    lhbuild.write_map(ENDGAME, z)


def roger():
    z = lhbuild.read(ROGER)
    if "Fixt Aegis Received" in z:
        return
    i = z.index("Node ID=70 the relic" + CR)
    j = z.index("Item Count=3" + CR, i)
    assert j - i < 700 and "Go to node ID=10 accept" in z[i:j]
    z = z[:j] + "Item Count=4" + CR + "Action=" + B(*flag(AEGIS)) + z[j + len("Item Count=3" + CR):]
    assert z.count(CR) == z.count("\n")
    (FX / ROGER).write_bytes(z.encode("latin-1"))


def main():
    write_var(AEGIS, "Fixt Aegis Received", "1 means Sir Roger has handed the player the Aegis of the Templars.")
    slides()
    endgame()
    roger()


if __name__ == "__main__":
    main()
