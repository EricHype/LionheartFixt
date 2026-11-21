"""Relican takes the Sceptre of Bone when he asks for it. A user report: "When relican asks me to get the scepter of bone,
i have it in my inventory, I can't turn it in to him without leaving the conversation."

`40 dark wielder task 1` is where Relican asks. Its only turn-in is vanilla's `I already have the Sceptre`, for the
spirited Sceptre, and it goes straight to `45 Rod Bone Returned`. That skips what `I will find the Sceptre.` does
(starts the quest, retires `Relican started giving quests already to player`, the Wielder Rank floor), and it never
completes the quest. The lifeless Sceptre (`... NO Spirit`, from DaVinci's
secret chamber) had no reply at all there or on `40 sceptre`: Fixt's `I have the Sceptre, but it is a dead thing`
(`47 Fixt Relican Binds Shell`) needs the quest already started, so it only appears on the next conversation.

  * A new `dead thing` reply on both asking nodes, for whoever holds the lifeless Sceptre, to `48 Fixt Relican Names the
    Madman`: Relican names the enchanter under the well, who can bind it properly (the 0.39.0 route, with its amulet and
    ring), and offers his own crude bind instead. *"Do it yourself, then."* runs the `I will find` actions, then the
    return reply's swap and the completion, to `47`. *"I will take it to the enchanter."* runs the `I will find` actions
    only, so the journal shows the lifeless-Sceptre state, which now names the enchanter too.
  * Vanilla's `I already have the Sceptre` gains the same `I will find` actions and the completion.

Neither pays XP itself: both lead on to `40 dark wielder task 2`, whose replies pay `Find Scepter of Bone Relican XP`,
which is how vanilla pays the turn-in at the ask. (The return dialogue's turn-ins pay there too and again in task 2,
vanilla's own double payment; left alone.)

Relican's bind is the crude one, in both places he does it (here and his return dialogue's `dead thing` reply): it
hands over `Fixt Crude Sceptre of Bone` (+1, not +2, to the eight Thought and Tribal disciplines; otherwise the
spirited Sceptre) and costs 25 Karma, the ether plane's own price for taunting the Enchanter. The Enchanter's bind
still gives the full Sceptre. Only Relican's tree reads the spirited Sceptre, and both crude binds complete the quest
in the same reply, so no later check needs the full one.

Tree-side: every save. A rerun is a no-op.

    python tools/build_relican_sceptre_at_ask.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

TREE = "Resources/Levels/1 Barcelona/Dialog/La Calle Perdida/Lord Relican.DialogTree"
ROD = "Inventory/Specific Item Cans/Quest Items/Wielder DARK Quest Rod Bone "
SEP = "------------------------------------------------------------"
MARK = "Fixt: lifeless Sceptre at the ask"
DASH = "-" * 60
ITEMS = "Resources/Inventory/Specific Item Cans/Quest Items/"
CRUDE_REL = ITEMS + "Fixt Crude Sceptre of Bone.InventoryItem"
CRUDE = "Inventory/Specific Item Cans/Quest Items/Fixt Crude Sceptre of Bone"
KARMA = ("CAddCharacterModifierToCharacterAction", [
    ("Modifier Description", "Karma"), ("Modification is permanent", "0"), ("Character to modify", "Player#1-9#"),
    ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
        ("Modification Amount", ("CConstant", [("Constant Value", "-25")])), ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "1"), ("Derived character attribute to modify", "Derived Character Attributes/Karma")]))])),
    ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])
NAMES = "48 Fixt Relican Names the Madman"
QUEST = "Resources/Levels/1 Barcelona/Quests/Calle Perdida/Wielder Initiation Quests/Create a Rod Of Bone.Quest.txt"
LINES = {
    "names": "Empty. Amontep's darkwood, and nothing in it. There is a madman in a prison under the well in this very city, an enchanter who has spent an age hoarding the spirits of everyone who fell in. He could fill it properly, if you can stand his company. Or hold it out now and I will do it myself. It will be crude, and the thing I put in it will hate you.",
    "bind": "Do it yourself, then.",
    "madman": "I will take it to the enchanter.",
    "crude": "Enchanted darkwood with a spirit forced into it, and the spirit resents you. Carrying the sceptre confers 1 skill point in the Thought and Tribal spell disciplines. Equipping the sceptre may cause others to react negatively towards you. When used as a magical club, it is a One-Handed weapon that does %s[damage].",
    "journal": "The Sceptre of Bone is in your hands, but it is lifeless: fashioned darkwood and nothing more, an empty shell without a spirit to power it. Relican says a mad enchanter imprisoned beneath the well in La Calle Perdida could bind a spirit into it, or Relican will do it himself, crudely, if asked.",
}
for _v in LINES.values():
    assert "—" not in _v and "--" not in _v


def node_span(t, nid):
    s = t.index("Node ID=" + nid + CR)
    e = t.index(SEP, s)
    return s, e


def reply_span(t, s, e, text):
    """(start, end) of the reply whose Reply Text is `text` inside [s, e): from its Requirement= line to the blank line."""
    r = t.index("Reply Text=" + text + CR, s, e)
    a = t.rindex(CR + CR + "Requirement=", s, r) + len(CR + CR)
    b = t.find(CR + CR, r)
    b = e if b == -1 or b > e else b + len(CR)
    return a, b


def actions_of(reply):
    """The inner action list of a reply's `Custom Action=CMultipleActionsAction` (text between Item Count and the array close)."""
    i = reply.index("Custom Action=CMultipleActionsAction" + CR)
    k = reply.index("Item Count=", i)
    n = int(reply[k + len("Item Count="):reply.index(CR, k)])
    body_start = reply.index(CR, k) + len(CR)
    arr_open = reply.rindex("Action=Array" + CR, 0, k) + len("Action=")
    arr_end = lhbuild.balanced(reply, arr_open)
    body = reply[body_start:reply.rindex("}", 0, arr_end)]
    return n, body


