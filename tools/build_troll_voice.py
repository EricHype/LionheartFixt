"""The trolls talk like trolls, and taking their ore unpaid is warned before it is theft. Reported from play after 0.99.23:
"his dialog is very long, which doesn't make a lot of sense", the entrance troll "also speaks too much", and "when we open
the red rock chest near him, he disappeared, but we still got the dialog and everything turned hostile".

**The voice.** Vanilla gave the trolls two lines, both in the register the drones' barks keep: *"You! Stop! No welcome."* and
*"We no trust Eduardo no more. We no trust no one. Too many dead Trolls."* Fixt grew `Warning Troll` to 37 nodes with a
median of 443 characters and one of 880, in fluent literary prose with paragraph-long stage directions. Every node is
rewritten here, keeping every fact, gate, reply and quest step: the entrance troll in the drones' full troll grammar, the
chief in a steadier one (short plain sentences, few articles dropped) because he is the one in charge, and the field
narration cut to what the player sees. Lengths are asserted.

**The chest.** 0.11.0 made opening the trolls' ore chest unpaid, with the peace held and the chief alive, fire the map's
`Troll desecration relay`. That relay was made for the old chief's body field: it DELETES `Troll Chief` and force-generates
a new one from `Troll answer chief`, a different spot, then opens `127`/`128` (about walking on their dead) with
`Speaker=$trigger`, which here is the chest. So the chief vanished in front of the player and a conversation about the
wrong crime opened from a box. Now the chest has its own scene:

* the first unpaid open does not open it: the chief says *"Not yours. You pay first."* over his head, and `ore warned` is
  switched on (an inactive checker, the way `ore paid` works);
* opening it again is theft: the chief, where he stands, speaks `93 theft` himself (`Speaker=Troll Chief`, a named speaker as
  vanilla's `Speaker=Shakespeare`), and its one reply breaks the peace the way the desecration relay does: the peace keeper
  goes, every troll goes to combat, and `The Chief Before` fails if it is active.

The body field keeps the desecration relay, which is what it was made for. **Reach:** the text reaches every save; the chest
reaches a Troll Pit not yet entered, and new games.

A rerun is a no-op.

    python tools/build_troll_voice.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH
from build_shrine_repairs import register

TREE_REL = "Resources/Levels/Sewers/Dialog/Warning Troll.DialogTree"
TREE = "Levels/Sewers/Dialog/Warning Troll"
MAP = "Levels/Sewers/05 Troll Pit.zax"
WARNED = "ore warned"

# the entrance troll: the drones' own grammar
DRONE = {
    # the hide this node once handed over is the chief's to give now; see build_troll_choices.py
    "30 troll trade": "<It looks at you a long time.> Wererats gone? They take Trolls. In the dark. Many. Now none. We count. You go to chief. My people not touch you.",
    "40 parley": "Small one. Yes. Is in the deep. Not my rock to give. You talk to chief. Chief is far end, where rock goes red. I say word down. My people not touch you.",
}
# the chief: steadier, still a troll
CHIEF = {
    "95 the chief": "<He is a head taller than the rest.> You walk in my rock, and my people let you. So. Say it.",
    "133 the hide": "Hides out there that nobody wears. You counted them. Take one. My word on it.",
    "96 the boy": "The small one. He put his hands in our ore. Not the first time. Your city takes from this rock and pays nothing. We keep him. He is what we caught.",
    "97 the price": "<He spreads one hand, and closes it twice.> Two hundred. Not for him. For the times we did not catch him.",
    "98 talked down": "<A long silence.> A child. Sent by men who are not. Take him. Tell the men above we counted every time.",
    "99 debt settled": "<He steps aside.> Go. Find him. We do not fetch. My people will not touch you today. Do not take that for gladness.",
    "100 the ore": "Not need. Owed. Red ore goes up on a small man's back. Once, iron came down for it. Now nothing. It goes to the smith, Eduardo. We are not thieves. We will not be robbed by them.",
    "101 terms given": "Then carry it whole. <He counts on his fingers.> The smith sends one man, in daylight. He knocks and waits. Pays iron, not coin. Same man every time, so we know the face.",
    "102 word carried": "<He calls something over his shoulder.> Daylight. Same face. Good. <He nods at a chest across the pit.> Take one, with your own hands. They will watch and not move. The first is not sold.",
    "110 the field of them": "You saw. Good. The one before me lies out there, among the ones who came for the ore. He stopped them there. We have not gone to him.",
    "111 why not": "A chief is counted by one who was not there. We were all there, and none of us stopped it. You owe him nothing. Go. Count him, and each of ours near him. Then tell me.",
    "112 counted": "<He is quiet a long time.> Then he is counted. <He calls one word down the pit, and many trolls start moving east.> Now we fetch them. All of them. It waited long enough.",
    "130 the man above": "Enrique Garcia. The beggars' man. He pays men to come down, and we put them on the rock. We cannot go up. A troll in your streets rings a bell.",
    "131 say it then": "<He weighs you.> Then say this. We never came up. Not once. All of it happened down here, to the ones who came. Ask him what he pays for.",
    "132 no price": "<He sits down, slowly. The floor complains.> No price. Every day I was chief, a price. I do not know the work without one. I will learn. Go careful on the stairs.",
    "150 he sizes you up": "<He looks away first, slowly. A courtesy.> You are not big. You stand like something hit that did not fall. Big is common down here.",
    "151 the bell": "<He looks at you properly.> Ah. Same word, near enough. You can walk up those stairs. I cannot. But you did not need telling what this place is.",
    "127 the chief knows": "<He is there, looking where the body was.> I asked you because you owed him nothing. I did not know there was a third thing you could be. <The rock starts to sound.> Do not run.",
    "128 the chief knows unasked": "<He is there, looking at the mark in the dust.> He stood here and stopped them. He is why there is still an us. You took him like a thing off a shelf. Try the rest of us.",
    "160 the peace broken rite": "<He looks at the one you put down.> You counted our chief, and the number was true. We fetched our dead for it. So I do not ask why. <The rock starts to sound.> We count you with the others.",
    "161 the peace broken ore": "Same man each time, so we know the face. I asked that. You carried it. My people watched you take ore and did not move. They watch now. <The rock starts to sound.> Come, then.",
    "162 the peace broken word": "You said the men above owed us. Not the small one. You made them stop paying. I believed you, and stopped watching the door. <The rock starts to sound.> Nobody sends you now. You came for free.",
}
# the player looking at the old chief's field
FIELD = {
    "120 the field": "<A huge lava troll lies on his back, arms out. Around him: wererats, thieves' dogs, thieves, a big man in Barcelona leathers. They lie where they fell.>",
    "121 the counting": "<You count him, then the four of his lying close. Five. It takes less than a minute. It only needed someone who was not there.>",
    "122 the ground says": "<His four lie on every side, as if they ran to him. The thieves face away. One still holds a bow, no arrow nocked. It ended fast.>",
    "123 who paid for this": "<Wererats and thieves, dead together, and they are enemies. Someone hired both for the same night, and told neither.>",
    "124 a lot of them": "<Thirteen. The big one fell too. Whatever came, it was worse than him.>",
    "125 the field after": "<Drag marks lead back to the pit. The trolls took their dead. Only the eight who came for the ore are left.>",
    "126 the field desecrated": "<A shape in the dust where he lay, and he is gone. Back in the pit, a sound goes through the rock.>",
}
NEW = {
    "92 not yours": "Not yours. You pay first.",
    "93 theft": "<He does not shout.> That is ours. I told you. <The rock starts to sound.>",
}
LIMIT = 200


def break_peace():
    groups = ["Lava Troll", "Troll Chief", "warning troll"]
    acts = [("CDeactivateAction", [("Target Name", "Troll Peace Keeper")])]
    for g in groups:
        acts += [("CSendAIDoneMessage", [("Target", g)]), ("CGoToCombatAction", [("Enemy Name", g)])]
    acts.append(("CSetQuestSatusToFailedIfActiveAction", [("Quest", "Levels/Sewers/Quests/The Chief Before")]))
    return lhbuild.multi(acts)


def build_tree():
    t = lhbuild.read(TREE_REL)
    if "Node ID=93 theft" + CR in t:
        return 0
    for nid, text in {**DRONE, **CHIEF, **FIELD}.items():
        assert len(text) <= LIMIT, (nid, len(text))
        m = re.search(r"Node ID=" + re.escape(nid) + r"\r\nText=([^\r\n]*)\r\n", t)
        assert m, nid
        t = t[:m.start(1)] + text + t[m.end(1):]
    theft = lhbuild.node("93 theft", NEW["93 theft"], [
        {"text": "<There is nothing to say.>", "action": break_peace(), "icon": "Fight Icon", "default": True}])
    warn = lhbuild.node("92 not yours", NEW["92 not yours"], [])
    assert t.endswith("}" + CR)
    t = t[:-len("}" + CR)] + DASH + CR + warn + DASH + CR + theft + "}" + CR
    (lhbuild.FX / TREE_REL).write_bytes(t.encode("latin-1"))
    register([TREE_REL])
    return len(DRONE) + len(CHIEF) + len(FIELD)


def build_chest():
    z = lhbuild.read(MAP)
    if "\t\t\tName=" + WARNED + CR in z:
        return 0
    # the warning flag: a copy of the `ore paid` checker, inactive until the chief has warned you
    i = z.index("\t\t\tName=ore paid" + CR)
    s = z.rindex("\t\tLevel Part=", 0, i)
    e = lhbuild.balanced(z, s)
    flag = z[s:e].replace("\t\t\tName=ore paid" + CR, "\t\t\tName=" + WARNED + CR, 1).lstrip("\t") + CR
    # the chest's peace branch: warn the first time, theft the second, and never the desecration relay
    i = z.index("\t\t\tName=red ore chest" + CR)
    s = z.rindex("\t\tLevel Part=", 0, i)
    e = lhbuild.balanced(z, s)
    chest = z[s:e]
    old = re.search(r"(?ms)^(\t*)Then=CMultipleActionsAction\r\n.*?Relay Name=Troll desecration relay\r\n", chest)
    assert old, "chest branch"
    b = lhbuild.balanced(chest, old.start())
    branch = chest[old.start():b]
    assert "Node ID=91 that is ours" in branch and branch.count("CTriggerRelayAction") == 1 and branch.count("CDisplayDialogBalloonAction") == 1, branch[:200]
    warn = lhbuild.multi([lhbuild.balloon(TREE, "92 not yours", "Troll Chief", "-70"), lhbuild.activate(WARNED)])
    theft = lhbuild.dialog(TREE, "93 theft", "Troll Chief")
    new = "Then=" + B(*lhbuild.if_action(("CCheckExistenceAction", [("Name To Check For", WARNED), ("Desired Minimum Count", "1")]), theft, warn))
    chest = chest[:old.start()] + old.group(1) + new.rstrip(CR) + chest[b:]
    z = z[:s] + chest + z[e:]
    lhbuild.write_map(MAP, lhbuild.add_parts(z, [flag]))
    register([MAP])
    return 1


def main():
    print("troll nodes rewritten:", build_tree(), "| chest:", build_chest())


if __name__ == "__main__":
    main()
