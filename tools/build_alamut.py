"""Act 8, from the 0.99.0 survey of Alamut: every ending reaches the stage, four repairs, the Acid Wash, and variety.

**Endings.** Nostradamus's ending tree runs on three maps, and since 0.71.0 its Escape fired `Fixt order epilogue relay`, which
lives only on the last battle map. There it is now the stage's source, so Escape skipped the stage; on Calle Perdida and the
Demesne it named nothing, and Escape could stall the credits. Escape now fires `Fixt Nostradamus continues`, which each map
defines as what its own conversation's reply does. And the dark ending, which went from Nostradamus straight to the credits and
never showed one Fixt slide, now goes to the stage like the rest.

**Repairs.**
* The goblin gate on Desert Sprawl asked whether `Goblin Khan is Dead` and `Grumdjum Dead` exist, and those markers live in
  Inquisition Chambers2 and Lake: an existence check sees only its own map. It reads character variables now. Grumdjum's
  companion variable already records a death (2 killed, 3 dead); the Khan's can sets a new one where it activates his marker.
* Grumdjum's recorded "Are you ready to continue our quest" had no trigger after 0.25.2. It greets you now when you go back to
  him after dismissing him.
* The Old Man's escape advanced through a relay queued half a second after he was deleted. The relay goes first now.
* Ten recorded nodes were flagged not to voice, among them siblings of voiced ones. They voice.

**The Acid Wash** was a channel whose sluices hurt only you while the archers watched. The acid now hurts anyone standing in
it, and a valve near the entrance, found by searching like any secret, shuts both sluices before you run them.

**Variety.** An Assassin Master at half health has an even chance of calling two guard dogs, once, by the clone pattern the
Shrine's druids use. A quarter of the desert's beast generators field Sand Spirits instead, a creature Desert Sprawl already
has four of.

**Companions.** The Knight of Saladin and Grumdjum each say one line on the first visit to the Acid Wash and the Dark Temple.
The Final Encounter is left alone, because its arrival is a cutscene.

A rerun is a no-op.

    python tools/build_alamut.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, activate, balanced, delay, if_action, multi, relay
from build_inquisition_slides import VARS, flag, write_var
from build_shrine_repairs import into_relay, register
from build_shrine_druids import parts, replace_groups, groups, wolf_source, setting
import build_shrine_druids as druids

A = "Levels/8 Alamut/"
SIEGE, CALLE, DEMESNE = A + "END GAME Siege Map.zax", A + "END GAME Calle Perdida.zax", A + "END GAME Nostrodomus Demesne.zax"
NOSTRA = "Resources/Levels/8 Alamut/Dialog/Nostrodomus Ending.DialogTree"
CONTINUES = "Fixt Nostradamus continues"
STAGE_ARRIVE = "Fixt Stage Arrival"
KHAN_DEAD = VARS + "Fixt Khan Slain"  # one record of his death; see build_carryovers.py
GRUMDJUM_VAR = VARS + "Fixt Companion Goblin Grumdjum"
KING_CAN = "Resources/Levels/Wilderness/Character Templates/Goblin King.can"
REJOIN_CAN = "Resources/Common Objects and Scripts/Fixt Dialog Indirection/Grumdjum companion joins.can"
FINAL = A + "08 Final Encounter.zax"
ACID = A + "05 Acid Wash.zax"
MUTED = {
    "Resources/Levels/8 Alamut/Dialog/AlamutAssassinCan.DialogTree": ["1 Conversation Start", "10 Goodbye", "20 master", "30 step aside"],
    "Resources/Levels/8 Alamut/Dialog/DaVinci Ending.DialogTree": ["10 Evil Ending All Die", "18 DaVinci Talk Evil2"],
    "Resources/Levels/8 Alamut/Dialog/Elemental Spirit Ending.DialogTree": ["10 Good Ending All Die", "40 Player wins outright"],
    "Resources/Levels/8 Alamut/Dialog/Galileo Ending.DialogTree": ["10 Good Ending All Survive"],
    "Resources/Levels/8 Alamut/Dialog/OldMan.DialogTree": ["300 inquisition scene"],
}
DOG_SOURCE, DOG_USED, DOG = "Fixt Assassin Dog Source", "Fixt Used Assassin Dog Source", "Assassin Dog"
DOGS = [("16", "Monster Cans/Animals/Guarddog"), ("23", "Monster Cans/Animals/Guarddog Tough"),
        ("40", "Monster Cans/Animals/Guarddog Super"), ("60", "Monster Cans/Animals/Guarddog Super")]
MASTERS = ["Monster Cans/Assasin Master" + t + k for t in ("", " Tough", " Super") for k in ("", " SPELLCASTER", " CHARACTER")]
DOG_MAPS = ["04 Maw of the Assasin", "05 Acid Wash", "06 Chamber of Torment", "07 Dark Temple", "01 Desert Sprawl"]
COMPANION_TREE = "Levels/8 Alamut/Dialog/Fixt Alamut Companions"
KNIGHT, GRUMDJUM = "Knight of Saladin", "Goblin Grumdjum"
LINES = {
    "1 knight acid": "Acid in the floor. The Old Man does not build halls. He builds graves.",
    "2 grumdjum acid": "This would make a fine verse, if any of us lives to write it.",
    "3 knight temple": "Stay close through the gates. Every one of them was set for us.",
    "4 grumdjum temple": "Gates, and spikes, and more gates. The Old Man has no poetry in him at all.",
}
REMARKS = {"05 Acid Wash": ("1 knight acid", "2 grumdjum acid"), "07 Dark Temple": ("3 knight temple", "4 grumdjum temple")}


def endings():
    t = lhbuild.read(NOSTRA)
    old = "Default Canceled Node Action=CTriggerRelayAction" + CR + "{" + CR + "Relay Name=Fixt order epilogue relay" + CR + "}"
    if old in t:
        (FX / NOSTRA).write_bytes(t.replace(old, old.replace("Fixt order epilogue relay", CONTINUES)).encode("latin-1"))
    good = ("CConditionalAction", [("Try Action", ("CCheckExistenceAction", [("Name To Check For", "Player got to back of Church BEFORE hit continue"), ("Desired Minimum Count", "1")])),
                                   ("Succeed Action", relay("MASTER NIS trigger")), ("Fail Action", activate("Player hit continue button before arrived")),
                                   ("Return failure if the TryAction failes", "0")])
    for rel, action in ((SIEGE, good), (DEMESNE, relay("MASTER Trigger for other Triggers End NIS")), (CALLE, relay("End NIS and ROLL Credits"))):
        z = lhbuild.read(rel)
        if "Name=" + CONTINUES + CR not in z:
            lhbuild.write_map(rel, lhbuild.add_parts(z, [lhbuild.relay_part(CONTINUES, action, 40, 40, once="0")]))
    z = lhbuild.read(CALLE)
    credits = re.search(r"Next Action=CShowCreditsAction\r\n\t*\{\r\n\t*\}", z)
    if credits:
        go = ("CForEachPlayerAction", [("Action", ("CTeleportAction", [("Return to map", "never"), ("New Map Name", "8 Alamut/Fixt Epilogue Stage"), ("New Location", STAGE_ARRIVE),
              ("Who To Switch", "$Instigator"), ("Relative Position", "0"), ("Ignore Party Ready Rules", "1"), ("Warp Behavior", "")]))])
        z = z[:credits.start()] + "Next Action=" + B(*go).rstrip() + z[credits.end():]
        lhbuild.write_map(CALLE, z)
    register([CALLE, DEMESNE])


def goblin_gate():
    c = lhbuild.read(KING_CAN)
    if KHAN_DEAD not in c:
        k = c.index("Target Name=Goblin Khan is Dead")
        a = c.rindex("Else=COtherMapAction", 0, k)
        v = a + len("Else=")
        e = balanced(c, v)
        both = multi([("CForEachPlayerAction", [("Action", flag(KHAN_DEAD))]), ("CFixtKeep", [])])
        text = B(*both).replace(B("CFixtKeep", []), c[v:e] + CR).rstrip()
        lhbuild.write_map(KING_CAN, c[:v] + text + c[e:])
    write_var(KHAN_DEAD, "Fixt Goblin Khan Dead", "1 means the Goblin Khan died. The act 8 goblin gate reads it, because the marker it read lives on another map.")
    register(["Resources/" + KHAN_DEAD + ".DerivedCharacterAttribute", KING_CAN[len("Resources/") - len("Resources/"):]])
    rel = A + "01 Desert Sprawl.zax"
    z = lhbuild.read(rel)
    if "Name To Check For=Goblin Khan is Dead" not in z:
        return

    def var(path, cmp, value):
        return B("CExpressionAction", [("Expression", (cmp, [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", path)])), ("Operator", ""),
                                                              ("Operand2", ("CConstant", [("Constant Value", value)]))])), ("Character to get attributes from", "$Instigator")]).rstrip()
    for name, text in (("Goblin Khan is Dead", var(KHAN_DEAD, "CIsGreaterThan", "0")), ("Grumdjum Dead", var(GRUMDJUM_VAR, "CIsGreaterThanOrEqual", "2"))):
        z, n = re.subn(r"CCheckExistenceAction\r\n\t*\{\r\n\t*Name To Check For=" + name + r"\r\n\t*Desired Minimum Count=1\r\n\t*\}", lambda m: text, z)
        assert n == 1, name
    lhbuild.write_map(rel, z)


def rejoin():
    c = lhbuild.read(REJOIN_CAN)
    if "300 grumdjum asks to rejoin" in c:
        return
    i = c.index("Object=") + len("Object=")
    e = balanced(c, i)
    say = lhbuild.balloon("Levels/Wilderness/Dialog/GoblinGrumdjum", "300 grumdjum asks to rejoin", "Goblin Grumdjum", "-80")
    both = multi([say, delay("2.5", ("CFixtKeep", []))])
    text = B(*both).replace(B("CFixtKeep", []), c[i:e] + CR).rstrip()
    lhbuild.write_map(REJOIN_CAN, c[:i] + text + c[e:])
    register([REJOIN_CAN[len("Resources/") - len("Resources/"):]])


def escape():
    """The fleeing Old Man's walk ends: delete him at 1 s, fire the relay at 1.5 s. Swapped, so the relay goes first."""
    z = lhbuild.read(FINAL)
    pat = (r"(Next Action=CDeleteAction\r\n\t*\{\r\n\t*Target Name=\$Trigger\r\n\t*\}\r\n\t*Delay=)(1|1\.5)(\r\n(?:(?!Level Part=).){0,400}?"
           r"Relay Name=Old Man Escaping Start Trigger\r\n\t*\}\r\n\t*Delay=)(1\.5|1)(\r\n)")
    m = re.search(pat, z, re.S)
    assert m
    if m.group(2) == "1.5":
        return
    lhbuild.write_map(FINAL, z[:m.start()] + m.group(1) + "1.5" + m.group(3) + "1" + m.group(5) + z[m.end():])


