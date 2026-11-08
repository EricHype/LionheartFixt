"""Act 7's druids are real, they call wolves, and on the three front maps they are what holds the soldiers.

0.19.0 put `Levels/7 English Shrine/Character Templates/Druid` into 195 spawn slots to bring the cult into its own shrine.
That can is a vanilla English Soldier, model, race and all, with a blank Category, blank Valid Targets and Max Distance 40:
the pacified shape. It spawned soldiers who stood until struck. The act's real druids are the Priest cans ("Druid") and
the Priestess cans ("Druidess"), whose three templates vanilla placed nowhere. Each slot now takes the real can at its tier,
the group's place in the generator: Priest on the front maps, Priestess deeper, as 0.19.0 meant.

**Wolves.** A druid at half health calls one wolf, once. The pattern is vanilla's Snakebreed Summoner: a one-shot series in
the can clones a hidden, inactive generator that the map holds, here `Fixt Druid Wolf Source`. A druid on a map without one
calls nothing, as the Summoner already does in the Grove, so priests elsewhere are untouched in practice.

**The hold.** On Temple Initiate, Stone Chamber and the Antechamber, the soldier generators take a room name and two
dedicated druid generators stand among them. While any druid of that room lives, the soldiers fight. When the last falls,
every soldier of that room stands down, says a dazed line, and can be talked to. Hit one and the whole room turns on you
again: the first hit of the room swaps them back together, so it runs once. No Karma here: these men were fighting you.
A click reads only an entity's first specifier, so the talk one goes on only after the fight one is removed.

Exalted Chambers and the Secret Chamber mix soldiers and priests in every generator, and a generator names all it spawns,
so they are not held. Crossroads to England turns three of its seven identical archer pairs into druids.

A rerun is a no-op.

    python tools/build_shrine_druids.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, balloon, delay, if_action, multi
from build_crossroads_standard import forget_specifier, specifier

SHRINE = "Levels/7 English Shrine/"
CROSSING = "Levels/6 Barcelona Attack/Crossroads to England map.zax"
PASSIVE = "Levels/7 English Shrine/Character Templates/Druid"
E = "Monster Cans/English Enemies/"
DRUID = [E + "Priest", E + "Priest Tough", E + "Priest Super", E + "Priest Super"]
DRUIDESS = [E + "Priestess", E + "Priestess Tough", E + "Priestess Super", E + "Priestess Super"]
FRONT = {"02 Temple Initiate": "Temple", "03 Stone Chamber": "Stone Chamber", "04 Antechamber of Lore": "Antechamber"}
DEEP = ["05 Exalted Chambers", "06 Meditation Chamber1", "07 Meditation Chamber2", "08 Meditation Chamber3", "09 Secret Chamber", "10 Inner Sanctum"]
SOURCE = "Fixt Druid Wolf Source"
USED = "Fixt Used Druid Wolf Source"
WOLF = "Druid Wolf"
WOLVES = [("16", "Monster Cans/Animals/Wolf Gray"), ("23", "Monster Cans/Animals/Wolf Gray Tough"),
          ("40", "Monster Cans/Animals/Wolf Black Tough"), ("60", "Monster Cans/Animals/Wolf Black Super")]
TREE = "Levels/7 English Shrine/Dialog/Fixt Shrine Woken"
LINES = [
    ("1 where", "Where am I? This is no barracks."),
    ("2 priests", "The priests. They were in my head."),
    ("3 dragon", "I heard a dragon. I swear I heard a dragon."),
    ("4 weeks", "How long have I been down here?"),
    ("5 stand down", "Stand down, lads. Stand down."),
    ("6 orders", "Whose orders were we following?"),
    ("7 lord", "My lord never sent us here."),
    ("8 forgive", "God forgive me. I would have killed you."),
]
NODES = [n for n, _ in LINES]


def parts(z):
    return re.findall(r"(?ms)^\t\tLevel Part=\w+\r\n\t\t\{\r\n.*?^\t\t\}", z)


def groups(x):
    """(start, end) of each CGeneratorAIGroup in a generator part, in order."""
    out = []
    for m in re.finditer(r"Group=CGeneratorAIGroup\r\n", x):
        out.append((m.start(), balanced(x, m.end() - 2)))
    return out


def swap(x, table):
    """The passive can, replaced in each group by the real one at that group's tier."""
    if PASSIVE not in x:
        return x
    out, last = "", 0
    for n, (a, b) in enumerate(groups(x)):
        g = x[a:b].replace("Entity=" + PASSIVE + CR, "Entity=" + table[min(n, 3)] + CR)
        out += x[last:a] + g
        last = b
    return out + x[last:]


