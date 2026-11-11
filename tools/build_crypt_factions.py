"""Four factions, four answers to the Crypt's siege. 0.99.15, after the route breakdown.

The Crypt now had a Templar route, an undead route and a kill-everything route, and a "neutral" one that was only the
Templar route with the Bonecaller's help. The maintainer's frame was by faction: a Templar helps his brothers, a
Necromancer sides with the dead, an Inquisitor purges both, and the Wielder was open. Every gate here already exists in
the game and is used by Jehanne's tier-7 replies: `Templar IS`, `Inquisitor IS`/`NOT`, `Saladin IS`, and `Wielder IS`
with or without the `Necromancer` title perk. Faction options are added beside what anyone can do; only the Wielder's
peace is exclusive, so neutral is a faction identity rather than a stat check.

- **Templar.** At the door, after the recruitment, a Templar can give the order's word: the line goes forward, +1 tide and
  the reserve at once, once per game. He can refuse the herald as a knight. He can still swear, but Jehanne names it.
- **Necromancer** (Wielder with the title). The Bonecaller takes a new hand rather than a bargain: the oath without the
  Karma gate, and since the player is its master, the debt never comes due.
- **Wielder** (without the title). At the binding, a Wielder rewrites one word of the order: take becomes keep. The hill
  goes quiet: the dead stand on it and fight nothing, the knights stand down from them, and the truce does not lapse.
  Striking anything breaks it and both sides take up the war again. 4,000 XP, and the Efreeti's freeing reads the quiet.
  Jehanne meets the quiet with her sword down, and her own way to the gate still has to be won.
- **Inquisitor.** At the door, the Holy Office condemns every dead thing on the hill, the knights included, and the
  alarm goes up the line. The Bonecaller will not bargain with the Church. When Jehanne and the Bonecaller have both
  fallen, the purge pays 4,000 XP.
- **Saladin.** The Efreeti's lamp is the order's: a Saracen knight of Saladin made the wish that bound the knights. A
  Saladin player can ask for what his elder should have: the knights freed and a true wish beside it.

Run after build_crypt_front.py. Map changes need a save that has not entered the Doomed Plateau; dialogue changes reach
any save. A rerun is a no-op.

    python tools/build_crypt_factions.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH, multi, activate, relay, exists, if_action
from build_shrine_druids import parts
from build_shrine_repairs import register
import build_crypt_front as f
from build_crypt_front import (MAP, TREE, UT, JOAN_TREE, TIDE, VARS, QUIET, MASTER, KNIGHT_NAMES, QUIET_LINES, BONECALLER,
                               name_of, xy, flat, target, drop_enemy, modify, say, not_, give_xp, anchor_part, tree_node, balanced)

EFREETI = "Resources/Levels/4 Crypt/Dialog/Efreeti.DialogTree"
FRONTS = "Resources/Levels/4 Crypt/Dialog/The Fronts.DialogTree"
FRONTS_REF = "Levels/4 Crypt/Dialog/The Fronts"
WORD = VARS + "Fixt Templar Word Given"
QUIET_ATTR = f.QUIET_ATTR
WRIT = "Fixt Inquisition writ"
ORDER_XP = ("Fixt The order rewritten XP", "4000")
PURGE_XP = ("Fixt The hill purged XP", "4000")


def attr_is(attr, cmp, value):
    return ("CExpressionAction", [("Expression", (cmp, [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", attr)])),
                                                         ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", value)]))])),
                                  ("Character to get attributes from", "$Instigator")])


def creq_attr_below(attr, value):
    """A reply's custom requirement on a character variable, in vanilla's GoblinKhan shape."""
    return "CActionExpression" + CR + "{" + CR + "Action=" + flat(attr_is(attr, "CIsLessThan", value)) + CR + "}" + CR


NOT_NECRO = ("CExpressionNot", [("Operand1", ("CHasPerkExpression", [("Perks To Check For", ("Array", [
    ("Item Count", "1"), ("Perk To Check For", "Perks/!Event Title Perks/Necromancer")]))]))])
NECRO = ("CHasPerkExpression", [("Perks To Check For", ("Array", [("Item Count", "1"), ("Perk To Check For", "Perks/!Event Title Perks/Necromancer")]))])


def wielder(and_what):
    """Jehanne's own gate for nodes 49 and 50: Wielder, with or without the Necromancer title."""
    return B("CAND", [("Operand1", ("CUseCannedExpressionExpression", [("Canned Expression", "Dialog/Requirements/Faction/Wielder IS")])),
                      ("Operator", ""), ("Operand2", and_what)])