def multi(n, body):
    return "Custom Action=CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=%d" % n + CR + body + "}" + CR + "}" + CR


def crude_item():
    """The spirited Sceptre with half its bound-spirit bonus: +1, not +2, to the eight Thought and Tribal disciplines."""
    t = lhbuild.read(ITEMS + "Wielder DARK Quest Rod Bone WITH Spirit.InventoryItem")
    s = t.index("Modifier Description=Bound Spirit")
    e = t.index("PlugIn Behavior=CPlugInBehaviorPutDownAction", s)
    block = t[s:e]
    assert block.count("Constant Value=2" + CR) == 8 and "Constant Value=1" + CR not in block
    t = t[:s] + block.replace("Constant Value=2" + CR, "Constant Value=1" + CR) + t[e:]
    old_desc = t[t.index("	Description=Enchanted darkwood"):t.index(CR, t.index("	Description=Enchanted darkwood"))]
    for old, new in (("Display Name=Sceptre of Bone" + CR, "Display Name=Crude Sceptre of Bone" + CR),
                     (old_desc, "	Description=" + LINES["crude"]),
                     ("Origonal Item=" + ROD + "WITH Spirit", "Origonal Item=" + CRUDE)):
        assert t.count(old) == 1, old[:40]
        t = t.replace(old, new)
    lhbuild.write_map(CRUDE_REL, t)