def setting(x, key, value):
    x, n = re.subn(r"(?m)^(\s*)" + re.escape(key) + r"=[^\r\n]*", lambda m: m.group(1) + key + "=" + value, x, count=1)
    assert n == 1, key
    return x


def druid_groups(table):
    def group(mojo, qty, can):
        return ("Group", ("CGeneratorAIGroup", [("Max Party Mojo", mojo), ("Quantity to generate min", qty), ("Quantity to generate max", qty),
                                                ("Things to Generate", ("Array", [("Item Count", "1"), ("Thing to Generate", ("CSpawnableCannedEntity", [("Weight", "1"), ("Entity", can)]))]))]))
    items = [group("16", "1", table[0]), group("23", "1", table[1]), group("40", "1", table[2]), group("60", "2", table[3])]
    return "Groups=" + B("Array", [("Item Count", str(len(items)))] + items).rstrip()


def wolf_groups():
    items = [("Group", ("CGeneratorAIGroup", [("Max Party Mojo", m), ("Quantity to generate min", "1"), ("Quantity to generate max", "1"),
                                              ("Things to Generate", ("Array", [("Item Count", "1"), ("Thing to Generate", ("CSpawnableCannedEntity", [("Weight", "1"), ("Entity", c)]))]))]))
             for m, c in WOLVES]
    return "Groups=" + B("Array", [("Item Count", str(len(items)))] + items).rstrip()


def replace_groups(x, new):
    i = x.index("Groups=Array")
    return x[:i] + new + x[balanced(x, i):]


def wolf_source(template):
    """Vanilla's Snakebreed source, with wolves in it, no sixty-second expiry, and our names."""
    x = replace_groups(template, wolf_groups())
    x = x.replace("Comment=Snakebreed Summoner Clone Generator", "Comment=" + SOURCE)
    x = x.replace("\t\t\tName=Snakebreed Summoner Clone Generator", "\t\t\tName=" + SOURCE)
    x = setting(x, "New Name", WOLF)
    effect = ("CSpawnEffectAction", [("Explosion Model", "Spell Effects/Hits and Effects/Summoning/Monster Summoning"), ("Location Entity", "$Instigator"),
                                     ("Make effect a child of the location entity", "1"), ("X Offset", "0"), ("Y Offset", "0"), ("Height Offset", "0"),
                                     ("Play Default Sound", "1"), ("Action to execute After Effect", "")])
    after = multi([effect, ("CPlaySoundAction", [("Sound", "Spells/Monster Summon.ogg"), ("Position", "$Trigger"), ("Multiplayer", "Heard by all players")]),
                   delay("1", ("CDeleteAction", [("Target Name", USED)]))])
    i = x.index("After Action=CMultipleActionsAction")
    v = i + len("After Action=")
    return x[:v] + B(*after).rstrip() + x[balanced(x, v):]


def summon(who):
    """Once per druid, at half health: the can's damage slot, beside what it already does."""
    clone = ("CCloneAction", [("New Location", "$Trigger"), ("Copy Height", "0"), ("Random Location Delta", "80"), ("Warp Behavior", ""),
                              ("Source Name", SOURCE), ("New Name", USED), ("Set Facing Angle", "0"), ("New Facing Angle", "0")])
    line = ("CPrintCombatTextAction", [("Text to print", who + " calls a wolf to her side."), ("Character to show text to", "Player1"),
                                       ("Emphasize", "0"), ("Suppress Duplicates", "0")])
    once = ("CSeriesAction", [("Action", [("Action", multi([line, clone])), ("Action", ("CSucceedAction", [("Action", "")]))]),
                              ("When Done", "Repeat Last Action"), ("Require Success To Advance", "1"), ("Next Action Index", "0")])

    def hp(cmp, v):
        return ("CExpressionAction", [("Expression", (cmp, [("Operand1", ("CExpressionHealthPercent", [])), ("Operator", ""),
                                                            ("Operand2", ("CConstant", [("Constant Value", v)]))])), ("Character to get attributes from", "$Trigger")])
    return if_action(hp("CIsLessThanOrEqual", "50"), if_action(hp("CIsGreaterThan", "0"), once))


