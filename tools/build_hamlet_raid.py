"""The raid on the burned hamlet has a leader, and more than one way through. Release 7 of the post-0.99 plan.

Hamlet Burned is Act 3's English raid on Montaillou: 21 nameless soldier generators across the map, beside the Templar
fights that triggers stage later. The Crossroads standard and the Shrine say the English are held by druid magic, and the
raid had no druid holding it. Now it does: a Druid War-Priest, a copy of the Priest cans with its own display name, one
tier above the local druid (Tough in the lowest band, Super above), so an Act 3 character meets a boss of Act 3's weight
and not the Shrine's. He keeps the priests' wolf and shield.

The 21 generators split by position into four bands. The War-Priest stands in the square with the largest.

Five ways through, and none of them is free:

1. **Fight.** Nothing stops you.
2. **Kill the War-Priest.** Every band stands down, wakes, and can be talked to. Hit a man and only his band turns again.
3. **Parley.** Close to him, he speaks first. Speech 75 talks him out of the village: he withdraws and the men are freed.
4. **The Weird Woman.** A Cathar friend can ask her to call the Cathars' bears off. They stop hunting you. The English
   and the War-Priest are untouched.
5. **Wrest a band free.** Tribal 75, and it costs all your mana: one band of his is freed per cast, his guard first. He
   speaks again when you come back to him later, so a weaker character wins some fights, not all of them.

The two staged squads with a priest, fight4 and fight6, are held by their own priest, and are armed only once he has been
seen alive, because their generators wait on triggers. fight8's priest and soldiers share `attacker near portal`, which a
vanilla script checks, so it is left alone.

The Weird Woman's `cathar friend` is an entity in her own hut, which this map cannot see. The promise replies, and every
reply of the greeting a Cathar friend gets, now also set `Fixt Cathar Friend`, so a save that promised before this
release still qualifies once it has spoken to her again.

A rerun is a no-op.

    python tools/build_hamlet_raid.py
"""
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, DASH, activate, balanced, deactivate, delay, exists, if_action, multi, relay
import build_shrine_druids as druids
from build_shrine_druids import parts, pos, replace_groups, setting
from build_shrine_repairs import register
from build_inquisition_slides import VARS, flag, write_var

MAP = "Levels/3 Montaillou/02 Hamlet Burned.zax"
WW = "Resources/Levels/3 Montaillou/Dialog/weirdwoman.DialogTree"
E = "Monster Cans/English Enemies/"
PRIEST_CAN = "Levels/3 Montaillou/Character Templates/Fixt Druid War-Priest"
PRIEST = "Druid War-Priest"
TREE = "Levels/3 Montaillou/Dialog/Fixt Hamlet Raid"
WOKEN_TREE = "Levels/3 Montaillou/Dialog/Fixt Hamlet Woken"
FRIEND = VARS + "Fixt Cathar Friend"
CALLED = VARS + "Fixt Cathars Called Off"
CATHAR = "Hamlet Cathar"
BANDS = ["Hamlet Square", "Hamlet West", "Hamlet Northeast", "Hamlet Southeast"]  # the guard first: the wrest frees them in this order
SQUADS = {"fight4": "Hamlet Squad 4", "fight6": "Hamlet Squad 6"}
MAY_TALK = "Fixt War-Priest may talk"
THREADS = "Fixt War-Priest threads left"
WATCH = "Fixt War-Priest watch"
WOKEN = [
    ("1 england", "This is not England. Where are we?"),
    ("2 burned", "Who burned this village?"),
    ("3 marching", "I do not remember marching here."),
    ("4 priest", "The priest. He spoke and we followed."),
    ("5 houses", "These were houses. People lived here."),
    ("6 down", "Put it down, lad. It is over."),
    ("7 home", "I want to go home."),
    ("8 forgive", "God forgive us. What have we done?"),
]
FREED = "The men around you lower their weapons, as if waking."
PARLEY = [
    ("1 parley", "You carry a spirit, and still you come at us. These men are mine, and they go where I send them.", None),
    ("2 withdraw", "Keep your ash heap, then. We have what we came for.", None),
    ("3 wrest", "<A thread of his spell tears loose in your hands.> You will not do that twice, spiritbearer.", None),
    ("4 again", "Back again. I felt you pull at them.", None),
]
CALL_OFF_NODE = "1740 Fixt call off the cathars"


