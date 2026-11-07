"""The standard at the crossroads can be broken. Act 6 scored 1 of 5: one line, no fork, and 108 men nobody talks to.

Vanilla's own dying English soldiers say a fog has lifted and they do not know why they came. So the army is held, and
the standard `The Crossing` already describes is what holds it. Break it and the men wake. Druids, golems and wolves
stay hostile, because they were never held.

Four ways, all priced. Thought, Divine or Tribal at 150 costs all your mana and half your health. A school is the sum of
its spells, so 150 means a main school rather than a dabble. ST 10 and EN 8 cost two thirds of your health. Joan dies
doing it, if you let her. The golem destroys itself on your order. Every route is a cutscene, so paying cannot get you
killed and the standard cannot be clicked twice. Both walk to the standard first, on a clone of
`Darsh Leaves for Good`'s task, because a hand-written walk is the bug this mod has shipped most often. The arrival and a
timer both fire a one-shot relay, so being blocked on the way cannot hang the scene. It runs as a cutscene: with Pause
Characters on, only a `NonInteractiveSequence Actor` moves, so nothing can hit you while it plays. The camera follows on
a `CAIAttractCamera` added to the walker, which re-reads its owner's position every tick. Its Disable Self must stay off,
because the engine would deactivate the owner, and here that is Jehanne.

The engine cannot address "nearby" enemies, only names, so it wakes every soldier on the map, which is why the prices
are high. Costs sit on the reply, because $Instigator resolves to nothing in a relay a reply fires. The damage steps
down for a wounded character, so paying can never kill you outright. Woken men can still be attacked: the one you hit
fights back, killing one costs 50 Karma, and the first kill darkens the slide. XP and drops are in the can's Effect slot,
which the script does not replace. A balloon fails on two matches, so the barks are anchored on $Trigger through a timer
on each man, firing a relay that loops its lines with a gap, because only a few men are ever on screen. 20 of the 34 generators mix
bows and blades, so no line may assume which he carries. Mana goes by CExpressionManaRemaining, because a take larger than the pool does nothing.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_crossroads_standard.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, activate, balanced, balloon, deactivate, delay, dialog, exists, if_action, multi, node, relay
from build_inquisition_slides import ENDGAME, SLIDES, VARS, flag, say, var_if, write_var

MAP = "Levels/6 Barcelona Attack/Crossroads Siege.zax"
TREE_PATH = "Levels/6 Barcelona Attack/Dialog/Fixt The Standard"
TREE = "Resources/" + TREE_PATH + ".DialogTree"
STANDARD, SPOT, SCAR = "Fixt The Standard", "Fixt Standard Spot", "Fixt Standard Scar"
FALLS, BY_JOAN, BY_GOLEM = "Fixt Standard Falls", "Fixt Standard Joan", "Fixt Standard Golem"
JOAN_ENDS, GOLEM_ENDS = "Fixt Standard Joan arrives", "Fixt Standard Golem arrives"
WOKE = "Fixt Standard Woke"
LINES = ["80 woke 1", "81 woke 2", "82 woke 3", "83 woke 4", "84 woke 5", "85 woke 6", "86 woke 7", "87 woke 8"]
THOUGHT_FX, DIVINE_FX, TRIBAL_FX, BRUTE_FX = "Fixt Standard Thought", "Fixt Standard Divine", "Fixt Standard Tribal", "Fixt Standard Brute"
X, Y = 1600, 1630  # the junction, where The Crossing says it is. Further east Catapult A at 1889, 1682 draws over it
BROKEN, JOAN_VAR, GOLEM_VAR = VARS + "Fixt Standard Broken", VARS + "Fixt Standard Joan", VARS + "Fixt Standard Golem"
BLOOD = VARS + "Fixt Standard Blood"
JOAN, GOLEM = "Joan of Arc", "Golem"
MEN = "English Soldier, English Bowman, English Bowmaster, English Sergeant, English Captain, English Lieutenant, English Guardsman, Royal Guardsman"
HP = "Derived Character Attributes/(HP) Hit Points"
ST, EN = "Character Attributes/(ST) Strength", "Character Attributes/(EN) Endurance"
FX_ROOT = "Spell Effects/Hits and Effects/"


def const(n):
    return ("CConstant", [("Constant Value", str(n))])


def school(name):
    return B("CIsGreaterThanOrEqual", [("Operand1", ("CVariableSkill", [("Skill", "Skills/" + name)])), ("Operator", ""), ("Operand2", const(150))])


def attr(path, n):
    return ("CIsGreaterThanOrEqual", [("Operand1", ("CVariableCharacterAttribute", [("Character Attribute", path)])), ("Operator", ""), ("Operand2", const(n))])


def strong():
    return B("CAND", [("Operand1", attr(ST, 10)), ("Operator", ""), ("Operand2", attr(EN, 8))])


def alive(name):
    return "CActionExpression" + CR + "{" + CR + "Action=" + B("CIsAliveAction", [("Name To Check For", name), ("Desired Minimum Count", "1")]) + "}" + CR


def damage(share):
    amount = ("CMultiply", [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", HP)])), ("Operator", ""), ("Operand2", const(share))])
    return ("CActionDoDamage", [("Character Doing Damage", "$instigator"), ("Character To Damage", "$instigator"), ("Defend Against", "0"), ("No Friendly Fire Check", "1"),
                                ("Damages", ("Array", [("Item Count", "1"), ("Damage", ("CXRPGDamage", [("Damage Type", "Damage Types/Electrical"), ("Damage Amount", amount)]))]))])


def above(percent, then, els=""):
    return ("CIfExpressionAction", [("If Expression", ("CIsGreaterThan", [("Operand1", ("CExpressionHealthPercent", [])), ("Operator", ""), ("Operand2", const(percent))])),
                                    ("Character to get attributes from", "$Instigator"), ("Then", then), ("Else", els)])


def hurt(share):
    """The share of full health, or half of it when wounded, and nothing below that. Paying must not kill."""
    p = int(share * 100)
    return above(p + 5, damage(share), above(p // 2 + 5, damage(share / 2)))


def drain():
    return ("CTakeManaFromCharacterAction", [("Character to take mana from", "$instigator"), ("Amount of mana to take", ("CExpressionManaRemaining", [])), ("Expression Context", "$Instigator")])


def fx(model, where=SPOT, sound="1"):
    return ("CSpawnEffectAction", [("Explosion Model", model), ("Location Entity", where), ("Make effect a child of the location entity", "0"), ("X Offset", "0"), ("Y Offset", "0"),
                                   ("Height Offset", "0"), ("Play Default Sound", sound), ("Action to execute After Effect", "")])


def shake(secs, pixels):
    return ("CShakeScreenAction", [("Time to Shake", str(secs)), ("Pixels To Shake", ("CLengthEnvelope", [
        ("Start Value", str(pixels)), ("End Value", "0"), ("Speed", "0"), ("Ending Behavior", "Stop at end"), ("Current Value", "0"), ("Using Start", "1"), ("Direction", "1")]))])


def begin():
    return ("CBeginNonInteractiveSequenceAction", [("Options", ("CNonInteractiveSequence", [("Pause Characters", "1"), ("Disable Player Controls", "1"), ("Can Fast Forward", "0")]))])


def end_scene(secs):
    return delay(secs, ("CEndNonInteractiveSequenceAction", []))


def karma(n):
    return ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", ""), ("Modification is permanent", "0"), ("Character to modify", "$Instigator"),
        ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", const(n)), ("Modification amount is a percent", "0"),
            ("Allow Accumulation", "1"), ("Derived character attribute to modify", "Derived Character Attributes/Karma")]))])),
        ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])


def fights_back():
    """Enemy is the per-man flag that this has run. Run on every hit, it removed the specifier the player's attack was holding,
    and each removal ended the attack (0x469160 reads it). The first hit still does, so the first follow-up takes one more click."""
    calm = ("CNotAction", [("Action", ("CCheckCategoryAction", [("Target Name", "$Trigger"), ("Category to check for", "Enemy")]))])
    return if_action(("CCheckCategoryAction", [("Target Name", "$Instigator"), ("Category to check for", "Player,Player Friend")]), if_action(calm, multi([
        ("CSetTargetTypeAction", [("Entity Name", "$Trigger"), ("Name To Target", ""), ("Valid Targets", "Player,Player Friend")]),
        ("CAddCategoryAction", [("Target Name", "$Trigger"), ("Categories to add", "Enemy")]),
        forget_specifier("$Trigger"),
        specifier("$Trigger", "GetCloseThenTriggerAndFight", ""),
        ("CGoToCombatAction", [("Enemy Name", "$Trigger")])])))


def mourned():
    return if_action(("CWasDamagedByPlayerAction", [("Entity To Check For Damage", "$Trigger")]),
                     ("CForEachPlayerAction", [("Action", multi([karma(-50), flag(BLOOD)]))]))


def forget_specifier(target):
    return ("CRemoveAIAction", [("Target Name", target), ("AI", "CAIInteractionSpecifier"), ("Delay Between Removes", "0")])


def specifier(target, kind, action):
    """A click reads only the entity's first specifier (0x46b0f0), and every soldier's can already has one that fights,
    so a new one does nothing until that one has been removed. Always forget_specifier first, and put the fight one back."""
    return ("CAddAIAction", [("Target Name", target), ("AI", ("CAIInteractionSpecifier", [
        ("Marked For Deletion", "0"), ("Publisher", ""), ("Trigger Only Once", "0"), ("Was Triggered", "0"), ("Auto-Flip Switch", "1"),
        ("Trigge Must Have HP", "0"), ("Triggered By Anything", "0"), ("Triggered By Players", "1"), ("Triggered By Player Friends", "0"),
        ("Triggered By Enemies", "0"), ("Triggered By Projectiles", "0"), ("Triggered By Name", ""), ("Interaction Description", ""),
        ("Interaction Type", "Interaction Specifiers/" + kind),
        ("Action", action),
        ("X Radius", "50"), ("Attacker Range Modifier", "0"), ("YX Ratio", "0.712766"), ("Highlight Self Time", "0"), ("Highlight Until Clicked", "0"),
        ("Is Locked", "0"), ("Allow Interact If Has Target", "1"), ("Lock Pick Adjustment", "0"), ("Inventory item to use as key", "Inventory Items/!None"),
        ("Is Bussy Talking", "0")])), ("Delay Between Adds", "0")])


def bewildered():
    """Every man says a line as he wakes. A balloon takes one match, so this is one timer per man, and the series holds it to
    once, since each man serialises his own copy. The delay scatters them, and the log stays out of it: 94 lines at once."""
    lines = [("CDisplayDialogBalloonAction", [("Dialog Tree File", TREE_PATH), ("Node ID", n), ("Name of Position", "$Trigger"), ("Position Offset", "0.000000,-80.000000"),
                                              ("After Action", ""), ("Include In Log", "0")]) for n in LINES]
    line = ("CRandomAction", [("Action", ("Array", [("Item Count", str(len(lines)))] + [("Action", x) for x in lines]))])
    soon = ("CDelayAction", [("Next Action", line), ("Delay", "1.5"), ("Plus or Minus", "1.5"), ("Forget Trigger", "0")])
    once = ("CSeriesAction", [("Action", [("Action", soon), ("Action", ("CSucceedAction", [("Action", "")]))]), ("When Done", "Repeat Last Action"),
                              ("Require Success To Advance", "0"), ("Next Action Index", "0")])
    return ("CAddAIAction", [("Target Name", MEN), ("AI", ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", once),
                                                                                     ("Delay Between Actions", "600"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "0")])),
                             ("Delay Between Adds", "0")])


def falls():
    return multi([
        ("CDeleteAction", [("Target Name", STANDARD)]),
        activate(SCAR),
        ("CSetTargetTypeAction", [("Entity Name", MEN), ("Name To Target", ""), ("Valid Targets", "")]),
        ("CRemoveCategoryAction", [("Target Name", MEN), ("Categories To Remove", "Enemy")]),
        ("CSetDamagedScriptActionAction", [("New Damaged Action", fights_back()), ("Target Name", MEN)]),
        ("CSetDestroyedScriptActionAction", [("New Destroyed Action", mourned()), ("Target Name", MEN)]),
        ("CFixtTimer", [("Target", MEN), ("Relay", WOKE)]),
        bewildered(),
        forget_specifier(MEN),
        specifier(MEN, "GetCloseThenTalk", ("CRandomAction", [("Action", ("Array", [("Item Count", str(len(LINES)))] + [("Action", balloon(TREE_PATH, n, "$trigger", "-80")) for n in LINES]))])),
    ])


def woke(name, nodes):
    """Every timer starts at once, so a line turns the relay off for a while and whichever man ticks next says the next."""
    steps = [multi([balloon(TREE_PATH, n, "$Trigger", "-80"), deactivate(name), delay("6", activate(name))]) for n in nodes]
    return ("CShuffledSeriesAction", [("Action", ("Array", [("Item Count", str(len(steps)))] + [("Action", x) for x in steps])),
                                      ("When Done", "Repeat Series"), ("Require Success To Advance", "0"), ("Next Action Index", "0")])


def timer(target, name):
    """A vanilla Attackers timer, retargeted. It ticks often, and the relay's own gap sets the pace."""
    z = lhbuild.read(MAP)
    i = z.index("AI=CRepeatTimerTriggerAI")
    t = z[i + len("AI="):balanced(z, i)]
    t = t.replace("Relay Name=Attackers dialog balloons", "Relay Name=" + name)
    t, n = re.subn(r"Delay Between Actions=[^\r\n]*", "Delay Between Actions=4", t)
    assert n == 1
    t, n = re.subn(r"Plus or Minus=[^\r\n]*", "Plus or Minus=3", t, count=1)
    assert n == 1
    return "CAddAIAction" + CR + "{" + CR + "Target Name=" + target + CR + "AI=" + t + CR + "Delay Between Adds=0" + CR + "}"


