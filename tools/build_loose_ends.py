"""0.94.0: four recorded lines that were one wire away, and a chant for the cathedral crypt.

Each edit asserts what it replaces, so a rerun is a no-op and a hand edit is never clobbered.

    python tools/build_loose_ends.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR, FX

DAVINCI = "Resources/Levels/1 Barcelona/Dialog/Gate District/DaVinciBarcelona.DialogTree"
DEMONIC = "Resources/Levels/Wilderness/Dialog/Demonic Spirit.DialogTree"
FORGE = "Levels/1 Barcelona/Blacksmith map.zax"
MICHEL = "Resources/Levels/3 Montaillou/Character Templates/Brother Michel.can"
CRYPT = "Levels/1 Barcelona/Church Crypt Interior.zax"


def save_tree(rel, text):
    # DialogTrees are not canonical resource text, so they skip write_map's round trip.
    assert text.count(CR) == text.count("\n"), rel + " lost its CRLF"
    (FX / rel).write_bytes(text.encode("latin-1"))


def swap(z, old, new, count=1):
    assert z.count(old) == count, (old[:60], z.count(old))
    return z.replace(old, new)


# ---- 1. DaVinci's reply answers itself with a goodbye -----------------------------------------

def inquisition_reply(z):
    done = "Reply Text=I could try to speak with the Inquisition about the gem." + CR + \
           "Go to node ID=320 speak to inquisition" + CR
    if done in z:
        return z
    return swap(z,
                "Reply Text=I could try to speak with the Inquisition about the gem." + CR +
                "Go to node ID=10 Goodbye" + CR,
                done, 2)


# ---- 2. The gem hand-in opens on the recorded line -------------------------------------------

def gem_voice(z):
    if "Go to node ID=340 return spirit" + CR in z:
        return z
    z = swap(z,
             "Reply Text=Is this the gem you're looking for?" + CR + "Go to node ID=3001 Gem recovered" + CR,
             "Reply Text=Is this the gem you're looking for?" + CR + "Go to node ID=340 return spirit" + CR)
    z = swap(z,
             "Reply Text=I have the gem you've been looking for." + CR + "Go to node ID=3001 Gem recovered" + CR,
             "Reply Text=I have the gem you've been looking for." + CR + "Go to node ID=340 return spirit" + CR)
    # 340 paid 400 gold and 1 XP of its own; 3002 already pays 1000, so its payout goes.
    start = z.index("Node ID=340 return spirit" + CR)
    end = z.index("-" * 20, start)
    old = z[start:end]
    assert "Value to give=400" in old and "(if deliver spirit to davinci" in old
    head = old[:old.index("Requirement=!None")]
    return z[:start] + head + "Requirement=!None" + CR + "Reply Text=" + CR + \
        "Go to node ID=3001 Gem recovered" + CR + "Is Default Reply=1" + CR + z[end:]


# ---- 3. The Demonic spirit's third goodbye ----------------------------------------------------

ABOVE_DARK = ("Custom Requirement=CIsGreaterThan" + CR + "{" + CR +
              "Operand1=CVariableDerivedCharacterAttribute" + CR + "{" + CR +
              "Character Attribute=Derived Character Attributes/Karma" + CR + "}" + CR +
              "Operator=" + CR + "Operand2=CConstant" + CR + "{" + CR +
              "Constant Value=800" + CR + "}" + CR + "}" + CR)


def split_on_karma(z, reply, target, tail):
    """Offer `reply` twice, as exact complements, so nobody ends up with no exit."""
    old = "Requirement=!None" + CR + "Reply Text=" + reply + CR + "Go to node ID=" + target + CR + tail
    new = ("Requirement=Karma equalless 800" + CR + "Reply Text=" + reply + CR +
           "Go to node ID=5 goodbye low karma" + CR + tail + CR +
           "Requirement=!None" + CR + ABOVE_DARK + "Reply Text=" + reply + CR +
           "Go to node ID=" + target + CR + tail)
    return swap(z, old, new)


def dark_goodbye(z):
    if "Go to node ID=5 goodbye low karma" + CR in z:
        return z
    z = split_on_karma(z, "I've heard enough out of you. Begone.", "5 goodbye neutral karma",
                       "Icon=Exit Icon" + CR)
    z = split_on_karma(z, "Thank you spirit. We should continue on now.", "5 goodbye neutral karma",
                       "Icon=Exit Icon" + CR + "Is Default Reply=1" + CR)
    return split_on_karma(z, "Agreed, we must pursue our enemy and recover the relics.",
                          "5 goodbye good karma", "Is Default Reply=1" + CR)


# ---- 4a. Eduardo remembers the jail -----------------------------------------------------------

def tabs(n, lines):
    return "".join("\t" * (n + d) + s + CR for d, s in lines)


def eduardo_memory(z):
    if "Name=eduardo jailed you" in z:
        return z
    arm = tabs(7, [(0, "Action=CActivateAction"), (0, "{"), (1, "Target Name=eduardo jailed you"),
                   (1, "Play Activate Sound=0"), (1, "Delay Between Activations=0"),
                   (1, "Warp Behavior="), (0, "}")])
    jail = "Item Count=8" + CR + "\t" * 7 + "Action=CDeactivateAction" + CR + "\t" * 7 + "{" + CR + \
           "\t" * 8 + "Target Name=Eduardo Sends you to jail" + CR
    z = swap(z, jail, "Item Count=9" + CR + arm + jail[len("Item Count=8" + CR):])

    # He is rebuilt by RESET MAP on every entry, so the line waits for him to exist.
    remark = tabs(7, [
        (0, "Action=CDelayAction"), (0, "{"),
        (1, "Next Action=CIfAction"), (1, "{"),
        (2, "If=CCheckExistenceAction"), (2, "{"),
        (3, "Name To Check For=eduardo jailed you"), (3, "Desired Minimum Count=1"), (2, "}"),
        (2, "Then=CMultipleActionsAction"), (2, "{"),
        (3, "Action=Array"), (3, "{"),
        (4, "Item Count=2"),
        (4, "Action=CDisplayDialogBalloonAction"), (4, "{"),
        (5, "Dialog Tree File=Levels/1 Barcelona/Dialog/Gate District/Blacksmith"),
        (5, "Node ID=100 attacked blacksmith"),
        (5, "Name of Position=eduardo"),
        (5, "Position Offset=0.000000,-80.000000"),
        (5, "After Action="), (5, "Include In Log=1"), (4, "}"),
        (4, "Action=CDeactivateAction"), (4, "{"),
        (5, "Target Name=eduardo jailed you"), (4, "}"),
        (3, "}"), (2, "}"),
        (2, "Else="), (2, "Return failure if the If failes=0"), (1, "}"),
        (1, "Delay=2"), (1, "Plus or Minus=0"), (1, "Forget Trigger=0"), (0, "}")])
    spawn = "Item Count=2" + CR + "\t" * 7 + "Action=CTriggerRelayAction" + CR + "\t" * 7 + "{" + CR + \
            "\t" * 8 + "Relay Name=RESET MAP for Invulnerable Eduardo" + CR + "\t" * 7 + "}" + CR + \
            "\t" * 7 + "Action=CTriggerRelayAction" + CR + "\t" * 7 + "{" + CR + \
            "\t" * 8 + "Relay Name=Visiting Customers for Blacksmith generator" + CR + "\t" * 7 + "}" + CR
    z = swap(z, spawn, "Item Count=3" + spawn[len("Item Count=2"):] + remark)
    return lhbuild.add_parts(z, [lhbuild.checker("eduardo jailed you", 472, 530)])


# ---- 4b. Michel's empty slot ------------------------------------------------------------------

def michel_slot(z):
    if "999 Michel pushed to the edge" in z:
        return z
    mark = "Name To Check For=Lucious dead"
    i = z.index(mark)
    then = z.index("Then=" + CR, i)
    assert then - i < 120, "the blank Then= is not the one beside Lucious dead"
    e = z.index("Else=CDisplayDialogBalloonAction", then)
    d = z[e:]
    d = d[:lhbuild.balanced(d, d.index("{"))]
    bark = d.replace("Else=", "Then=", 1).replace("Node ID=1000 Michel Attacked", "Node ID=999 Michel pushed to the edge")
    assert bark != d and "Node ID=999" in bark
    return z[:then] + bark + CR + z[then + len("Then=" + CR):]


# ---- 5. The monks under the cathedral ---------------------------------------------------------

def crypt_chant(z):
    if "Ambiant Song=1 Barcelona/MX_CHAMB_MED.ogg" in z:
        return z
    return swap(z, "Ambiant Song=1 Barcelona/AMB_barc_cathedral.ogg", "Ambiant Song=1 Barcelona/MX_CHAMB_MED.ogg")


def main():
    z = lhbuild.read(DAVINCI)
    save_tree(DAVINCI, gem_voice(inquisition_reply(z)))
    save_tree(DEMONIC, dark_goodbye(lhbuild.read(DEMONIC)))
    lhbuild.write_map(FORGE, eduardo_memory(lhbuild.read(FORGE)))
    lhbuild.write_map(MICHEL, michel_slot(lhbuild.read(MICHEL)))
    lhbuild.write_map(CRYPT, crypt_chant(lhbuild.read(CRYPT)))


if __name__ == "__main__":
    main()
