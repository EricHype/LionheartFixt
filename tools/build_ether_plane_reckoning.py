"""The spirits who built your bridge to the Enchanter answer for what you did with it. Asked: "you get help to get to the
mad enchanter by promising to end him from the dead templar and marco polo, shouldn't they react if you work with him
instead?"

Vanilla's bridge is built on a promise. Marco Polo forms it after *"I want to end the madness here. The enchanter must
die."*, and Jameson, the dead Templar, spends his voice moving his island because he would "love to see that enchanter
suffer". 0.39.0 let you spare the Enchanter (the bargain, the crystal) and then sell him to Relican (`70`/`71 Fixt
Pact`), and neither spirit noticed.

  * **Spared** (`45 Barter 3`'s goodbye, `61 Fixt Bound Token`'s thanks): the checker `Fixt Enchanter Spared`. Marco,
    still on the plane, greets you once with `700 Fixt spared` and then talks as before. Worn or carried, his boots say
    `600 Fixt spared`. Marco offered the crystal himself, so sparing costs nothing else.
  * **The pact** (`71 Fixt Pact 2`'s reply): the checker `Fixt Enchanter Pact Made` and -50 Karma (twice the plane's own
    -25 for taunting the Enchanter). Marco on the plane greets you only with `710 Fixt betrayed` from then on, which
    ends the conversation, so no favour and no boots. The boots say `610 Fixt pact`, and are taken away and replaced by
    `Fixt Empty Walking Boots`; the plain pair is given only if the removal succeeded. A Templar also activates
    `Fixt Jameson Whisper`, a once-only oval at the exit crystal (the way out after a pact; Jameson's island is off that
    road), which plays Jameson's `700 Fixt Jameson judges`.

The boots remark and the swap run in the reply itself, where `$Instigator` is the player (a relay fired from a reply
resolves it to nothing). Marco's greeting is a branch around his vanilla `CSeriesAction`, which is kept intact.

The ether plane parts are map-side: a plane not yet entered. The trees reach every save. A rerun is a no-op.

    python tools/build_ether_plane_reckoning.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH, activate, exists, if_action
from build_shrine_repairs import register

D = "Resources/Levels/1 Barcelona/Dialog/La Calle Perdida/"
ENCHANTER = D + "Mad EnchanterEncounter.DialogTree"
MARCO = D + "MarcoPoloSpirit.DialogTree"
BOOTS_TREE = D + "MarcoPoloSpirit Boots.DialogTree"
JAMESON = D + "Trapped Spirit1.DialogTree"
MAP = "Levels/1 Barcelona/TrappedEtherPlane.zax"
ITEMS = "Resources/Inventory/Specific Item Cans/Quest Items/"
BOOTS = "Inventory/Specific Item Cans/Quest Items/Marco Polo Boots"
EMPTY_REL = ITEMS + "Fixt Empty Walking Boots.InventoryItem"
EMPTY = "Inventory/Specific Item Cans/Quest Items/Fixt Empty Walking Boots"
T_BOOTS, T_MARCO, T_JAMESON = (p[len("Resources/"):-len(".DialogTree")] for p in (BOOTS_TREE, MARCO, JAMESON))

SPARED, PACT, HEARD, WHISPER = "Fixt Enchanter Spared", "Fixt Enchanter Pact Made", "Fixt Marco Heard Spared", "Fixt Jameson Whisper"

LINES = {
    "marco spared": "I felt you cross my bridge, traveler, and I felt you come back with him still breathing. Three hundred years I have wanted that man dead. But I offered you the crystal myself, so I cannot curse you for taking the gentler road. Only do not ask me to forgive him.",
    "marco spared reply": "He has suffered enough here. So have you.",
    "boots spared": "He lives, then. Well. I told you there was another way out, and I suppose I meant it.",
    "marco betrayed": "You gave him a master. I spent the last of my strength on that bridge so you could end him, and you have sold him to a necromancer, and every spirit on this plane with him. I asked a favor of you once. I withdraw it. Go, traveler, and do not come back to me.",
    "marco betrayed reply": "Then stay here with him.",
    "boots pact": "No. I will walk a thousand leagues with you, traveler, but not one step in Relican's service. Find another pair of feet.",
    "jameson": "<A voice, barely there.> So. I gave up my voice for that bridge, and you used it to strike a bargain with the man who keeps us here. A Knight Templar. The order deserved better of you. So did I.",
    "empty boots": "Ordinary walking boots, well travelled and empty. Whoever lived in the leather has gone.",
}
for v in LINES.values():
    assert "—" not in v and "--" not in v


def balloon(tree, node, anchor):
    return ("CDisplayDialogBalloonAction", [("Dialog Tree File", tree), ("Node ID", node), ("Name of Position", anchor),
                                            ("Position Offset", "0.000000,-75.000000"), ("After Action", ""), ("Include In Log", "1")])


def has_boots():
    return ("CActionCheckForInventoryItem", [("Who to give check", "$instigator"), ("Inventory Item To Check For", BOOTS)])


def conditional(try_, ok, fail=""):
    return ("CConditionalAction", [("Try Action", try_), ("Succeed Action", ok), ("Fail Action", fail),
                                   ("Return failure if the TryAction failes", "0")])


def multi(items):
    return ("CMultipleActionsAction", [("Action", ("Array", [("Item Count", str(len(items)))] + [("Action", i) for i in items]))])


KARMA = ("CAddCharacterModifierToCharacterAction", [
    ("Modifier Description", "Karma"), ("Modification is permanent", "0"), ("Character to modify", "Player#1-9#"),
    ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
        ("Modification Amount", ("CConstant", [("Constant Value", "-50")])), ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "1"), ("Derived character attribute to modify", "Derived Character Attributes/Karma")]))])),
    ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])
SWAP = conditional(("CActionRemoveInventoryItem", [("Who to remove from", "$instigator"), ("Inventory Item To remove", BOOTS)]),
                   ("CActionGiveStandardInventoryItem", [("Who to give to", "$instigator"), ("Delete Trigger", "0"), ("Notify Player", "1"),
                                                         ("Inventory Item To Give", EMPTY), ("Additions to add", ("Array", [("Item Count", "0")]))]))
SPARED_ACTIONS = [activate(SPARED), conditional(has_boots(), balloon(T_BOOTS, "600 Fixt spared", "$Instigator"))]
PACT_ACTIONS = [activate(PACT), KARMA,
                conditional(has_boots(), multi([balloon(T_BOOTS, "610 Fixt pact", "$Instigator"), SWAP])),
                ("CIfExpressionAction", [("If Expression", ("CUseCannedExpressionExpression", [("Canned Expression", "Dialog/Requirements/Faction/Templar IS")])),
                                         ("Character to get attributes from", "$Instigator"), ("Then", activate(WHISPER)), ("Else", "")])]


def node(nid, text, replies=()):
    return lhbuild.node(nid, text, list(replies))


def append_nodes(t, nodes):
    assert t.endswith("}" + CR)
    return t[:-len("}" + CR)] + CR + DASH + CR + (CR + DASH + CR).join(nodes) + "}" + CR


def write_tree(rel, t):
    p = lhbuild.FX / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(t.encode("latin-1"))
    return [rel]


def extend_reply(t, reply_text, extra):
    """Give a reply's Custom Action the extra actions, keeping what it already does first."""
    r = t.index("Reply Text=" + reply_text + CR)
    assert t.count("Reply Text=" + reply_text + CR) == 1, reply_text
    c = t.index("Custom Action=", r) + len("Custom Action=")
    assert t.index(CR + CR, r) > c, reply_text
    e = lhbuild.balanced(t, c) + len(CR)
    old = t[c:e]
    if old.startswith("CMultipleActionsAction" + CR):
        k = old.index("Item Count=")
        n = int(old[k + len("Item Count="):old.index(CR, k)])
        close = old.rindex("}", 0, old.rindex("}"))
        new = (old[:k] + "Item Count=%d" % (n + len(extra)) + old[old.index(CR, k):close] +
               "".join("Action=" + B(*a) for a in extra) + old[close:])
    else:
        new = ("CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=%d" % (1 + len(extra)) + CR +
               "Action=" + old + "".join("Action=" + B(*a) for a in extra) + "}" + CR + "}" + CR)
    return t[:c] + new + t[e:]