def write_tree(rel, t):
    assert t.count("\n") == t.count(CR)
    (lhbuild.FX / rel).write_bytes(t.encode("latin-1"))
    register([rel])


def append_nodes(t, nodes):
    assert t.endswith("}" + CR)
    return t[:-len("}" + CR)] + CR + DASH + CR + (CR + DASH + CR).join(nodes) + "}" + CR


def insert_reply(block, before_text, reply):
    """A reply, written in lhbuild.node's form, placed before the reply whose text is `before_text`."""
    k = block.index("Reply Text=" + before_text)
    k = block.rindex("Requirement=", 0, k)
    k = block.rindex(CR + CR, 0, k) + 4      # past the blank line, so the new reply gets one of its own
    return block[:k] + reply + CR + block[k:]


def reply(text, go="", req="!None", creq=None, action=None, icon=None):
    out = "Requirement=" + req + CR
    if creq:
        out += "Custom Requirement=" + creq
    out += "Reply Text=" + text + CR + "Go to node ID=" + go + CR
    if action:
        out += "Custom Action=" + B(*action)
    if icon:
        out += "Icon=" + icon + CR
    return out


def edit_node(t, nid, fn):
    blocks = t.split(DASH)
    hits = [n for n, b in enumerate(blocks) if re.search(r"Node ID=" + re.escape(nid) + r"\r\n", b)]
    assert len(hits) == 1, nid
    blocks[hits[0]] = fn(blocks[hits[0]])
    return DASH.join(blocks)


# ---------------------------------------------------------------- files
def build_attrs():
    done = 0
    for attr, label in ((WORD, "Fixt Templar Word Given"), (QUIET_ATTR, "Fixt The Hill Is Quiet"), (MASTER, "Fixt Master of the Bonecaller")):
        rel = "Resources/" + attr + ".DerivedCharacterAttribute"
        if not (lhbuild.FX / rel).exists():
            src = lhbuild.read("Resources/" + TIDE + ".DerivedCharacterAttribute")
            lhbuild.write_map(rel, src.replace("Crypt War Tide", label))
            register([rel])
            done += 1
    return done