def cans():
    done = 0
    for can in sorted(set(DRUID + DRUIDESS)):
        rel = "Resources/" + can + ".can"
        z = lhbuild.read(rel)
        if SOURCE in z:
            continue
        who = re.search(r"User Assigned Name=([^\r\n]*)", z).group(1)
        k = z.index("Damaged Script Action=")
        v = k + len("Damaged Script Action=")
        e = balanced(z, v)
        old = z[v:e]
        new = "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR + "Action=" + old + CR + \
              "Action=" + B(*summon(who)) + "}" + CR + "}"
        lhbuild.write_map(rel, z[:v] + new + z[e:])
        done += 1
    return done


def woken_tree():
    p = FX / ("Resources/" + TREE + ".DialogTree")
    if p.exists():
        return
    t = "CDialogTree" + CR + "{" + CR + "Name=English Soldier" + CR + "Portrait=!None" + CR + "Should Have Voiceovers=0" + CR + \
        "Default Canceled Node Action=" + CR
    for n, text in LINES:
        t += "-" * 60 + CR + lhbuild.node(n, text, [])
    p.write_bytes((t + "}" + CR).encode("latin-1"))


def stand_down(room):
    men, druids = room + " Soldier", room + " Druid"
    say = ("CRandomAction", [("Action", ("Array", [("Item Count", str(len(NODES)))] + [("Action", balloon(TREE, n, "$trigger", "-80")) for n in NODES]))])
    once_each = ("CAddAIAction", [("Target Name", men), ("AI", ("CRepeatTimerTriggerAI", [
        ("Marked For Deletion", "0"), ("Publisher", ""),
        ("Action", ("CSeriesAction", [("Action", [("Action", ("CDelayAction", [("Next Action", ("CRandomAction", [("Action", ("Array", [("Item Count", str(len(NODES)))] + [
            ("Action", ("CDisplayDialogBalloonAction", [("Dialog Tree File", TREE), ("Node ID", n), ("Name of Position", "$Trigger"), ("Position Offset", "0.000000,-80.000000"),
                        ("After Action", ""), ("Include In Log", "0")])) for n in NODES]))])), ("Delay", "1.5"), ("Plus or Minus", "1.5"), ("Forget Trigger", "0")])),
            ("Action", ("CSucceedAction", [("Action", "")]))]), ("When Done", "Repeat Last Action"), ("Require Success To Advance", "0"), ("Next Action Index", "0")])),
        ("Delay Between Actions", "600"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "0")])), ("Delay Between Adds", "0")])
    turn = multi([
        ("CSetTargetTypeAction", [("Entity Name", men), ("Name To Target", ""), ("Valid Targets", "Player,Player Friend")]),
        ("CAddCategoryAction", [("Target Name", men), ("Categories to add", "Enemy")]),
        forget_specifier(men),
        specifier(men, "GetCloseThenTriggerAndFight", ""),
        ("CGoToCombatAction", [("Enemy Name", "$Trigger")])])
    calm = ("CNotAction", [("Action", ("CCheckCategoryAction", [("Target Name", "$Trigger"), ("Category to check for", "Enemy")]))])
    room_turns = if_action(("CCheckCategoryAction", [("Target Name", "$Instigator"), ("Category to check for", "Player,Player Friend")]), if_action(calm, turn))
    return multi([
        ("CSetTargetTypeAction", [("Entity Name", men), ("Name To Target", ""), ("Valid Targets", "")]),
        ("CRemoveCategoryAction", [("Target Name", men), ("Categories To Remove", "Enemy")]),
        ("CSetDamagedScriptActionAction", [("New Damaged Action", room_turns), ("Target Name", men)]),
        once_each,
        forget_specifier(men),
        specifier(men, "GetCloseThenTalk", say),
    ])


def watcher(room, x, y):
    """Polls for the room's druids. They spawn on the map's first tick, so the first look waits ten seconds."""
    falls = "Fixt " + room + " druids fall"
    look = if_action(("CNotAction", [("Action", ("CIsAliveAction", [("Name To Check For", room + " Druid"), ("Desired Minimum Count", "1")]))]),
                     ("CTriggerRelayAction", [("Relay Name", falls)]))
    timer = ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", look), ("Delay Between Actions", "2"),
                                       ("Plus or Minus", "0"), ("Seconds Till Next Execute", "10")])
    return [lhbuild.relay_part(falls, multi([stand_down(room), ("CDeactivateAction", [("Target Name", "Fixt " + room + " druid watch")])]), x, y),
            lhbuild.entity("Fixt " + room + " druid watch", "1", [timer], "Editor/Position Marker", x + 20, y)]


