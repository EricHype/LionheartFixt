"""The trolls' hide is the chief's to give, and the lost boy can be sold out. Asked for after the 0.99.24 voice pass.

**The entrance troll no longer hands over a hide.** His wererat reply had the player say *"I am the reason no more of your
people are being dragged off in the dark"*, a thing nothing in the game tells you, and it was gated on Quinn's hide errand
because it paid that errand. Now the player says only what they know (*"The wererats are finished. The beggars' guild is
done."*), on any of the three routes that finish them, and the troll makes the connection himself and sends you to the
chief, with the peace. A hide is one of their dead, so asking for it is the chief's business: he gives one for the
wererats as a debt (`134 the hide owed`), beside the existing route for speaking to Enrique for them (`133 the hide`).

**Selling the boy out.** The trolls already have him, so what the player sells is silence: *"Keep him. Nobody up there will
miss one beggar boy. Pay me, and I tell them he drowned."* The chief is afraid of exactly that, men coming down for a
missing boy (*"A troll in your streets rings a bell"*). He pays in coin taken from the dead on the rock, which is no use to
him in the dark: 150, against the 200 he asks to let the boy go. It costs 75 karma, sets `Fixt Tomas Sold`, and hides the
chief's boy reply for good. Marisol then has one more answer, *"He is dead. The trolls had him."*, which fails the quest;
the smith's later *"Send Tomas"* reply already needs the quest found or done, so it never appears.

**A Slayer of Innocents** (`Child Killer`, given for harming a child) is known to them only as *"The rock tells us of your
misdeeds."*: the trolls cannot know whose child. The Speech plea *"He is a child..."* does not work from that mouth; it
gets a refusal and the price. And the silence deal is met as expected, without the contempt.

**The double-cross.** Nothing on Tomas's chamber asks the trolls: `secret door1` is found by searching and opens onto
`Save Tomas relay` whatever was agreed. So a player who sold their silence can still free him, and that is theft from the
trolls as surely as the ore chest. The rescue plays as ever, then at the end of it (`Back to Player cam`, whose arrival ends
the scene) the chief says *"Coin, and the small one. Both."* over his head and the peace breaks exactly as for the chest.
The karma stays spent. Marisol's lie (*"He is dead"*) shows only while he is still missing.

Run after `build_troll_voice.py`. The dialogue reaches every save; the double-cross is in the Troll Pit map, so it reaches a
pit not yet entered, and new games. A rerun is a no-op.

    python tools/build_troll_choices.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH
from build_shrine_repairs import register

TROLL = "Resources/Levels/Sewers/Dialog/Warning Troll.DialogTree"
MARISOL = "Resources/Levels/Sewers/Dialog/marisol.dialogtree"
VARS = "Derived Character Attributes/Game Scripting Variables/"
SOLD = "Fixt Tomas Sold"
SOLD_DCA = "Resources/" + VARS + SOLD + ".DerivedCharacterAttribute"
TOMAS_QUEST = "Levels/1 Barcelona/Quests/Port District/Find the lost boy Tomas in the Sewers"
QUINN = "Levels/1 Barcelona/Quests/Gate District/Troll Hide for Quinn"
HIDE = "Inventory/Specific Item Cans/Quest Items/Lava Troll Hide"
CHILD_KILLER = "Perks/!Event Title Perks/Child Killer"
OLD_WERERAT = "The wererats are finished. Whatever else you think of me, I am the reason no more of your people are being dragged off in the dark."
WERERAT = "The wererats are finished. The beggars' guild is done."
PLEA = "He is a child. He was sent by men who are not children, and it is those men who owe you. Take it out of them, not out of him."
SELL = "Keep him. Nobody up there will miss one beggar boy. Pay me, and I tell them he drowned."
PAY = "150"
KARMA = "-75"

TEXT = {
    "30 troll trade": "<It looks at you a long time.> Wererats gone? They take Trolls. In the dark. Many. Now none. We count. You go to chief. My people not touch you.",
    "134 the hide owed": "<He is quiet a long time.> A hide is one of ours. You ask for one of our dead. You ended the wererats, and Trolls do not like to owe. Take one from the field. My word on it.",
    "135 the silence": "<He looks at you a long time.> Your own small one. You sell him for coin. <He holds out coin from the dead on the rock.> Go. Do not come back to my rock.",
    "136 the silence expected": "<He does not wait.> The rock tells us of your misdeeds. I wondered if you would ask. <He holds out coin from the dead on the rock.> Here. Go.",
    "137 the rock tells": "You say child. You. <He does not move.> The rock tells us of your misdeeds. No. You pay, or you go.",
    "36 dead": "<She goes very still.> No. No, he knows the tunnels, he always comes back... <She turns and runs.>",
    "94 both": "Coin, and the small one. Both.",
}
FOUND_STATE = "ZZKX5PFU"
MAP = "Levels/Sewers/05 Troll Pit.zax"


def act(e):
    return CActionExpression(e)


def CActionExpression(action):
    return ("CActionExpression", [("Action", action)])


def done(q):
    return act(("CIsQuestCompletedAction", [("Quest", q)]))


def NOT(x):
    return ("CExpressionNot", [("Operand1", x)])


def AND(a, b):
    return ("CAND", [("Operand1", a), ("Operator", ""), ("Operand2", b)])


def OR(a, b):
    return ("COR", [("Operand1", a), ("Operator", ""), ("Operand2", b)])


def wererats_finished():
    return OR(done("Levels/Sewers/Quests/Discover a cure for wererat lycanthropy"),
              OR(done("Levels/Sewers/Quests/Kill The Beggar Master"), done("Levels/Sewers/Quests/Help the Thieves Destroy the Beggars Guild")))


def child_killer():
    return act(("CExpressionAction", [("Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [("Item Count", "1"), ("Perk To Check For", CHILD_KILLER)]))])),
                                      ("Character to get attributes from", "$Instigator")]))


def has_hide():
    return act(("CActionCheckForInventoryItem", [("Who to give check", "$instigator"), ("Inventory Item To Check For", HIDE)]))


def give_hide():
    return ("CActionGiveStandardInventoryItem", [("Who to give to", "$instigator"), ("Delete Trigger", "0"), ("Notify Player", "1"),
                                                 ("Inventory Item To Give", HIDE), ("Additions to add", ("Array", [("Item Count", "0")]))])


def modifier(who, attr, amount, accumulate):
    return ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", ""), ("Modification is permanent", "0"), ("Character to modify", who),
        ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", ("CConstant", [("Constant Value", amount)])), ("Modification amount is a percent", "0"),
            ("Allow Accumulation", accumulate), ("Derived character attribute to modify", "Derived Character Attributes/" + attr)]))])),
        ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])


def sold():
    return ("CIsGreaterThan", [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", VARS + SOLD)])),
                               ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "0")]))])


def reply(text, go="", req="!None", creq=None, action=None, icon=None):
    """`Requirement=` names a requirement can or `!None`; an expression gate goes in `Custom Requirement=`."""
    if not isinstance(req, str):
        req, creq = "!None", (AND(req, creq) if creq else req)
    out = "Requirement=" + req + CR
    if creq:
        out += "Custom Requirement=" + B(*creq)
    out += "Reply Text=" + text + CR + "Go to node ID=" + go + CR
    if action:
        out += "Custom Action=" + B(*action)
    if icon:
        out += "Icon=" + icon + CR
    return out + CR


def node_span(t, nid):
    i = t.index("Node ID=" + nid + CR)
    j = t.find(DASH, i)
    return i, (j if j >= 0 else t.rindex("}" + CR))


def reply_start(t, nid, text):
    """Where the reply with this text begins (its Requirement= line) inside node nid."""
    i, j = node_span(t, nid)
    k = t.index("Reply Text=" + text + CR, i, j)
    return t.rindex(CR + CR + "Requirement=", i, k) + len(CR + CR)


def add_node(t, nid, text, replies):
    assert len(text) <= 200, (nid, len(text))
    body = "Node ID=" + nid + CR + "Text=" + text + CR + "Should Have Voiceover=0" + CR + (CR + "".join(replies).rstrip(CR) + CR if replies else "")
    k = t.rindex("}" + CR)
    return t[:k] + DASH + CR + body + t[k:]


def build_dca():
    if (lhbuild.FX / SOLD_DCA).exists():
        return
    t = lhbuild.read("Resources/" + VARS + "Fixt Fernand Stride.DerivedCharacterAttribute")
    t = t.replace("Fixt Fernand Stride", SOLD)
    t = re.sub(r"Description=[^\r\n]*", "Description=1 once the player has sold out the lost boy Tomas to the troll chief (tools/build_troll_choices.py).", t)
    (lhbuild.FX / SOLD_DCA).write_bytes(t.encode("latin-1"))
    register([SOLD_DCA])


def build_troll():
    t = lhbuild.read(TROLL)
    if "Node ID=134 the hide owed" + CR in t:
        return 0
    # 1. the wererat news: what the player knows, on any route that finished them, and no hide
    n = 0
    for nid in ("01 Greeting", "20 no trust"):
        s = reply_start(t, nid, OLD_WERERAT)
        e = t.index("Reply Text=" + OLD_WERERAT + CR, s)
        t = t[:s] + "Requirement=!None" + CR + "Custom Requirement=" + B(*wererats_finished()) + "Reply Text=" + WERERAT + CR + \
            t[e + len("Reply Text=" + OLD_WERERAT + CR):]
        n += 1
    i, j = node_span(t, "30 troll trade")
    blk = t[i:j]
    m = re.search(r"Text=[^\r\n]*\r\n", blk)
    blk = blk[:m.start()] + "Text=" + TEXT["30 troll trade"] + CR + blk[m.end():]
    blk = blk.replace("Reply Text=<Take it.> Your people can sleep." + CR, "Reply Text=Then I will go to your chief." + CR, 1)
    g = blk.index("Action=CActionGiveStandardInventoryItem")
    blk = blk[:g] + blk[lhbuild.balanced(blk, g) + len(CR):]
    assert blk.count("Item Count=3" + CR) == 1 and HIDE not in blk
    blk = blk.replace("Item Count=3" + CR, "Item Count=2" + CR, 1)
    t = t[:i] + blk + t[j:]
    # 2. the chief gives a hide for the wererats, beside the Enrique route
    errand = AND(act(("CWasQuestEverActivatedAction", [("Quest", QUINN)])), AND(NOT(done(QUINN)), NOT(has_hide())))
    gate = AND(errand, AND(wererats_finished(), NOT(done("Levels/Sewers/Quests/Speak for the Trolls"))))
    k = reply_start(t, "95 the chief", "Nothing yet. I am only looking.")
    t = t[:k] + reply("The herbalist in the city needs the hide of a lava troll. I am asking you for one.", "134 the hide owed", gate, icon="Quest Icon") + t[k:]
    t = add_node(t, "134 the hide owed", TEXT["134 the hide owed"],
                 [reply("<Take it.> I will not forget what it cost.", action=give_hide(), icon="Quest Icon")])
    # 3. the silence deal, and the Slayer of Innocents' plea
    k = reply_start(t, "96 the boy", PLEA)
    e = t.index("Reply Text=" + PLEA, k)
    assert t[k:e] == "Requirement=Speech moreequal 45" + CR, t[k:e]
    t = t[:e] + "Custom Requirement=" + B(*NOT(child_killer())) + t[e:]
    k = reply_start(t, "96 the boy", "I will come back to this.")
    take = lhbuild.multi([("CGiveMoneyAction", [("Give to", "$instigator"), ("Value to give", PAY)]),
                          modifier("$Instigator", "Karma", KARMA, "1"),
                          modifier("Player1", "Game Scripting Variables/" + SOLD, "1", "0")])
    t = t[:k] + reply(PLEA, "137 the rock tells", "Speech moreequal 45", child_killer(), icon="Speach Skill Icon") + \
        reply(SELL, "135 the silence", creq=NOT(child_killer())) + reply(SELL, "136 the silence expected", creq=child_killer()) + t[k:]
    for nid in ("135 the silence", "136 the silence expected"):
        t = add_node(t, nid, TEXT[nid], [reply("<Take the coin.>", action=take, icon="Exit Icon")])
    t = add_node(t, "94 both", TEXT["94 both"], [])
    t = add_node(t, "137 the rock tells", TEXT["137 the rock tells"],
                 [reply("Name your price, then.", "97 the price", icon="Quest Icon"), reply("I will come back to this.", icon="Exit Icon")])
    # 4. once he is sold, the chief's boy reply is gone
    k = reply_start(t, "95 the chief", "I am looking for a human child. Small, and not from down here. He came into the dark and did not come out again.")
    e = t.index("Reply Text=", k)
    head = t[k:e]
    # its gate is in Custom Requirement (Requirement is !None), so that is the field to widen
    assert head.startswith("Requirement=!None" + CR + "Custom Requirement="), head[:80]
    old = head[len("Requirement=!None" + CR + "Custom Requirement="):]
    wrapped = B("CAND", [("Operand1", "RAW"), ("Operator", ""), ("Operand2", NOT(sold()))]).replace("Operand1=RAW" + CR, "Operand1=" + old, 1)
    t = t[:k] + "Requirement=!None" + CR + "Custom Requirement=" + wrapped + t[e:]
    (lhbuild.FX / TROLL).write_bytes(t.encode("latin-1"))
    register([TROLL])
    return n


def build_marisol():
    t = lhbuild.read(MARISOL)
    if "Node ID=36 dead" + CR in t:
        return 0
    k = reply_start(t, "4 Return dialogue 2", "No, I was not able to.")
    fail = ("CSetQuestSatusToFailedIfActiveAction", [("Quest", TOMAS_QUEST)])
    # the lie is only on offer while he is still missing: a double-cross that freed him leaves the truth to tell
    still_missing = NOT(act(("CIsQuestStateTheCurrentStateAction", [("Quest", TOMAS_QUEST), ("State", FOUND_STATE)])))
    t = t[:k] + reply("He is dead. The trolls had him.", "36 dead", AND(sold(), still_missing), action=fail) + t[k:]
    t = add_node(t, "36 dead", TEXT["36 dead"], [reply("")])
    (lhbuild.FX / MARISOL).write_bytes(t.encode("latin-1"))
    register([MARISOL])
    return 1


def build_double_cross():
    from build_troll_voice import break_peace
    z = lhbuild.read(MAP)
    i = z.index("\t\t\tName=Back to Player cam" + CR)
    s = z.rindex("\t\tLevel Part=", 0, i)
    e = lhbuild.balanced(z, s)
    part = z[s:e]
    if "94 both" in part:
        return 0
    m = re.search(r"Camera Arrived Action=CMultipleActionsAction\r\n(\t*)\{\r\n\t*Action=Array\r\n\t*\{\r\n\t*Item Count=2\r\n", part)
    assert m, "camera arrived"
    peace = ("CCheckExistenceAction", [("Name To Check For", "Troll Peace Keeper"), ("Desired Minimum Count", "1")])
    react = lhbuild.multi([lhbuild.balloon(lhbuild_tree(), "94 both", "Troll Chief", "-70"), break_peace()])
    cross = ("CIfExpressionAction", [("If Expression", sold()), ("Character to get attributes from", "Player1"),
                                     ("Then", lhbuild.if_action(peace, react)), ("Else", "")])
    # the existing two actions end the scene and clear the fog; the double-cross goes last, once control is back.
    # Insert at the start of the array's closing-brace line, never by searching for a brace inside it
    a = part.index("Item Count=2" + CR, m.start())
    part = part[:a] + "Item Count=3" + CR + part[a + len("Item Count=2" + CR):]
    end = lhbuild.balanced(part, part.index("Action=Array", m.start()))
    close = part.rindex(CR, 0, end) + len(CR)
    assert part[close:end].strip("\t") == "}", repr(part[close:end])
    part = part[:close] + "Action=" + B(*cross) + part[close:]
    z = z[:s] + part + z[e:]
    lhbuild.write_map(MAP, z)
    register([MAP])
    return 1


def lhbuild_tree():
    return "Levels/Sewers/Dialog/Warning Troll"


def main():
    build_dca()
    print("troll replies reworded:", build_troll(), "| marisol:", build_marisol(), "| double-cross:", build_double_cross())


if __name__ == "__main__":
    main()
