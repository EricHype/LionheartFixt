"""Ernesto joins the companion system: he grows on level-up with a balloon, and his name shows how hurt he is. Reported
from play after 0.99.25: "when we levelled up there was no hover text for ernesto".

0.84.0 gave every companion a `Fixt Companion Joined/<name>` script, run by their tree on join and rejoin: it sets
`Fixt Companion <name>`, arms the level-up watch (`Fixt Companion Growth Install`) and the injury names (`Fixt Companion
Health Install`). Fifteen companions have one. Ernesto, the Trapped Conquistador on the Lake (`Crazy Goblin Trapped
Conquistador.DialogTree`, entity `Trapped Conquistador`), has none, so he never grew and never said so.

* `Fixt Companion Joined/Trapped Conquistador`, a copy of Fang's with his flag, called from both of his join replies.
* **Growth.** The level-up watch is armed once, on the player, with the companions written into it, so adding him to
  `Fixt Companion Growth Install` would never reach a game where it is already armed. He gets his own watch instead,
  armed once by his Joined script behind `Fixt Companion Growth Watch Trapped Conquistador`: Fang's block, his name,
  the same +9 health, +8 armor, +3 one-handed (he fights with a sword), and the balloon `Fixt Companion Growth` /
  `Trapped Conquistador`. It is not in the shared installer, so he cannot grow twice.
* **Injury names.** His block is added to `Fixt Companion Health Install`, which runs on every join: `Ernesto (Injured)`,
  `(Badly Injured)`, `(Near Death)`.

Reach: every save, from the next time he joins or rejoins. One already in the party needs dismissing and asking back once.

A rerun is a no-op.

    python tools/build_ernesto_companion.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH
from build_shrine_repairs import register

NAME = "Trapped Conquistador"
DISPLAY = "Ernesto"
COS = "Common Objects and Scripts/"
VARS = "Derived Character Attributes/Game Scripting Variables/"
JOINED_FANG = "Resources/" + COS + "Fixt Companion Joined/Fang.can"
JOINED = "Resources/" + COS + "Fixt Companion Joined/" + NAME + ".can"
GROWTH_INSTALL = "Resources/" + COS + "Fixt Companion Growth Install.can"
HEALTH_INSTALL = "Resources/" + COS + "Fixt Companion Health Install.can"
GROWTH_TREE = "Resources/Levels/Fixt Companion Growth.DialogTree"
TREE = "Resources/Levels/Wilderness/Dialog/Crazy Goblin Trapped Conquistador.DialogTree"
FLAG, HEALTH, WATCH = ("Fixt Companion " + NAME, "Fixt Companion Health Watch " + NAME, "Fixt Companion Growth Watch " + NAME)
BALLOON = "<Ernesto salutes the sky with his blade.> Another bout, another lesson! Spain will hear of this! <+9 health, +8 armor, +3 fighting skill>"


def flat(t):
    return re.sub(r"\r\n\t*", CR, t)


def block_at(t, key_pos):
    """The Key=CClass{...} text starting at key_pos (after its tabs)."""
    return t[key_pos:lhbuild.balanced(t, key_pos)]


def key_start(t, i, key_cls):
    """Start of the nearest `<key_cls>` line at or before i, after its tabs."""
    c = t.rindex(key_cls + CR, 0, i)
    s = t.rindex(CR, 0, c) + len(CR)
    return s + len(t[s:c]) - len(t[s:c].lstrip("\t"))


def build_dcas():
    n = 0
    for name in (FLAG, HEALTH, WATCH):
        rel = "Resources/" + VARS + name + ".DerivedCharacterAttribute"
        if (lhbuild.FX / rel).exists():
            continue
        src = {FLAG: "Fixt Companion Fang", HEALTH: "Fixt Companion Health Watch Fang", WATCH: "Fixt Companion Growth Watch"}[name]
        t = lhbuild.read("Resources/" + VARS + src + ".DerivedCharacterAttribute").replace(src, name)
        t = re.sub(r"Description=[^\r\n]*", "Description=" + {FLAG: "1 once Ernesto has joined the party", HEALTH: "1 once Ernesto's injury names are armed",
                                                                 WATCH: "1 once Ernesto's level-up growth is armed"}[name] + " (tools/build_ernesto_companion.py).", t)
        (lhbuild.FX / rel).write_bytes(t.encode("latin-1"))
        register([rel])
        n += 1
    return n


def growth_watch():
    """Ernesto's own level-up watch: the installer's AI with only Fang's block, renamed."""
    t = lhbuild.read(GROWTH_INSTALL)
    i = t.index("Character Attribute=" + "Derived Character Attributes/Game Scripting Variables/Fixt Companion Fang" + CR)
    item = block_at(t, key_start(t, i, "Action=CIfExpressionAction"))
    assert item.count("Fang") == 5, item.count("Fang")   # flag, existence, modify, balloon node and position
    ai_s = key_start(t, i, "AI=CXRPGAITriggerWhenLevelUp")
    ai = block_at(t, ai_s)
    a = ai.index("Action=CMultipleActionsAction" + CR)
    ai = ai[:a] + item + ai[lhbuild.balanced(ai, a):]
    ai = flat(ai).replace("Fixt Companion Fang" + CR, FLAG + CR).replace("=Fang" + CR, "=" + NAME + CR)
    assert "Fang" not in ai
    value = ai[len("AI="):]
    add = "CAddAIAction" + CR + "{" + CR + "Target Name=Player1" + CR + "AI=" + value + CR + "}"
    from build_troll_choices import modifier
    armed = B(*modifier("Player1", "Game Scripting Variables/" + WATCH, "1", "0"))
    return ("CIfExpressionAction{If Expression=" + B("CIsEqualTo", [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", VARS + WATCH)])),
                                                                     ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "0")]))])
            + "Character to get attributes from=Player1" + CR + "Then=CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR
            + "Item Count=2" + CR + "Action=" + add + CR + "Action=" + armed + "}" + CR + "}" + CR + "Else=" + CR + "}").replace("CIfExpressionAction{", "CIfExpressionAction" + CR + "{" + CR)