def walks(party, arrive):
    """Leave the party, stop fighting, and go to the standard. The placeholder becomes the cloned task in crossroads()."""
    return multi([delay("12", relay(arrive)), begin(), deactivate("Attackers dialog balloons"),
                  ("CReleaseCompanionAction", [("Companion To Release", party)]),
                  ("CRemoveAIAction", [("Target Name", party), ("AI", "CAIInteractionSpecifier"), ("Delay Between Removes", "0")]),
                  ("CAddAIAction", [("Target Name", party), ("AI", ("CAIAttractCamera", [("Marked For Deletion", "0"), ("Publisher", ""), ("Camera Arrived Action", ""), ("Disable Self When Camera Arrives", "0")])), ("Delay Between Adds", "0")]),
                  ("CSetTargetTypeAction", [("Entity Name", party), ("Name To Target", ""), ("Valid Targets", "")]),
                  ("CAddCategoryAction", [("Target Name", party), ("Categories to add", "NonInteractiveSequence Actor")]),
                  ("CFixtWalk", [("Target", party), ("Arrive", arrive)])])


def remove_camera(party):
    """Before the End, in its own timer: outside a sequence an attractor marks the player's own camera tracker (`0x4ab080`)."""
    return ("CRemoveAIAction", [("Target Name", party), ("AI", "CAIAttractCamera"), ("Delay Between Removes", "0")])