def unmute():
    for rel, nodes in MUTED.items():
        t = lhbuild.read(rel)
        for n in nodes:
            i = t.index("Node ID=" + n + CR)
            e = t.index("-" * 60, i) if "-" * 60 in t[i:] else len(t)
            t = t[:i] + t[i:e].replace("Should Have Voiceover=0", "Should Have Voiceover=1", 1) + t[e:]
        (FX / rel).write_bytes(t.encode("latin-1"))
        register([rel])


def acid():
    z = lhbuild.read(ACID)
    new = z
    for name in ("acid 01", "acid 02 Landscaper"):
        i = new.index("\t\t\tName=" + name + CR)
        a = new.rindex("Level Part=", 0, i)
        e = balanced(new, a)
        p = new[a:e]
        q = p.replace("Triggered By Enemies=0", "Triggered By Enemies=1").replace("Triggered By Companions=0", "Triggered By Companions=1")
        new = new[:a] + q + new[e:]
    if "Name=Fixt the sluice valve" + CR not in new:
        shut = multi([
            ("CPrintCombatTextAction", [("Text to print", "Behind a loose stone, a hand valve. You turn it, and up the channel the sluice gates groan shut."),
                                        ("Character to show text to", "$Instigator"), ("Emphasize", "0"), ("Suppress Duplicates", "0")]),
            relay("End level switch turn traps off")])
        found = ("CMultipleActionsAction", [("Action", ("Array", [("Item Count", "2"), ("Action", ("CShowAction", [("Target Name", "$Trigger")])),
                                                                ("Action", ("CPlaySoundAction", [("Sound", "Skills/Secret Door found.wav"), ("Position", "$Trigger")]))]))])
        use = ("CAIInteractionSpecifier", [("Marked For Deletion", "0"), ("Publisher", ""), ("Trigger Only Once", "1"), ("Was Triggered", "0"), ("Auto-Flip Switch", "1"),
                                           ("Trigge Must Have HP", "0"), ("Triggered By Anything", "0"), ("Triggered By Players", "1"), ("Triggered By Player Friends", "0"),
                                           ("Triggered By Enemies", "0"), ("Triggered By Projectiles", "0"), ("Triggered By Companions", "0"), ("Triggered By Name", ""),
                                           ("Interaction Description", ""), ("Interaction Type", "Interaction Specifiers/GetCloseThenTrigger"), ("Action", shut),
                                           ("X Radius", "50"), ("Attacker Range Modifier", "0"), ("YX Ratio", "0.712766"), ("Highlight Self Time", "0"),
                                           ("Highlight Until Clicked", "0"), ("Is Locked", "0"), ("Allow Interact If Has Target", "1"), ("Lock Pick Adjustment", "0"),
                                           ("Inventory item to use as key", "Inventory Items/!None"), ("Is Bussy Talking", "0")])
        secret = ("CAISecretReveal", [("Marked For Deletion", "0"), ("Publisher", ""), ("Skill Adjustment", "20"), ("Reveal Action", found),
                                      ("AIs To Add", ("Array", [("Item Count", "1"), ("AI", use)])), ("Has Been Revealed", "0")])
        valve = lhbuild.entity("Fixt the sluice valve", "1", [secret], "Special Effects/Secret Icon", 3040, 660, visible="0")
        new = lhbuild.add_parts(new, [valve])
    if new != z:
        lhbuild.write_map(ACID, new)