def enchanter():
    t = lhbuild.read(ENCHANTER)
    if "Target Name=" + PACT in t:
        return []
    t = extend_reply(t, "Very well. Goodbye.", SPARED_ACTIONS)
    t = extend_reply(t, "You have my thanks, enchanter.", SPARED_ACTIONS)
    t = extend_reply(t, "He will have your service, and I will carry your seal.", PACT_ACTIONS)
    return write_tree(ENCHANTER, t)


def trees():
    done = []
    t = lhbuild.read(BOOTS_TREE)
    if "Node ID=600 Fixt spared" not in t:
        done += write_tree(BOOTS_TREE, append_nodes(t, [node("600 Fixt spared", LINES["boots spared"]),
                                                        node("610 Fixt pact", LINES["boots pact"])]))
    t = lhbuild.read(MARCO)
    if "Node ID=700 Fixt spared" not in t:
        done += write_tree(MARCO, append_nodes(t, [
            node("700 Fixt spared", LINES["marco spared"],
                 [{"text": LINES["marco spared reply"], "go": "03 Return Dialogue", "action": activate(HEARD), "default": True}]),
            node("710 Fixt betrayed", LINES["marco betrayed"], [{"text": LINES["marco betrayed reply"], "default": True}])]))
    t = lhbuild.read(JAMESON)
    if "Node ID=700 Fixt Jameson judges" not in t:
        done += write_tree(JAMESON, append_nodes(t, [node("700 Fixt Jameson judges", LINES["jameson"])]))
    return done


