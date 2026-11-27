"""Sahar's word sends you north, and Relican hears of Montserrat and takes Sir Tomas's journal. Reported: "I have forged
the alliance with sahar but montaillou doesn't unlock on the map to teleport to. Also, I cannot turn in the journal as
an evil playthrough because i cannot access the cathedral to meet sir javier."

af25409 left Brother Montgomerie unfired on the peaceful route, saying nothing mechanical depended on him. His dying
reply did three things nothing else in the game does: it enables the Plains on the world map (the only enable it has;
the Plains lead to the Mountain Pass, whose walk enables Montaillou), it completes whichever patron's Montserrat quest is
current (`seek out` / `protect the Crown of Thorns`, `Ensure safety of Monserrat Relics`), and it pays the 2500
`Montserrat XP` with each. A character who took Sahar's ring had no road north and an open patron quest forever.

  * **Sahar's ring** (`50 her word`, `<Take the ring.>`) now runs Montgomerie's three quest closes and the Plains
    enable, copied from his reply. Both play in `02 Druid Council Level2`, where `Montserrat XP` stands.
  * **For a save past the ring:** `60 the ring is on your hand`, what she says to a ring-bearer, gains *"Which road
    north?"*, which runs the same and answers in `61 Fixt the road north`. Each close is guarded on its quest's current
    state, so nothing pays twice.
  * **Every patron's Montaillou reply enables the Plains** too: each reply in Javier, Cedric, Raphael and Amir whose
    action activates *Travel to Montaillou*. So a report-back alone opens the road. The 2500 XP stays Sahar's, because
    an award must name a marker on the map it plays in.
  * **Relican**, the one patron 0.10.0's journal pass missed. His greeting gains, once and on the peaceful route, a
    Montserrat report (`95 Fixt Relican hears of Montserrat`) that marks the Plains, and, while the journal is carried,
    a hand-in (`96 Fixt Relican reads Sir Tomas`) that closes *Sir Tomas's Journal* as Cedric's does, paying from
    Calle Perdida's own `Sir Tomas journal XP`.

Trees and a new variable, so every save. A rerun is a no-op.

    python tools/build_sahar_road_north.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH
from build_shrine_repairs import register

DLG = "Resources/Levels/"
SAHAR = DLG + "2 Montserrat/Dialog/Sahar.DialogTree"
MONTGOMERIE = DLG + "2 Montserrat/Dialog/Brother Montgomerie.DialogTree"
RELICAN = DLG + "1 Barcelona/Dialog/La Calle Perdida/Lord Relican.DialogTree"
CEDRIC = DLG + "1 Barcelona/Dialog/La Calle Perdida/CedricAlsen.DialogTree"
# tree: (replies wrapped, the reply texts wrapped by name because their action does not itself activate the quest)
PATRONS = {
    DLG + "1 Barcelona/Dialog/Temple District/LordJavier.DialogTree": (3, []),
    CEDRIC: (2, []),
    DLG + "1 Barcelona/Dialog/Temple District/InquisitorRaphael.DialogTree": (4, []),
    DLG + "1 Barcelona/Dialog/Gate District/Jafar.DialogTree": (1, ["I will go to Montaillou now."]),
}
VARS = "Resources/Derived Character Attributes/Game Scripting Variables/"
HEARD = "Fixt Relican Heard Montserrat"
HEARD_REL = VARS + HEARD + ".DerivedCharacterAttribute"
PLAINS = "Interface/World Map/Plains"
POI = ("CEnablePointOfInterestOnWorldMapAction", [("Point Of Interest to Enable", PLAINS)])
CROWN = "Levels/1 Barcelona/Quests/Calle Perdida/Go to Montserrat and seek out the Crown of Thorns"
JOURNAL = "Inventory/Specific Item Cans/Quest Items/Books/Sir Tomas Journal"
TRAVEL = re.compile(r"CActivateQuestStateAction\r\n\{\r\n(?:Object ID=[^\r\n]*\r\n)?Quest=Levels/2 Montserrat/Quests/Travel to Montaillou")

NODE_ROAD = "61 Fixt the road north"
NODE_HEARS = "95 Fixt Relican hears of Montserrat"
NODE_READS = "96 Fixt Relican reads Sir Tomas"
LINES = {
    "road": "Which road north?",
    NODE_ROAD: ("<She points with her chin, not her hand.> Down to the plains, then up through the pass. Montaillou is "
                "past it. Walk it. Nothing of ours will stop you."),
    "hears": ("Montserrat is lost. Sahar's people took the Crown north over the mountains, and she let me walk out "
              "wearing her ring."),
    NODE_HEARS: ("Let you walk out. <He studies the ring without touching it.> Then she thinks you belong to her master, "
                 "and you will let her go on thinking it. A thief who carries a relic north is only a porter, brother. "
                 "What matters is the hand at the end of the road. That road runs over the plains and through the "
                 "mountains. I have marked it on your map."),
    "reads": "I took Sir Tomas de Vilanova's journal from his body. His last words were for Javier.",
    NODE_READS: ("<He opens it, as none of the others would.> A dead knight writing to a living one. Javier will never "
                 "read it. I would rather he wondered. <He stops at a page near the end, and smiles.> He names the "
                 "order's brothers in the north, and where they keep what they keep. The Templars bury their secrets "
                 "with their dead, brother, and forget that some of us dig. Leave it with me."),
}
for v in LINES.values():
    assert "—" not in v and "--" not in v


def no_ids(s):
    return re.sub(r"Object ID=[^\r\n]*\r\n", "", s)


def items(t, at):
    """The top-level items of the first Array at or after `at`: (raw items each ending CR, Item Count span, end)."""
    a = t.index("Action=Array" + CR, at)
    m = re.compile(r"Item Count=(\d+)\r\n").search(t, a)
    pos, out = m.end(), []
    for _ in range(int(m.group(1))):
        assert t.startswith("Action=", pos), t[pos:pos + 60]
        e = lhbuild.balanced(t, pos)
        assert t.startswith(CR, e)
        out.append(t[pos:e + len(CR)])
        pos = e + len(CR)
    assert t.startswith("}" + CR, pos), t[pos:pos + 60]
    return out, m, pos


def montgomerie_work():
    """His dying reply's three quest closes and the Plains enable, without the travel activation, door or death."""
    t = lhbuild.read(MONTGOMERIE)
    r = t.index("Reply Text=I will find Brother Michel. Rest now, warrior." + CR)
    got, _, _ = items(t, t.index("Custom Action=CMultipleActionsAction" + CR, r))
    assert len(got) == 10, len(got)
    work = got[1:5]
    assert all(w.startswith("Action=CConditionalAction" + CR) for w in work[:3]) and PLAINS in work[3], work[3][:120]
    assert "Montserrat XP" in work[0] and "Montserrat XP" in work[2]
    return [no_ids(w) for w in work]


