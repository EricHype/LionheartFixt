"""Machiavelli pays his Montaillou debt once. Issue #16: "I got the next bug with Machiavelli in Montaillou, everytime I
talk with him he gives 500 gold."

0.9.0 staged vanilla's unused inn scene: `Machiavelli in Montaillou generator` in `04 Inn Interior` opens
`300 machiavelli helps you in montaillou`, whose only reply carries vanilla's `CGiveMoneyToAllPlayersAction` of 500. The
greeting sends every click to `300`, so every conversation paid again.

  * The reply's payment now runs only while the new variable `Fixt Machiavelli Paid in Montaillou` is 0, and sets it.
    A tree edit, so it reaches every save (one already paid more than once keeps what it has, and is paid no more).
  * The inn's greeting sends a character he has already paid to a new `305 Fixt Machiavelli again`, which carries
    `300 ... 3`'s own replies (the ring, the betrayal, the snake captain) so nothing becomes unreachable. Map-side: an
    inn not yet entered; an existing save hears the repayment speech again, without the gold.

A rerun is a no-op.

    python tools/build_machiavelli_pays_once.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH
from build_shrine_repairs import register

TREE = "Resources/Levels/1 Barcelona/Dialog/Temple District/Machiavelli.DialogTree"
MAP = "Levels/3 Montaillou/04 Inn Interior.zax"
VARS = "Resources/Derived Character Attributes/Game Scripting Variables/"
TEMPLATE = VARS + "Fixt Vault Guard Fought.DerivedCharacterAttribute"
PAID_REL = VARS + "Fixt Machiavelli Paid in Montaillou.DerivedCharacterAttribute"
PAID = "Derived Character Attributes/Game Scripting Variables/Fixt Machiavelli Paid in Montaillou"
AGAIN = "305 Fixt Machiavelli again"
LINE = ("You again. I pay my debts once, and that one is paid. Advice costs me nothing, so take some: the Old Man's "
        "assassins have not stopped looking for either of us. Sit with your back to a wall.")
assert "—" not in LINE and "--" not in LINE


def var_is(cls, value, who):
    return ("CExpressionAction", [("Expression", (cls, [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", PAID)])),
                                                         ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", value)]))])),
                                  ("Character to get attributes from", who)])


SET_PAID = ("CAddCharacterModifierToCharacterAction", [
    ("Modifier Description", ""), ("Modification is permanent", "1"), ("Character to modify", "Player1"),
    ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
        ("Modification Amount", ("CConstant", [("Constant Value", "1")])), ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "0"), ("Derived character attribute to modify", PAID)]))])),
    ("OPTIONAL Duration", ""), ("Expression Context", "Player1")])


def var_file():
    p = lhbuild.FX / PAID_REL
    if p.exists():
        return []
    t = lhbuild.read(TEMPLATE)
    d = t[t.index("\tDescription="):t.index(CR, t.index("\tDescription="))]
    t = t.replace("Fixt Vault Guard Fought", "Fixt Machiavelli Paid in Montaillou")
    t = t.replace(d, "\tDescription=1 once Machiavelli has paid his Montaillou debt, so he pays it only once.")
    assert "Vault" not in t and "Import and Export=0" in t
    p.write_bytes(t.encode("latin-1"))
    return [PAID_REL]


def multi_wrap(old):
    """The vanilla payment, run only while unpaid, followed by the flag."""
    return ("CIfAction", [("If", var_is("CIsEqualTo", "0", "$Instigator")),
                          ("Then", ("CMultipleActionsAction", [("Action", ("Array", [("Item Count", "2"), ("Action", "@OLD@"), ("Action", SET_PAID)]))])),
                          ("Else", ""), ("Return failure if the If failes", "0")])


def b_with_old(old):
    return B(*multi_wrap(old)).replace("Action=@OLD@" + CR, "Action=" + old)


def build_map():
    t = lhbuild.read(MAP)
    if PAID in t:
        return []
    g = t.index("\t\t\tName=Machiavelli in Montaillou generator" + CR)
    end = t.index("\t\tLevel Part=", g)
    k = t.index("Else=CDisplayDialogTreeAction", g)
    assert k < end and "Node ID=300 machiavelli helps you in montaillou" + CR in t[k:k + 400]
    s = k + len("Else=")
    e = lhbuild.balanced(t, s)
    old = t[s:e]
    again = old.replace("Node ID=300 machiavelli helps you in montaillou" + CR, "Node ID=" + AGAIN + CR)
    new = ("CIfAction" + CR + "{" + CR + "If=" + B(*var_is("CIsGreaterThan", "0", "$Instigator")) + "Then=" + again + CR +
           "Else=" + old + CR + "Return failure if the If failes=0" + CR + "}")
    lhbuild.write_map(MAP, t[:s] + new + t[e:])
    return [MAP]


def main():
    done = var_file()
    t = lhbuild.read(TREE)
    if PAID not in t:
        s = t.index("Node ID=300 machiavelli helps you in montaillou" + CR)
        c = t.index("Custom Action=", s) + len("Custom Action=")
        ce = lhbuild.balanced(t, c) + len(CR)
        old = t[c:ce]
        assert old.count("Value to give=500") == 1
        t = t[:c] + b_with_old(old) + t[ce:]
        s3 = t.index("Node ID=300 machiavelli helps you in montaillou 3" + CR)
        e3 = t.index(DASH, s3)
        body = t[s3:e3]
        replies = body[body.index(CR + CR + "Requirement=") + len(CR + CR):]
        again = "Node ID=" + AGAIN + CR + "Text=" + LINE + CR + "Should Have Voiceover=0" + CR + CR + replies
        assert t.endswith("}" + CR)
        t = t[:-len("}" + CR)] + CR + DASH + CR + again.rstrip(CR) + CR + "}" + CR
        (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
        done.append(TREE)
    done += build_map()
    if done:
        register(done)
    print("machiavelli pays once:", done)


if __name__ == "__main__":
    main()