def empty_boots():
    p = lhbuild.FX / EMPTY_REL
    if p.exists():
        return []
    t = lhbuild.read(ITEMS + "Marco Polo Boots.InventoryItem")
    s = t.index("\tPlugIn Behaviors=Array")
    e = lhbuild.balanced(t, s) + len(CR)
    keep = t[t.index("\t\tPlugIn Behavior=CPlugInBehaviorPutDownAction", s):]
    keep = keep[:lhbuild.balanced(keep, len("\t\tPlugIn Behavior=")) + len(CR)]
    plug = "\tPlugIn Behaviors=Array" + CR + "\t{" + CR + "\t\tItem Count=1" + CR + keep + "\t}" + CR
    t = t[:s] + plug + t[e:]
    for old, new in (("Constant Value=350", "Constant Value=20"), ("Is Magic=1", "Is Magic=0"),
                     ("Display Name=Marco Polo's Boots", "Display Name=Walking Boots"),
                     ("Origonal Item=" + BOOTS, "Origonal Item=" + EMPTY)):
        assert t.count(old) == 1, old
        t = t.replace(old, new)
    d = t.index("\tDescription=These boots contain")
    t = t[:d] + "\tDescription=" + LINES["empty boots"] + t[t.index(CR, d):]
    assert "Marco Pick up his boots" not in t and "Walk a Mile" not in t
    lhbuild.write_map(EMPTY_REL, t)
    return [EMPTY_REL]


def map_parts():
    t = lhbuild.read(MAP)
    if "Name=" + PACT + CR in t:
        return []
    m = t.index("\t\t\tName=Marco Polo" + CR)
    s = t.index("Action=CSeriesAction", m) + len("Action=")
    e = lhbuild.balanced(t, s)
    series = t[s:e]
    assert "Node ID=01 Conversation Start" in series and "Node ID=03 Return Dialogue" in series and e < t.index("\t\tLevel Part=", m)
    spoken = lambda nid: B("CDisplayDialogTreeAction", [("Dialog Tree File", T_MARCO), ("Node ID", nid), ("Speaker", "$trigger"),
                                                       ("Player Being Spoken To", "$Instigator")])
    first_spared = B("CAndAction", [("Action", ("Array", [("Item Count", "2"), ("Action", exists(SPARED)),
                                                          ("Action", ("CNotAction", [("Action", exists(HEARD))]))])), ("Early Exit", "0")])
    branch = ("CIfAction" + CR + "{" + CR + "If=" + B(*exists(PACT)) + "Then=" + spoken("710 Fixt betrayed") +
              "Else=CIfAction" + CR + "{" + CR + "If=" + first_spared + "Then=" + spoken("700 Fixt spared") +
              "Else=" + series + CR + "Return failure if the If failes=0" + CR + "}" + CR +
              "Return failure if the If failes=0" + CR + "}")
    t = t[:s] + branch + t[e:]
    crystal = t.index("\t\t\tName=Teleporter Crystal" + CR)
    cx = t[t.index("Position X=", crystal) + len("Position X="):t.index(CR, t.index("Position X=", crystal))]
    cy = t[t.index("Position Y=", crystal) + len("Position Y="):t.index(CR, t.index("Position Y=", crystal))]
    whisper = lhbuild.touch_oval(WHISPER, B(*balloon(T_JAMESON, "700 Fixt Jameson judges", "$trigger")).rstrip(CR),
                                 int(float(cx)), int(float(cy)) + 60, radius="180", active="0")
    t = lhbuild.add_parts(t, [lhbuild.checker(SPARED, 1500, 900), lhbuild.checker(PACT, 1520, 900),
                              lhbuild.checker(HEARD, 1140, 1240), whisper])
    lhbuild.write_map(MAP, t)
    return [MAP]


def main():
    done = enchanter() + trees() + empty_boots() + map_parts()
    if done:
        register(done)
    print("ether plane reckoning:", len(done), "files")
    for d in done:
        print("  ", d)


if __name__ == "__main__":
    main()
