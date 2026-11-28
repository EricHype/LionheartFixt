"""Shakespeare gets an ending slide, which pays off the play he promised you. Asked for after the 0.60.0 restoration
was found to leave a promise unkept: at the Crossroads he says *"You must return later and I will reveal to you the
opening scene of your play!"*, and every later visit says only that it is not ripe yet. The game recorded no scene, so
the payoff is new writing and goes where his pitch points -- *"a tale whose ending you will complete"* -- to the end.

Three slides, tested in this order, so resentment always wins:

  * `900 friend shakespeare resents` -- `Fixt Shakespeare Resents You` is set (0.83.5's variable; all four moments that
    raise it are the Shylocke debt). He writes you in after all, as the moneylender's servant.
  * `900 friend shakespeare` -- you told him at the Crossroads you were pleased and flattered. The play is written from
    rumour, about another Richard, and still opens with the scene he wrote for you.
  * `900 friend shakespeare home` -- you sent him back to Barcelona. He finishes it at home and sends you a copy.

Anyone else gets no slide. Each slide's claims about the past are from his tree (the muse, the debt, his hovel in the Port
District, the Richard II pitch); the real-world hooks are the play's opening quarrel, its "sad stories of the death of
kings", its abdication scene cut from the early printings, Shylock's servant who leaves him for a better master, and the
second-best bed.

  * Two character variables, `Fixt Shakespeare Encouraged` and `Fixt Shakespeare Sent Home`, set on his two replies at
    `1000 in wilderness 2`. A dialogue edit, so it reaches a save already in progress -- from the next time he is
    spoken to at the Crossroads; a save that already answered him gets no slide for it.
  * The three nodes in `Fixt Ending Slides`, each firing the epilogue relay, as every slide does.
  * One step in `END GAME Siege Map`'s epilogue series, after Ernesto's. `build_epilogue_stage.py` (run after this) lifts
    it onto the stage with his figure.

A rerun is a no-op.

    python tools/build_shakespeare_slide.py
    python tools/build_epilogue_stage.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH
from build_shrine_repairs import register
from build_inquisition_slides import VARS, flag, write_var, say

TREE = "Resources/Levels/1 Barcelona/Dialog/Port District/shakespeare.dialogtree"
SLIDES = "Resources/Levels/8 Alamut/Dialog/Fixt Ending Slides.DialogTree"
ENDGAME = "Levels/8 Alamut/END GAME Siege Map.zax"
RELAY = "Fixt order epilogue relay"
RESENTS = VARS + "Fixt Shakespeare Resents You"
ENCOURAGED = VARS + "Fixt Shakespeare Encouraged"
SENT_HOME = VARS + "Fixt Shakespeare Sent Home"
PITCH = "1000 in wilderness 2"
PLEASED = "I'm pleased and flattered, William. I look forward to your work."
SEND_HOME = "This place is too dangerous for you. Return to Barcelona."
RESENTS_ID, ALIVE, HOME = "900 friend shakespeare resents", "900 friend shakespeare", "900 friend shakespeare home"
TEXT = {
    RESENTS_ID: (
        "William Shakespeare never forgave you the moneylender's errand. He wrote you a part all the same. His Venice play "
        "has a moneylender in it, and the moneylender keeps a servant. The servant is a clown who sells his loyalty to "
        "whoever pays better. That part is yours, and it got the laughs. He did write a Richard II. It is about a "
        "different Richard, and there is nobody like you in it. He left his wife his second-best bed, and you nothing."),
    ALIVE: (
        "William Shakespeare went home to London with his muse and an unfinished play. He had promised you its opening "
        "scene, and he wrote it the week he arrived. Then he waited for the ending you were to supply. News of you "
        "travelled slowly, and wrongly. The ballads that reached London were about another Richard entirely. He finished "
        "the play from those. Richard II is about a king who talks his crown away and sits on the ground to tell sad "
        "stories. It still opens with the scene he wrote for you. Two men quarrel, and both swear they are loyal."),
    HOME: (
        "You sent William Shakespeare back to Barcelona, and he went. He finished the play in his hovel in the Port "
        "District. Without the battle sites he wrote what he knew, which was a man arguing for his life with words. He "
        "called it Richard II. The king in it speaks beautifully and loses everything. He sent you a copy, care of the "
        "Templars, with a dedication. It never reached you. The printers later cut the scene where the king gives up his "
        "crown, and nobody could say why."),
}
for _t in TEXT.values():
    assert "—" not in _t and "--" not in _t
    assert max(len(s.split()) for s in re.split(r"(?<=[.!?])\s+", _t)) <= 25


def build_vars():
    made = []
    for path, short, desc in [
            (ENCOURAGED, "Fixt Shakespeare Encouraged",
             "1 means the player told Shakespeare at the Crossroads that they looked forward to his play. Read by his ending slide."),
            (SENT_HOME, "Fixt Shakespeare Sent Home",
             "1 means the player sent Shakespeare home from the Crossroads. Read by his ending slide.")]:
        rel = "Resources/" + path + ".DerivedCharacterAttribute"
        if not (lhbuild.FX / rel).exists():
            write_var(path, short, desc)
            made.append(rel)
    return made


def build_tree():
    t = lhbuild.read(TREE)
    if ENCOURAGED in t and SENT_HOME in t:
        return 0
    i = t.index("Node ID=" + PITCH + CR)
    e = t.index(CR + DASH + CR, i)
    node = t[i:e]
    # The pleased reply carries no action: it gains the flag.
    a = "Reply Text=" + PLEASED + CR + "Go to node ID=1000 shakespeare continues work" + CR
    assert node.count(a) == 1 and node[node.index(a) + len(a):].startswith(CR), "the pleased reply already has an action"
    node = node.replace(a, a + "Custom Action=" + B(*flag(ENCOURAGED)), 1)
    # The send-home reply already fades him out and removes him: that action becomes the second of two.
    b = "Reply Text=" + SEND_HOME + CR + "Go to node ID=1000 leave wilderness" + CR + "Custom Action="
    assert node.count(b) == 1
    s = node.index(b) + len(b)
    end = lhbuild.balanced(node, s)
    old = node[s:end]
    assert old.startswith("CDelayAction" + CR) and "Target Name=William in the wilderness" in old
    wrapped = ("CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR +
               "Action=" + B(*flag(SENT_HOME)) + "Action=" + old + CR + "}" + CR + "}")
    node = node[:s] + wrapped + node[end:]
    new = t[:i] + node + t[e:]
    import dialogtree_format as dt
    assert [len(n.replies) for n in dt.parse(t).nodes] == [len(n.replies) for n in dt.parse(new).nodes]
    assert "\n" not in new.replace(CR, "")
    (lhbuild.FX / TREE).write_bytes(new.encode("latin-1"))
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
    (lhbuild.FX / SLIDES).write_bytes(t.replace(key, add + key).encode("latin-1"))
    return 3


def var_test(path, op, value, then, els):
    return ("CIfExpressionAction", [
        ("If Expression", (op, [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", path)])),
                                ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", value)]))])),
        ("Character to get attributes from", "Player1"), ("Then", then), ("Else", els)])


def build_step():
    z = lhbuild.read(ENDGAME)
    if "Node ID=" + ALIVE + CR in z:
        return 0
    a = z.index("\t\t\tName=" + RELAY + CR)
    # After Ernesto's step, which is the last companion-style step before the golem's.
    i = z.index("Game Scripting Variables/Fixt Companion Trapped Conquistador" + CR, a)
    s = z.rindex("\t" * 7 + "Action=CIfExpressionAction" + CR, a, i) + 7
    e = lhbuild.balanced(z, s)
    skip = lhbuild.delay("0.1", lhbuild.relay(RELAY))
    step = var_test(RESENTS, "CIsGreaterThanOrEqual", "1", say(RESENTS_ID),
                    var_test(ENCOURAGED, "CIsEqualTo", "1", say(ALIVE),
                             var_test(SENT_HOME, "CIsEqualTo", "1", say(HOME), skip)))
    z = z[:e] + CR + "\t" * 7 + "Action=" + B(*step).rstrip(CR) + z[e:]
    from build_epilogue_flow import items
    before = len(items(z[a:z.index("\r\n\t\t}", a)])[2])
    series = z.index("Action=CSeriesAction" + CR, a)
    m = re.compile(r"Item Count=(\d+)\r\n").search(z, series)
    assert m.start() - series < 120 and int(m.group(1)) == before - 1, (m.group(1), before)
    z = z[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + z[m.end():]
    lhbuild.write_map(ENDGAME, z)
    return 1


def main():
    made = build_vars()
    tree, slides, step = build_tree(), build_slides(), build_step()
    register(made + [TREE, SLIDES, ENDGAME])
    print("vars:", len(made), "| tree:", tree, "| slides:", slides, "| step:", step)


if __name__ == "__main__":
    main()