def summon_dogs(who):
    clone = ("CCloneAction", [("New Location", "$Trigger"), ("Copy Height", "0"), ("Random Location Delta", "80"), ("Warp Behavior", ""),
                              ("Source Name", DOG_SOURCE), ("New Name", DOG_USED), ("Set Facing Angle", "0"), ("New Facing Angle", "0")])
    line = ("CPrintCombatTextAction", [("Text to print", who + " whistles, and guard dogs come running."), ("Character to show text to", "Player1"),
                                       ("Emphasize", "0"), ("Suppress Duplicates", "0")])
    roll = ("CExpressionAction", [("Expression", ("CIsLessThan", [
        ("Operand1", ("CRandom", [("Operator", ""), ("Minimum", ("CConstant", [("Constant Value", "0")])), ("Maximum", ("CConstant", [("Constant Value", "100")]))])),
        ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "50")]))])), ("Character to get attributes from", "$Trigger")])
    once = ("CSeriesAction", [("Action", [("Action", if_action(roll, multi([line, clone]))), ("Action", ("CSucceedAction", [("Action", "")]))]),
                              ("When Done", "Repeat Last Action"), ("Require Success To Advance", "0"), ("Next Action Index", "0")])

    def hp(cmp, v):
        return ("CExpressionAction", [("Expression", (cmp, [("Operand1", ("CExpressionHealthPercent", [])), ("Operator", ""),
                                                            ("Operand2", ("CConstant", [("Constant Value", v)]))])), ("Character to get attributes from", "$Trigger")])
    return if_action(hp("CIsLessThanOrEqual", "50"), if_action(hp("CIsGreaterThan", "0"), once))


