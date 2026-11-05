"""Build the Holy Shield of the Templars: the game's only shield progression.

The Templar thread already spans three acts and pays off in nothing material. You forge the
Lion Shield as an initiate in act 1, you are knighted, you find a dead knight's helm in act 3,
and in act 4 you free two hundred years of damned Templar dead -- a questline with five dialogue
trees, three quest states and, until now, **no item reward anywhere in the Crypt**. Not one
dialogue in that act gives anything.

This puts the reward at the moment the quest completes: the wish that lifts Jehanne's curse
turns the shield you forged into the shield of a knight of the order.

Why a shield specifically, and why this one:

* **The Lion Shield is a fixed quest item with no enchantment slots, and it stays flat while
  acts 5 to 8 do not.** An earlier draft of this note claimed shields never roll enchantments at
  all, reading `Item Count=0` off the group files. That was wrong and the correction matters:
  **a group file lists only the groups it nests, while membership is declared by the addition**,
  which names its group in its own `Inventory Addition Group=`. `Shield LARGE Additions` is
  `Item Count=0` and has twelve members. So ordinary large shields do roll Better and Special
  enchantments -- resistances, a mana well, elemental absorbs -- and this shield, being a quest
  item on `Inventory/!None`, rolls nothing ever.
* **`Shield Holy` is the one unused shield icon**, and the only one with a Christian cross as
  its device. 81x102, a heater shape matching no tier, extra to the 4-families-by-3-tiers
  scheme. It has sat unreferenced since 2003.
* **`Number of Templar Items` is a real set counter that nothing makes worth assembling.**
  `(AC) Armor Class` reads it in its own `Expression` and grants **+4 AC at two pieces**. The
  only two items that raise it are the Helm of the Templars and the Spirit Templar Shield, both
  looted from one corpse, both wearing generic icons. Making the Holy Shield a Templar item
  gives the helm a reason to exist and the set bonus a reason to be worn.

                      Lion      Holy
    AC                  10   ->   14
    Pierce/Slash/Crush  15/10/10 -> 20/15/15
    Thresholds          +1   ->   +2
    Fire/Cold/Elec       -   ->   10 each
    Attack Magic Speed -0.07 -> -0.05
    Templar set item     no  ->   yes
    Value              500   -> 1500

The elemental resists are what make it read as consecrated rather than merely bigger, and they
use attributes the shipped game actually exercises. `Elemental Deflector Percentage` and
`Mana Shield Percentage` both exist and would have been the thematic pick, and **neither is used
by a single item, perk or spell in the game** -- an unproven mechanic is not where a quest
capstone belongs. The lighter speed penalty is the second axis: a knight's shield should handle
better than an initiate's, so the upgrade is not just a larger number.

**The raise-and-read split is safe here.** The shield raises `Number of Templar Items` and the
AC attribute's own Expression reads it. An Expression recomputes from scratch, so there is no
stored addition to reverse -- this is the host docs/engine-notes.md recommends, and it is what
vanilla's own Templar set does. The leak that bit the Thief set needs an *item modifier* reading
a flag it also moves, which is not this shape.

Gating is possession of the Lion Shield, which is equivalent to having run the Templar
initiation: the blacksmith's forge reply is behind `Blacksmith Need LionShield`, and the
non-Templar path through that conversation returns a sword instead. So the item check is the
faction check, without a second gate to keep in sync.

Also fixes the Spirit Templar Shield, which carries **no model override plugin at all** and so
renders nothing on the character -- the same invisibility class 0.89.0 found on magic weapons.
Every other shield and every other helmet in the game has one; it and the Helm of the Templars
are the only two exceptions in either family. It gets the `Shield Lion` mesh, matching the
`LionShield_PU` ground art it already borrows. Its icon is left alone: the Holy art belongs to
the shield you earn in the Crypt, not to a corpse you loot three acts earlier.

Usage: python tools/build_holy_shield.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import CR, FX, read
import resource_format
from resource_format import ResourceNode as RN

LION = "Inventory/Specific Item Cans/Quest Items/Lion Shield Templar Quest"
HOLY = "Inventory/Specific Item Cans/Quest Items/Holy Shield of the Templars"
LION_REL = "Resources/" + LION + ".InventoryItem"
HOLY_REL = "Resources/" + HOLY + ".InventoryItem"
SPIRIT_REL = "Resources/Inventory/Specific Item Cans/Quest Items/Spirit Templar Shield.InventoryItem"
HELM_REL = "Resources/Inventory/Specific Item Cans/Quest Items/Helm of the Templars.InventoryItem"
HELMET_REL = "Resources/Inventory Items/Helmet.InventoryItem"
EFREETI_REL = "Resources/Levels/4 Crypt/Dialog/Efreeti.DialogTree"

# NOT the orphaned `Shield Holy` art. That is a steel heater with no lion -- a different
# shield entirely, and using it put a different object in the inventory from the one on
# the player's back. `Shield Holy Fixt` is the Lion Shield's own icon with the lion faded
# and the cross laid over it, matching the mesh. The steel heater is the AEGIS now, where
# being a different object is the point: Sir Roger takes your shield and hands you a new one.
HOLY_ICON = "Items/Inventory Images/Armor/Shield Holy Fixt"
HOLY_MESH = "Shield Holy"
HOLY_MODEL = "Models3D/Weapons/Shields/Shield Holy/Shield Holy"

DESC = ("This shield was forged for an initiate and consecrated for a knight. "
        "+14 AC, Piercing Resist 20%, Crushing and Slashing Resist 15%, Crushing, Slashing and "
        "Piercing Damage Thresholds +2, Fire, Cold and Electrical Resist 10%, Attack Speed -5%, "
        "Unarmed Skill -10. Counts as an item of the Knights Templar.")

# (attribute path under Derived Character Attributes, value)
DERIVED = [
    ("Damage Related/Piercing Damage Resistance", "20"),
    ("Damage Related/Piercing Damage Threshold", "2"),
    ("Damage Related/Slashing Damage Resistance", "15"),
    ("Damage Related/Slashing Damage Threshold", "2"),
    ("Damage Related/Crushing Damage Resistance", "15"),
    ("Damage Related/Crushing Damage Threshold", "2"),
    ("Damage Related/Fire Damage Resistance", "10"),
    ("Damage Related/Cold Damage Resistance", "10"),
    ("Damage Related/Electrical Damage Resistance", "10"),
    ("(AC) Armor Class", "14"),
    ("Speed/Attack Magic Speed Multiplier", "-0.05"),
    ("Number of Templar Items", "1"),
    # Raised only while the shield is equipped, because CPlugInBehaviorModifyCharacterWhenSelected
    # applies only then -- which is the engine's one way to ask "is this WORN", and Sir Roger's
    # offer needs it: he cannot be looking at a shield that is in your pack. Added here rather
    # than patched onto the generated file, or regenerating the item would silently drop it.
    ("Game Scripting Variables/Fixt Wearing Templar Shield", "1"),
]
SKILLS = [("Skills/Fighting/Unarmed", "-10")]


def write(rel, text):
    assert text.count("\n") == text.count(CR), rel + " is not all-CRLF"
    p = FX / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(resource_format.parse_resource_text(text).to_text().encode("latin-1"))
    return p


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


def slot_block(key_source, arm_value):
    """Rebuild a 14-slot map, replacing only the Arm row."""
    out = []
    for k, v in key_source.fields:
        if k == "Character Slot Types/Arm":
            out.append((k, arm_value))
        else:
            out.append((k, v))
    return out


def build_item():
    root = resource_format.parse_resource_text(read(LION_REL))

    plugins = root.get("PlugIn Behaviors")
    assert plugins is not None, "no PlugIn Behaviors on the Lion Shield"
    mod_plugin = ovr_plugin = None
    for p in plugins.items():
        if p.type_name == "CPlugInBehaviorModifyCharacterWhenSelected":
            mod_plugin = p
        elif p.type_name == "CPlugInBehaviorXRPGCharacterCompositeGrannyModelOverride":
            ovr_plugin = p
    assert mod_plugin is not None and ovr_plugin is not None, "Lion Shield shape changed"

    mods = [derived_mod(a, v) for a, v in DERIVED] + [skill_mod(s, v) for s, v in SKILLS]
    arr = mod_plugin.get("Modifiers")
    arr.fields = [("Item Count", str(len(mods)))] + [("Modifier", m) for m in mods]

    # the Arm row lives in BOTH maps and only Override Names is read; set both so the file
    # does not contradict itself, but pin each by its own block rather than by name
    names = ovr_plugin.get("Override Names")
    models = ovr_plugin.get("Override Models")
    assert names is not None and models is not None
    names.fields = slot_block(names, HOLY_MESH)
    models.fields = slot_block(models, HOLY_MODEL)

    root.set("Value", RN("CConstant", [("Constant Value", "1500")]))
    root.set("Display Name", "Holy Shield of the Templars")
    root.set("Description", DESC)
    root.set("Origonal Item", HOLY)
    imgs = root.get("Inventory Window Images")
    imgs.fields = [(k, HOLY_ICON) for k, _ in imgs.fields]

    text = root.to_text()
    assert "Shield Holy" in text and "Constant Value=14" in text
    p = write(HOLY_REL, text)
    print("item      %s  (%d bytes)" % (HOLY_REL.split("/")[-1], p.stat().st_size))


def set_override(rel, donor_rel, slot, mesh, model_path, label):
    """Both Templar set pieces ship with no model override at all, so neither renders on the
    character. They are the ONLY two exceptions in their families -- every other shield in the
    game carries an Arm mesh and every other helmet a Head mesh.

    **The mesh is chosen to match the icon the item already wears, not its ground art.** The
    first build gave the Spirit Templar Shield `Shield Lion`, reasoning from the LionShield_PU
    ground sprite it borrows, and that was the wrong anchor: it put a gold lion on the
    character while the inventory icon stayed a wooden crusader-cross shield. The icon is what
    the player looks at. So the shield gets `Shield Lrg Better`, which is the mesh its
    `Shield Large Better` icon actually depicts, and the helm gets `Helmet1`, which is its own
    icon. The ground sprite stays mismatched, but that mismatch is vanilla's.

    **Do not trust the shield mesh filenames.** The directory `Shield Lrg Better` holds a
    texture called `ShieldLrg.tga` and the directory `Shield Lrg` holds `ShieldLrgBetter.tga`
    -- the file names are crossed. The *registry* names are right: `Shield Lrg Better` really
    is the crusader-cross shield. Verified by decoding all four large-shield skins and
    comparing them against the three icons, not by reading names.
    """
    root = resource_format.parse_resource_text(read(rel))
    plugins = root.get("PlugIn Behaviors")
    ovr = None
    for p in plugins.items():
        if p.type_name == "CPlugInBehaviorXRPGCharacterCompositeGrannyModelOverride":
            ovr = p
    added = False
    if ovr is None:
        donor = resource_format.parse_resource_text(read(donor_rel))
        for p in donor.get("PlugIn Behaviors").items():
            if p.type_name == "CPlugInBehaviorXRPGCharacterCompositeGrannyModelOverride":
                ovr = p
        assert ovr is not None, donor_rel + " has no override plugin to lend"
        n = len(plugins.items()) + 1
        plugins.fields = ([("Item Count", str(n))]
                          + [(k, v) for k, v in plugins.fields if k != "Item Count"]
                          + [("PlugIn Behavior", ovr)])
        added = True

    # the slot key appears in BOTH maps; pin each by its own block, never by name
    key = "Character Slot Types/" + slot
    names, models = ovr.get("Override Names"), ovr.get("Override Models")
    assert names is not None and models is not None, rel + ": malformed override plugin"
    before = names.get(key)
    names.fields = [(k, mesh if k == key else v) for k, v in names.fields]
    models.fields = [(k, model_path if k == key else v) for k, v in models.fields]
    # every other slot in Override Names must stay blank, or the item wears two meshes
    extra = [k for k, v in names.fields if k != key and str(v).strip()]
    assert not extra, "%s: %s also carry a mesh" % (rel, extra)

    text = root.to_text()
    assert text.count(key + "=" + mesh) == 1, "%s: %s=%s not set once" % (rel, key, mesh)
    write(rel, text)
    print("%-9s %-6s %s=%s%s" % (label, "added" if added else "set", slot, mesh,
                                 "" if before in (None, mesh) else "  (was %r)" % before))


GRANT = CR.join([
    "Action=CIfAction",
    "{",
    "If=CActionCheckForInventoryItem",
    "{",
    "Who to give check=$instigator",
    "Inventory Item To Check For=" + LION,
    "}",
    "Then=CMultipleActionsAction",
    "{",
    "Action=Array",
    "{",
    "Item Count=3",
    "Action=CActionRemoveInventoryItem",
    "{",
    "Who to remove from=$instigator",
    "Inventory Item To remove=" + LION,
    "}",
    "Action=CActionGiveStandardInventoryItem",
    "{",
    "Who to give to=$instigator",
    "Delete Trigger=0",
    "Notify Player=1",
    "Inventory Item To Give=" + HOLY,
    "Additions to add=Array",
    "{",
    "Item Count=0",
    "}",
    "}",
    "Action=CPrintCombatTextAction",
    "{",
    "Text to print=The knights' release passes through the shield you forged. It is theirs now, and yours.",
    "Character to show text to=$Instigator",
    "}",
    "}",
    "}",
    "Else=",
    "Return failure if the If failes=0",
    "}",
    "",
])

ANCHOR = CR.join([
    "Action=CUseCannedActionAction",
    "{",
    "Canned Object=Levels/4 Crypt/Quests/Doomed Knights XP",
    "}",
    "",
])


def wire_efreeti():
    cur = read(EFREETI_REL)
    if HOLY in cur:
        print("efreeti   already wired, left alone")
        return
    assert cur.count(ANCHOR) == 1, "expected exactly one Doomed Knights XP call, got %d" % cur.count(ANCHOR)

    # bump the governing Item Count: the nearest one before the anchor
    i = cur.index(ANCHOR)
    j = cur.rfind("Item Count=", 0, i)
    m = re.match(r"Item Count=(\d+)", cur[j:])
    assert m, "no Item Count before the anchor"
    old, new = m.group(0), "Item Count=%d" % (int(m.group(1)) + 1)
    assert int(m.group(1)) == 5, "action array was %s, expected 5" % m.group(0)
    cur = cur[:j] + new + cur[j + len(old):]

    # insert the grant after the XP call, before the relays
    i = cur.index(ANCHOR) + len(ANCHOR)
    cur = cur[:i] + GRANT + cur[i:]

    assert cur.count("\n") == cur.count(CR), "Efreeti tree lost CRLF"
    (FX / EFREETI_REL).write_bytes(cur.encode("latin-1"))
    print("efreeti   grant wired after the XP award, %s -> %s" % (old, new))


if __name__ == "__main__":
    build_item()
    set_override(SPIRIT_REL, LION_REL, "Arm", "Shield Lrg Better",
                 "Models3D/Weapons/Shields/Shield Lrg Better/Shield Lrg", "spirit")
    set_override(HELM_REL, HELMET_REL, "Head", "Helmet1",
                 "Models3D/Player Characters/Male/Armor/Helmet1", "helm")
    wire_efreeti()