def node_span(t, nid):
    s = t.index(CR + "Node ID=" + nid + CR) + len(CR)
    e = t.find(DASH, s)
    return s, (t.rindex("}" + CR) if e < 0 else e)


def append_nodes(t, nodes):
    assert t.endswith("}" + CR)
    return t[:-len("}" + CR)].rstrip(CR) + CR + "".join(DASH + CR + n for n in nodes) + "}" + CR


def multi_raw(raw_items):
    return ("CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=" + str(len(raw_items)) + CR +
            "".join(raw_items) + "}" + CR + "}" + CR)


def exit_reply(go=""):
    return CR + "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + go + CR + "Icon=Exit Icon" + CR + "Is Default Reply=1" + CR


def write(rel, t):
    (lhbuild.FX / rel).write_bytes(t.encode("latin-1"))
    return [rel]


def build_sahar(work):
    t = lhbuild.read(SAHAR)
    if "Node ID=" + NODE_ROAD + CR in t:
        return []
    # the ring
    s, e = node_span(t, "50 her word")
    r = t.index("Reply Text=<Take the ring.>" + CR, s, e)
    got, m, end = items(t, t.index("Custom Action=CMultipleActionsAction" + CR, r))
    assert len(got) == 10 and end < e, len(got)
    t = t[:end] + "".join(work) + t[end:]
    t = t[:m.start()] + "Item Count=" + str(len(got) + len(work)) + CR + t[m.end():]
    # a ring-bearer asks the road
    s, e = node_span(t, "60 the ring is on your hand")
    k = t.index("Requirement=!None" + CR + "Reply Text=<Draw.>" + CR, s, e)
    reply = ("Requirement=!None" + CR + "Reply Text=" + LINES["road"] + CR + "Go to node ID=" + NODE_ROAD + CR +
             "Custom Action=" + multi_raw(work) + "Icon=Quest Icon" + CR + CR)
    t = t[:k] + reply + t[k:]
    t = append_nodes(t, ["Node ID=" + NODE_ROAD + CR + "Text=" + LINES[NODE_ROAD] + CR + "Should Have Voiceover=0" + CR + exit_reply()])
    return write(SAHAR, t)


def reply_text(t, i):
    r = t.rindex(CR + "Reply Text=", 0, i) + len(CR + "Reply Text=")
    return t[r:t.index(CR, r)]