def build_joined():
    if (lhbuild.FX / JOINED).exists():
        return 0
    t = flat(lhbuild.read(JOINED_FANG))
    assert t.count("Fixt Companion Fang" + CR) == 2 and t.count("Item Count=3" + CR) == 1
    t = t.replace("Fixt Companion Fang" + CR, FLAG + CR).replace("Item Count=3" + CR, "Item Count=4" + CR, 1)
    # his own growth watch goes last, after the shared installers
    end = t.rindex("}" + CR + "}" + CR + "}" + CR)
    t = t[:end] + "Action=" + growth_watch() + CR + t[end:]
    lhbuild.write_map(JOINED, t)
    register([JOINED])
    return 1


def build_health():
    t = lhbuild.read(HEALTH_INSTALL)
    if "New Display Name=" + DISPLAY + CR in t:
        return 0
    i = t.index("Name To Check For=Fang" + CR)
    s = key_start(t, i, "=CIfAction")
    blk = flat(block_at(t, s))
    assert blk.startswith("Action=CIfAction"), blk[:40]
    blk = blk.replace("New Display Name=Fang", "New Display Name=" + DISPLAY).replace("Health Watch Fang" + CR, "Health Watch " + NAME + CR)
    blk = re.sub(r"=Fang\r\n", "=" + NAME + CR, blk)
    assert "Fang" not in blk, blk[blk.index("Fang") - 80:blk.index("Fang") + 20]
    # append to the top-level array, at the start of its closing-brace line
    m = re.compile(r"\t\t\tItem Count=(\d+)\r\n").search(t)
    assert m and m.start() < 120
    t = t[:m.start()] + "\t\t\tItem Count=" + str(int(m.group(1)) + 1) + CR + t[m.end():]
    tail = "\t\t}" + CR + "\t}" + CR + "}" + CR
    assert t.endswith(tail)
    t = t[:-len(tail)] + blk + CR + tail
    lhbuild.write_map(HEALTH_INSTALL, t)
    register([HEALTH_INSTALL])
    return 1


def build_balloon():
    t = lhbuild.read(GROWTH_TREE)
    if "Node ID=" + NAME + CR in t:
        return 0
    assert t.endswith("}" + CR)
    t = t[:-len("}" + CR)] + DASH + CR + "Node ID=" + NAME + CR + "Text=" + BALLOON + CR + "Should Have Voiceover=0" + CR + "}" + CR
    (lhbuild.FX / GROWTH_TREE).write_bytes(t.encode("latin-1"))
    register([GROWTH_TREE])
    return 1


def build_tree():
    t = lhbuild.read(TREE)
    call = "Canned Object=" + COS + "Fixt Companion Joined/" + NAME + CR
    if call in t:
        return 0
    joined = B("CUseCannedActionAction", [("Canned Object", COS + "Fixt Companion Joined/" + NAME)])
    # 1. the first join: append to its four actions
    i = t.index("Node ID=40 Return Barcelona" + CR)
    k = t.index("Reply Text=Sure. Let's go." + CR, i)
    a = t.index("Item Count=4" + CR, k)
    assert a - k < 200
    t = t[:a] + "Item Count=5" + CR + t[a + len("Item Count=4" + CR):]
    arr = t.rindex("Action=Array" + CR, 0, a)
    end = lhbuild.balanced(t, arr)
    close = t.rindex(CR, 0, end) + len(CR)
    assert t[close:end] == "}", repr(t[close:end])
    t = t[:close] + "Action=" + joined + t[close:]
    # 2. the rejoin: a lone CSetCompanionAction becomes the pair
    i = t.index("Node ID=3 return after released as a companion" + CR)
    k = t.index("Reply Text=Sure, come with me." + CR, i)
    c = t.index("Custom Action=CSetCompanionAction" + CR, k)
    e = lhbuild.balanced(t, c)
    old = t[c + len("Custom Action="):e]
    pair = ("CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR
            + "Action=" + old + CR + "Action=" + joined + "}" + CR + "}")
    t = t[:c] + "Custom Action=" + pair + t[e:]
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    register([TREE])
    return 2


def main():
    print("dcas:", build_dcas(), "| joined:", build_joined(), "| health:", build_health(), "| balloon:", build_balloon(), "| tree:", build_tree())


if __name__ == "__main__":
    main()