def walk_task(party, arrive):
    """Darsh's own walk-off, retargeted. Its Move Behavior is filled, which is the part that must not be written by hand."""
    z = lhbuild.read("Levels/2 Montserrat/01 Grove Exterior.zax")
    i = z.index("\t\t\tName=Darsh Leaves for Good" + CR)
    s = z.index("Action=CAssignTemporaryTaskAction", i)
    t = z[s + len("Action="):balanced(z, s)]
    t = re.sub(r"(\n\s*)Target=Darsh\r", lambda m: m.group(1) + "Target=" + party + CR, t)
    t = t.replace("Destination=Companion goto spot for deletion", "Destination=" + SPOT)
    t = t.replace("Sequence=Run", "Sequence=")
    a = t.index("Done action=CDeleteAction")
    b = balanced(t, a)
    t = t[:a] + "Done action=" + B(*relay(arrive)).rstrip() + t[b:]
    assert "Darsh" not in t and "Move Behavior=CEntityBehaviorMoveToPos" in t
    return t


def spends(party):
    """The body stays, and the delete only covers a death that did not land, because a hale companion left standing
    is worse than a vanished one."""
    return [("CPainAction", [("Hit Points", "99999"), ("Damage Type", "Unavoidable"), ("Sound", "!None.wav"), ("Target", party)]),
            delay("4", if_action(("CIsAliveAction", [("Name To Check For", party), ("Desired Minimum Count", "1")]), ("CDeleteAction", [("Target Name", party)])))]


