"""A dead Shylocke's debt dies with him. Reported: "we killed shylocke, but the goons on the plains still ask for his
money".

Taking his loan (`60 borrow money`) activates `Player owes debt to Shylocke` on the Plains by `COtherMapAction`, and the
goons' trip poly reads it: present, the shakedown (`1 Conversation Start`); absent, a plain robbery (`3 Robbery`). Repaying
deactivates it, and so does scaring the collectors off (`210 intimidate`). His death did not: `Shylocke.can`'s death
script fails his quests and gives Merchant Slayer, and the flag stays on. The user's QuickSave has `Shylocke murdered`
active in his shop and the flag active on the Plains.

  * **His death.** `Shylocke.can`'s `Destroyed Effect Action` now also deactivates the Plains flag and sets `Fixt Shylocke
    Dead`, whoever kills him. A can reaches only a Shylocke not yet spawned.
  * **The shakedown, for a save already past it.** The five nodes that press for the money (`1`, `10`, `20`, `40`, `50`),
    and `5 Return`, the leader's click once the ambush has fired, gain *"Shylocke is dead. I killed him myself."*, to `250 Fixt ledger closed`, which does what `210 intimidate` does
    (debt cleared, the goons go quiet) and sets the variable. No tree can see his shop, so for a save that killed him
    before this the gate is Merchant Slayer, which his death gives; a debtor who killed some other merchant could claim
    it too, and the goons, a long way from Barcelona, would believe him.
  * **The robbery.** With the debt paid or never taken, the robbers still spoke of him alive: `232 who sends you`,
    `240 haggled`, and the guild and eloquence replies. Each of those replies is now gated on `Fixt Shylocke Dead` being 0,
    with a twin for 1 that goes to a copy of its node with the line changed (`233`, `234`, `235`), or, for eloquence,
    only its own wording changed. The robbery reads the variable alone, because Merchant Slayer would put a dead
    Shylocke into the mouths of robbers whose victim never met him.

Trees, one can, one variable. The shakedown reply reaches every save; the robbery twins and the can need his death after
this. A rerun is a no-op.

    python tools/build_shylocke_dead_debt.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH, balanced
from build_shrine_repairs import register
from build_sahar_road_north import var_is, set_var

TREE = "Resources/Levels/Wilderness/Dialog/ShylockeGoons.DialogTree"
CAN = "Resources/Levels/1 Barcelona/Character Templates/Port District/Shylocke.can"
VARS = "Resources/Derived Character Attributes/Game Scripting Variables/"
DEAD = "Fixt Shylocke Dead"
FLAG = "Player owes debt to Shylocke"
SLAYER = "Perks/!Event Title Perks/Merchant Slayer"

CLAIM = "Shylocke is dead. I killed him myself."
CLOSED = "250 Fixt ledger closed"
LINES = {
    CLOSED: ("<The leader looks at the others, and they look at their boots.> Dead. Then there's no ledger, and nobody "
             "paying us to sit on this road. Go on. We were never here."),
    "233 Fixt who sends you dead": ("Nobody, now. Shylocke paid us to sit on this road for the ones who owed him, and "
                                    "somebody did for him in his own shop. A man still has to eat."),
    "234 Fixt haggled dead": "...A hundred. There's nobody left to count it. Go on, before I remember what I said.",
    "235 Fixt guild dead": "Juanita's. Bah. We don't cross the guild for a purse. Go on, and tell her we were civil about it.",
}
SHAKEDOWN = ["1 Conversation Start", "10 Debt", "20 wrong person", "40 loan amount", "50 test patience",
             "5 Return"]  # the leader's click once the ambush has fired, which is all a save past it has left
ROBBERY = ["3 Robbery", "230 lie or die", "232 who sends you"]
# reply goes to -> (its node's dead twin or None to keep the node, the reply's dead wording or None to keep it)
TWINS = {
    "232 who sends you": ("233 Fixt who sends you dead", None),
    "240 haggled": ("234 Fixt haggled dead", None),
    "241 guild": ("235 Fixt guild dead", "Juanita's people don't rob each other."),
    "244 eloquence": (None, "Rob me, and every trader between here and Montaillou hears that you work the road like "
                            "common thieves. Let me pass, and they hear you were civil."),
}
for v in list(LINES.values()) + [CLAIM] + [w for _, w in TWINS.values() if w]:
    assert "—" not in v and "--" not in v


def span(t, nid):
    s = t.index(CR + "Node ID=" + nid + CR) + len(CR)
    e = t.find(DASH, s)
    return s, (t.rindex("}" + CR) if e < 0 else e)


def blocks(node):
    """A node's header and its reply blocks, each without the blank line between them."""
    parts = node.rstrip(CR).split(CR + CR)
    assert all(p.startswith("Requirement=") for p in parts[1:]), [p[:40] for p in parts[1:]]
    return parts[0], parts[1:]


def join(head, replies):
    return (CR + CR).join([head] + replies) + CR


