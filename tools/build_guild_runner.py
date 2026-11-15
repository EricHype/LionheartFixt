"""A guild runner at both sewer entrances takes a thieves' ally straight to Juanita for 5 gold. Requested from play: "one of
the more frustrating parts of play is having to go back to Juanita when you side with the thieves guild, you have to cross
the same area over and over again and nothing is happening there."

**Who.** A copy of `Weak sewer entrance theif4sword`, vanilla's peaceful thief (no targets, no `Enemy`, one talk
specifier whose action is empty), named `Guild Runner`, with that empty action filled by his conversation. One stands
beside each arrival point in `01 Sewer Main Entrance`: `Start Here`, where the Port District drops you, and
`From Temple District`.

**When.** Each is a `CSimpleGeneratorForCannedEntitiesAI`, inactive, the way `Tomas Generator` waits for its door. Both
arrival points' `Per Party Spawn Action` now ask, every arrival: if *Help the Thieves Destroy the Beggars Guild* has been
started and has not failed, the runners' generators are activated, and a generator makes its runner once; if it has failed
(the player refused Juanita, *"I'll not kill for you again"*), any runner is deleted. Nothing else in either action changes.

**The trip.** *"Take me to Juanita."* costs 5 gold (`CTakeMoneyAction`, shown only with `CHasMoneyAction` 5) and is the same
`CRelocateAction` the sewer's own transitions use, to `test only` in `02 Thieves Congregation`, an existing spawn point
about 190 from Juanita whose spawn action does nothing. Existing, so it is there in any save.

**Reach.** The runners and the arrival checks are in `01 Sewer Main Entrance`, so they reach a save that has not entered the
sewers yet, and new games: a visited map is frozen into the save, and nothing in the engine creates an entity in another
map (every one of the 912 vanilla `COtherMapAction`s acts on something that already exists there).

A rerun is a no-op.

    python tools/build_guild_runner.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

MAP = "Levels/Sewers/01 Sewer Main Entrance.zax"
SOURCE = "Resources/Levels/Sewers/Character Templates/Weak sewer entrance theif4sword.can"
RUNNER_CAN = "Levels/Sewers/Character Templates/Fixt Guild Runner"
TREE = "Levels/Sewers/Dialog/Fixt Guild Runner"
RUNNER = "Fixt Guild Runner"
QUEST = "Levels/Sewers/Quests/Help the Thieves Destroy the Beggars Guild"
PRICE = "5"
DEST_MAP, DEST = "Sewers/02 Thieves Congregation", "test only"
# arrival point -> where its runner stands (50 to the side, so the player does not land on him)
POSTS = {"Start Here": (5489, 3053), "From Temple District": (3246, 781)}


def gen_name(post):
    return "Fixt Guild Runner at " + post


def money(n):
    return ("CActionExpression", [("Action", ("CHasMoneyAction", [("Character to Check", "$instigator"), ("Value to check for", n)]))])


def build_tree():
    rel = "Resources/" + TREE + ".DialogTree"
    if (lhbuild.FX / rel).exists():
        return 0
    trip = lhbuild.multi([("CTakeMoneyAction", [("Take From", "$instigator"), ("Value to take", PRICE)]),
                          ("CRelocateAction", [("Return to map", "unlikely soon"), ("New Map Name", DEST_MAP), ("New Location", DEST),
                                               ("Who To Switch", "$Instigator"), ("Relative Position", "0"), ("Ignore Party Ready Rules", "0")])])
    nodes = [
        lhbuild.node("1 runner", "<A wiry lad in a thief's coat, cleaning his nails with a knife.> Juanita's? Five gold, and I know the quick way. No rats, no beggars.", [
            {"creq": B(*money(PRICE)), "text": "Take me to Juanita. <Pay five gold.>", "action": trip, "icon": "Quest Icon"},
            {"creq": B("CExpressionNot", [("Operand1", money(PRICE))]), "text": "I do not have five gold.", "go": "2 broke"},
            {"text": "Not now.", "icon": "Exit Icon", "default": True}]),
        lhbuild.node("2 broke", "Then you walk, like everyone else.", []),
    ]
    (lhbuild.FX / rel).write_bytes(lhbuild.tree("Guild Runner", nodes).encode("latin-1"))
    register([rel])
    return len(nodes)


def build_can():
    rel = "Resources/" + RUNNER_CAN + ".can"
    if (lhbuild.FX / rel).exists():
        return 0
    t = lhbuild.read(SOURCE)
    assert t.count("Activity=CAIInteractionSpecifier") == 1
    i = t.index("Interaction Type=Interaction Specifiers/GetCloseThenTalk" + CR)
    m = re.compile(r"(\t*)Action=\r\n").search(t, i)
    assert m and m.start() - i < 200
    talk = B(*lhbuild.dialog(TREE, "1 runner", "$trigger"))
    t = t[:m.start()] + m.group(1) + "Action=" + talk + t[m.end():]
    t, n = re.subn(r"User Assigned Name=Thief Swordsman", "User Assigned Name=Guild Runner", t)
    assert n == 1
    lhbuild.write_map(rel, t)
    register([rel])
    return 1


def generator(post, x, y):
    ai = ("CSimpleGeneratorForCannedEntitiesAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Already Generated", "0"),
                                                  ("Entity", RUNNER_CAN), ("New Name", RUNNER), ("Remove Default AIs", "0"),
                                                  ("AIs to Add", ("Array", [("Item Count", "0")])),
                                                  ("Canned AIs to Add", ("Array", [("Item Count", "0")])), ("After Action", "")])
    return lhbuild.entity(gen_name(post), "0", [ai], "Editor/Character Generator Point", x, y)


def arrival_check():
    sided = ("CAndAction", [("Action", ("Array", [("Item Count", "2"),
                            ("Action", ("CWasQuestEverActivatedAction", [("Quest", QUEST)])),
                            ("Action", ("CNotAction", [("Action", ("CIsQuestFailedAction", [("Quest", QUEST)]))]))])), ("Early Exit", "0")])
    show = lhbuild.multi([lhbuild.activate(gen_name(p)) for p in POSTS])
    turned = lhbuild.if_action(("CIsQuestFailedAction", [("Quest", QUEST)]), ("CDeleteAction", [("Target Name", RUNNER)]))
    return lhbuild.if_action(sided, show, turned)


def build_map():
    z = lhbuild.read(MAP)
    if gen_name("Start Here") in z:
        return 0
    check = B(*arrival_check())
    for post in POSTS:
        i = z.index("\t\t\tName=" + post + CR)
        s = z.rindex("\t\tLevel Part=", 0, i)
        e = lhbuild.balanced(z, s)
        part = z[s:e]
        m = re.search(r"(?m)^(\t*)Per Party Spawn Action=([^\r\n]*)\r\n", part)
        b = lhbuild.balanced(part, m.start()) if m.group(2) else m.end() - len(CR)
        old = re.sub(r"\r\n\t*", CR, part[m.start():b]).lstrip("\t")[len("Per Party Spawn Action="):]
        if old.startswith("CMultipleActionsAction" + CR):
            # append to the existing list, at the start of its closing-brace line
            arr = old.index("Action=Array")
            end = lhbuild.balanced(old, arr)
            n = int(re.search(r"Item Count=(\d+)", old[arr:]).group(1))
            old = old.replace("Item Count=" + str(n) + CR, "Item Count=" + str(n + 1) + CR, 1)
            end = lhbuild.balanced(old, arr)
            close = old.rindex(CR, 0, end) + len(CR)
            assert old[close:end] == "}", repr(old[close:end])
            new = old[:close] + "Action=" + check + old[close:]
        else:
            new = "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR + \
                  "Action=" + old + CR + "Action=" + check + "}" + CR + "}"
        part = part[:m.start()] + m.group(1) + "Per Party Spawn Action=" + new.rstrip(CR) + part[b:]
        z = z[:s] + part + z[e:]
    z = lhbuild.add_parts(z, [generator(p, x, y) for p, (x, y) in POSTS.items()])
    lhbuild.write_map(MAP, z)
    register([MAP])
    return 1


def main():
    print("tree:", build_tree(), "| runner can:", build_can(), "| map:", build_map())


if __name__ == "__main__":
    main()