# ---------------------------------------------------------------- the Bonecaller's tree
def build_captains_tree():
    t = lhbuild.read(TREE)
    if "Node ID=25 the new hand" + CR in t:
        return 0
    # the oath's actions, as node 21's reply carries them now, for the new hand to reuse
    b21 = [b for b in t.split(DASH) if "Node ID=21 the bargain" + CR in b][0]
    k = b21.index("Custom Action=") + len("Custom Action=")
    oath = b21[k:balanced(b21, k)]
    master = oath.replace("Item Count=", "Item Count=", 1)
    m = re.compile(r"Item Count=(\d+)\r\n").search(master)
    master = master[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + "Action=" + B(*modify(MASTER, "1", "Master of the Bonecaller")) + master[m.end():]

    def node1(b):
        b = insert_reply(b, "What are you?", reply("I raise the dead too. I will not owe you. You will follow me.", "25 the new hand",
                                                   creq=wielder(NECRO)))
        b = insert_reply(b, "What are you?", reply("The Holy Office has a writ for every dead thing on this hill.", "27 the church",
                                                   req="Inquisitor IS"))
        # the Church gets no offer
        old = "Requirement=!None" + CR + "Reply Text=You said something that is not a sword. Name it."
        assert b.count(old) == 1
        return b.replace(old, "Requirement=Inquisitor NOT" + CR + "Reply Text=You said something that is not a sword. Name it.")

    def node10(b):
        b = insert_reply(b, "Then you die with it on.", reply("Your order was to take the spear. I am changing one word in it: keep.", "26 keep it",
                                                              creq=wielder(NOT_NECRO)))
        old = "Requirement=Karma LESS 600" + CR + "Reply Text=Keep your orders."
        assert b.count(old) == 1
        return b.replace(old, "Requirement=Karma LESS 600" + CR + "Custom Requirement=" +
                         B("CUseCannedExpressionExpression", [("Canned Expression", "Dialog/Requirements/Faction/Inquisitor NOT")]) + "Reply Text=Keep your orders.")

    t = edit_node(t, "1 the bonecaller", node1)
    t = edit_node(t, "10 bound", node10)
    quiet = multi([relay("Fixt the hill goes quiet"), give_xp(ORDER_XP[0]), modify(QUIET_ATTR, "1", "The hill is quiet")])
    nodes = [
        "Node ID=25 the new hand" + CR + "Text=<It looks at you for a long time, the way you would look at a door you had been told was locked.> "
        "The pointing has outlived the hand. I said so. And here is a new hand, and it is one of mine. Point, then." + CR +
        "Should Have Voiceover=0" + CR + CR + "Requirement=!None" + CR + "Reply Text=Then follow me." + CR + "Go to node ID=" + CR +
        "Custom Action=" + master + CR + "Icon=Exit Icon" + CR + "Is Default Reply=1" + CR,
        tree_node("26 keep it", "<Something in the rotted mail goes very still.> Keep. <It says it again, more quietly.> Then I am a guard on "
                  "the same hill, with the same dead, and the knights are guarding the same door, and two hundred years of the same work "
                  "can go on without anyone dying of it again. That is not what I was raised for. It is better.",
                  [{"text": "Then keep it well.", "action": quiet, "default": True}]),
        tree_node("27 the church", "<It laughs, or the mail does.> A church court. The last person on this hill who trusted one is still "
                  "burning in the keep. There is nothing for us to say to each other.",
                  [{"text": "Then the writ is served.", "action": multi([relay("Fixt Bonecaller fights"), ("CGoToCombatAction", [("Enemy Name", "$Trigger")])]),
                    "icon": "Fight Icon", "default": True}]),
        tree_node("140 the dead keep", "Keep. We keep.", []),
        tree_node("141 the dead the word", "One word. He changed one word.", []),
        tree_node("142 the dead nothing climbs", "Nothing climbs now. Go where you like.", []),
    ]
    # the herald: a Templar refuses as a knight
    def herald(b):
        return insert_reply(b, "No. Get out of my way.", reply("I am a Knight of the Temple. Tell your master no.", "202 the herald turns",
                                                               req="Templar IS", action=relay("Fixt herald refused")))
    t = edit_node(t, "200 the herald", herald)
    write_tree(TREE, append_nodes(t, nodes))
    return 1


# ---------------------------------------------------------------- the door, and Jehanne
def build_door_tree():
    t = lhbuild.read(UT)
    if "Node ID=42 the order's word" + CR in t:
        return 0

    def n40(b):
        k = b.index("Requirement=!None" + CR + "Reply Text=Then I am at your orders.")
        r = reply("I bring the order's word, brother. The line goes forward.", "42 the order's word", req="Templar IS",
                  creq=creq_attr_below(WORD, "1"),
                  action=multi([relay("Fixt the line holds"), modify(TIDE, "1", "Crypt war tide"), modify(WORD, "1", "The order's word")]))
        return b[:k] + r + CR + b[k:]

    def n01(b):
        return insert_reply(b, "No, I'll be leaving now. Goodbye.",
                            reply("By the writ of the Holy Office, every dead thing on this hill is condemned. That includes you.", "23 condemned",
                                  req="Inquisitor IS", action=multi([activate(WRIT), relay(f.ARMS)]), icon="Fight Icon"))

    t = edit_node(t, "40 knight", n40)
    t = edit_node(t, "01 Conversation Start", n01)
    nodes = [tree_node("42 the order's word", "<He straightens, and for a moment he is not a dead man at all.> Two hundred years, and the order "
                       "still sends word. Then the line goes forward. Find the Lady. Tell her the Temple stands.", []),
             tree_node("23 condemned", "<His face does not change, because it cannot.> We were condemned once already, and here we are. To arms!", [])]
    write_tree(UT, append_nodes(t, nodes))
    return 1


def build_joan_tree():
    t = lhbuild.read(JOAN_TREE)
    if "Node ID=710 the quiet" + CR in t:
        return 0

    def n700(b):
        return insert_reply(b, "I am going.", reply("I wear the same cross you do.", "702 the cross", req="Templar IS"))

    t = edit_node(t, "700 the oath", n700)
    nodes = [tree_node("702 the cross", "Then you have sold it as well as worn it. Draw.",
                       [{"text": "So be it.", "action": relay("Joan Player chose combat in dialog"), "icon": "Fight Icon", "default": True}]),
             tree_node("710 the quiet", "<For the first time her sword is down, though she has not let go of it.> The dead have stopped coming up "
                       "the hill. They stand where they stood, and they do nothing, and my knights do not know what to do with their hands. I "
                       "have a sword and nothing to point it at. Was that you?",
                       [{"text": "It was. I changed one word in the order that raised them.", "go": "10 jehanne", "default": True}])]
    write_tree(JOAN_TREE, append_nodes(t, nodes))
    return 1


# ---------------------------------------------------------------- the Efreeti
def build_efreeti():
    t = lhbuild.read(EFREETI)
    if "Node ID=101 the order's debt" + CR in t:
        return 0
    b211 = [b for b in t.split(DASH) if "Node ID=211 true wish" + CR in b][0]
    stats = {}
    for name in ("(ST) Strength", "(IN) Intelligence", "(AG) Agility"):
        i = b211.index("Character attribute to modify=Character Attributes/" + name)
        k = b211.rindex("Custom Action=", 0, i) + len("Custom Action=")
        stats[name] = b211[k:balanced(b211, k)]
    saladin = reply("I am a Knight of Saladin. My order rubbed this lamp before. Hear the wish my elder should have made.",
                    "101 the order's debt", req="Saladin IS")
    for nid in ("01 Conversation Start", "10 efreeti"):
        t = edit_node(t, nid, lambda b: insert_reply(b, "I wish to undo the curse laid upon Jehanne's soul and the souls of her fellow knights.", saladin))
    rs = ""
    for text, name in (("Then free them, and make me stronger.", "(ST) Strength"), ("Then free them, and make me wiser.", "(IN) Intelligence"),
                       ("Then free them, and make me quicker.", "(AG) Agility")):
        rs += CR + "Requirement=!None" + CR + "Reply Text=" + text + CR + "Go to node ID=100 save inga" + CR + "Custom Action=" + stats[name] + CR
    n101 = ("Node ID=101 the order's debt" + CR + "Text=<The flames bank low.> A son of the order that rubbed my lamp. Your elder asked me for aid "
            "against the dead, and I gave him precisely that: dead that never stop. You ask the way he should have. Very well. Have both. The "
            "knights go free, and you may have the thing he should have asked for besides." + CR + "Should Have Voiceover=0" + CR + rs)
    # the freeing reads the quiet hill before the tide
    def n100(b):
        k = b.index("Custom Action=CMultipleActionsAction")
        i = b.index("Action=CIfAction", k) + len("Action=")
        end = balanced(b, i)
        peace = lhbuild.balloon(FRONTS_REF, "4 freed in peace", "$Instigator", "-60")
        return b[:i] + "CIfAction" + CR + "{" + CR + "If=" + flat(attr_is(QUIET_ATTR, "CIsGreaterThanOrEqual", "1")) + CR + \
            "Then=" + flat(peace) + CR + "Else=" + b[i:end] + CR + "Return failure if the If failes=0" + CR + "}" + b[end:]
    t = edit_node(t, "100 save inga", n100)
    write_tree(EFREETI, append_nodes(t, [n101]))
    fr = lhbuild.read(FRONTS)
    if "Node ID=4 freed in peace" + CR not in fr:
        write_tree(FRONTS, append_nodes(fr, [tree_node("4 freed in peace", "The knights go out like lamps, slowly, one at a time, on a hill where "
                                                       "nothing is climbing towards them any more. The last of them sets down a sword he has not "
                                                       "needed since you changed a word.", [])]))
    return 1


# ---------------------------------------------------------------- the Plateau
def build_map():
    z = lhbuild.read(MAP)
    if "Name=Fixt the hill goes quiet" + CR in z:
        return 0
    dead = sorted({f.new_name(p) for p in parts(z) if f.is_dead_gen(p) and f.new_name(p)})
    quiet = multi([activate(f.TRUCE), activate(QUIET)] +
                  [a for n in dead for a in (target(n, ""), drop_enemy(n)) + tuple(f.talk_click(n))] +
                  [target(k, "") for k in KNIGHT_NAMES] + [target(BONECALLER, "")] +
                  [say("The order is rewritten. On the whole hill, nothing is climbing and nothing is holding.")])
    purge = if_action(exists(WRIT), if_action(exists("Fixt Jehanne fallen"), if_action(exists("Fixt Bonecaller fallen"),
                      if_action(not_(exists("Fixt purged")), multi([activate("Fixt purged"), give_xp(PURGE_XP[0]),
                                                                     say("The hill is purged, knights and dead alike. The Holy Office will hear of it.")])))))
    x, y = xy([p for p in parts(z) if name_of(p) == "Fixt Sworn to the Bonecaller XP"][0])
    new_parts = [lhbuild.relay_part("Fixt the hill goes quiet", quiet, x, y + 40),
                 lhbuild.relay_part("Fixt the purge", purge, x + 20, y + 40, once="0"),
                 lhbuild.checker(WRIT, x + 40, y + 40), lhbuild.checker("Fixt Jehanne fallen", x + 60, y + 40),
                 lhbuild.checker("Fixt purged", x + 80, y + 40),
                 anchor_part(z, ORDER_XP[0], ORDER_XP[1], x + 40, y), anchor_part(z, PURGE_XP[0], PURGE_XP[1], x + 60, y)]
    # Jehanne's death and the Bonecaller's both look for the purge
    j = [p for p in parts(z) if name_of(p) == "Joan of Arc Generator"][0]
    k = j.index("New Destroyed Action=CMultipleActionsAction")
    m = re.compile(r"Item Count=(\d+)\r\n").search(j, k)
    j2 = j[:m.start()] + "Item Count=" + str(int(m.group(1)) + 2) + CR + "Action=" + flat(activate("Fixt Jehanne fallen")) + CR + \
        "Action=" + flat(relay("Fixt the purge")) + CR + j[m.end():]
    z = z.replace(j, j2, 1)
    bc = [p for p in parts(z) if name_of(p) == "Fixt Bonecaller generator"][0]
    i = bc.index("New Destroyed Action=") + len("New Destroyed Action=")
    end = balanced(bc, i)
    both = "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR + "Action=" + bc[i:end] + CR + \
        "Action=" + flat(relay("Fixt the purge")) + CR + "}" + CR + "}"
    bc2 = bc[:i] + both + bc[end:]
    assert "Fixt the purge" in bc2 and bc[i:end] in bc2
    z = z.replace(bc, bc2, 1)
    lhbuild.write_map(MAP, lhbuild.add_parts(z, new_parts))
    register([MAP])
    return 1


def main():
    print("attrs:", build_attrs(), "| captains:", build_captains_tree(), "| door:", build_door_tree(), "| Jehanne:", build_joan_tree(),
          "| Efreeti:", build_efreeti(), "| map:", build_map())


if __name__ == "__main__":
    main()