def dogs():
    done = 0
    for can in MASTERS:
        rel = "Resources/" + can + ".can"
        try:
            z = lhbuild.read(rel)
        except Exception:
            continue
        if DOG_SOURCE in z:
            continue
        who = re.search(r"User Assigned Name=([^\r\n]*)", z).group(1)
        k = z.index("Damaged Script Action=")
        v = k + len("Damaged Script Action=")
        if z[v:v + 2] == CR:
            new = B(*summon_dogs(who)).rstrip()
            lhbuild.write_map(rel, z[:v] + new + z[v:])
        else:
            e = balanced(z, v)
            new = "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR + "Action=" + z[v:e] + CR + \
                  "Action=" + B(*summon_dogs(who)) + "}" + CR + "}"
            lhbuild.write_map(rel, z[:v] + new + z[e:])
        register([rel])
        done += 1
    import zipfile
    hand = zipfile.ZipFile(lhbuild.VANILLA).read("Levels/5 Nostrodomus/02 Clan of the Hand A.zax").decode("latin-1")
    i = hand.index("\t\t\tName=Snakebreed Summoner Clone Generator" + CR)
    a = hand.rindex("Level Part=", 0, i)
    druids.SOURCE, druids.USED, druids.WOLF, druids.WOLVES = DOG_SOURCE, DOG_USED, DOG, DOGS
    source = wolf_source(hand[a:balanced(hand, a)]) + CR
    # two dogs, not one
    source = re.sub(r"Quantity to generate min=1\r\nQuantity to generate max=1", "Quantity to generate min=2" + CR + "Quantity to generate max=2", source)
    source = re.sub(r"(Quantity to generate min=)1(\r\n\t*Quantity to generate max=)1", r"\g<1>2\g<2>2", source)
    for m in DOG_MAPS:
        rel = A + m + ".zax"
        z = lhbuild.read(rel)
        if DOG_SOURCE not in z:
            lhbuild.write_map(rel, lhbuild.add_parts(z, [source]))
    return done