def relays():
    fall = relay(FALLS)
    return [
        lhbuild.relay_part(FALLS, falls(), X + 20, Y + 40),
        lhbuild.relay_part(WOKE, woke(WOKE, LINES), X + 40, Y + 40, once="0"),
        lhbuild.relay_part(THOUGHT_FX, multi([end_scene("4"), delay("2.2", fall), fx(FX_ROOT + "Fire Attacks/Fireball Med Lrg Hit"), shake(3, 4),
                                              delay("0.7", fx(FX_ROOT + "Electrical Attacks/Lightning Storm")),
                                              delay("1.4", fx(FX_ROOT + "Ice Attacks/Ice Ring Large"))]), X - 40, Y + 40),
        lhbuild.relay_part(DIVINE_FX, multi([end_scene("4"), delay("2.2", fall), fx(FX_ROOT + "Target Affected/Exorcise"), delay("1", fx(FX_ROOT + "Shield/Holy Fire Divine"))]), X - 60, Y + 40),
        lhbuild.relay_part(TRIBAL_FX, multi([end_scene("4"), delay("2.2", fall), fx(FX_ROOT + "Corpse Effects/Absorb Spirit"), delay("1", fx("Special Effects/Spirit Calls/Ancestral"))]), X - 80, Y + 40),
        lhbuild.relay_part(BRUTE_FX, multi([end_scene("3"), delay("1.2", fall), shake(2, 3), fx(FX_ROOT + "Electrical Attacks/Electrical Burst Med")]), X - 100, Y + 40),
        lhbuild.relay_part(BY_JOAN, walks(JOAN, JOAN_ENDS), X - 120, Y + 60),
        lhbuild.relay_part(BY_GOLEM, walks(GOLEM, GOLEM_ENDS), X - 140, Y + 60),
        lhbuild.relay_part(JOAN_ENDS, multi([delay("5", ("CEndNonInteractiveSequenceAction", [])), delay("4.8", remove_camera(JOAN)), delay("2.6", fall), delay("2.4", multi(spends(JOAN))),
                                             fx(FX_ROOT + "Divine Radial Cast Effect", JOAN), delay("1.2", fx(FX_ROOT + "Shield/Holy Fire Divine 2", JOAN))]), X - 120, Y + 40),
        lhbuild.relay_part(GOLEM_ENDS, multi([delay("4.5", ("CEndNonInteractiveSequenceAction", [])), delay("4.3", remove_camera(GOLEM)), delay("2.2", fall), delay("2", multi(spends(GOLEM))),
                                              fx(FX_ROOT + "Electrical Attacks/Electrical Burst Lrg", GOLEM), shake(4, 6),
                                              delay("1", fx(FX_ROOT + "Fire Attacks/Fireball Med Lrg Hit", GOLEM)),
                                              delay("1.6", fx(FX_ROOT + "Fire Attacks/Fire Circle Medium"))]), X - 140, Y + 40),
    ]


