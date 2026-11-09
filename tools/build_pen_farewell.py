"""The prisoners of Toulouse leave on their feet. Issue #9: talk the titans into going, and the pen simply emptied.

`Peaceful Ending Relay` deleted the villagers and Thierry the moment Lethos agreed. Now it sets vanilla's own `peaceful
ending` checker, which nothing ever set, and they stay where they are until you tell them. Thierry leads them out along
the same e1-e10 path the normal escape uses. That relay is not reused: `Prisoners escape` activates his Montaillou
generator, which the peaceful ending has already done, and fires the titans' reaction to the escape. It also leans on
`Guards return relay` to take the walkers off at the end of the path, and that relay is off by now, so this does it.

If he is dead, a villager takes the same scene, and the child is left out of it.

Walking away is safe. Montaillou is resolved exactly when it always was, so the quest and Esclarmonde never wait on
this, and each spawn point clears the pen on the way back in, or he would stand in two towns at once. Any other ending
is untouched.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_pen_farewell.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, activate, balanced, balloon, deactivate, delay, dialog, exists, if_action, multi, node, relay

MAP = "Levels/3 Montaillou/Titan Village.zax"
DIALOG = "Levels/3 Montaillou/Dialog/"
THIERRY = DIALOG + "ToulouseAlexander"
GENERAL = DIALOG + "ToulouseGeneral"
SEP = "-" * 60 + CR
FLAG = "peaceful ending"
WALK = "Fixt pen walks out"
LEAD, FREE, NO_LEAD, NO_LEAD_2, CHILD, ASK = ("03 Fixt the camp is quiet", "04 Fixt free to go", "67 Fixt no Thierry",
                                             "68 Fixt no Thierry 2", "69 Fixt the child", "60 Fixt ask Thierry")


def alive(name):
    return ("CIsAliveAction", [("Name To Check For", name), ("Desired Minimum Count", "1")])


def remove_ai(name, ai):
    return ("CRemoveAIAction", [("Target Name", name), ("AI", ai), ("Delay Between Removes", "0")])


def done(name):
    return ("CSendAIDoneMessage", [("Target", name)])


def add_nodes(rel, before, nodes):
    z = lhbuild.read(rel)
    if nodes[0].split(CR)[0] in z:
        return
    key = "Node ID=" + before + CR
    assert z.count(key) == 1
    z = z.replace(key, "".join(n + SEP for n in nodes) + key)
    assert z.count(CR) == z.count("\n")
    (FX / rel).write_bytes(z.encode("latin-1"))


def trees():
    add_nodes("Resources/" + THIERRY + ".DialogTree", "20 Questions", [
        node(LEAD, "The camp has gone quiet. No shouting, no ogres at the fence, and nobody has come for the sheep. I have been a prisoner long enough to distrust quiet. What has happened out there?", [
            {"text": "The titans have gone. All of them. You are free to go.", "go": FREE},
            {"text": "I will come back for you.", "icon": "Exit Icon", "default": True}]),
        node(FREE, "Gone? Walked away, with nobody dead at the fence? <He grips the rail for a moment.> I will not ask what you said to them. I have a wife in Montaillou who has waited long enough, and I intend to correct her.", [
            {"text": "Then go. I will see you in Montaillou.", "action": relay(WALK), "icon": "Quest Icon", "default": True}]),
    ])
    add_nodes("Resources/" + GENERAL + ".DialogTree", "60 Villager Man 1", [
        node(ASK, "The ogres have gone, and nobody will say why. Thierry will know what to do. Ask him, please.", []),
        node(CHILD, "Is it over? Can we go home now?", []),
        node(NO_LEAD, "Thierry is dead, and Thierry is dead, and nobody will tell us how. Is it true? Is there nobody left to keep us here?", [
            {"text": "They are gone. You are free to go.", "go": NO_LEAD_2},
            {"text": "<Leave.>", "icon": "Exit Icon", "default": True}]),
        node(NO_LEAD_2, "Then we walk, and we do not stop until somebody stops us. God keep you.", [
            {"text": "Go safely.", "action": relay(WALK), "icon": "Quest Icon", "default": True}]),
    ])


def wrap_talk(z, name, nth, then):
    i = -1
    for _ in range(nth):
        i = z.index("\t\t\tName=" + name + CR, i + 1)
    i = z.index("Interaction Type=Interaction Specifiers/GetCloseThenTalk", i)
    s = z.index("Action=C", i)
    e = balanced(z, s)
    old = z[s:e]
    assert re.match(r"Action=C(SeriesAction|DisplayDialogTreeAction)\r\n", old)
    new = ("Action=CIfAction" + CR + "{" + CR + "If=" + B(*exists(FLAG)) + "Then=" + B(*then) + "Else=" + old[len("Action="):] + CR +
           "Return failure if the If failes=0" + CR + "}")
    return z[:s] + new + z[e:]


def pits(z):
    # The pen stays standing until spoken to, so a return visit has to clear it.
    clear = B(*if_action(exists(FLAG), multi([("CDeleteAction", [("Target Name", "Villager")]), ("CDeleteAction", [("Target Name", "Thierry")])])))
    i = z.index("\t\t\tName=start here" + CR)
    key = "Per Party Spawn Action=" + CR
    k = z.index(key, i)
    assert k - i < 900
    z = z[:k] + "Per Party Spawn Action=" + clear + z[k + len(key):]

    i = z.index("\t\t\tName=warp to toulouse" + CR)
    k = z.index("Per Party Spawn Action=CSeriesAction", i)
    a = z.index("Item Count=2", k)
    b = z.index("When Done=", a)
    block = z[a:b]
    assert len(re.findall(r"Action=\r\n", block)) == 2
    z = z[:a] + re.sub(r"Action=\r\n", lambda m: "Action=" + clear, block) + z[b:]

    i = z.index("\t\t\tName=crystal start here" + CR)
    k = z.index("Per Party Spawn Action=CMultipleActionsAction", i)
    a = z.index("Item Count=5" + CR, k)
    assert a - k < 200
    return z[:a] + "Item Count=6" + CR + "Action=" + clear + z[a + len("Item Count=5" + CR):]


def peace(z):
    i = z.index("Comment=Resolves Villagers")
    a = z.index("Item Count=5" + CR, i)
    assert a - i < 120
    s = z.index("Action=CDeleteAction", a)
    s = z.rindex(CR, 0, s) + len(CR)
    e = z.index("Action=CDeactivateAction", s)
    e = z.rindex(CR, 0, e) + len(CR)
    gone = z[s:e]
    assert "Target Name=villager" in gone and "Target Name=Thierry" in gone and "Delay=1" in gone
    z = z[:s] + "Action=" + B(*activate(FLAG)) + z[e:]
    return z[:a] + "Item Count=4" + z[a + len("Item Count=5"):]


def walk():
    return multi([
        if_action(alive("Thierry"), balloon(THIERRY, "99 Follow me", "Thierry")),
        remove_ai("Thierry", "CAIInteractionSpecifier"),
        remove_ai("Villager", "CAIInteractionSpecifier"),
        remove_ai("Thierry", "CSkeletonAI"),
        done("Thierry"),
        delay("0.5", remove_ai("Villager", "CSkeletonAI")),
        delay("0.5", done("Villager")),
        delay("28", multi([deactivate("Villager"), deactivate("Thierry")])),
    ])


def fixt_map():
    z = lhbuild.read(MAP)
    if WALK in z:
        return
    z = peace(z)
    z = wrap_talk(z, "Thierry Generator", 1, dialog(THIERRY, LEAD, "$trigger"))
    for nth, adult in ((1, False), (2, True), (3, True)):
        said = dialog(GENERAL, ASK, "$trigger") if adult else dialog(GENERAL, CHILD, "$trigger")
        lost = dialog(GENERAL, NO_LEAD, "$trigger") if adult else dialog(GENERAL, CHILD, "$trigger")
        z = wrap_talk(z, "Villager Generator", nth, if_action(alive("Thierry"), said, lost))
    z = pits(z)
    lhbuild.write_map(MAP, lhbuild.add_parts(z, [lhbuild.relay_part(WALK, walk(), 606, 893)]))


def main():
    trees()
    fixt_map()


if __name__ == "__main__":
    main()