def pos(x):
    p = re.findall(r"Position X=(-?[\d.]+)\r\n\s*Position Y=(-?[\d.]+)", x)[-1]
    return float(p[0]), float(p[1])


def soldierly(x, passive=False):
    """Only soldiers spawn here. On a held map a passive slot counts, and the druid that replaces it is held with them."""
    e = re.findall(r"Entity=([^\r\n]*)", x)
    return e and all(re.search(r"English Enemies/Soldier", i) or (passive and i == PASSIVE) for i in e)


def front(rel, room, source):
    z = lhbuild.read(rel)
    if "Name=" + room + " Druid" + CR in z:
        return 0
    gens = [x for x in parts(z) if "CGeneratorAI" in x]
    new = z
    held = []
    for x in gens:
        y = swap(x, DRUID)
        nn = re.search(r"New Name=([^\r\n]*)", y).group(1)
        if soldierly(x, passive=True) and not nn:
            y = setting(y, "New Name", room + " Soldier")
            held.append(y)
        new = new.replace(x, y)
    # two druid posts, at the two largest held generators farthest apart
    big = sorted(held, key=lambda x: -len(x))[:6]
    a = big[0]
    b = max(big[1:], key=lambda x: (pos(x)[0] - pos(a)[0]) ** 2 + (pos(x)[1] - pos(a)[1]) ** 2)
    posts = []
    for n, anchor in enumerate((a, b), 1):
        g = replace_groups(anchor, druid_groups(DRUID))
        g = setting(g, "New Name", room + " Druid")
        g = re.sub(r"(?m)^(\t\t\t)Name=[^\r\n]*", lambda m: m.group(1) + "Name=Fixt " + room + " druid post " + str(n), g, count=1)
        g = re.sub(r"(?m)^(\t\t\t)Active=\d", lambda m: m.group(1) + "Active=1", g, count=1)
        posts.append(g.replace("\t\t" + "Level Part=", "Level Part=", 1) + CR)
    px, py = pos(a)
    new = lhbuild.add_parts(new, posts + watcher(room, px, py + 60) + [source])
    lhbuild.write_map(rel, new)
    return len(held)


def deep(rel, source):
    z = lhbuild.read(rel)
    if PASSIVE not in z and SOURCE in z:
        return
    new = z
    for x in [x for x in parts(z) if "CGeneratorAI" in x]:
        new = new.replace(x, swap(x, DRUIDESS))
    if SOURCE not in new:
        new = lhbuild.add_parts(new, [source])
    lhbuild.write_map(rel, new)


def crossing(source):
    z = lhbuild.read(CROSSING)
    if SOURCE in z:
        return 0
    archers = [x for x in parts(z) if "CGeneratorAI" in x and soldierly(x) and "Bow" in x and not re.search(r"New Name=[^\r\n]", x)]
    new = z
    for x in archers[:3]:
        new = new.replace(x, replace_groups(x, druid_groups(DRUID)))
    lhbuild.write_map(CROSSING, lhbuild.add_parts(new, [source]))
    return min(3, len(archers))


def main():
    import zipfile
    z = zipfile.ZipFile(lhbuild.VANILLA)
    hand = z.read("Levels/5 Nostrodomus/02 Clan of the Hand A.zax").decode("latin-1")
    i = hand.index("\t\t\tName=Snakebreed Summoner Clone Generator" + CR)
    a = hand.rindex("Level Part=", 0, i)
    source = wolf_source(hand[a:balanced(hand, a)]) + CR
    print(cans(), "druid cans call wolves")
    woken_tree()
    for m, room in FRONT.items():
        print(m, front(SHRINE + m + ".zax", room, source), "soldier generators held")
    for m in DEEP:
        deep(SHRINE + m + ".zax", source)
    print(crossing(source), "archer pairs at the crossing are druids now")
    mods = FX.parent / "mod.json"
    text = mods.read_bytes().decode("utf8")
    rel = "Resources/" + TREE + ".DialogTree"
    if '"' + rel + '"' not in text:
        nl = "\r\n" if "\r\n" in text else "\n"
        anchor = '    "Levels/8 Alamut/01 Desert Sprawl.zax",'
        add = ['    "' + rel + '",'] + ['    "Resources/' + c + '.can",' for c in sorted(set(DRUID + DRUIDESS)) if '"Resources/' + c + '.can"' not in text]
        mods.write_bytes(text.replace(anchor, nl.join(add) + nl + anchor).encode("utf8"))


if __name__ == "__main__":
    main()