def tree():
    sides = [
        {"creq": school("Thought"), "text": "<Obliterate it.>", "go": "10 thought"},
        {"creq": school("Divine"), "text": "<Exorcise it.>", "go": "20 divine"},
        {"creq": school("Tribal"), "text": "<It holds their spirits. Take them back.>", "go": "30 tribal"},
        {"creq": strong(), "text": "<Take hold of it and tear it out of the stones.>", "go": "40 brute"},
        {"creq": alive(JOAN), "text": "<Look to Jehanne.>", "go": "50 joan"},
        {"creq": alive(GOLEM), "text": "<Order the golem to destroy it.>", "go": "60 golem"},
        {"text": "<Leave it.>", "icon": "Exit Icon", "default": True},
    ]

    def done(cost, fxr):
        # The relay holds the only End, so it goes first: nothing that can fail below may stand between Begin and it.
        return {"text": "", "action": multi([relay(fxr), begin(), deactivate("Attackers dialog balloons"), ("CForEachPlayerAction", [("Action", flag(BROKEN))])] + cost), "default": True}

    nodes = [
        node("1 the standard", "<A twisted druid lamp-stand stands in the paving with no socket to hold it. The air around it tastes of iron. Every soldier in sight of it wears the same slack face, and none of them is blinking.>", sides),
        node("10 thought", "<You do not study it. You call down everything you have, fire and lightning and cold, until there is nothing left of it. A black ring is burned into the crossroads where it stood, and there is nothing left in you.>", [done([drain(), hurt(0.5)], THOUGHT_FX)]),
        node("20 divine", "<You lay a hand on the wood and speak the rite. It burns from the inside, and so do you. When the flame goes out, you have nothing left to call on.>", [done([drain(), hurt(0.5)], DIVINE_FX)]),
        node("30 tribal", "<You have bent minds yourself, and you know the shape of this. You reach into the stand and pull back what it took from them. It splits to the ground, and every one of them passes through you on the way out.>", [done([drain(), hurt(0.5)], TRIBAL_FX)]),
        node("40 brute", "<It does not want to come. You set your feet and pull until something in your back gives way. The stones let go first. The spell goes through you on its way out, and you are still standing, which surprises you both.>", [done([hurt(0.66)], BRUTE_FX)]),
        node("50 joan", "<Jehanne steps forward and studies the stand without fear.> I know this work. It is a vow with the prayer taken out of it. A thing like this is unmade by one who gives more than it took. I held a door for two hundred years, crusader. I can hold this one a little longer.", [
            {"text": "Do it.", "go": "55 joan gives"},
            {"text": "No. We will find another way.", "icon": "Exit Icon", "default": True}]),
        node("55 joan gives", "Tell them they are free. Tell them who they were.", [
            {"text": "", "action": multi([("CForEachPlayerAction", [("Action", multi([flag(BROKEN), flag(JOAN_VAR)]))]), relay(BY_JOAN)]), "default": True}]),
        node("60 golem", "<Brrrt> <It turns its head toward you and waits to be sure, as it always has. It was built in England to break a line.>", [
            {"text": "", "action": multi([("CForEachPlayerAction", [("Action", multi([flag(BROKEN), flag(GOLEM_VAR)]))]), relay(BY_GOLEM)]), "default": True}]),
        node("80 woke 1", "Where is this? Who are you people?", []),
        node("81 woke 2", "What have we done? God forgive us, what have we done?", []),
        node("82 woke 3", "This is Spain. Why am I in Spain?", []),
        node("83 woke 4", "Who gave that order? Did anyone give that order?", []),
        node("84 woke 5", "I was in Kent. It was harvest. I was at home.", []),
        node("85 woke 6", "Whose blood is this?", []),
        node("86 woke 7", "Stand down. All of you, stand down. I do not know why we are here.", []),
        node("87 woke 8", "Put up your swords! In God's name, who are we fighting?", []),
    ]
    z = lhbuild.tree("The Standard", nodes)
    assert z.count(CR) == z.count("\n")
    (FX / TREE).parent.mkdir(parents=True, exist_ok=True)
    (FX / TREE).write_bytes(z.encode("latin-1"))


