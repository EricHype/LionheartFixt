"""A Necromancer can compel Jameson to raise the bridge. Asked: "When meeting the spirit of jameson in the mad enchanter
dungeon - there are limited ways to convince him. I'm a necromancer - can't i compell the spirit at a karma cost?"

Vanilla's Jameson (`Trapped Spirit1`) builds his piece of the bridge two ways: shamed as a Templar (`220 Speech`, open to
anyone who asked his name), or sent back to him by Marco (`07`/`08`). Begging fails and insulting him ends it.

  * Where he refuses, `160 island` ("*If* I was properly motivated") and `170 begging`, a character with Relican's
    `Necromancer` title (the check Galileo's and the camp's lines use) gains "I did not come to ask, ghost..." ahead of
    the insult, to a new `720 Fixt Jameson compelled`.
  * Its one reply raises the bridge through the same `Move Second Rock for Path` relay `220` fires, and costs 50 Karma,
    twice the insult's 25 and the Enchanter pact's price. No XP, as the shame route pays none.
  * The reply is hidden once `Jameson already activated bridge` exists, so it cannot be paid for twice.

A tree edit: every save. A rerun is a no-op.

    python tools/build_jameson_compelled.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH, relay
from build_shrine_repairs import register

TREE = "Resources/Levels/1 Barcelona/Dialog/La Calle Perdida/Trapped Spirit1.DialogTree"
NODE = "720 Fixt Jameson compelled"
LINES = {
    "compel": "I did not come to ask, ghost. The dead answer to me now. Raise the bridge.",
    "jameson": ("<The spirit jerks, as if on a chain.> What... what is that? Three hundred years I have kept my own will in "
                "this place, and you take it in a breath. Stop! Very well, you shall have your bridge. I pray the enchanter "
                "keeps you here forever."),
    "silent": "Good. Now be silent.",
}
for v in LINES.values():
    assert "—" not in v and "--" not in v

KARMA = ("CAddCharacterModifierToCharacterAction", [
    ("Modifier Description", "Karma"), ("Modification is permanent", "0"), ("Character to modify", "Player#1-9#"),
    ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
        ("Modification Amount", ("CConstant", [("Constant Value", "-50")])), ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "1"), ("Derived character attribute to modify", "Derived Character Attributes/Karma")]))])),
    ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])

GATE = ("CAND" + CR + "{" + CR +
        "Operand1=" + B("CHasPerkExpression", [("Perks To Check For", ("Array", [
            ("Item Count", "1"), ("Perk To Check For", "Perks/!Event Title Perks/Necromancer")]))]) +
        "Operator=" + CR +
        "Operand2=CExpressionNot" + CR + "{" + CR + "Operand1=" +
        B("CActionExpression", [("Action", ("CCheckExistenceAction", [
            ("Name To Check For", "Jameson already activated bridge"), ("Desired Minimum Count", "1")]))]) +
        "}" + CR + "}" + CR)

COMPEL = ("Requirement=!None" + CR + "Custom Requirement=" + GATE + "Reply Text=" + LINES["compel"] + CR +
          "Go to node ID=" + NODE + CR + CR)


def insert_before_insult(t, node):
    s = t.index("Node ID=" + node + CR)
    e = t.index(DASH, s)
    r = t.index("Reply Text=I have heard enough from you, ghost.", s, e)
    k = t.rindex(CR + CR + "Requirement=", s, r) + len(CR + CR)
    return t[:k] + COMPEL + t[k:]


def build():
    t = lhbuild.read(TREE)
    if "Node ID=" + NODE + CR in t:
        return False
    t = insert_before_insult(t, "160 island")
    t = insert_before_insult(t, "170 begging")
    actions = [relay("Move Second Rock for Path"), KARMA]
    reply = ("Requirement=!None" + CR + "Reply Text=" + LINES["silent"] + CR + "Go to node ID=" + CR +
             "Custom Action=" + B("CMultipleActionsAction", [("Action", ("Array", [("Item Count", str(len(actions)))] +
                                                                         [("Action", a) for a in actions]))]) +
             "Icon=Exit Icon" + CR + "Is Default Reply=1" + CR)
    new = ("Node ID=" + NODE + CR + "Text=" + LINES["jameson"] + CR + "Should Have Voiceover=0" + CR + CR + reply)
    assert t.endswith("}" + CR)
    t = t[:-len("}" + CR)].rstrip(CR) + CR + CR + DASH + CR + new + "}" + CR
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    register([TREE])
    return True


def main():
    print("jameson compelled:", build())


if __name__ == "__main__":
    main()
