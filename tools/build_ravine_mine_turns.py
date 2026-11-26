"""The silver mine in Ravine Cave West turns as one, spares the Khan's friends, and its foreman talks. Reported: "in the
western part of the cave, after i was hostile to the goblins, the pack on the right, further from the green crystal,
was not hostile like the others. I had to attack them first", then: "Why can't they follow the flag set by becoming
hostile to their leader".

cf1df05 pacified the archer post at the Scar Ravine mouth and put the foreman Nurg beside it, so a parley could happen,
and left the three deep posts as vanilla's hostile goblins. Nothing linked the two: a player who came in by the
teleport from the east cave fought the deep posts, and the mouth pack went on standing there peaceful until struck.
The foreman also had Hrargrub's trap, a talk specifier added behind his can's fight one (a click reads only the first,
`0x46b0f0`). And the mine never read goblin standing, so the Khan's Champion was shot by the Khan's own miners.

  * **One flag.** `Fixt mine turned`, lit by `Fixt mine turns` (once), which restores `Player,Player Friend` and
    `Enemy` on `Mine Guards` and `Mine Foreman`, gives Nurg his fight specifier back and sends them all to combat.
    Every mine goblin's damaged script fires it (the Mongol Camp's way), and so does Nurg's fight, `70 combat`.
    A goblin spawned after it is lit is left hostile.
  * **Who is spared.** A character the Horde counts as its own (`Goblin Horde IS`: Chum, Blooded or Champion, not
    Traitor) finds the whole mine at peace. Anyone else meets the mouth pack and Nurg holding fire for the parley, and
    the deep posts hostile: the back door is a fight, but now the whole mine joins it.
  * **Nurg talks.** His spawn forgets the can's specifier before adding the talk one.

Standing is read at spawn, so it is what the character held on the first visit. Map edits: a `Ravine Cave West` not
yet entered. The tree edit reaches every save. A rerun is a no-op.

    python tools/build_ravine_mine_turns.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, relay, activate, if_action, multi
from build_shrine_repairs import register
from build_crossroads_standard import forget_specifier, specifier

MAP = "Levels/Wilderness Maps/Ravine Cave West.zax"
TREE = "Resources/Levels/Wilderness/Dialog/Fixt Mine Foreman.DialogTree"
GUARDS, FOREMAN = "Mine Guards", "Mine Foreman"
TURN, TURNED = "Fixt mine turns", "Fixt mine turned"
MOUTH_X = "2387.5"

FRIEND = ("CExpressionAction", [("Expression", ("CUseCannedExpressionExpression", [
    ("Canned Expression", "Dialog/Requirements/Faction/Goblin Horde IS")])), ("Character to get attributes from", "Player1")])
NOT_TURNED = ("CNotAction", [("Action", ("CCheckExistenceAction", [("Name To Check For", TURNED), ("Desired Minimum Count", "1")]))])
CALM = [("CSetTargetTypeAction", [("Entity Name", "$Instigator"), ("Name To Target", ""), ("Valid Targets", "")]),
        ("CRemoveCategoryAction", [("Target Name", "$Instigator"), ("Categories To Remove", "Enemy")])]
LINKED = ("CSetDamagedScriptActionAction", [("New Damaged Action", relay(TURN)), ("Target Name", "$Instigator")])


def talk():
    return specifier("$Instigator", "GetCloseThenTalk", ("CDisplayDialogTreeAction", [
        ("Dialog Tree File", "Levels/Wilderness/Dialog/Fixt Mine Foreman"), ("Node ID", "1 the foreman challenges you"),
        ("Speaker", "$trigger"), ("Player Being Spoken To", "$Instigator")]))


def guard_after(mouth):
    calm = multi(CALM + [LINKED])
    if mouth:  # the parley post holds fire for everyone
        body = calm
    else:      # a deep post holds fire only for the Khan's friends, and is linked either way
        body = if_action(FRIEND, calm, LINKED)
    return if_action(NOT_TURNED, body)


FOREMAN_AFTER = if_action(NOT_TURNED, multi(CALM + [forget_specifier("$Instigator"), talk(), LINKED]))


def hostile(name):
    return [("CSetTargetTypeAction", [("Entity Name", name), ("Name To Target", ""), ("Valid Targets", "Player,Player Friend")]),
            ("CAddCategoryAction", [("Target Name", name), ("Categories to add", "Enemy")])]


TURN_ACTION = multi([activate(TURNED)] + hostile(GUARDS) + hostile(FOREMAN) +
                    [forget_specifier(FOREMAN), specifier(FOREMAN, "GetCloseThenTriggerAndFight", ""),
                     ("CGoToCombatAction", [("Enemy Name", FOREMAN)]), ("CGoToCombatAction", [("Enemy Name", GUARDS)])])


def set_after(p, action):
    a = p.index("After Action=")
    v = a + len("After Action=")
    end = v + len(CR) if p.startswith(CR, v) else lhbuild.balanced(p, v) + len(CR)
    return p[:v] + B(*action) + p[end:]


def build_map():
    z = lhbuild.read(MAP)
    if "Name=" + TURN + CR in z:
        return []
    out, last, guards, foreman = [], 0, 0, 0
    for m in re.finditer(r"\r\n\t\tLevel Part=", z):
        s = m.start() + len(CR)
        e = lhbuild.balanced(z, s)
        p = z[s:e]
        nn = re.search(r"New Name=([^\r]*)\r\n", p)
        if "Activity=CGeneratorAI" in p and nn and nn.group(1) in (GUARDS, FOREMAN):
            x = re.search(r"\r\n\t\t\tPosition X=([^\r]*)\r\n", p).group(1)
            if nn.group(1) == FOREMAN:
                p = set_after(p, FOREMAN_AFTER)
                foreman += 1
            else:
                p = set_after(p, guard_after(x == MOUTH_X))
                guards += 1
            out.append(z[last:s] + p)
            last = e
    out.append(z[last:])
    z = "".join(out)
    assert (guards, foreman) == (4, 1), (guards, foreman)
    z = lhbuild.add_parts(z, [lhbuild.checker(TURNED, 2360, 960), lhbuild.relay_part(TURN, TURN_ACTION, 2380, 960)])
    lhbuild.write_map(MAP, z)
    return [MAP]


def build_tree():
    t = lhbuild.read(TREE)
    s = t.index("Node ID=70 combat" + CR)
    e = t.index("-" * 60, s)
    node = t[s:e]
    if "Relay Name=" + TURN in node:
        return []
    m = re.search(r"Item Count=(\d+)\r\n", node)
    node = node[:m.start()] + "Item Count=" + str(int(m.group(1)) + 1) + CR + "Action=" + B(*relay(TURN)) + node[m.end():]
    t = t[:s] + node + t[e:]
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    return [TREE]


def main():
    done = build_map() + build_tree()
    if done:
        register(done)
    print("ravine mine turns:", done)


if __name__ == "__main__":
    main()