def school(name, n):
    return ("CIsGreaterThanOrEqual", [("Operand1", ("CVariableSkill", [("Skill", "Skills/" + name)])), ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", str(n))]))])


def var_gt(path, n=0):
    return ("CIsGreaterThan", [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", path)])), ("Operator", ""),
                               ("Operand2", ("CConstant", [("Constant Value", str(n))]))])


def b_and(a, b):
    return ("CAND", [("Operand1", a), ("Operator", ""), ("Operand2", b)])


def b_not(a):
    return ("CExpressionNot", [("Operand1", a)])


def on_map(name):
    return ("CActionExpression", [("Action", exists(name))])


def note(text):
    return ("CPrintCombatTextAction", [("Text to print", text), ("Character to show text to", "Player1"), ("Emphasize", "0"), ("Suppress Duplicates", "0")])


def fx(where):
    return ("CSpawnEffectAction", [("Explosion Model", "Spell Effects/Hits and Effects/Summoning/Monster Summoning"), ("Location Entity", where),
                                   ("Make effect a child of the location entity", "0"), ("X Offset", "0"), ("Y Offset", "0"), ("Height Offset", "0"),
                                   ("Play Default Sound", "1"), ("Action to execute After Effect", "")])


def priest_cans():
    out = []
    for t in (" Tough", " Super"):
        rel = "Resources/" + PRIEST_CAN + t + ".can"
        if not (FX / rel).exists():
            c = lhbuild.read("Resources/" + E + "Priest" + t + ".can")
            c, n = re.subn(r"User Assigned Name=Druid\r\n", "User Assigned Name=" + PRIEST + CR, c)
            assert n == 1
            lhbuild.write_map(rel, c)
        out.append(rel)
    register(out)


def priest_groups():
    def group(mojo, can):
        return ("Group", ("CGeneratorAIGroup", [("Max Party Mojo", mojo), ("Quantity to generate min", "1"), ("Quantity to generate max", "1"),
                                                ("Things to Generate", ("Array", [("Item Count", "1"), ("Thing to Generate", ("CSpawnableCannedEntity", [("Weight", "1"), ("Entity", can)]))]))]))
    tiers = [("16", " Tough"), ("23", " Super"), ("40", " Super"), ("60", " Super")]
    items = [group(m, PRIEST_CAN + t) for m, t in tiers]
    return "Groups=" + B("Array", [("Item Count", str(len(items)))] + items).rstrip()


def trees():
    p = FX / ("Resources/" + WOKEN_TREE + ".DialogTree")
    if not p.exists():
        p.write_bytes(lhbuild.tree("English Soldier", [lhbuild.node(n, t, []) for n, t in WOKEN]).encode("latin-1"))
    p = FX / ("Resources/" + TREE + ".DialogTree")
    if p.exists():
        return
    take_all = ("CTakeManaFromCharacterAction", [("Character to take mana from", "$instigator"), ("Amount of mana to take", ("CExpressionManaRemaining", [])),
                                                 ("Expression Context", "$Instigator")])
    mana = ("CIsGreaterThanOrEqual", [("Operand1", ("CExpressionManaRemaining", [])), ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "20")]))])
    wrest_ok = B(*b_and(b_and(school("Tribal", 75), mana), on_map(THREADS)))
    wrest_no_mana = B(*b_and(b_and(school("Tribal", 75), b_not(mana)), on_map(THREADS)))
    talk = [
        {"req": "Speech moreequal 75", "text": "Your hold on them is thin. Every man you lose here is one less at your Shrine. Take your spell and go.",
         "go": "2 withdraw", "action": relay("Fixt War-Priest withdraws")},
        {"creq": wrest_ok, "text": "<The spell that holds them is a spirit's work. Take hold of it and pull.>", "go": "3 wrest",
         "action": multi([take_all, relay("Fixt War-Priest wrest")])},
        {"creq": wrest_no_mana, "text": "<You can feel his spell, but you have no strength left to pull at it.>", "go": ""},
        {"text": "Then I will cut them loose myself.", "go": "", "icon": "Exit Icon", "default": True},
    ]
    leave = [{"text": "<Leave.>", "go": "", "icon": "Exit Icon", "default": True}]
    nodes = [lhbuild.node("1 parley", PARLEY[0][1], talk), lhbuild.node("2 withdraw", PARLEY[1][1], leave),
             lhbuild.node("3 wrest", PARLEY[2][1], leave), lhbuild.node("4 again", PARLEY[3][1], talk)]
    p.write_bytes(lhbuild.tree(PRIEST, nodes).encode("latin-1"))


