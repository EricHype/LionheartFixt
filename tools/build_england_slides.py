"""The conspiracy's two ends the England slide did not know about.

`Servant of the Queen` covers giving Fawkes the Armada plans, so blowing up the Duke of Medina read the same as
declining to, and killing Fawkes for Spain read as nothing at all. Both are quest history. Slaying the Duke is
`K3MMM906`, or `8O3LLPQ4` for the player who changed their mind on the way. Run after `build_slide_rhythm.py`.

A rerun is a no-op.

    python tools/build_england_slides.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, relay
from build_inquisition_slides import ENDGAME, SLIDES, say
from build_goblin_slides import state

QUEST = "Levels/1 Barcelona/Quests/Gate District/ConspiracyAgainst Spain"
HANGED = "Any week of it would have hanged you. "
DUKE = ("You lured the Duke of Medina to a keg of gunpowder behind DaVinci's workshop. The Armada lost its head a "
        "season before it was due to sail. ")
SPAIN = ("Guy Fawkes told you his real name outside the Gate District, and you killed him for it. The Duke of Medina "
         "thanked you personally and went back to his ship. Spain never learned how close the powder had been. England "
         "lost an agent it had never admitted to having. History has no record of Guy Fawkes after that year, and never "
         "had any reason to.")


def england_text(z):
    base = re.search(r"Node ID=900 order england\r\nText=([^\r\n]*)", z).group(1)
    assert base.count(HANGED) == 1
    return base.replace(HANGED, HANGED + DUKE)


def slides():
    z = lhbuild.read(SLIDES)
    if "900 order spain" in z:
        return
    add = ""
    for nid, text in (("900 order england duke", england_text(z)), ("900 order spain", SPAIN)):
        add += ("Node ID=" + nid + CR + "Text=" + text + CR + "Should Have Voiceover=1" + CR + CR +
                "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR +
                "Custom Action=" + B(*relay("Fixt order epilogue relay")) + "Is Default Reply=1" + CR + "-" * 60 + CR)
    key = "Node ID=900 order omalley" + CR
    assert z.count(key) == 1
    z = z.replace(key, add + key)
    assert z.count(CR) == z.count("\n")
    (FX / SLIDES).write_bytes(z.encode("latin-1"))


def endgame():
    z = lhbuild.read(ENDGAME)
    if "900 order spain" in z:
        return
    k = z.index("Node ID=900 order england" + CR)
    t = z.rindex("Then=CDisplayDialogTreeAction", 0, k)
    assert k - t < 200
    e = balanced(z, t)
    plain = z[t + len("Then="):e]
    assert z[e:e + 200].lstrip().startswith("Else=CTriggerRelayAction"), z[e:e + 80]
    els = z.index("Else=CTriggerRelayAction", e)
    els_end = balanced(z, els)
    duke = state(QUEST, "K3MMM906", say("900 order england duke"), state(QUEST, "8O3LLPQ4", say("900 order england duke"), plain))
    fawkes = state(QUEST, "VJZDD7I6", say("900 order spain"), relay("Fixt order epilogue relay"))
    z = z[:t] + "Then=" + B(*duke) + "Else=" + B(*fawkes).rstrip(CR) + z[els_end:]
    lhbuild.write_map(ENDGAME, z)


def main():
    slides()
    endgame()


if __name__ == "__main__":
    main()