def wrap_plains(t, names):
    """Prefix the Plains enable to every Custom Action that activates Travel to Montaillou, and to the replies named.
    Returns (text, count)."""
    n, k = 0, 0
    while True:
        i = t.find(CR + "Custom Action=", k)
        if i < 0:
            return t, n
        v = i + len(CR + "Custom Action=")
        if t.startswith(CR, v):
            k = v
            continue
        e = lhbuild.balanced(t, v)
        val = t[v:e]
        if (TRAVEL.search(val) or reply_text(t, i) in names) and PLAINS not in val:
            new = multi_raw(["Action=" + B(*POI), "Action=" + val + CR]).rstrip(CR)
            t = t[:v] + new + t[e:]
            e = v + len(new)
            n += 1
        k = e


def build_patrons():
    done = []
    for rel, (want, names) in PATRONS.items():
        t = lhbuild.read(rel)
        t, n = wrap_plains(t, names)
        if n == 0:
            continue
        assert n == want, (rel, n)
        done += write(rel, t)
    return done


def var_is(name, value):
    return B("CIsEqualTo", [("Operand1", ("CVariableDerivedCharacterAttribute", [
        ("Character Attribute", "Derived Character Attributes/Game Scripting Variables/" + name)])), ("Operator", ""),
        ("Operand2", ("CConstant", [("Constant Value", value)]))])


def cand(a, b):
    return "CAND" + CR + "{" + CR + "Operand1=" + a + "Operator=" + CR + "Operand2=" + b + "}" + CR


SET_HEARD = ("CAddCharacterModifierToCharacterAction", [
    ("Modifier Description", HEARD), ("Modification is permanent", "1"), ("Character to modify", "Player#1-9#"),
    ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
        ("Modification Amount", ("CConstant", [("Constant Value", "1")])), ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "0"),
        ("Derived character attribute to modify", "Derived Character Attributes/Game Scripting Variables/" + HEARD)]))])),
    ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])


def cedric_journal_action():
    t = lhbuild.read(CEDRIC)
    s, e = node_span(t, "531 tomas")
    i = t.rindex("Custom Action=CMultipleActionsAction" + CR, s, e)
    v = i + len("Custom Action=")
    val = no_ids(t[v:lhbuild.balanced(t, v)]) + CR
    assert JOURNAL in val and "Get XP Frome=Sir Tomas journal XP" in val and "CSetQuestSatusToCompletedAction" in val
    return val


def build_relican():
    t = lhbuild.read(RELICAN)
    if "Node ID=" + NODE_HEARS + CR in t:
        return []
    hears_gate = cand(cand(var_is("Fixt Montserrat Peaceful", "1"), var_is(HEARD, "0")),
                      B("CActionExpression", [("Action", ("CWasQuestEverActivatedAction", [("Quest", CROWN)]))]))
    reads_gate = B("CActionExpression", [("Action", ("CActionCheckForInventoryItem", [
        ("Who to give check", "$instigator"), ("Inventory Item To Check For", JOURNAL)]))])
    replies = ("Requirement=!None" + CR + "Custom Requirement=" + hears_gate + "Reply Text=" + LINES["hears"] + CR +
               "Go to node ID=" + NODE_HEARS + CR + "Custom Action=" + B(*lhbuild.multi([POI, SET_HEARD])) + "Icon=Quest Icon" + CR + CR +
               "Requirement=!None" + CR + "Custom Requirement=" + reads_gate + "Reply Text=" + LINES["reads"] + CR +
               "Go to node ID=" + NODE_READS + CR + "Custom Action=" + cedric_journal_action() + "Icon=Quest Icon" + CR + CR)
    s, e = node_span(t, "5 Return Dialogue")
    k = t.index("Requirement=!None" + CR + "Reply Text=Tell me more about the tasks." + CR, s, e)
    t = t[:k] + replies + t[k:]
    back = CR + "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=5 Return Dialogue" + CR
    t = append_nodes(t, ["Node ID=" + n + CR + "Text=" + LINES[n] + CR + "Should Have Voiceover=0" + CR + back
                         for n in (NODE_HEARS, NODE_READS)])
    return write(RELICAN, t)


def build_var():
    if (lhbuild.FX / HEARD_REL).exists():
        return []
    v = lhbuild.read(VARS + "Esteban Dead.DerivedCharacterAttribute").replace("Esteban Dead", HEARD)
    v = v.replace("Description=" + CR, "Description=1 means Lord Relican has heard the player's Montserrat report on Sahar's route." + CR)
    (lhbuild.FX / HEARD_REL).write_bytes(v.encode("latin-1"))
    return [HEARD_REL]


def main():
    done = build_var() + build_sahar(montgomerie_work()) + build_patrons() + build_relican()
    if done:
        register(done)
    print("sahar road north:", done)


if __name__ == "__main__":
    main()