def weird_woman():
    """The Cathar friend is remembered as a character variable, and a Cathar friend can ask her to call the bears off."""
    p = FX / WW
    raw = lhbuild.read(WW)
    if CALL_OFF_NODE in raw:
        return 0
    crlf = raw.count(CR)
    w = raw
    mark = B(*flag(FRIEND))

    def wrap(block):
        """Every reply of the block gets the flag, beside whatever action it has."""
        out, last = "", 0
        replies = [m.start() + 2 for m in re.finditer(r"\r\n\r\nRequirement=", block)]
        ends = replies[1:] + [len(block)]
        for a, e in zip(replies, ends):
            r = block[a:e]
            if "Custom Action=" in r:
                k = r.index("Custom Action=") + len("Custom Action=")
                old = r[k:balanced(r, k)]
                r = r[:k] + "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR + \
                    "Action=" + old + CR + "Action=" + mark + "}" + CR + "}" + r[balanced(r, k):]
            else:
                k = r.index("Go to node ID=")
                k = r.index(CR, k) + 2
                r = r[:k] + "Custom Action=" + mark + r[k:]
            out += block[last:a] + r
            last = e
        return out + block[last:]

    blocks = w.split(DASH)
    n = 0
    for i, b in enumerate(blocks):
        nid = re.search(r"Node ID=([^\r\n]*)", b)
        if not nid:
            continue
        if nid.group(1) == "100 Favorable Return":
            blocks[i] = wrap(b)
            n += 1
        elif nid.group(1) == "50 Caverns":
            # only the two replies that make you a Cathar friend
            out, last = "", 0
            replies = [m.start() + 2 for m in re.finditer(r"\r\n\r\nRequirement=", b)]
            ends = replies[1:] + [len(b)]
            for a, e in zip(replies, ends):
                r = b[a:e]
                if "Target Name=cathar friend" in r:
                    r = wrap(CR + r)[2:]
                    n += 1
                out += b[last:a] + r
                last = e
            blocks[i] = out + b[last:]
        elif nid.group(1) == "06 Return Destroyed Montaillou":
            gate = B(*b_and(var_gt(FRIEND), b_not(var_gt(CALLED))))
            ask = CR + CR + "Requirement=!None" + CR + "Custom Requirement=" + gate + \
                "Reply Text=The Cathars' bears are tearing at me with the English. Call them off." + CR + "Go to node ID=" + CALL_OFF_NODE
            k = b.index(CR + CR + "Requirement=")
            blocks[i] = b[:k] + ask + b[k:]
            n += 1
    new = "Node ID=" + CALL_OFF_NODE + CR + "Text=They are frightened, and they do not know you as I do. Go. They will not touch you again." + CR + \
        "Should Have Voiceover=0" + CR + CR + "Requirement=!None" + CR + "Reply Text=Thank you." + CR + "Go to node ID=06 Return Destroyed Montaillou" + CR + \
        "Custom Action=" + B(*multi([("CForEachPlayerAction", [("Action", flag(CALLED))]), activate("Fixt Hamlet Cathars called off")])) + \
        "Is Default Reply=1" + CR
    w = DASH.join(blocks)
    k = w.rindex("}")
    w = w[:k] + DASH + CR + new + w[k:]
    assert w.count(CR) > crlf and "\n" not in w.replace(CR, ""), "line endings"
    p.write_bytes(w.encode("latin-1"))
    register([WW])
    return n


def stand_down_all(skip=()):
    return multi([druids.stand_down(b) for b in BANDS if b not in skip])