def glow():
    """The charm the men are under, at lamp height. It lives on the stand, so deleting the stand stops it. Silent: it runs for the whole map."""
    return ("CSpawnEffectAction", [("Explosion Model", FX_ROOT + "Target Affected/Charm"), ("Location Entity", SPOT), ("Make effect a child of the location entity", "0"),
                                   ("X Offset", "0"), ("Y Offset", "0"), ("Height Offset", "90"), ("Play Default Sound", "0"), ("Action to execute After Effect", "")])


def move_the_description(z):
    """`what the standard is` describes it as you approach, so its polygon goes with it."""
    i = z.index("\t\t\tName=what the standard is" + CR)
    a = z.index("Polygon=", i)
    e = z.index(CR, a)
    return z[:a] + "Polygon=1450, 1480, 1750, 1480, 1750, 1780, 1450, 1780, 1450, 1480" + z[e:]


def crossroads():
    z = lhbuild.read(MAP)
    if STANDARD + CR in z:
        return
    z = move_the_description(z)
    talk = lhbuild.specifier("GetCloseThenTalk", dialog(TREE_PATH, "1 the standard", "$trigger"), radius="90")
    pulse = ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", glow()), ("Delay Between Actions", "5"),
                                       ("Plus or Minus", "1"), ("Seconds Till Next Execute", "0")])
    props = [
        lhbuild.entity(STANDARD, "1", [talk, pulse], "Environments/Druid Grove/Torches/TorchStand1", X, Y - 80, visible="1", collideable="0"),  # its anchor sits 80 above its base
        lhbuild.entity(SCAR, "0", [], "Environments/Heart of Fire/Burned Pieces/Burn Ground 01 A", X, Y, visible="1", collideable="0"),
        lhbuild.marker(SPOT, X, Y),
    ]
    z = lhbuild.add_parts(z, props + relays())
    for party, arrive in ((JOAN, JOAN_ENDS), (GOLEM, GOLEM_ENDS)):
        ph = B("CFixtWalk", [("Target", party), ("Arrive", arrive)])
        assert z.count(ph) == 1
        z = z.replace(ph, walk_task(party, arrive) + CR)
    for target, name in ((MEN, WOKE),):
        ph = B("CFixtTimer", [("Target", target), ("Relay", name)])
        assert z.count(ph) == 1
        z = z.replace(ph, timer(target, name) + CR)
    assert "CFixtWalk" not in z and "CFixtTimer" not in z
    lhbuild.write_map(MAP, z)


