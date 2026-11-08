"""The end slides play on a stage, so each character stands in view while their text runs. Asked for after 0.97.4, when the
slides turned out to run in the corner of the last battle with nothing to look at.

`Empty Scratch map` is the base, with one stone texture lit in a pool at the mark and fading to black. Like the Undercroft it
needs no `.frm16` or `.way`. The player arrives out of frame, the camera pans in the dark, and CAIPushFogOfWar clears the
stage, because the player is too far off to.

The slide series is lifted whole from `END GAME Siege Map`, conditions and all, so this file owns no ending logic. Each
CDisplayDialogTreeAction gains a stand-in: a generator per step, spawned as `Fixt Stage Figure`, cleared before the next. A
step with no figure leaves the stage empty. The relay keeps the name `Fixt order epilogue relay` because the slides' replies
and the tree's Default Canceled Node Action already fire it, and the speaker keeps its name for the same reason.

One condition could not move. `Player talked way into Ahriman death` is an existence check, local to its map, so the last
battle turns it into a scripting variable on the way out.

MASTER NIS trigger now fires `Fixt to the epilogue stage` where it fired the series. The old relay stays in the last battle
unfired, as the source for a rerun. A rerun rebuilds the stage.

    python tools/build_epilogue_stage.py
"""
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from build_epilogue_flow import ENDGAME, items, relay_span
from build_inquisition_slides import VARS, flag, write_var
from lhbuild import B, CR, FX, activate, balanced, delay, if_action, multi, relay

MAP = "Levels/8 Alamut/Fixt Epilogue Stage.zax"
TEMPLATE = "Levels/Empty Scratch map.zax"
RELAY = "Fixt order epilogue relay"
LEAVE = "Fixt to the epilogue stage"
MARK = "Fixt Stage Mark"
SPEAKER = "Fake Talker for NIS"
ARRIVE = "Fixt Stage Arrival"
FIGURE = "Fixt Stage Figure"
TALKED = VARS + "Fixt Talked Ahriman Dead"
AHRIMAN = "Player talked way into Ahriman death"
STAGE_X, STAGE_Y = 640, 480
PLAYER_X, PLAYER_Y = 1540, 480  # out of frame at any resolution, and near enough that the fade outlasts the pan
LIGHT = r"Light Overlay Row ([0-9]+)=[0-9A-F]+"

C = "Levels/%s/Character Templates/"
KNIGHT = C % "Sewers" + "Lost Knight"
SALADIN = C % "8 Alamut" + "Knight of Saladin"
GOBLIN_KHAN = C % "Wilderness" + "Goblin King"
GRACE = C % "7 English Shrine" + "Grace OMalley"
SOLDIER = "Monster Cans/English Enemies/Soldier1"
WIELDER = C % "1 Barcelona" + "Temple District/Prisoner Wielder"
# Who stands on the stage, by the step's first slide. First match wins; None leaves the stage empty. Keyed by slide rather
# than by position, so a step added to the series does not shift every figure after it.
FIGURES = [
    ("900 order templar", KNIGHT), ("900 order inquisition", C % "3 Montaillou" + "Inquisitor Fournier"),
    ("900 order cult", C % "2 Montserrat" + "Brother Pau"), ("900 order saladin", SALADIN),
    ("900 order wielder", WIELDER), ("900 order relican", WIELDER), ("900 order standard", SOLDIER),
    ("900 order pits", None), ("900 order horde", GOBLIN_KHAN), ("900 order savage heart", None),
    ("900 order goblins eyes", None), ("900 order goblins esteban", None), ("900 order goblins", GOBLIN_KHAN),
    ("900 order england", "Monster Cans/English Enemies/Soldier4"), ("900 order spain", "Monster Cans/English Enemies/Soldier4"),
    ("900 order omalley", GRACE), ("900 order none", None), ("900 order shrine", C % "7 English Shrine" + "Druid Master"),
    ("900 friend cervantes", C % "1 Barcelona" + "Temple District/Cervantes"), ("900 shade", C % "Wilderness" + "Don Quixote"),
    ("900 friend cortes", C % "1 Barcelona" + "Port District/Cortez"), ("900 friend joan", C % "4 Crypt" + "Joan of Arc"),
    ("900 friend roger", C % "7 English Shrine" + "Sir Roger Templeton"), ("900 friend grumdjum", C % "Wilderness" + "Goblin Grumdjum"),
    ("900 friend diego", C % "Wilderness" + "Diego"), ("900 friend darsh", C % "Wilderness" + "Inquisitor Darsch"),
    ("900 friend goblin girl", "Monster Cans/Mongol Vendor Village"), ("900 friend saladin knight", SALADIN),
    ("900 friend fernand", C % "1 Barcelona" + "Port District/Distressed Sailor"), ("900 friend grace", GRACE),
    ("900 friend fang", "Monster Cans/Animals/Cub Companion"), ("900 friend golem", "Monster Cans/English Enemies/Wargolem Deactivated"),
    ("900 friend lost knight", KNIGHT),
]
CAST = {}