def two_phase(name, who, then, x, y):
    """Arms once `who` has been seen alive, then fires `then` when none is left. A rerun of the arming cannot fire it early."""
    armed = name + " armed"
    look = if_action(("CIsAliveAction", [("Name To Check For", who), ("Desired Minimum Count", "1")]),
                     multi([activate(armed), deactivate(name)]))
    fall = if_action(("CNotAction", [("Action", ("CIsAliveAction", [("Name To Check For", who), ("Desired Minimum Count", "1")]))]),
                     multi([then, deactivate(armed)]))

    def timer(act, first):
        return ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", act), ("Delay Between Actions", "2"),
                                          ("Plus or Minus", "0"), ("Seconds Till Next Execute", first)])
    return [lhbuild.entity(name, "1", [timer(look, "3")], "Editor/Position Marker", x, y),
            lhbuild.entity(armed, "0", [timer(fall, "2")], "Editor/Position Marker", x + 20, y)]


def build():
    z = lhbuild.read(MAP)
    if "New Name=" + PRIEST + CR in z:
        return None
    new = z
    gens = [x for x in parts(z) if "CGeneratorAI" in x]
    raid = []
    for x in gens:
        act = re.search(r"(?m)^\t\t\tActive=(\d)", x).group(1)
        name = re.search(r"(?m)^\t\t\tName=([^\r\n]*)", x).group(1)
        nn = re.search(r"New Name=([^\r\n]*)", x).group(1)
        full = re.findall(r"Entity=([^\r\n]*)", x)
        if act == "1" and not name and not nn and all(E + "Soldier" in e for e in full):
            raid.append(x)
    assert len(raid) == 21, len(raid)

    def band(x):
        px, py = pos(x)
        if px < 2100:
            return "Hamlet West"
        if px < 3600:
            return "Hamlet Square"
        return "Hamlet Northeast" if py < 1600 else "Hamlet Southeast"
    count = {}
    square = []
    for x in raid:
        b = band(x)
        count[b] = count.get(b, 0) + 1
        y = setting(x, "New Name", b + " Soldier")
        new = new.replace(x, y)
        if b == "Hamlet Square":
            square.append(y)
    # the War-Priest at the generator nearest the square's middle
    cx = sum(pos(x)[0] for x in square) / len(square)
    cy = sum(pos(x)[1] for x in square) / len(square)
    anchor = min(square, key=lambda x: (pos(x)[0] - cx) ** 2 + (pos(x)[1] - cy) ** 2)
    g = replace_groups(anchor, priest_groups())
    g = setting(g, "New Name", PRIEST)
    g = re.sub(r"(?m)^(\t\t\t)Name=[^\r\n]*", lambda m: m.group(1) + "Name=Fixt War-Priest post", g, count=1)
    g = g.replace("\t\t" + "Level Part=", "Level Part=", 1) + CR
    px, py = pos(anchor)

    # the staged squads with a priest: their own hold
    squads = []
    for x in gens:
        name = re.search(r"(?m)^\t\t\tName=([^\r\n]*)", x).group(1)
        nn = re.search(r"New Name=([^\r\n]*)", x).group(1)
        full = re.findall(r"Entity=([^\r\n]*)", x)
        if name not in SQUADS or nn:
            continue
        room = SQUADS[name]
        if all(E + "Priest" in e for e in full):
            new = new.replace(x, setting(x, "New Name", room + " Druid"))
        elif all(E + "Soldier" in e for e in full):
            new = new.replace(x, setting(x, "New Name", room + " Soldier"))
            sx, sy = pos(x)
            squads.append((room, sx, sy))

    # the Cathars' bears get a name the Weird Woman can reach
    bears = 0
    for x in gens:
        if "New Name=test guy" + CR in x and all("Cathar Bearform" in e for e in re.findall(r"Entity=([^\r\n]*)", x)):
            new = new.replace(x, x.replace("New Name=test guy" + CR, "New Name=" + CATHAR + CR, 1))
            bears += 1

    druids.TREE, druids.NODES = WOKEN_TREE, [n for n, _ in WOKEN]
    extra = [g]
    # 2. decapitation
    fell = multi([stand_down_all(), note("The War-Priest falls, and his hold on the English breaks."), deactivate(MAY_TALK), deactivate(THREADS)])
    extra += two_phase(WATCH, PRIEST, fell, px, py + 80)
    # 3. parley: he leaves, and takes his spell with him
    gone = multi([fx(PRIEST), deactivate(WATCH + " armed"), deactivate(MAY_TALK), deactivate(THREADS),
                  delay("0.5", ("CDeleteAction", [("Target Name", PRIEST)])), stand_down_all(), note("The War-Priest withdraws, and his hold on the English goes with him.")])
    extra.append(lhbuild.relay_part("Fixt War-Priest withdraws", gone, px + 40, py + 80))
    # 5. the wrest: one band per cast, his guard first
    steps = []
    for i, b in enumerate(BANDS):
        if i < len(BANDS) - 1:
            then = [activate(THREADS + " pulled"), delay("20", activate(MAY_TALK))]
        else:
            then = [deactivate(THREADS)]
        steps.append(("Action", multi([druids.stand_down(b), note(FREED)] + then)))
    wrest = ("CSeriesAction", [("Action", steps + [("Action", ("CSucceedAction", [("Action", "")]))]), ("When Done", "Repeat Last Action"),
                               ("Require Success To Advance", "0"), ("Next Action Index", "0")])
    extra.append(lhbuild.relay_part("Fixt War-Priest wrest", wrest, px + 60, py + 80, once="0"))
    extra.append(lhbuild.entity(THREADS, "1", [], "Editor/Position Marker", px + 80, py + 80))
    extra.append(lhbuild.entity(MAY_TALK, "1", [], "Editor/Position Marker", px + 100, py + 80))
    # he speaks when you come close, once, and again after each wrest
    first = if_action(exists(MAY_TALK), if_action(("CIsAliveAction", [("Name To Check For", PRIEST), ("Desired Minimum Count", "1")]),
                                                  multi([deactivate(MAY_TALK), if_action(exists(THREADS + " pulled"),
                                                                                         lhbuild.dialog(TREE, "4 again", PRIEST),
                                                                                         lhbuild.dialog(TREE, "1 parley", PRIEST))])))
    extra.append(lhbuild.touch_oval("Fixt War-Priest parley", first, px, py, radius="260", once="0"))
    extra.append(lhbuild.entity(THREADS + " pulled", "0", [], "Editor/Position Marker", px + 120, py + 80))
    # 4. the Weird Woman calls the bears off, and they stay off, including those the staged fights bring later
    calm = ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""),
                                      ("Action", multi(lhbuild.passive(CATHAR))), ("Delay Between Actions", "3"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "0")])
    extra.append(lhbuild.entity("Fixt Hamlet Cathars called off", "0", [calm], "Editor/Position Marker", px + 140, py + 80))
    # the staged squads
    for room, sx, sy in squads:
        extra += two_phase("Fixt " + room + " druid watch", room + " Druid", druids.stand_down(room), sx, sy + 60)
    # the priests' wolves need their source on this map
    hand = zipfile.ZipFile(lhbuild.VANILLA).read("Levels/5 Nostrodomus/02 Clan of the Hand A.zax").decode("latin-1")
    i = hand.index("\t\t\tName=Snakebreed Summoner Clone Generator" + CR)
    a = hand.rindex("Level Part=", 0, i)
    if druids.SOURCE not in new:
        extra.append(druids.wolf_source(hand[a:balanced(hand, a)]) + CR)
    lhbuild.write_map(MAP, lhbuild.add_parts(new, extra))
    register([MAP, "Resources/" + TREE + ".DialogTree", "Resources/" + WOKEN_TREE + ".DialogTree"])
    return count, len(squads), bears


def main():
    for path, short, text in ((FRIEND, "Fixt Cathar Friend", "1 means the Weird Woman knows the player as a friend of the Cathars."),
                              (CALLED, "Fixt Cathars Called Off", "1 means the Weird Woman has called the Cathars' bears off in the burned hamlet.")):
        rel = "Resources/" + path + ".DerivedCharacterAttribute"
        if not (FX / rel).exists():
            write_var(path, short, text)
        register([rel])
    priest_cans()
    trees()
    print("weird woman replies touched:", weird_woman())
    print("raid:", build())


if __name__ == "__main__":
    main()