def sand():
    """Every fourth beast-only generator fields the matching Sand Spirit tier instead. Counts are unchanged."""
    swap = {"Monster Cans/Animals/Desert Beast": "Monster Cans/Sand Spirit", "Monster Cans/Animals/Desert Beast, feral": "Monster Cans/Sand Spirit"}
    done = 0
    for m in ("01 Desert Sprawl", "02 Shifting Dunes"):
        rel = A + m + ".zax"
        z = lhbuild.read(rel)
        if "Fixt sand spirits" in z:
            continue
        beasts = [x for x in parts(z) if "CGeneratorAI" in x and re.findall(r"Entity=([^\r\n]*)", x)
                  and all(e.startswith("Monster Cans/Animals/Desert Beast") for e in re.findall(r"Entity=([^\r\n]*)", x))]
        new = z
        for x in beasts[::4]:
            y = x
            for tier in (" Super", " Tough", ""):
                for b, s in swap.items():
                    y = y.replace("Entity=" + b + tier + CR, "Entity=" + s + tier + CR)
            new = new.replace(x, y)
            done += 1
        marker = lhbuild.entity("Fixt sand spirits", "0", [], "Editor/Position Marker", 20, 20)
        lhbuild.write_map(rel, lhbuild.add_parts(new, [marker]))
    return done


def companions():
    p = FX / ("Resources/" + COMPANION_TREE + ".DialogTree")
    if not p.exists():
        t = "CDialogTree" + CR + "{" + CR + "Name=" + CR + "Portrait=!None" + CR + "Should Have Voiceovers=0" + CR + "Default Canceled Node Action=" + CR
        for n, x in LINES.items():
            t += "-" * 60 + CR + lhbuild.node(n, x, [])
        p.write_bytes((t + "}" + CR).encode("latin-1"))
        register(["Resources/" + COMPANION_TREE + ".DialogTree"])

    def line(who, node):
        return if_action(("CIsAliveAction", [("Name To Check For", who), ("Desired Minimum Count", "1")]), lhbuild.balloon(COMPANION_TREE, node, who, "-80"))
    for m, (k, g) in REMARKS.items():
        rel = A + m + ".zax"
        z = lhbuild.read(rel)
        name = "Fixt companions remark"
        if "Name=" + name + CR in z:
            continue
        timer = ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""),
                                           ("Action", multi([line(KNIGHT, k), delay("4", line(GRUMDJUM, g)), ("CDeactivateAction", [("Target Name", name)])])),
                                           ("Delay Between Actions", "600"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "3")])
        lhbuild.write_map(rel, lhbuild.add_parts(z, [lhbuild.entity(name, "1", [timer], "Editor/Position Marker", 60, 60)]))


def main():
    endings()
    goblin_gate()
    rejoin()
    escape()
    unmute()
    acid()
    print(dogs(), "assassin master cans may call dogs")
    print(sand(), "beast generators field sand spirits")
    companions()
    register([A + m + ".zax" for m in ("01 Desert Sprawl", "02 Shifting Dunes", "04 Maw of the Assasin", "05 Acid Wash", "06 Chamber of Torment", "07 Dark Temple", "08 Final Encounter")])
    print("alamut built")


if __name__ == "__main__":
    main()