def gated(reply, gate):
    """The reply with `gate` ANDed onto its custom requirement, or as it."""
    m = re.match(r"Requirement=[^\r\n]*\r\n", reply)
    k = m.end()
    if reply.startswith("Custom Requirement=", k):
        v = k + len("Custom Requirement=")
        e = balanced(reply, v)
        old = reply[v:e] + CR
        new = "CAND" + CR + "{" + CR + "Operand1=" + old + "Operator=" + CR + "Operand2=" + gate + "}" + CR
        return reply[:v] + new + reply[e + len(CR):]
    return reply[:k] + "Custom Requirement=" + gate + reply[k:]


def go_of(reply):
    return re.search(r"\r\nGo to node ID=([^\r\n]*)", reply).group(1)


def alive():
    return var_is(DEAD, "0")


def dead():
    return var_is(DEAD, "1")


def twin_replies(replies):
    out = []
    for r in replies:
        g = go_of(r)
        if g not in TWINS:
            out.append(r)
            continue
        node, words = TWINS[g]
        out.append(gated(r, alive()))
        t = gated(r, dead())
        if node:
            t, n = re.subn(r"(?m)^Go to node ID=" + re.escape(g) + r"(?=\r?$)", lambda _m: "Go to node ID=" + node, t)
            assert n == 1, (g, t[-120:])
        if words:
            t = re.sub(r"\r\nReply Text=[^\r\n]*", lambda m: CR + "Reply Text=" + words, t, count=1)
        out.append(t)
    return out


def closed_action(t):
    s, e = span(t, "210 intimidate")
    i = t.index("Custom Action=", s, e)
    v = i + len("Custom Action=")
    raw = t[v:balanced(t, v)]
    assert FLAG in raw and "Give Shylocke Goon Balloon Dialog" in raw
    a = raw.index("Action=Array" + CR)
    m = re.compile(r"Item Count=(\d+)\r\n").search(raw, a)
    n = int(m.group(1))
    raw = raw[:m.start()] + "Item Count=" + str(n + 1) + CR + "Action=" + B(*set_var(DEAD)) + raw[m.end():]
    return raw + CR


def build_tree():
    t = lhbuild.read(TREE)
    if "Node ID=" + CLOSED + CR in t:
        return []
    claim_gate = "COR" + CR + "{" + CR + "Operand1=" + dead() + "Operator=" + CR + "Operand2=" + B("CHasPerkExpression", [
        ("Perks To Check For", ("Array", [("Item Count", "1"), ("Perk To Check For", SLAYER)]))]) + "}" + CR
    claim = ("Requirement=!None" + CR + "Custom Requirement=" + claim_gate + "Reply Text=" + CLAIM + CR +
             "Go to node ID=" + CLOSED + CR + "Icon=Quest Icon")
    for nid in SHAKEDOWN:
        s, e = span(t, nid)
        head, replies = blocks(t[s:e])
        t = t[:s] + join(head, replies + [claim]) + t[e:]
    for nid in ROBBERY:
        s, e = span(t, nid)
        head, replies = blocks(t[s:e])
        t = t[:s] + join(head, twin_replies(replies)) + t[e:]
    new = []
    for g, (node, _) in TWINS.items():
        if not node:
            continue
        s, e = span(t, g)
        body = t[s:e]
        old = re.search(r"\r\nText=([^\r\n]*)", body).group(1)
        body = body.replace("Node ID=" + g + CR, "Node ID=" + node + CR, 1).replace("Text=" + old + CR, "Text=" + LINES[node] + CR, 1)
        new.append(body)
    closed = ("Node ID=" + CLOSED + CR + "Text=" + LINES[CLOSED] + CR + "Should Have Voiceover=0" + CR + CR +
              "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR + "Custom Action=" + closed_action(t) +
              "Is Default Reply=1" + CR)
    assert t.endswith("}" + CR)
    t = t[:-len("}" + CR)] + "".join(DASH + CR + n for n in new + [closed]) + "}" + CR
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    return [TREE]


def build_can():
    t = lhbuild.read(CAN)
    if "Game Scripting Variables/" + DEAD + CR in t:
        return []
    m = re.search(r"(?m)^\t\tDestroyed Effect Action=", t)
    v = m.end()
    e = balanced(t, v)
    old = re.sub(r"\r\n\t+", CR, t[v:e]) + CR
    clear = ("COtherMapAction", [("Action", ("CDeactivateAction", [("Target Name", FLAG)])), ("Other Map Name", "Wilderness Maps/Plains")])
    both = ("CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=3" + CR + "Action=" + old +
            "Action=" + B(*set_var(DEAD)) + "Action=" + B(*clear) + "}" + CR + "}")
    lhbuild.write_map(CAN, t[:v] + both + t[e:])
    return [CAN]


def build_var():
    rel = VARS + DEAD + ".DerivedCharacterAttribute"
    if (lhbuild.FX / rel).exists():
        return []
    v = lhbuild.read(VARS + "Esteban Dead.DerivedCharacterAttribute").replace("Esteban Dead", DEAD)
    v = v.replace("Description=" + CR, "Description=1 means Shylocke is dead, and his Plains debt with him." + CR)
    (lhbuild.FX / rel).write_bytes(v.encode("latin-1"))
    return [rel]


def main():
    done = build_var() + build_can() + build_tree()
    if done:
        register(done)
    print("shylocke dead debt:", done)


if __name__ == "__main__":
    main()