SLIDE_TEXT = {
    "900 order standard": "The English at the crossroads woke in one moment, in the wrong country, with blood on them. Most of them went home. Nobody in England would hear what had happened, because the druids had already told it differently. The men stopped talking about it. You knew what you had broken, and you were the only one who did.",
    "900 order standard blood": "The English at the crossroads woke in one moment, in the wrong country, with blood on them. You killed a good many of them while they were still asking where they were. The rest went home and told nobody, because nobody in England would have heard it. You knew what you had broken, and you knew what you had done after.",
    "900 friend joan standard": "Jehanne d'Arc died at the crossroads outside Barcelona with her hands on a druid's standard. An English army woke in the same moment and did not know her name. The Crypt she had held for two hundred years went unguarded. Most of the men who went home would not speak of that road. One of them paid for a mass at Rennes every year, and would not say why.",
    "900 friend golem standard": "The golem ended at the crossroads outside Barcelona, on your order. It had been built in England to break a line, and it broke the thing that was holding this one. The men who woke there never learned what freed them. A shoulder plate with its makers' marks turned up in the paving. A church in Cornwall kept it as a relic, without any idea what it was.",
}


def slides():
    z = lhbuild.read(SLIDES)
    if "900 order standard" in z:
        return
    add = ""
    for nid, text in SLIDE_TEXT.items():
        add += ("Node ID=" + nid + CR + "Text=" + text + CR + "Should Have Voiceover=1" + CR + CR +
                "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR +
                "Custom Action=" + B(*relay("Fixt order epilogue relay")) + "Is Default Reply=1" + CR + "-" * 60 + CR)
    key = "Node ID=900 order none" + CR
    assert z.count(key) == 1
    z = z.replace(key, add + key)
    assert z.count(CR) == z.count("\n")
    (FX / SLIDES).write_bytes(z.encode("latin-1"))


def first(z, nid, var, new):
    """Test the sacrifice ahead of the whole slide, so it holds whatever the companion variable says."""
    k = z.index("Node ID=" + nid + CR)
    s = z.rindex("\t" * 7 + "Action=C", 0, k)
    i = z.index("Action=C", s)
    e = balanced(z, i)
    old = z[i + len("Action="):e]
    wrapped = ("CIfExpressionAction" + CR + "{" + CR + "If Expression=" + B(*var_if(var, "", "")[1][0][1]) +
               "Character to get attributes from=Player1" + CR + "Then=" + B(*say(new)) + "Else=" + old + CR + "}")
    return z[:i] + "Action=" + wrapped + z[e:]


def endgame():
    z = lhbuild.read(ENDGAME)
    if "900 order standard" in z:
        return
    z = first(z, "900 friend joan dead", JOAN_VAR, "900 friend joan standard")
    z = first(z, "900 friend golem dead", GOLEM_VAR, "900 friend golem standard")
    k = z.index("Node ID=900 order pits killed")
    s = z.rindex("\t" * 7 + "Action=C", 0, k)
    next_step = delay("0.1", relay("Fixt order epilogue relay"))
    z = z[:s] + "\t" * 7 + "Action=" + B(*var_if(BROKEN, var_if(BLOOD, say("900 order standard blood"), say("900 order standard")), next_step)) + z[s:]
    a = z.index("\t\t\tName=Fixt order epilogue relay" + CR)
    i = z.index("Item Count=32" + CR, a)
    assert i - a < 900
    z = z[:i] + "Item Count=33" + z[i + len("Item Count=32"):]
    lhbuild.write_map(ENDGAME, z)


def main():
    write_var(BROKEN, "Fixt Standard Broken", "1 means the player broke the standard at the crossroads.")
    write_var(JOAN_VAR, "Fixt Standard Joan", "1 means Joan of Arc died breaking the standard at the crossroads.")
    write_var(GOLEM_VAR, "Fixt Standard Golem", "1 means the war golem destroyed itself on the standard at the crossroads.")
    write_var(BLOOD, "Fixt Standard Blood", "1 means the player killed English soldiers after the standard woke them.")
    tree()
    crossroads()
    slides()
    endgame()


if __name__ == "__main__":
    main()