def figure(step):
    nodes = re.findall(r"Node ID=([^\r\n]*)", step)
    if not nodes:
        return None
    for prefix, can in FIGURES:
        if nodes[0].startswith(prefix):
            return can
    raise SystemExit("no figure rule for slide " + nodes[0])


def generator(template, name, entity, new_name, x, y, active):
    t = template
    t = re.sub(r"Name=Fake Talker for NIS generator", "Name=" + name, t, count=1)
    t = re.sub(r"(?m)^(\s*)Active=\d", lambda m: m.group(1) + "Active=" + active, t, count=1)
    t = re.sub(r"Entity=[^\r\n]*", "Entity=" + entity, t, count=1)
    t = re.sub(r"New Name=[^\r\n]*", "New Name=" + new_name, t, count=1)
    t = re.sub(r"Remove Default AIs=\d", "Remove Default AIs=1", t, count=1)
    t = re.sub(r"Position X=[^\r\n]*", "Position X=" + str(x), t, count=1)
    t = re.sub(r"Position Y=[^\r\n]*", "Position Y=" + str(y), t, count=1)
    return t + CR


def clear():
    return ("CDeleteAction", [("Target Name", FIGURE)])


def camera():
    return ("CAddAIAction", [("Target Name", MARK), ("AI", ("CAIAttractCamera", [("Marked For Deletion", "0"), ("Publisher", ""), ("Camera Arrived Action", ""),
                                                                                 ("Disable Self When Camera Arrives", "0")])), ("Delay Between Adds", "0")])


def leaf(step, display):
    """One slide: clear the last figure, bring on this one, and give him a moment before the text."""
    steps = [clear()] + ([activate(f"Fixt Stage Figure {step} generator")] if step in CAST else [])
    action = B(*multi(steps + [delay("1.5", ("CFixtDisplay", []))]))
    return action.replace(B("CFixtDisplay", []), display + CR).rstrip()


def staged(step, text):
    text, _ = re.subn(r"CDisplayDialogTreeAction\r\n\s*\{.*?\}", lambda m: leaf(step, m.group(0)), text, flags=re.S)
    talked = B("CExpressionAction", [("Expression", ("CIsGreaterThan", [
        ("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", TALKED)])), ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "0")]))])),
        ("Character to get attributes from", "Player1")]).rstrip()
    return re.sub(r"CCheckExistenceAction\r\n\s*\{\s*Name To Check For=" + AHRIMAN + r"\r\n\s*Desired Minimum Count=1\r\n\s*\}", lambda m: talked, text)


def curtain(text):
    """The last step: off the stage, and the camera let go before the sequence ends."""
    m = re.search(r"Item Count=(\d+)\r\n", text)
    assert m
    extra = "Action=" + B(*clear()) + "Action=" + B("CRemoveAIAction", [("Target Name", MARK), ("AI", "CAIAttractCamera"), ("Delay Between Removes", "0")])
    return text[:m.start()] + "Item Count=" + str(int(m.group(1)) + 2) + CR + extra + text[m.end():]


def series(last):
    i, e = relay_span(last)
    a = last.rindex("Level Part=", 0, i)
    part = last[a:balanced(last, a)]
    p = last[i:e]
    _, _, steps = items(p)
    assert "CShowCreditsAction" in steps[-1] and all("CShowCreditsAction" not in s for s in steps[:-1])
    CAST.clear()
    CAST.update({n: f for n, s in enumerate(steps[:-1]) if (f := figure(s))})
    new = part
    for n, s in enumerate(steps):
        assert new.count(s) == 1, n
        new = new.replace(s, curtain(s) if n == len(steps) - 1 else staged(n, s))
    new = re.sub(r"Position X=[^\r\n]*", "Position X=" + str(PLAYER_X), new)
    return re.sub(r"Position Y=[^\r\n]*", "Position Y=" + str(PLAYER_Y + 120), new) + CR


def arrival():
    opening = ("CBeginNonInteractiveSequenceAction", [("Options", ("CNonInteractiveSequence", [
        ("Pause Characters", "1"), ("Disable Player Controls", "1"), ("Can Fast Forward", "0")]))])
    # The camera pans from the player, so it does that in the dark.
    start = multi([("CFadeScreenDownAction", [("Time Until Auto Fade Up", "2.5")]), opening, camera(), delay("2.5", relay(RELAY))])
    spawn = ("CSpawnPointAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Per Party Spawn Action", delay("0.5", start)),
                               ("Per Character Spawn Action", ""), ("Set Facing Angle", "1"), ("Facing Angle", "180")])
    return lhbuild.entity(ARRIVE, "1", [spawn], "Editor/Spawn Point", PLAYER_X, PLAYER_Y)


def floor(z):
    """Num Textures=0 draws garbage, not black. One stone texture, lit in a pool at the mark and fading to black: Light
    Overlay is three bytes a vertex and 80 is unlit, and a vertex is every 64 units."""
    z, n = re.subn(r"Num Textures=0", "Num Textures=1" + CR + "Texture 0=VykaCrypt/Floor1 darker", z)
    assert n == 1
    z, n = re.subn(r"Blending=[^\r\n]*", "Blending=0.9", z)
    assert n == 1

    def row(m):
        y = int(m.group(1)) * 64
        out = ""
        for c in range(65):
            d = math.hypot(c * 64 - STAGE_X, (y - STAGE_Y) * 1.3)
            v = 0x80 if d < 170 else max(0, int(0x80 * (1 - (d - 170) / 220)))
            out += ("%02X" % v) * 3
        return "Light Overlay Row " + m.group(1) + "=" + out
    z, n = re.subn(LIGHT, row, z)
    assert n == 15, n
    return z


