"""The Knights Templar will not take the man who killed their own. Asked: "i killed estenban on the crossroads - shouldn't
that make me an enemy of the templars", then option 1 of three: close the order.

0.47.0 gave the `FACTION Templar Killer` title ("Enemy of the Knights Templar") to anyone who kills a Templar of the 13
order cans, but Guard Esteban has his own can and was never one of them, and nothing in the initiation read the title:
Javier would knight a man who had cut down a Port District patrol. 0.10.3 went further and let a character who lost
Esteban go on to Auric, because his death runs the same script whoever killed him.

  * **The title for Esteban.** His can's `Destroyed Effect Action` (the slot a generator's `CSetDestroyedScriptAction`
    leaves alone) now grants the title when the player or a companion damaged him, through `CForEachPlayerAction` as the
    map kill titles do. A can edit: Esteban spawned from now on. The goblin patrol leader's payment (`40 paid`) grants
    it too, which is a tree and reaches a save where he is dead and the contract unpaid.
  * **Who is refused.** The title, or `Esteban Dead` with the goblin contract ever taken: the only motive the game gives
    for killing him, and the fallback for a save past the payment. A knight (`Templar IS`) keeps his rank.
  * **Javier.** Every initiation reply on his three greetings (joining, the donation, each "I have completed...", the
    slavers, 0.10.3's "Sir Esteban is dead.") is hidden from such a character. In their place, once, *"Sir Esteban is
    dead."* (the contract) or *"I would like to become an initiate."* (the title alone) opens his refusal; its exit sets
    `Fixt Templar Order Refused` and fails every open initiation quest. Darsh's rescue is filed with the initiation but
    the goblin camp reads it, so it is left.
  * **Auric** stops sponsoring and stops handing out or taking in initiation tasks for the same character.

Trees and a new variable reach every save; the Esteban can reaches only a new spawn. A rerun is a no-op.

    python tools/build_templar_killer_refused.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH
from build_shrine_repairs import register

TD = "Resources/Levels/1 Barcelona/Dialog/Temple District/"
JAVIER = TD + "LordJavier.DialogTree"
AURIC = TD + "SirAuric.DialogTree"
PATROL = "Resources/Levels/Wilderness/Dialog/Goblin Patrol Leader.DialogTree"
ESTEBAN = "Resources/Levels/Wilderness/Character Templates/Guard Esteban.can"
VARS = "Resources/Derived Character Attributes/Game Scripting Variables/"
REFUSED = "Fixt Templar Order Refused"
REFUSED_REL = VARS + REFUSED + ".DerivedCharacterAttribute"
PERK = "Perks/!Event Title Perks/FACTION Templar Killer"
CONTRACT = "Levels/Wilderness/Quests/Kill Guard Esteban for the Goblin Patrol"
INIT = "Levels/1 Barcelona/Quests/Temple District/Knights Templar Initiation/"
QUESTS = ["Seek out Lord Javier", "Seek out Sir Auric", "Donate Gold to Knights Templar", "Seek out Guard Esteban",
          "Aid Sir Auric", "Discover Fate of the Lost Knight Patrol", "Forge a Lion Shield",
          "Eliminate Slaver menace in Barcelona", "Initiation Quest of the Knights Templar"]
NODE_E = "1 Fixt refuses Esteban's killer"
NODE_T = "1 Fixt refuses a Templar killer"
LINES = {
    "esteban": "Sir Esteban is dead.",
    "initiate": "I would like to become an initiate.",
    NODE_E: ("Spare me your words. The goblins at the crossroads boast of the coin they paid for Sir Esteban's life, and "
             "of the hand that took it. No one who sold the blood of this order will ever wear its cross. Leave my "
             "cathedral, and do not come to me seeking honor again."),
    NODE_T: ("You? The names of the brothers you cut down were read aloud in this cathedral, and I said the prayers for "
             "them myself. No one who has spilled the blood of this order will ever wear its cross. Leave my cathedral, "
             "and do not come to me seeking honor again."),
    "go": "Then I will go.",
}
for v in LINES.values():
    assert "—" not in v and "--" not in v

JAVIER_GATED = {
    "Sir Auric said he will sponsor me to become a Knight Templar.",
    "Sir Auric said he will sponsor me in becoming a Knight Templar.",
    "I have decided that I would like to become an initiate.",
    "I would like to donate the thousand gold.",
    "Sir Esteban is dead.",
    "I have completed Esteban's quests.",
    "I have completed Auric's quest.",
    "I have completed Auric's quests.",
    "I have forged my Lion Shield.",
    "I have convinced the leader of the slavers to leave. He will not trouble Barcelona again.",
    "I have convinced the leader of the Slavers to leave. He will not trouble Barcelona again.",
    "I have eliminated the slavers.",
}
JAVIER_NODES = ["1 Conversation Start", "3 Return Dialogue", "5 questions"]
AURIC_GATED = {
    "How can I become a knight?",
    "Lord Javier sent me here to get my next initiation quest.",
    "I am ready for an initiation quest.",
    "The knight died in the sewers.",
    "I rescued the knight in the Sewers.",
    "Benito the thief has been dealt with.",
}
AURIC_NODES = ["3 Return Dialogue", "5 questions", "20 knight", "3 Return Hostile", "1 Conversation Start Tainted Auric Listens",
               "30 armory", "100 return with quest"]


def expr_action(action):
    return B("CActionExpression", [("Action", action)])


def cand(a, b):
    return "CAND" + CR + "{" + CR + "Operand1=" + a + "Operator=" + CR + "Operand2=" + b + "}" + CR


def cnot(a):
    return "CExpressionNot" + CR + "{" + CR + "Operand1=" + a + "}" + CR


def var_above_zero(name):
    return B("CIsGreaterThan", [("Operand1", ("CVariableDerivedCharacterAttribute", [
        ("Character Attribute", "Derived Character Attributes/Game Scripting Variables/" + name)])), ("Operator", ""),
        ("Operand2", ("CConstant", [("Constant Value", "0")]))])


HAS_TITLE = B("CHasPerkExpression", [("Perks To Check For", ("Array", [("Item Count", "1"), ("Perk To Check For", PERK)]))])
CONTRACT_KILL = cand(var_above_zero("Esteban Dead"), expr_action(("CWasQuestEverActivatedAction", [("Quest", CONTRACT)])))
KILLER = lhbuild.cor(HAS_TITLE, CONTRACT_KILL)
OPEN = cand(cnot(var_above_zero(REFUSED)),
            cnot("CUseCannedExpressionExpression" + CR + "{" + CR + "Canned Expression=Dialog/Requirements/Faction/Templar IS" + CR + "}" + CR))


def grant(who="$Instigator"):
    return ("CConditionalAction", [
        ("Try Action", ("CExpressionAction", [
            ("Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [("Item Count", "1"), ("Perk To Check For", PERK)]))])),
            ("Character to get attributes from", who)])),
        ("Succeed Action", ""),
        ("Fail Action", ("CGiveCharacterPerkAction", [("Character to give perk to", who), ("Perk to give", PERK)])),
        ("Return failure if the TryAction failes", "0")])


SET_REFUSED = ("CAddCharacterModifierToCharacterAction", [
    ("Modifier Description", REFUSED), ("Modification is permanent", "1"), ("Character to modify", "Player#1-9#"),
    ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
        ("Modification Amount", ("CConstant", [("Constant Value", "1")])), ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "0"),
        ("Derived character attribute to modify", "Derived Character Attributes/Game Scripting Variables/" + REFUSED)]))])),
    ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])


def gate_replies(t, nodes, texts, gate):
    """AND `gate` into every reply of `nodes` whose text is in `texts`. Returns the text and the number gated."""
    n = 0
    for nid in nodes:
        heads = [i for i in range(len(t)) if t.startswith("Node ID=" + nid + CR, i) and (i == 0 or t[i - 2:i] == CR)]
        assert len(heads) == 1, (nid, len(heads))
        s = heads[0]
        e = t.find(DASH, s)
        e = len(t) if e < 0 else e
        k = s
        while True:
            r = t.find(CR + "Reply Text=", k, e)
            if r < 0:
                break
            line_end = t.index(CR, r + 2)
            text = t[r + len(CR + "Reply Text="):line_end]
            k = line_end
            if text not in texts:
                continue
            q = t.rindex(CR + "Requirement=", s, r) + len(CR)
            q_end = t.index(CR, q) + len(CR)
            if t.startswith("Custom Requirement=", q_end):
                v = q_end + len("Custom Requirement=")
                ve = lhbuild.balanced(t, v)
                new = cand(gate, t[v:ve] + CR)
                t = t[:v] + new + t[ve + len(CR):]
            else:
                t = t[:q_end] + "Custom Requirement=" + gate + t[q_end:]
            n += 1
            e = t.find(DASH, s)
            e = len(t) if e < 0 else e
            k = t.index(CR + "Reply Text=" + text + CR, q) + 2
    return t, n


def refusal_reply(text, node, gate):
    return ("Requirement=!None" + CR + "Custom Requirement=" + gate + "Reply Text=" + text + CR + "Go to node ID=" + node + CR +
            "Icon=Quest Icon" + CR + CR)


def build_javier():
    t = lhbuild.read(JAVIER)
    if "Node ID=" + NODE_E + CR in t:
        return []
    t, n = gate_replies(t, JAVIER_NODES, JAVIER_GATED, cnot(KILLER))
    assert n == 26, n
    by_contract = cand(OPEN, CONTRACT_KILL)
    by_title = cand(OPEN, cand(HAS_TITLE, cnot(CONTRACT_KILL)))
    new_replies = refusal_reply(LINES["esteban"], NODE_E, by_contract) + refusal_reply(LINES["initiate"], NODE_T, by_title)
    for nid in JAVIER_NODES:
        s = t.index(CR + "Node ID=" + nid + CR) + len(CR)
        e = t.index(DASH, s)
        anchor = "Reply Text=Tell me about this Cathedral." + CR
        a = t.index(anchor, s, e)
        k = t.rindex(CR + CR + "Requirement=", s, a) + len(CR + CR)
        t = t[:k] + new_replies + t[k:]
    exit_actions = [SET_REFUSED] + [("CSetQuestSatusToFailedIfActiveAction", [("Quest", INIT + q)]) for q in QUESTS]
    exit_reply = ("Requirement=!None" + CR + "Reply Text=" + LINES["go"] + CR + "Go to node ID=" + CR +
                  "Custom Action=" + B("CMultipleActionsAction", [("Action", ("Array", [("Item Count", str(len(exit_actions)))] +
                                                                              [("Action", a) for a in exit_actions]))]) +
                  "Icon=Exit Icon" + CR + "Is Default Reply=1" + CR)
    nodes = ["Node ID=" + nid + CR + "Text=" + LINES[nid] + CR + "Should Have Voiceover=0" + CR + CR + exit_reply
             for nid in (NODE_E, NODE_T)]
    assert t.endswith("}" + CR)
    t = t[:-len("}" + CR)].rstrip(CR) + CR + CR + "".join(DASH + CR + x for x in nodes) + "}" + CR
    (lhbuild.FX / JAVIER).write_bytes(t.encode("latin-1"))
    return [JAVIER]


def build_auric():
    t = lhbuild.read(AURIC)
    if PERK in t:
        return []
    t, n = gate_replies(t, AURIC_NODES, AURIC_GATED, cnot(KILLER))
    assert n == 11, n
    (lhbuild.FX / AURIC).write_bytes(t.encode("latin-1"))
    return [AURIC]


def build_patrol():
    t = lhbuild.read(PATROL)
    if PERK in t:
        return []
    s = t.index("Node ID=40 paid" + CR)
    c = t.index("Item Count=2" + CR, s)
    k = t.index("Action=CGiveMoneyToAllPlayersAction", c)
    t = t[:c] + "Item Count=3" + CR + t[c + len("Item Count=2" + CR):k] + "Action=" + B(*grant()) + t[k:]
    (lhbuild.FX / PATROL).write_bytes(t.encode("latin-1"))
    return [PATROL]


def build_esteban():
    t = lhbuild.read(ESTEBAN)
    if PERK in t:
        return []
    s = t.index("\t\tDestroyed Effect Action=CMultipleActionsAction" + CR)
    c = t.index("Item Count=2" + CR, s)
    e = lhbuild.balanced(t, s)
    close = t.rindex("\t\t\t}" + CR, s, e)  # the Array's closing brace line
    extra = "Action=" + B("CIfAction", [
        ("If", ("CWasDamagedByPlayerAction", [("Entity To Check For Damage", "$Trigger")])),
        ("Then", ("CForEachPlayerAction", [("Action", grant())])),
        ("Else", ""), ("Return failure if the If failes", "0")])
    t = t[:close] + extra + t[close:]
    t = t[:c] + "Item Count=3" + CR + t[c + len("Item Count=2" + CR):]
    lhbuild.write_map(ESTEBAN, t)
    return [ESTEBAN]


def build_var():
    if (lhbuild.FX / REFUSED_REL).exists():
        return []
    v = lhbuild.read(VARS + "Esteban Dead.DerivedCharacterAttribute").replace("Esteban Dead", REFUSED)
    v = v.replace("Description=" + CR, "Description=1 means Lord Javier has refused the player the Templar initiation for killing the order's own." + CR)
    (lhbuild.FX / REFUSED_REL).write_bytes(v.encode("latin-1"))
    return [REFUSED_REL]


def main():
    done = build_var() + build_javier() + build_auric() + build_patrol() + build_esteban()
    if done:
        register(done)
    print("templar killer refused:", done)


if __name__ == "__main__":
    main()
