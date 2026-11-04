"""Build the Aegis of the Templars: tier three, and the end of the Templar shield chain.

The order has three ranks and the game only ever used two of them for anything you can hold.
`Templar Squire`, `Templar Warden` and `Templar Paladin` all exist, all set `Uber Perks/Templar
Rank`, and all three are assigned somewhere -- but the only material thing the ladder ever gave
you was the Lion Shield at the bottom of it. 0.93.0 put the Holy Shield at Warden. This puts the
last shield at Paladin, so each rank is worth reaching.

**It is given by a person, and that was the second design.** The first hung it on the
`Templar Paladin` promotion that fires when you complete *Search for the Five Ways Crystals*.
That worked and it was hollow: the crystals are a magic collection quest with nothing Templar in
them, there is no scene and no agent, and the shield transmuted in your pack the instant you
touched the fifth stone.

**Sir Roger Templeton** is a Knight Templar who rides with you -- Fixt's England companion, met
in `7 English Shrine/02 Temple Initiate`, present at the act 8 siege and in the ending slides.
The Templar camp in that act is his; its quartermaster and surgeon both speak of him. His
greeting already carries a `Requirement=Templar IS` branch in which you hail him as a brother
knight, and until now he gave you nothing at all.

So the Aegis is handed over by a brother of the order who recognises what you are carrying. The
Holy Shield is steel bearing an old cross with a lion ghosted beneath it, transfigured by freeing
knights two centuries dead -- a living Templar reading that as grave-goods is accurate, not just
evocative. The gate is **Templar membership plus the Holy Shield in hand**, not Paladin rank:
Sir Roger is met early in act 7 and the crystals complete later, so a rank gate would be
unreachable at the only moment that matters.

**The branch must exit through `10 accept`.** That greeting fires inside a non-interactive
sequence, and this project has already soft-locked a cutscene for two years by adding a reply
inside one that did not fire what the working exit fires. `10 accept` is where every other
greeting reply lands, and it is also what recruits Sir Roger -- `CSetCompanionAction`, the Fixt
companion-joined can, 200 XP and four relays. So the relic scene is an alternative to the
existing Templar accept reply rather than a detour around it: a knight who shows his shield also
accepts his brother's aid, which is what that reply already did.

The reply is added to all **four** nodes that carry the Templar greeting -- both greetings and
both return dialogues, male and female -- so refusing him once and coming back still works.

                      Lion    Holy    Aegis
    AC                  10      14       18
    Pierce/Slash/Crush  15/10/10  20/15/15  25/20/20
    Thresholds          +1      +2       +3
    Fire/Cold/Elec       -      10       15 each
    Attack Magic Speed -0.07  -0.05    -0.03
    Templar set item    no     yes      yes
    Value              500    1500     3000

**The speed line is the design, not the AC line.** -0.03 matches the Spirit Templar Shield, the
lightest shield in the game, so the tier that mitigates most also encumbers least. That is the
opposite of how the ordinary Small/Medium/Large line works -- there AC and penalty climb together
-- and it is what makes this chain read as three increasingly well-made objects rather than three
increasingly large ones.

**The reflect value is 0.15, and it is calibrated against two peers rather than guessed.**
`Physical Damage Percentage Given To Attacker Zero To One` is written by three things, and all
three agree that the attribute takes a fraction:

    Dragon Scales   CDivide( <"percentagechange" = 10>, 100 )  -> 0.10, permanent, armour
    Backlash        CDivide( <"percent" = 20..35>,      100 )  -> 0.20-0.35, a temporary spell
    Aegis           0.15                                        -> permanent, one endgame shield

Two earlier readings of this were wrong and both are worth recording, because the trap is easy.
First: a bare `Constant Value=100` appears in both vanilla users and looks like the house style
for "100%". It is not a value at all -- **it is the divisor**, and a naive scan that takes the
last `Constant Value` in a modifier block reports it as the amount. Second: `Dragon Scales` is
not broken and not unreachable; it is a well-formed 10% reflect belonging to
`Shields and Armor/Armor Additions`, 27 members, named by 6 armour items, and its own description
says "will take 10% of that damage themselves".

So 0.15 sits just above vanilla's permanent reflect and well below its temporary one, which is
where an endgame quest reward belongs. It is still a number to confirm in play.

Usage: python tools/build_aegis.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import CR, T, FX, read
import resource_format
from resource_format import ResourceNode as RN

HOLY = "Inventory/Specific Item Cans/Quest Items/Holy Shield of the Templars"
AEGIS = "Inventory/Specific Item Cans/Quest Items/Aegis of the Templars"
HOLY_REL = "Resources/" + HOLY + ".InventoryItem"
AEGIS_REL = "Resources/" + AEGIS + ".InventoryItem"

AEGIS_ICON = "Items/Inventory Images/Armor/Shield Aegis"
AEGIS_MESH = "Shield Aegis"
AEGIS_MODEL = "Models3D/Weapons/Shields/Shield Aegis/Shield Aegis"

# zero-to-one. Backlash divides its percent by 100 and caps at 35, so 0.15 is a permanent
# effect set deliberately below vanilla's best temporary one. Confirm in play.
REFLECT = "0.15"

TREE = "Resources/Levels/7 English Shrine/Dialog/SirRoger.DialogTree"
DASH = "-" * 60

DERIVED = [
    ("Damage Related/Piercing Damage Resistance", "25"),
    ("Damage Related/Piercing Damage Threshold", "3"),
    ("Damage Related/Slashing Damage Resistance", "20"),
    ("Damage Related/Slashing Damage Threshold", "3"),
    ("Damage Related/Crushing Damage Resistance", "20"),
    ("Damage Related/Crushing Damage Threshold", "3"),
    ("Damage Related/Fire Damage Resistance", "15"),
    ("Damage Related/Cold Damage Resistance", "15"),
    ("Damage Related/Electrical Damage Resistance", "15"),
    ("Damage Related/Physical Damage Percentage Given To Attacker Zero To One", REFLECT),
    ("(AC) Armor Class", "18"),
    ("Speed/Attack Magic Speed Multiplier", "-0.03"),
    ("Number of Templar Items", "1"),
]
SKILLS = [("Skills/Fighting/Unarmed", "-10")]

DESC = ("The order's last shield, gilded for a Paladin. "
        "+18 AC, Piercing Resist 25%, Crushing and Slashing Resist 20%, Crushing, Slashing and "
        "Piercing Damage Thresholds +3, Fire, Cold and Electrical Resist 15%, Attack Speed -3%, "
        "Unarmed Skill -10. Returns 15% of physical damage to the attacker. "
        "Counts as an item of the Knights Templar.")


def write(rel, text):
    assert text.count("\n") == text.count(CR), rel + " is not all-CRLF"
    p = FX / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(resource_format.parse_resource_text(text).to_text().encode("latin-1"))


def derived_mod(attr, value):
    return RN("CCharacterModifierDerivedAttribute", [
        ("Modification Amount", RN("CConstant", [("Constant Value", value)])),
        ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "1"),
        ("Derived character attribute to modify", "Derived Character Attributes/" + attr),
    ])


def skill_mod(skill, value):
    return RN("CCharacterModifierSkill", [
        ("Modification Amount", RN("CConstant", [("Constant Value", value)])),
        ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "1"),
        ("Skill to modify", skill),
    ])


def build_item():
    root = resource_format.parse_resource_text(read(HOLY_REL))
    plugins = root.get("PlugIn Behaviors")
    mod = ovr = None
    for p in plugins.items():
        if p.type_name == "CPlugInBehaviorModifyCharacterWhenSelected":
            mod = p
        elif p.type_name == "CPlugInBehaviorXRPGCharacterCompositeGrannyModelOverride":
            ovr = p
    assert mod is not None and ovr is not None, "Holy Shield shape changed"

    mods = [derived_mod(a, v) for a, v in DERIVED] + [skill_mod(s, v) for s, v in SKILLS]
    arr = mod.get("Modifiers")
    arr.fields = [("Item Count", str(len(mods)))] + [("Modifier", m) for m in mods]

    key = "Character Slot Types/Arm"
    names, models = ovr.get("Override Names"), ovr.get("Override Models")
    names.fields = [(k, AEGIS_MESH if k == key else v) for k, v in names.fields]
    models.fields = [(k, AEGIS_MODEL if k == key else v) for k, v in models.fields]
    extra = [k for k, v in names.fields if k != key and str(v).strip()]
    assert not extra, "stray meshes on %s" % extra

    root.set("Value", RN("CConstant", [("Constant Value", "3000")]))
    root.set("Display Name", "Aegis of the Templars")
    root.set("Description", DESC)
    root.set("Origonal Item", AEGIS)
    imgs = root.get("Inventory Window Images")
    imgs.fields = [(k, AEGIS_ICON) for k, _ in imgs.fields]

    text = root.to_text()
    assert "Constant Value=18" in text and AEGIS_MESH in text
    write(AEGIS_REL, text)
    print("item      Aegis of the Templars.InventoryItem  (%d modifiers, reflect=%s)"
          % (len(mods), REFLECT))



ANCHOR = (CR.join(["Requirement=Templar IS",
                   "Reply Text=Well met, brother knight. Your aid is welcome.",
                   "Go to node ID=10 accept"]) + CR)

NEW_REPLY = (CR.join([
    "Requirement=Templar IS",
    # WORN, not merely carried: he cannot be looking at a shield that is in your pack.
    # There is no equipped test in this engine, so the shield raises a flag while selected
    # and this reads it. See tools/build_holy_shield.py.
    "Custom Requirement=CUseCannedExpressionExpression",
    "{",
    "Canned Expression=Dialog/Requirements/Fixt Wearing Templar Shield",
    "}",
    # The player must have a REASON to show him the shield. The first version had them
    # volunteering it unprompted, which reads as the player knowing about a reward. Here he
    # is noticed looking, and the reply asks him why -- so the scene is his doing, not a
    # menu pick. No quest marker either: that flagged it as a hook to collect rather than a
    # thing that happens in the conversation.
    "Reply Text=<You notice him looking at the shield on your arm.> What is it you see, brother?",
    "Go to node ID=70 the relic",
    "",
]) + CR)

RELIC = (CR.join([
    DASH,
    "Node ID=70 the relic",
    "Text=Forgive me. I have seen that "
    "mark in a chapter roll, and the men who bore it have been dust for two centuries. You carry "
    "a relic, brother, and a relic is a thing we lay on tombs. A knight of your standing should "
    "bear a shield the Order is proud to see raised. Give it here.",
    "Should Have Voiceover=0",
    "",
    "Requirement=!None",
    "Reply Text=Then let it be seen raised.",
    "Go to node ID=10 accept",
    "Custom Action=CMultipleActionsAction",
    "{",
    "Action=Array",
    "{",
    "Item Count=3",
    "Action=CActionRemoveInventoryItem",
    "{",
    "Who to remove from=$instigator",
    "Inventory Item To remove=" + HOLY,
    "}",
    "Action=CActionGiveStandardInventoryItem",
    "{",
    "Who to give to=$instigator",
    "Delete Trigger=0",
    "Notify Player=1",
    "Inventory Item To Give=" + AEGIS,
    "Additions to add=Array",
    "{",
    "Item Count=0",
    "}",
    "}",
    "Action=CPrintCombatTextAction",
    "{",
    "Text to print=Sir Roger has gilded the shield of the order. You carry the Aegis of the Templars.",
    "Character to show text to=$Instigator",
    "}",
    "}",
    "}",
    "Icon=Quest Icon",
    "Is Default Reply=1",
]) + CR)


def wire():
    t = read(TREE)
    if AEGIS in t:
        print("SirRoger    already wired, left alone")
        return
    n = t.count(ANCHOR)
    assert n == 4, "expected 4 Templar greeting replies, found %d" % n
    t = t.replace(ANCHOR, NEW_REPLY + ANCHOR, 4)

    # the relic node goes at the end, before the tree's closing brace
    close = CR + "}" + CR
    assert t.endswith(close), "unexpected tail: %r" % t[-40:]
    t = t[:-len(close)] + CR + RELIC + "}" + CR

    assert t.count("\n") == t.count(CR), "lost CRLF"
    assert t.count("Node ID=70 the relic") == 1
    assert t.count("Inventory Item To Give=" + AEGIS) == 1
    assert t.count("Go to node ID=70 the relic") == 4
    (FX / TREE).parent.mkdir(parents=True, exist_ok=True)
    (FX / TREE).write_bytes(t.encode("latin-1"))
    print("SirRoger    4 greeting branches + node '70 the relic'")


if __name__ == "__main__":
    build_item()
    wire()