def build():
    t = lhbuild.read(TREE)
    if MARK in t:
        return False
    s, e = node_span(t, "40 dark wielder task 1")
    fa, fb = reply_span(t, s, e, "I will find the Sceptre.")
    n_find, find_body = actions_of(t[fa:fb])
    assert n_find == 3 and "Relican started giving quests already to player" in find_body
    # the return dialogue's dead-thing reply carries the swap, the completion and the XP. Relican's bind is the crude
    # one: it now hands over the weaker Crude Sceptre and costs Karma, and the ask's copy below inherits both
    d = t.index("Reply Text=I have the Sceptre, but it is a dead thing")
    da = t.rindex(CR + CR + "Requirement=", 0, d) + len(CR + CR)
    db = t.index(CR + CR, d) + len(CR)
    ret = t[da:db]
    give = "Inventory Item To Give=" + ROD + "WITH Spirit" + CR
    assert ret.count(give) == 1 and ret.count("Item Count=4" + CR) == 1
    ret = ret.replace(give, "Inventory Item To Give=" + CRUDE + CR).replace("Item Count=4" + CR, "Item Count=5" + CR)
    ret = ret.replace("Action=CSetQuestSatusToCompletedAction", "Action=" + B(*KARMA) + "Action=CSetQuestSatusToCompletedAction", 1)
    t = t[:da] + ret + t[db:]
    db = da + len(ret)
    n_dead, dead_body = actions_of(t[da:db])
    assert n_dead == 5 and ROD + "NO Spirit" in dead_body and CRUDE in dead_body
    reply_line = t[t.index("Reply Text=", da):t.index(CR, t.index("Reply Text=", da)) + len(CR)]
    # no XP here: every turn-in lands on `40 dark wielder task 2`, whose replies pay `Find Scepter of Bone Relican XP`,
    # and that is vanilla's at-the-ask payment
    xp = dead_body.index("Action=CGiveExperiencePointsToAllPlayersAction")
    xp_end = lhbuild.balanced(dead_body, xp + len("Action=")) + len(CR)
    dead_body = dead_body[:xp] + dead_body[xp_end:]
    n_dead -= 1
    complete = dead_body[dead_body.index("Action=CSetQuestSatusToCompletedAction"):]
    assert complete.count("Action=C") == 1 and "Get XP" not in dead_body

    new_reply = ("Requirement=!None" + CR + "Custom Requirement=CActionExpression" + CR + "{" + CR +
                 "Action=CActionCheckForInventoryItem" + CR + "{" + CR + "Who to give check=$instigator" + CR +
                 "Inventory Item To Check For=" + ROD + "NO Spirit" + CR + "}" + CR + "}" + CR +
                 reply_line + "Go to node ID=" + NAMES + CR +
                 "Action work in progress=(" + MARK + ")" + CR + "Icon=Quest Icon" + CR + CR)
    names = lhbuild.node(NAMES, LINES["names"], [])
    names += (CR + "Requirement=!None" + CR + "Reply Text=" + LINES["bind"] + CR + "Go to node ID=47 Fixt Relican Binds Shell" + CR +
              multi(n_find + n_dead, find_body + dead_body) + "Icon=Quest Icon" + CR +
              CR + "Requirement=!None" + CR + "Reply Text=" + LINES["madman"] + CR + "Go to node ID=" + CR +
              multi(n_find, find_body) + "Icon=Quest Icon" + CR + "Is Default Reply=1" + CR)

    # 1. vanilla's spirited turn-in: give it the ask's own setup, the completion and the XP
    ha, hb = reply_span(t, s, e, "I already have the Sceptre")
    have = t[ha:hb]
    assert "Custom Action=" not in have and "Go to node ID=45 Rod Bone Returned" in have
    go = "Go to node ID=45 Rod Bone Returned" + CR
    have = have.replace(go, go + multi(n_find + 1, find_body + complete), 1)
    t = t[:ha] + have + t[hb:]
    # 2. the lifeless Sceptre on both asking nodes, ahead of their "I will find" reply
    for nid in ("40 dark wielder task 1", "40 sceptre"):
        s, e = node_span(t, nid)
        fa, _ = reply_span(t, s, e, "I will find the Sceptre.")
        t = t[:fa] + new_reply + t[fa:]
    assert t.endswith("}" + CR)
    t = t[:-len("}" + CR)] + CR + DASH + CR + names + "}" + CR
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    crude_item()
    q = lhbuild.read(QUEST)
    old = q[q.index("Text=The Sceptre of Bone is in your hands, but it is lifeless"):]
    old = old[:old.index(CR)]
    q = q.replace(old, "Text=" + LINES["journal"])
    lhbuild.write_map(QUEST, q)
    return True


def main():
    changed = build()
    if changed:
        register([TREE, QUEST, CRUDE_REL])
    print("relican sceptre at the ask:", changed)


if __name__ == "__main__":
    main()
