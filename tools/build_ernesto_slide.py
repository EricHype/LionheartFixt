"""Ernesto gets an ending slide. Asked for after 0.99.27; 0.99.26 brought him into the companion system, and he was the
only companion with no slide.

Two slides, on the Fang pattern: `Fixt Companion Trapped Conquistador` 1 (he travelled with you and lived) shows
`900 friend ernesto`, 3 (he died with you) shows `900 friend ernesto dead`, anything else skips. Every claim about the past
is from his tree (`Crazy Goblin Trapped Conquistador.DialogTree`): the goblin pen he took for the Tourney of Champions,
the silver-tongued arena masters, Spain, the fair maiden Dulcena, the Chalice of Victory, and going home to tell
Barcelona his exploits. The rest happens after the game.

* `Fixt Companion Died/Trapped Conquistador`, a copy of Fang's: 1 becomes 3.
* His death runs it. His can's `Destroyed Script Action` was empty and nothing replaces it (his Lake generator's After
  Action is blank), so it goes there, for a Lake not yet entered. His Joined script also sets it on him with
  `CSetDestroyedScriptActionAction`, which reaches a save from his next join or rejoin; the slot held nothing to lose.
* The step goes after Fang's in `END GAME Siege Map`'s epilogue relay, and `build_epilogue_stage.py` (run after this)
  lifts it onto the stage with his figure.

A rerun is a no-op.

    python tools/build_ernesto_slide.py
    python tools/build_epilogue_stage.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH
from build_shrine_repairs import register

NAME = "Trapped Conquistador"
FLAG = "Fixt Companion " + NAME
COS = "Common Objects and Scripts/"
DIED_FANG = "Resources/" + COS + "Fixt Companion Died/Fang.can"
DIED = "Resources/" + COS + "Fixt Companion Died/" + NAME + ".can"
JOINED = "Resources/" + COS + "Fixt Companion Joined/" + NAME + ".can"
CAN = "Resources/Levels/Wilderness/Character Templates/Crazy Goblin-Trapped Conquistador.can"
SLIDES = "Resources/Levels/8 Alamut/Dialog/Fixt Ending Slides.DialogTree"
ENDGAME = "Levels/8 Alamut/END GAME Siege Map.zax"
RELAY = "Fixt order epilogue relay"
ALIVE, DEAD = "900 friend ernesto", "900 friend ernesto dead"
TEXT = {
    ALIVE: ("Ernesto went home to Barcelona, as he had always meant to, and told the people his exploits. He told them "
            "nightly for twenty years. In his telling the goblin pen by the lake was the Tourney of Champions, the arena "
            "masters were silver-tongued, and every bout was fair. The stranger who walked out at his side was a fellow "
            "champion. He never asked your name and never needed it. He fought every battle after that for Spain and for "
            "the fair maiden Dulcena, whom nobody in Barcelona ever met. The Chalice of Victory was never found. He kept a "
            "space on it for you regardless."),
    DEAD: ("Ernesto died in a bout he had never been told was real. He went down shouting for Spain, which was the one part "
           "of it he had always had right. Nobody in Barcelona heard his exploits, there being nobody left who could tell "
           "them the way he did. The fair maiden Dulcena, if she was anywhere, did not hear either. If there was ever a "
           "Chalice of Victory, his name is not on it. The goblins by the lake told the story for a while, badly, and "
           "always as a comedy."),
}


def died_call():
    return B("CUseCannedActionAction", [("Canned Object", COS + "Fixt Companion Died/" + NAME)])


def build_died():
    if (lhbuild.FX / DIED).exists():
        return 0
    t = lhbuild.read(DIED_FANG)
    assert t.count("Fixt Companion Fang" + CR) >= 2 and "Fang" not in t.replace("Fixt Companion Fang" + CR, "")
    (lhbuild.FX / DIED).write_bytes(t.replace("Fixt Companion Fang" + CR, FLAG + CR).encode("latin-1"))
    register([DIED])
    return 1


def build_can():
    t = lhbuild.read(CAN)
    if "Fixt Companion Died/" + NAME in t:
        return 0
    m = re.search(r"(?m)^(\t*)Destroyed Script Action=\r\n", t)
    assert m and t.count("Destroyed Script Action=") == 1
    t = t[:m.start()] + m.group(1) + "Destroyed Script Action=" + died_call().rstrip(CR) + CR + t[m.end():]
    lhbuild.write_map(CAN, t)
    register([CAN])
    return 1


def build_joined():
    t = lhbuild.read(JOINED)
    if "Fixt Companion Died/" + NAME in t:
        return 0
    hook = B("CSetDestroyedScriptActionAction", [("New Destroyed Action", "RAW"), ("Target Name", NAME)]).replace(
        "New Destroyed Action=RAW" + CR, "New Destroyed Action=" + died_call(), 1)
    flat = re.sub(r"\r\n\t*", CR, t)
    assert flat.count("Item Count=4" + CR) == 1 and flat.index("Item Count=4" + CR) < 80
    flat = flat.replace("Item Count=4" + CR, "Item Count=5" + CR, 1)
    end = flat.rindex("}" + CR + "}" + CR + "}" + CR)
    flat = flat[:end] + "Action=" + hook + flat[end:]
    lhbuild.write_map(JOINED, flat)
    register([JOINED])
    return 1


def build_slides():
    t = lhbuild.read(SLIDES)
    if "Node ID=" + ALIVE + CR in t:
        return 0
    add = ""
    for nid, text in TEXT.items():
        add += ("Node ID=" + nid + CR + "Text=" + text + CR + "Should Have Voiceover=1" + CR + CR + "Requirement=!None" + CR +
                "Reply Text=" + CR + "Go to node ID=" + CR + "Custom Action=" + B(*lhbuild.relay(RELAY)) +
                "Is Default Reply=1" + CR + DASH + CR)
    key = "Node ID=900 friend golem" + CR
    assert t.count(key) == 1
    t = t.replace(key, add + key)
    (lhbuild.FX / SLIDES).write_bytes(t.encode("latin-1"))
    register([SLIDES])
    return 2


def build_step():
    z = lhbuild.read(ENDGAME)
    if "Node ID=" + ALIVE + CR in z:
        return 0
    a = z.index("\t\t\tName=" + RELAY + CR)
    i = z.index("Character Attribute=Derived Character Attributes/Game Scripting Variables/Fixt Companion Fang" + CR, a)
    s = z.rindex("\t" * 7 + "Action=CIfExpressionAction" + CR, a, i) + 7
    e = lhbuild.balanced(z, s)
    fang = z[s:e]
    assert fang.count("Fixt Companion Fang" + CR) == 2 and fang.count("Node ID=900 friend fang") == 2, fang[:200]
    step = fang.replace("Fixt Companion Fang" + CR, FLAG + CR).replace("Node ID=900 friend fang dead" + CR, "Node ID=" + DEAD + CR) \
               .replace("Node ID=900 friend fang" + CR, "Node ID=" + ALIVE + CR)
    assert "fang" not in step.lower()
    z = z[:e] + CR + "\t" * 7 + step + z[e:]
    from build_epilogue_flow import items
    before = len(items(z[a:z.index("\r\n\t\t}", a)])[2])
    series = z.index("Action=CSeriesAction" + CR, a)
    m = re.compile(r"Item Count=(\d+)\r\n").search(z, series)
    assert m.start() - series < 120 and int(m.group(1)) == before - 1, (m.group(1), before)
    z = z[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + z[m.end():]
    lhbuild.write_map(ENDGAME, z)
    register([ENDGAME])
    return 1


def main():
    print("died:", build_died(), "| can:", build_can(), "| joined:", build_joined(), "| slides:", build_slides(), "| step:", build_step())


if __name__ == "__main__":
    main()
