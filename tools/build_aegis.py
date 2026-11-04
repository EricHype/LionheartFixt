"""Build the Aegis of the Templars: tier three, and the end of the Templar shield chain.

The order has three ranks and the game only ever used two of them for anything you can hold.
`Templar Squire`, `Templar Warden` and `Templar Paladin` all exist, all set `Uber Perks/Templar
Rank`, and all three are assigned somewhere -- but the only material thing the ladder ever gave
you was the Lion Shield at the bottom of it. 0.93.0 put the Holy Shield at Warden. This puts the
last shield at Paladin, so each rank is worth reaching.

**The promotion already exists and needed no ceremony invented.** Completing *Search for the Five
Ways Crystals* runs a faction-agnostic block that promotes whichever order you belong to --
Saladin to Exalted, Inquisitor to Hallowed, Templar to Paladin -- and grants elemental
resistances in the same breath. It is duplicated verbatim in two maps so it fires wherever you
finish the set:

    7 English Shrine/09 Secret Chamber
    8 Alamut/02 Shifting Dunes

Both get the same insertion, as a fifth entry in the `Action=Array` that already holds the four
faction conditionals, immediately after the Templar one.

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

MAPS = ("Levels/7 English Shrine/09 Secret Chamber.zax",
        "Levels/8 Alamut/02 Shifting Dunes.zax")

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


def grant_block(indent):
    """The swap, at `indent` tabs. Maps are tab-indented; a resource line whose value is led by
    whitespace crashes the engine on load (0.9.1 shipped one), so every line is built explicitly
    rather than re-indented afterwards."""
    I = T * indent
    L = []
    a = L.append
    a(I + "Action=CIfAction")
    a(I + "{")
    a(I + T + "If=CActionCheckForInventoryItem")
    a(I + T + "{")
    a(I + T * 2 + "Who to give check=$instigator")
    a(I + T * 2 + "Inventory Item To Check For=" + HOLY)
    a(I + T + "}")
    a(I + T + "Then=CMultipleActionsAction")
    a(I + T + "{")
    a(I + T * 2 + "Action=Array")
    a(I + T * 2 + "{")
    a(I + T * 3 + "Item Count=3")
    a(I + T * 3 + "Action=CActionRemoveInventoryItem")
    a(I + T * 3 + "{")
    a(I + T * 4 + "Who to remove from=$instigator")
    a(I + T * 4 + "Inventory Item To remove=" + HOLY)
    a(I + T * 3 + "}")
    a(I + T * 3 + "Action=CActionGiveStandardInventoryItem")
    a(I + T * 3 + "{")
    a(I + T * 4 + "Who to give to=$instigator")
    a(I + T * 4 + "Delete Trigger=0")
    a(I + T * 4 + "Notify Player=1")
    a(I + T * 4 + "Inventory Item To Give=" + AEGIS)
    a(I + T * 4 + "Additions to add=Array")
    a(I + T * 4 + "{")
    a(I + T * 5 + "Item Count=0")
    a(I + T * 4 + "}")
    a(I + T * 3 + "}")
    a(I + T * 3 + "Action=CPrintCombatTextAction")
    a(I + T * 3 + "{")
    a(I + T * 4 + "Text to print=The Ways gild the shield of the order. You carry the Aegis of the Templars.")
    a(I + T * 4 + "Character to show text to=$Instigator")
    a(I + T * 3 + "}")
    a(I + T * 2 + "}")
    a(I + T + "}")
    a(I + T + "Else=")
    a(I + T + "Return failure if the If failes=0")
    a(I + "}")
    return CR.join(L) + CR


def wire(rel):
    t = read(rel)
    if AEGIS in t:
        print("%-26s already wired, left alone" % rel.split("/")[-1])
        return
    ls = t.split(CR)
    pi = [i for i, l in enumerate(ls) if l.strip() == "Faction To Assign=Factions/Templar Paladin"]
    assert len(pi) == 1, "%s: %d Paladin assignments, expected 1" % (rel, len(pi))
    pi = pi[0]
    ci = next(i for i in range(pi, -1, -1) if ls[i].strip() == "Action=CConditionalAction")
    indent = len(ls[ci]) - len(ls[ci].lstrip(T))
    depth, end = 0, None
    for i in range(ci + 1, len(ls)):
        s = ls[i].strip()
        if s == "{":
            depth += 1
        elif s == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    assert end is not None, rel + ": unterminated conditional"

    ai = next(i for i in range(ci, -1, -1)
              if ls[i].strip() == "Action=Array"
              and (len(ls[i]) - len(ls[i].lstrip(T))) == indent - 1)
    ii = next(i for i in range(ai, ai + 4) if ls[i].strip().startswith("Item Count="))
    n = int(ls[ii].strip().split("=")[1])
    ls[ii] = T * (indent) + "Item Count=%d" % (n + 1)

    block = grant_block(indent).rstrip(CR).split(CR)
    out = ls[:end + 1] + block + ls[end + 1:]
    new = CR.join(out)
    assert new.count("\n") == new.count(CR), rel + " lost CRLF"
    assert new.count("Inventory Item To Give=" + AEGIS) == 1
    # no value may be led by whitespace: that is the 0.9.1 map-crash shape
    bad = [l for l in block if re.match(r"^\t*[^\t=]+=[ \t]", l)]
    assert not bad, "whitespace-led value in %r" % bad[:2]
    (FX / rel).parent.mkdir(parents=True, exist_ok=True)
    (FX / rel).write_bytes(new.encode("latin-1"))
    print("%-26s wired at indent %d, Item Count %d -> %d" % (
        rel.split("/")[-1], indent, n, n + 1))


if __name__ == "__main__":
    build_item()
    for m in MAPS:
        wire(m)
