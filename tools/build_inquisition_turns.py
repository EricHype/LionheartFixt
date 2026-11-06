"""0.96.0: what follows Torquemada's death. Run after `build_torquemada.py`.

Starting the fight with him is the point of no return. It sets `Fixt Inquisition Hostile`, and from then
on every Inquisitor in Barcelona and Montaillou attacks on sight. Only one thing clears it: a deal with
Raphael, who stands apart in the foyer once Torquemada is dead.

    Deal                 neutral again. An Inquisitor pays nothing, anyone else pays all their gold
    Refuse or attack     a real fight, and the deal is gone for good
    Kill him             `Sede Vacante`, and the Inquisition breaks

Hostility is one relay per map, run from every spawn point, because the cans share no switch. Guards
carry scripts that end in jail, so the relay stands the jail relays down first. It reads player
variables and map names only, and it does nothing to anyone on a save without the flag.

The engine can only take a fixed sum, so the donation is a ladder of `CHasMoneyAction` and
`CTakeMoneyAction`, from 2^19 down to 1, which empties any purse exactly.

Raphael's fight and deal live in the mortal generator, which RESET picks. A dead Torquemada is read from
his two titles. Before that Raphael stays invulnerable, so you cannot skip to him.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_inquisition_turns.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, activate, balanced, deactivate, delay, exists, if_action, multi, relay
from build_inquisition_slides import ENDGAME, SLIDES, TITLES, VARS, flag, say, var_if, write_var
from build_torquemada import clone, give, part_span, title, to_combat, write_raw

HOSTILE = VARS + "Fixt Inquisition Hostile"
ABSOLVED = VARS + "Fixt Inquisition Absolved"
RAPHAEL_DEAD = VARS + "Fixt Raphael Dead"
SEDE = TITLES + "Sede Vacante"
FOYER = "Levels/1 Barcelona/Inquisition Foyer1.zax"
CHAMBERS = "Levels/1 Barcelona/Inquisition Chambers2.zax"
TREE_PATH = "Levels/1 Barcelona/Dialog/Temple District/InquisitorRaphael"
TREE = "Resources/" + TREE_PATH + ".DialogTree"
TEMPLATES = "Levels/1 Barcelona/Character Templates/Temple District/"
CAN = "Resources/" + TEMPLATES + "Inquisitor Raphael.can"
MORTAL_CAN = "Resources/" + TEMPLATES + "Inquisitor Raphael Mortal.can"
RACE = "Resources/Races/NPCs/Inquisitor Rahael.Race"
MORTAL_RACE = "Resources/Races/NPCs/Inquisitor Rahael Mortal.Race"
TURN = "Fixt Inquisition turns"
FIGHT = "Fixt Raphael fight"
DEAL = "Fixt Raphael deal"
RESET = "RESET MAP for Invulnerable Raphael"
GUARD_CAN = "Inquisition Guard Generic"

MAPS = {
    FOYER: ["Raphael Sends you to jail", "Guards pissed", "Detected Spellcast"],
    CHAMBERS: ["Grand Inquisitor Sends you to jail", "Guard chasing player"],
    "Levels/1 Barcelona/Inquisition Forest Exterior.zax": [],
    "Levels/1 Barcelona/Temple District.zax": ["Yard sends you to jail"],
    "Levels/1 Barcelona/Gate District.zax": [],
    "Levels/1 Barcelona/Port District.zax": [],
    "Levels/3 Montaillou/04 Inn Interior.zax": [],
    "Levels/3 Montaillou/05 Church Interior.zax": [],
}
CAN_RE = re.compile(r"Entity=Levels/[^\r\n]*/(Inquisition Guard Generic|Inquisitor Generic|Inquisitor Monk Generic|"
                    r"Inquisitor Sermon|Inquisitor Agent|Inquisitor Fournier|Inquisitor Dominguez Pac Man|"
                    r"Prison Inquisition Jailor)\r\n")
SKIP = {"Guard to DIE", "Inquisitor Fugitive1", "Fixt Torquemada guard", "Inquisition Buyer", ""}

MEMBER = ("The Grand Inquisitor has died of a fever. It will be recorded so by nightfall, and I will sign it. "
          "<He does not look up.> You were his instrument, child. Now you are mine, whether you wish it or not. "
          "Leave Barcelona. The men at the door do not read what I sign.")
OUTSIDER = ("A fever took the Grand Inquisitor. That is what the Holy Office will write, because the alternative is "
            "that one heathen walked into these chambers and out again. <He looks at you at last.> I suppose I "
            "expected too much of him. You will make a donation to the Holy Office. All of it. It is a small price "
            "for the absolution of your sin.")

SLIDE_TEXT = {
    "900 order inquisition dark": (
        "The Inquisition entered the siege with a new head. Torquemada died in his own chambers, and the Holy Office "
        "recorded it as a fever. The truth was worse: the hand that killed him still wore the mark. Raphael knew. He "
        "took the chair within the year, and he burned more than Torquemada ever had, with better records. The "
        "cities paid for the wood. No one ever named you. He never needed to. The archive keeps a box with nothing "
        "written on it, and its keepers lower their voices."),
    "900 order inquisition broken": (
        "The Inquisition entered the siege with a new head. Torquemada died in his own chambers, at the hand of "
        "someone who owed the Holy Office nothing, and it recorded a fever. Raphael took the chair within the year. "
        "He burned more than Torquemada ever had, with better records. Within ten years, no city dared stop paying "
        "for the wood. No one in those cities knew your name. The Holy Office did. It kept the page open."),
    "900 order inquisition donated": (
        "The Inquisition entered the siege with a new head. Torquemada died in his own chambers, at the hand of "
        "someone who owed the Holy Office nothing, and it recorded a fever. Raphael took the chair within the year. "
        "He burned more than Torquemada ever had, with better records. Your gold paid for the first of the wood. "
        "Within ten years, no city dared stop paying for the rest. The receipt is in the archive, made out to a "
        "penitent. It is the only page with your name on it."),
    "900 order inquisition dark sede": (
        "The Inquisition entered the siege without a head, and without the man who would have been the next one. You "
        "had worn its mark, and you killed them both. Nobody was left to write a fever. The Holy Office lost its chair "
        "and its story in the same week. His would-be successors agreed on nothing, and the fires burned low. Within "
        "ten years, some cities stopped paying for the wood. The archive keeps your name under a heading it invented "
        "for the purpose. Nobody has ever been entered there since."),
    "900 order inquisition broken sede": (
        "The Inquisition entered the siege without a head, and without the man who would have been the next one. You "
        "owed the Holy Office nothing, and you killed them both. Nobody was left to write a fever. Its would-be "
        "successors fought over the chair for years. The fires did not go out, but they burned low. Within ten years, "
        "some cities stopped paying for the wood. No one in those cities knew your name. The Holy Office did. It "
        "never again had the strength to do anything about it."),
    "900 order cult contested": (
        "The Dark Inquisitors paid you for Bishop Diego. Nobody paid you for Torquemada, though it was the job they "
        "wanted most. They came down from the plains in good habits, with good letters, and found Raphael in the "
        "chair. There was no honest bishop left to read them, and he did not need one. Within a generation it was "
        "hard to say whether he had burned them or hired them."),
}


# ---- race, can, title -------------------------------------------------------------------------

def mortal_race():
    r = lhbuild.read(RACE)
    r, n = re.subn(r"(\(AC\) Armor Class\s+Value To Preset=)1000", r"\g<1>200", r)
    assert n == 1
    r, n = re.subn(r"(\(HP\) Hit Points\s+Value To Preset=)10000", r"\g<1>220", r)
    assert n == 1
    r, n = re.subn(r"((?:Fire|Cold|Electrical) Damage Resistance\s+Value To Preset=)\d+", r"\g<1>50", r)
    assert n == 3, n
    r = re.sub(r"((?:Acid|Crushing|Disease|Piercing|Poison|Slashing) Damage Resistance\s+Value To Preset=)\d+", r"\g<1>25", r)
    assert not re.search(r"Value To Preset=9[0-9]\r|Value To Preset=100\r", r)
    write_raw(MORTAL_RACE, r)


def mortal_can():
    z = lhbuild.read(CAN)
    assert z.count("Race=Races/NPCs/Inquisitor Rahael" + CR) == 1 and z.count("\t\tCategory=Spell Immunity" + CR) == 1
    z = z.replace("Race=Races/NPCs/Inquisitor Rahael" + CR, "Race=Races/NPCs/Inquisitor Rahael Mortal" + CR)
    z = z.replace("\t\tCategory=Spell Immunity" + CR, "\t\tCategory=" + CR)
    s = z.index("Destroyed Script Action=")
    e = balanced(z, s)
    was = z[s + len("Destroyed Script Action="):e]
    assert "FACTION Inquisitor Killer" in was
    death = multi([("CForEachPlayerAction", [("Action", multi([was, flag(RAPHAEL_DEAD), give(SEDE)]))])])
    z = z[:s] + "Destroyed Script Action=" + B(*death) + z[e + len(CR):]
    lhbuild.write_map(MORTAL_CAN, z)


# ---- hostility --------------------------------------------------------------------------------

def spawn_names(z):
    out = []
    for m in CAN_RE.finditer(z):
        e = z.index(CR + "\t\t}" + CR, m.start())
        n = re.search(r"New Name=([^\r\n]*)", z[m.start():e])
        name = n.group(1).strip() if n else ""
        if name not in SKIP and name not in out:
            out.append(name)
    return out


def turn_relay(z, stand_down):
    extra = []
    if "Fixt Torquemada fight" in z:
        extra = [if_action(exists("Fixt Torquemada is dead"), "", relay("Fixt Torquemada fight"))]
    body = multi([deactivate(n) for n in stand_down] + [to_combat(n) for n in spawn_names(z)] + extra)
    return delay(1.5, var_if(HOSTILE, var_if(ABSOLVED, "", body), ""))


def wire_spawns(z):
    out, i = "", 0
    key = "Per Party Spawn Action="
    while True:
        j = z.find(key, i)
        if j < 0:
            return out + z[i:]
        start = j + len(key)
        if z.startswith(CR, start):
            out += z[i:start] + B(*relay(TURN)).rstrip(CR)
            i = start
        else:
            e = balanced(z, start)
            out += z[i:start] + B(*multi([relay(TURN), z[start:e]])).rstrip(CR)
            i = e


def hostile_maps():
    for rel, stand_down in MAPS.items():
        z = lhbuild.read(rel)
        if "\t\t\tName=" + TURN + CR in z:
            continue
        action = turn_relay(z, stand_down)
        z = wire_spawns(z)
        z = lhbuild.add_parts(z, [lhbuild.relay_part(TURN, action, 40, 40, once="0")])
        lhbuild.write_map(rel, z)


# ---- the chambers: starting his fight is the point of no return -------------------------------

def chambers_flag():
    z = lhbuild.read(CHAMBERS)
    if "Fixt Inquisition Hostile" in part_text(z):
        return
    s, e = part_span(z, "Fixt Torquemada fight")
    p = z[s:e]
    k = p.index("Item Count=", p.index("Action=CMultipleActionsAction"))
    n = int(re.match(r"Item Count=(\d+)", p[k:]).group(1))
    head = "Item Count=%d" % n
    add = "Action=" + B("CForEachPlayerAction", [("Action", flag(HOSTILE))]) + "Action=" + B(*relay(TURN))
    p = p[:k] + "Item Count=%d" % (n + 2) + CR + add + p[k + len(head) + len(CR):]
    lhbuild.write_map(CHAMBERS, z[:s] + p + z[e:])


def part_text(z):
    s, e = part_span(z, "Fixt Torquemada fight")
    return z[s:e]


# ---- the foyer ---------------------------------------------------------------------------------

def titled(then, els):
    def has(perk, a, b):
        return ("CIfExpressionAction", [
            ("If Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [
                ("Item Count", "1"), ("Perk To Check For", TITLES + perk)]))])),
            ("Character to get attributes from", "Player1"), ("Then", a), ("Else", b)])
    return has("Dark Inquisitor", then, has("Breaker of the Hammer", then, els))


def foyer():
    z = lhbuild.read(FOYER)
    if "Fixt Mortal Raphael generator" in z:
        return
    s, e = part_span(z, "Inquisitor Raphael generator")
    gen = z[s:e]
    a = gen.index("\t\t\t\t\t\t\tAction=CIfAction")
    b = balanced(gen, a + 7)
    greet = ("CIfExpressionAction", [
        ("If Expression", ("CUseCannedExpressionExpression", [("Canned Expression", "Dialog/Requirements/Faction/Inquisitor IS")])),
        ("Character to get attributes from", "$Instigator"),
        ("Then", lhbuild.dialog(TREE_PATH, "1300 Fixt the fever member", "$trigger")),
        ("Else", lhbuild.dialog(TREE_PATH, "1300 Fixt the fever", "$trigger"))])
    gen2 = gen[:a] + "\t\t\t\t\t\t\tAction=" + B(*greet) + gen[b + len(CR):]
    a = gen2.index("After Action=CMultipleActionsAction")
    b = gen2.index("New Facing Angle=", a)
    after = multi([
        ("CSetDamagedScriptActionAction", [("New Damaged Action", relay(FIGHT)), ("Target Name", "$Instigator")]),
        ("CAddAIAction", [("Target Name", "$Instigator"),
                          ("AI", ("CHandleMessageAI", [("Marked For Deletion", "0"), ("Publisher", ""),
                                                       ("Message To Handle", "Gotocombat"), ("Action", relay(FIGHT))])),
                          ("Delay Between Adds", "0")]),
        ("CAddCategoryAction", [("Target Name", "$Instigator"), ("Categories to add", "NonInteractiveSequence Actor")])])
    gen2 = gen2[:a] + "After Action=" + B(*after) + gen2[b:]
    assert gen2.count("Name=Inquisitor Raphael generator") == 1
    gen2 = gen2.replace("Name=Inquisitor Raphael generator", "Name=Fixt Mortal Raphael generator")
    old = "Entity=" + TEMPLATES + "Inquisitor Raphael" + CR
    assert gen2.count(old) == 1
    gen2 = gen2.replace(old, "Entity=" + TEMPLATES + "Inquisitor Raphael Mortal" + CR)

    s, e = part_span(z, RESET)
    reset = z[s:e]
    i = reset.index("Source Name=Inquisitor Raphael generator")
    c = reset.rindex("Action=CDelayAction", 0, i)
    d = balanced(reset, c)
    u = reset.index("Action=CDeleteAction", d)
    v = balanced(reset, u)
    assert "Used Raphael Generator" in reset[u:v]
    pick = titled(var_if(ABSOLVED, "", var_if(RAPHAEL_DEAD, "", clone("Fixt Mortal Raphael generator", "Used Raphael Generator"))),
                  var_if(HOSTILE, "", clone("Inquisitor Raphael generator", "Used Raphael Generator")))
    reset = reset[:c] + "Action=" + B(*pick).rstrip(CR) + reset[v:]
    k = reset.index("Item Count=10" + CR)
    reset = reset[:k] + "Item Count=9" + reset[k + len("Item Count=10"):]
    z = z[:s] + reset + z[e:]

    fight = multi([
        deactivate(FIGHT), deactivate("Raphael Sends you to jail"), deactivate("Guards pissed"), deactivate("Detected Spellcast"),
        ("CRemoveAIAction", [("Target Name", "Inquisitor Raphael"), ("AI", "CAIInteractionSpecifier"), ("Delay Between Removes", "0")]),
        ("CForEachPlayerAction", [("Action", flag(HOSTILE))]),
        to_combat("Inquisitor Raphael"), to_combat("Inquisitor Guard")])
    deal = multi([
        ("CFadeScreenDownAction", [("Time Until Auto Fade Up", "2")]),
        delay(1, multi([("CDeleteAction", [("Target Name", "Inquisitor Raphael")]), relay(RESET)]))])
    z = lhbuild.add_parts(z, [lhbuild.relay_part(FIGHT, fight, 880, 1180, once="0"),
                              lhbuild.relay_part(DEAL, deal, 880, 1200, once="1"),
                              gen2.lstrip("\t")])
    lhbuild.write_map(FOYER, z)


# ---- the conversation --------------------------------------------------------------------------

def donation():
    steps = []
    for power in range(19, -1, -1):
        n = str(2 ** power)
        steps.append(if_action(("CHasMoneyAction", [("Character to Check", "$instigator"), ("Value to check for", n)]),
                               ("CTakeMoneyAction", [("Take From", "$instigator"), ("Value to take", n)])))
    return steps


def tree():
    z = lhbuild.read(TREE)
    if "1300 Fixt the fever" in z:
        return
    refuse = lambda text: ("Requirement=!None" + CR + "Reply Text=" + text + CR + "Go to node ID=" + CR +
                           "Custom Action=" + B(*relay(FIGHT)) + "Icon=Fight Icon" + CR)
    accept = lambda text, acts: ("Requirement=!None" + CR + "Reply Text=" + text + CR + "Go to node ID=" + CR +
                                 "Custom Action=" + B(*multi(acts)) + "Icon=Exit Icon" + CR + "Is Default Reply=1" + CR)
    add = ("Node ID=1300 Fixt the fever member" + CR + "Text=" + MEMBER + CR + "Should Have Voiceover=0" + CR + CR +
           accept("<Say nothing, and leave the mark where it is.>", [flag(ABSOLVED), relay(DEAL)]) + CR +
           refuse("You are next, Raphael.") + "-" * 60 + CR +
           "Node ID=1300 Fixt the fever" + CR + "Text=" + OUTSIDER + CR + "Should Have Voiceover=0" + CR + CR +
           accept("<Hand over your purse.>", [flag(ABSOLVED)] + donation() + [relay(DEAL)]) + CR +
           refuse("I did not kill one Inquisitor to pay another.") + "-" * 60 + CR)
    key = "Node ID=1000 attack raphael" + CR
    assert z.count(key) == 1
    z = z.replace(key, add + key)
    assert z.count(CR) == z.count("\n")
    (FX / TREE).write_bytes(z.encode("latin-1"))


# ---- the ending --------------------------------------------------------------------------------

def slides():
    z = lhbuild.read(SLIDES)
    if "900 order inquisition donated" in z:
        return
    for nid in ("900 order inquisition dark", "900 order inquisition broken"):
        z, n = re.subn(r"(Node ID=" + nid + r"\r\nText=)[^\r\n]*", lambda m: m.group(1) + SLIDE_TEXT[nid], z)
        assert n == 1
    add = ""
    for nid in ("900 order inquisition donated", "900 order inquisition dark sede", "900 order inquisition broken sede", "900 order cult contested"):
        add += ("Node ID=" + nid + CR + "Text=" + SLIDE_TEXT[nid] + CR + "Should Have Voiceover=1" + CR + CR +
                "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR +
                "Custom Action=" + B(*relay("Fixt order epilogue relay")) + "Is Default Reply=1" + CR + "-" * 60 + CR)
    key = "Node ID=900 order wielder ring" + CR
    assert z.count(key) == 1
    z = z.replace(key, add + key)
    assert z.count(CR) == z.count("\n")
    (FX / SLIDES).write_bytes(z.encode("latin-1"))


def sede_if(then, els):
    return ("CIfExpressionAction", [
        ("If Expression", ("CHasPerkExpression", [("Perks To Check For", ("Array", [
            ("Item Count", "1"), ("Perk To Check For", SEDE)]))])),
        ("Character to get attributes from", "Player1"), ("Then", then), ("Else", els)])


def endgame_all():
    z = lhbuild.read(ENDGAME)
    if "900 order inquisition donated" in z:
        return

    def dark():
        return sede_if(say("900 order inquisition dark sede"), say("900 order inquisition dark"))

    def broken():
        return sede_if(say("900 order inquisition broken sede"),
                       var_if(ABSOLVED, say("900 order inquisition donated"), say("900 order inquisition broken")))

    def cult():
        return sede_if(say("900 order cult inherited"), say("900 order cult contested"))

    for node, build, want in (("900 order inquisition dark", dark, 1), ("900 order inquisition broken", broken, 1),
                              ("900 order cult inherited", cult, 2)):
        marker = "Node ID=" + node + CR
        hits = []
        pos = 0
        while True:
            k = z.find(marker, pos)
            if k < 0:
                break
            s = max(z.rfind("Then=CDisplayDialogTreeAction", 0, k), z.rfind("Else=CDisplayDialogTreeAction", 0, k))
            assert k - s < 260, node
            hits.append(s)
            pos = k + 1
        assert len(hits) == want, (node, len(hits))
        for s in reversed(hits):
            e = balanced(z, s)
            z = z[:s] + z[s:s + 5] + B(*build()).rstrip(CR) + z[e:]
    lhbuild.write_map(ENDGAME, z)


def main():
    write_var(HOSTILE, "Fixt Inquisition Hostile", "1 means the player started the fight with Torquemada or Raphael.")
    write_var(ABSOLVED, "Fixt Inquisition Absolved", "1 means Raphael took the deal, and the Inquisition stands down.")
    write_var(RAPHAEL_DEAD, "Fixt Raphael Dead", "1 means the player killed Inquisitor Raphael.")
    if not (FX / MORTAL_RACE).exists():
        mortal_race()
    if not (FX / MORTAL_CAN).exists():
        mortal_can()
    title(SEDE, "Sede Vacante", "The seat of the Holy Office stands empty, and you emptied it. Twice.")
    foyer()
    chambers_flag()
    hostile_maps()
    tree()
    slides()
    endgame_all()


if __name__ == "__main__":
    main()
