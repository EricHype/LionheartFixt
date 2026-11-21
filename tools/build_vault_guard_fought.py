"""The vault job pays for quiet only if nobody fought the door man. A user report: "my companions immediately attacked the
guard, I still talked to him and chose the sneak by before they killed him. The quest giver still paid me as though i
snuck by."

The door man (`Secret Quest Guard`, spawned as `Vault Guard` from the Theif4 Sword cans) is made passive by his generator
with a blank target list, but keeps the cans' `Enemy` category, and companions attack anything in it. His four quiet
replies (Thief Friend, Speech 40, Barter 35, Sneak 35) set `Fixt Vault Door Quiet`, and Skulker pays 500 for quiet and
400 otherwise. Nothing reads whether he was hurt, so a fight that had already started could still be talked past.

  * The generator also removes `Enemy` (the den's own pacifier, line 8849's shape), so companions leave him alone.
  * Any damage to him sets the new `Fixt Vault Guard Fought` and gives `Enemy` back, through the generator's existing
    `CDamagedMessage` handler (the cans' own damaged scripts are left alone). So does his warning oval and the den's
    `Thief enemy trigger`, which his fight reply fires.
  * His quiet replies hide once he has been fought, and Skulker's quiet offer needs quiet AND not fought; the 400 offer
    takes either.

The variable is cloned from `Fixt Vault Door Quiet` and not exported. The generator is map-side (a den not yet entered);
the trees reach every save. A rerun is a no-op.

    python tools/build_vault_guard_fought.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

MAP = "Levels/Sewers/02 Thieves Congregation.zax"
GUARD_TREE = "Resources/Levels/Sewers/Dialog/SecretQuestGuard.DialogTree"
SKULKER = "Resources/Levels/Sewers/Dialog/Skulker.DialogTree"
VARS = "Resources/Derived Character Attributes/Game Scripting Variables/"
QUIET_REL = VARS + "Fixt Vault Door Quiet.DerivedCharacterAttribute"
FOUGHT_REL = VARS + "Fixt Vault Guard Fought.DerivedCharacterAttribute"
QUIET = "Derived Character Attributes/Game Scripting Variables/Fixt Vault Door Quiet"
FOUGHT = "Derived Character Attributes/Game Scripting Variables/Fixt Vault Guard Fought"


def var_cmp(cls, attr, value):
    return (cls, [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", attr)])), ("Operator", ""),
                  ("Operand2", ("CConstant", [("Constant Value", value)]))])


def req(expr):  # a Custom Requirement operand, as Skulker's own replies write it
    return ("CActionExpression", [("Action", ("CExpressionAction", [("Expression", expr), ("Character to get attributes from", "Player1")]))])


NOT_FOUGHT = req(var_cmp("CIsEqualTo", FOUGHT, "0"))
SET_FOUGHT = ("CAddCharacterModifierToCharacterAction", [
    ("Modifier Description", ""), ("Modification is permanent", "1"), ("Character to modify", "Player1"),
    ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
        ("Modification Amount", ("CConstant", [("Constant Value", "1")])), ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "0"), ("Derived character attribute to modify", FOUGHT)]))])),
    ("OPTIONAL Duration", ""), ("Expression Context", "Player1")])


def enemy_again(target):
    return ("CAddCategoryAction", [("Target Name", target), ("Categories to add", "Enemy")])


def bin_text(cls, a, b):
    """A binary expression from two already-written operand blocks (each ending in CR)."""
    return cls + CR + "{" + CR + "Operand1=" + a + "Operator=" + CR + "Operand2=" + b + "}" + CR


def flat(block):
    return "Action=" + B(*block)


def var_file():
    p = lhbuild.FX / FOUGHT_REL
    if p.exists():
        return []
    t = lhbuild.read(QUIET_REL)
    old_desc = t[t.index("\tDescription="):t.index(CR, t.index("\tDescription="))]
    t = t.replace("Fixt Vault Door Quiet", "Fixt Vault Guard Fought")
    t = t.replace(old_desc, "\tDescription=1 once anyone has hurt the thieves' vault door man. Skulker then pays the loud price, whatever was said to him.")
    t = t.replace("Include in character Import and Export=1", "Include in character Import and Export=0")
    assert "Quiet" not in t and "Import and Export=0" in t
    p.write_bytes(t.encode("latin-1"))
    return [FOUGHT_REL]


def prepend(t, at, items):
    """Insert actions at the head of the action array opening at or after `at`; returns (text, end of insertion)."""
    a = t.index("Action=Array", at)
    k = t.index("Item Count=", a)
    e = t.index(CR, k)
    n = int(t[k + len("Item Count="):e])
    ins = "".join(flat(i) for i in items)
    return t[:k] + "Item Count=%d" % (n + len(items)) + CR + ins + t[e + len(CR):]


def build_map():
    t = lhbuild.read(MAP)
    if "Categories to add=Enemy" in t and FOUGHT in t:
        return []
    g = t.index("\t\t\tName=Secret Quest Guard" + CR)
    end = t.index("\t\tLevel Part=", g)
    # order matters: edit from the bottom of the part up so earlier offsets stay valid
    after = t.index("After Action=CMultipleActionsAction", t.index("Canned AIs to Add=", g), end)
    t = prepend(t, after, [("CRemoveCategoryAction", [("Target Name", "$Instigator"), ("Categories To Remove", "Enemy")])])
    dmg = t.index("Message To Handle=CDamagedMessage", g)
    assert dmg < after
    t = prepend(t, dmg, [SET_FOUGHT, enemy_again("Vault Guard")])
    oval = t.index("Enter Action=CMultipleActionsAction", t.index("AI=CTouchingOvalTriggerAI", g))
    assert oval < dmg and "Node ID=Attack" in t[oval:dmg]
    t = prepend(t, oval, [enemy_again("$trigger")])
    r = t.index("\t\t\tName=Thief enemy trigger" + CR)
    t = prepend(t, t.index("Action=CMultipleActionsAction", r), [enemy_again("Vault Guard")])
    lhbuild.write_map(MAP, t)
    return [MAP]


def build_guard_tree():
    t = lhbuild.read(GUARD_TREE)
    if FOUGHT in t:
        return []
    for r in ("Thief Friend IS", "Speech moreequal 40", "Sneak moreequal 35"):
        line = "Requirement=" + r + CR
        assert t.count(line) == 1, r
        t = t.replace(line, line + "Custom Requirement=" + B(*NOT_FOUGHT))
    line = "Requirement=Barter moreequal 35" + CR + "Custom Requirement="
    i = t.index(line) + len(line)
    e = lhbuild.balanced(t, i) + len(CR)
    old = t[i:e]
    t = t[:i] + bin_text("CAND", old, B(*NOT_FOUGHT)) + t[e:]
    (lhbuild.FX / GUARD_TREE).write_bytes(t.encode("latin-1"))
    return [GUARD_TREE]


def build_skulker():
    t = lhbuild.read(SKULKER)
    if FOUGHT in t:
        return []
    jobs = [(node, value) for node, value in (("62 paid for the vault", "0"), ("63 nobody saw you", "1"))
            for _ in range(t.count("Go to node ID=" + node + CR))]
    assert len(jobs) == 4, "%s: expected each strongbox reply on both of Skulker's greetings" % SKULKER
    seen = {}
    for node, value in jobs:
        go = "Go to node ID=" + node + CR
        nth = seen[node] = seen.get(node, -1) + 1
        g = -1
        for _ in range(nth + 1):
            g = t.index(go, g + 1)
        c = t.rindex("Custom Requirement=CAND" + CR, 0, g) + len("Custom Requirement=")
        e = lhbuild.balanced(t, c) + len(CR)
        blk = t[c:e]
        assert ("Character Attribute=" + QUIET) in blk and ("Constant Value=" + value + CR) in blk
        s = blk.index("Operand2=") + len("Operand2=")
        se = lhbuild.balanced(blk, s) + len(CR)
        quiet = blk[s:se]
        if value == "0":  # the loud offer: not quiet, or fought
            new_op = bin_text("COR", quiet, B(*req(var_cmp("CIsGreaterThan", FOUGHT, "0"))))
        else:  # the quiet offer: quiet and not fought
            new_op = bin_text("CAND", quiet, B(*NOT_FOUGHT))
        t = t[:c] + blk[:s] + new_op + blk[se:] + t[e:]
    (lhbuild.FX / SKULKER).write_bytes(t.encode("latin-1"))
    return [SKULKER]


def main():
    done = var_file() + build_map() + build_guard_tree() + build_skulker()
    if done:
        register(done)
    print("vault guard fought:", done)


if __name__ == "__main__":
    main()