def stage(last):
    z = lhbuild.read(TEMPLATE)
    i = last.index("Name=Fake Talker for NIS generator")
    a = last.rindex("Level Part=", 0, i)
    talker = last[a:balanced(last, a)]

    z, n = re.subn(r"(?ms)^\t\tLevel Part=\w+\r\n\t\t\{\r\n.*?^\t\t\}\r\n", "", z)
    assert n == 1, n
    z = re.sub(r"Elevations Row (\d+)=[0-9A-F]+", lambda m: "Elevations Row " + m.group(1) + "=" + "00" * 65, z)
    z = floor(z)
    z, n = re.subn(r"Partial File Name=[^\r\n]*", "Partial File Name=8 Alamut/Fixt Epilogue Stage", z)
    assert n == 1
    z, n = re.subn(r"Map Description=[^\r\n]*", "Map Description=The End", z)
    assert n == 1
    z, n = re.subn(r"(?m)^(\s*)Spawn Point Name=[^\r\n]*", lambda m: m.group(1) + "Spawn Point Name=" + ARRIVE, z)
    assert n == 1

    # The player is out of frame, so nothing else lifts the fog over the stage.
    fog = ("CAIPushFogOfWar", [("Marked For Deletion", "0"), ("Publisher", ""), ("Push Radius", ("CConstant", [("Constant Value", "800")])), ("YX Ratio", "0.95")])
    parts = [arrival(), lhbuild.entity(MARK, "1", [fog], "Editor/Position Marker", STAGE_X, STAGE_Y),
             generator(talker, SPEAKER + " generator", "Levels/1 Barcelona/Character Templates/Generic Gaurd NPC", SPEAKER, PLAYER_X, PLAYER_Y - 120, "1"),
             series(last)]
    parts += [generator(talker, f"Fixt Stage Figure {n} generator", can, FIGURE, STAGE_X, STAGE_Y, "0") for n, can in sorted(CAST.items())]
    for can in CAST.values():
        lhbuild.read("Resources/" + can + ".can")

    assert "Level Part=" not in z
    m = re.search(r"Tree List=CSortList2D\r\n\t\{\r\n", z)
    assert m
    z = z[:m.end()] + "".join("\t\t" + p.rstrip() + CR for p in parts) + z[m.end():]
    lhbuild.write_map(MAP, z)


def rewire(last):
    """The last battle hands over: the one flag that cannot leave the map, then the curtain, then the teleport."""
    if LEAVE + CR in last:
        return last
    i, e = relay_span(last)
    before, inside, after = last[:i], last[i:e], last[e:]
    key = "Relay Name=" + RELAY
    assert before.count(key) + after.count(key) == 2
    z = before.replace(key, "Relay Name=" + LEAVE) + inside + after.replace(key, "Relay Name=" + LEAVE)
    go = ("CTeleportAction", [("Return to map", "never"), ("New Map Name", "8 Alamut/Fixt Epilogue Stage"), ("New Location", ARRIVE), ("Who To Switch", "$Instigator"),
                              ("Relative Position", "0"), ("Ignore Party Ready Rules", "1"), ("Warp Behavior", "")])
    talked = if_action(("CCheckExistenceAction", [("Name To Check For", AHRIMAN), ("Desired Minimum Count", "1")]), flag(TALKED))
    action = multi([("CFadeScreenDownAction", [("Time Until Auto Fade Up", "4")]), ("CEndNonInteractiveSequenceAction", []),
                    delay("1", ("CForEachPlayerAction", [("Action", multi([talked, go]))]))])
    return lhbuild.add_parts(z, [lhbuild.relay_part(LEAVE, action, 1293, 490)])


def register(rel):
    mods = FX.parent / "mod.json"
    text = mods.read_bytes().decode("utf8")
    if json.loads(text)["files"].count(rel) == 0:
        anchor = '    "Levels/8 Alamut/01 Desert Sprawl.zax",'
        assert text.count(anchor) == 1
        nl = "\r\n" if "\r\n" in text else "\n"
        mods.write_bytes(text.replace(anchor, '    "' + rel + '",' + nl + anchor).encode("utf8"))


def main():
    last = lhbuild.read(ENDGAME)
    write_var(TALKED, "Fixt Talked Ahriman Dead", "1 means the player talked Ahriman into death. Carried to the epilogue stage, because the checker it replaces is local to the last battle.")
    stage(last)
    new = rewire(last)
    if new != last:
        lhbuild.write_map(ENDGAME, new)
    register(MAP)
    register("Resources/" + TALKED + ".DerivedCharacterAttribute")
    print("stage built")


if __name__ == "__main__":
    main()
