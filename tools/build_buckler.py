"""Build the buckler: a fourth shield that occupies a different design space.

Designed in docs/unused-content.md under "The buckler, designed". The short version: the
three shipped shields are one design -- flat mitigation, AC and crushing/piercing/slashing
resistance climbing together, paid for with escalating Unarmed and casting penalties. A
buckler is a fist shield strapped to the forearm for parrying and punching, so it mitigates
nothing and improves the fight instead.

    Buckler   +1 AC, no resistances, +4 Unarmed, +2 Critical Chance, enc 1, value 6
    Small     +2 AC, 3/3/3,  Unarmed -5,  enc 3, value 10
    Medium    +4 AC, 5/5/5,  Unarmed -10, enc 5, value 20
    Large     +7 AC, 15/10/10, Unarmed -15, enc 10, value 25

+4 Unarmed is the identity and it completes a set with exactly one gap: seventeen things in
the game modify that skill, and an unarmed build has gear for every slot except the off-hand,
because all four shields penalise it. +4 matches `Gauntlets of La Mancha`, itself an unarmed
item. It does real work rather than being cosmetic -- `UnarmedDamageMinimum` and
`UnarmedDamageMaximum` both read `Skills/Fighting/Unarmed`.

+2 Critical Chance rather than +5, because `CriticalChance` adds Luck unconditionally and
gates only its ranged component on a bow, so a melee character's whole crit chance *is* their
Luck, around 5 to 10. +5 would roughly double it and make this compete with Shield Small for
every melee build. At +1 AC and no resistance, no armed build has a reason to take it over a
real shield, so it never competes; an unarmed character currently carries nothing in that
hand.

The art already exists and is a deliberate two-tier set: `Buckler` and `BucklerSpecial`
meshes, both registered in *both* player composites, and `Shield Buckler` and
`Shield Buckler Best` icons. There is no Better tier, which is the Scimitar case from 0.89.0:
the Better-grade additions name the base mesh rather than a missing one.

There is no buckler ground sprite. The item uses the small shield's, and all twelve addition
copies leave `On the ground=!Unknown Model` so none of them overrides it with small-shield
BETTER or SPECIAL art. That is the one visibly unfinished part of the item.

Placement: `All Armor and Shields.can` holds no items of its own, it nests `All Shields` and
`All Armor`, so there is no way to reach the ten merchants that stock it without also hitting
the 69 chest and drop sites that reference `All Shields` directly. So this adds a new can that
nests `All Shields` beside the buckler and repoints `All Armor and Shields` at it: merchants
get bucklers, and no chest in the game has its shield mix diluted.

Usage: python tools/build_buckler.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import CR, T, FX, zf, read
import resource_format

SRC = "Resources/Inventory Items/ShieldSmall.InventoryItem"
DEST = "Resources/Inventory Items/ShieldBuckler.InventoryItem"
AG = "Inventory/Inventory Addition Groups/Shields and Armor/"
SMALL_GROUP = AG + "Shield Additions"
BUCKLER_GROUP = AG + "Shield BUCKLER Additions"
COPY_DIR = "Inventory/Inventory Additions/Shield/BUCKLER/"
MAGIC = "Inventory/Creating Random Magic Items/"
NEW_CAN = MAGIC + "All Shields and Buckler"
ARM = T * 4 + "Character Slot Types/Arm="


def write(rel, text):
    assert text.count("\n") == text.count(CR), rel + " is not all-CRLF"
    p = FX / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(resource_format.parse_resource_text(text).to_text().encode("latin-1"))


def modifier(amount, target, kind="Derived"):
    cls = "CCharacterModifierDerivedAttribute" if kind == "Derived" else "CCharacterModifierSkill"
    field = ("Derived character attribute to modify" if kind == "Derived" else "Skill to modify")
    return (T * 4 + "Modifier=" + cls + CR + T * 4 + "{" + CR +
            T * 5 + "Modification Amount=CConstant" + CR + T * 5 + "{" + CR +
            T * 6 + "Constant Value=" + str(amount) + CR + T * 5 + "}" + CR +
            T * 5 + "Modification amount is a percent=0" + CR +
            T * 5 + "Allow Accumulation=1" + CR +
            T * 5 + field + "=" + target + CR +
            T * 4 + "}" + CR)


# ---------------------------------------------------------------- the item
t = read(SRC)
out = t

# the modifier block: replace the small shield's five with the buckler's three
start = out.index(T * 3 + "Modifiers=Array" + CR)
end = lhbuild.balanced(out, start)
block = (T * 3 + "Modifiers=Array" + CR + T * 3 + "{" + CR +
         T * 4 + "Item Count=3" + CR +
         modifier(1, "Derived Character Attributes/(AC) Armor Class") +
         modifier(2, "Derived Character Attributes/CriticalChance") +
         modifier(4, "Skills/Fighting/Unarmed", kind="Skill") +
         T * 3 + "}" + CR)
out = out[:start] + block + out[end + len(CR):]

swaps = [
    (ARM + "Shield Small" + CR, ARM + "Buckler" + CR),
    (T + "Value=CConstant" + CR + T + "{" + CR + T * 2 + "Constant Value=10" + CR,
     T + "Value=CConstant" + CR + T + "{" + CR + T * 2 + "Constant Value=6" + CR),
    (T + "Encumbrance=3" + CR, T + "Encumbrance=1" + CR),
    (T + "Display Name=Small Shield" + CR, T + "Display Name=Buckler" + CR),
    (T + "Description=+2 AC, Crushing Resist 3%, Piercing Resist 3%, Slashing Resist 3%, "
         "Unarmed Skill -5." + CR,
     T + "Description=+1 AC, Unarmed Skill +4, Critical Chance +2. Strapped to the forearm, "
         "so the hand stays free." + CR),
    (T * 2 + "Basic=Items/Inventory Images/Armor/Shield Small" + CR,
     T * 2 + "Basic=Items/Inventory Images/Armor/Shield Buckler" + CR),
    (T * 2 + "Better=Items/Inventory Images/Armor/Shield Small Better" + CR,
     T * 2 + "Better=Items/Inventory Images/Armor/Shield Buckler" + CR),
    (T * 2 + "Special=Items/Inventory Images/Armor/Shield Small Best" + CR,
     T * 2 + "Special=Items/Inventory Images/Armor/Shield Buckler Best" + CR),
    (T + "Inventory Addition Group=" + SMALL_GROUP + CR,
     T + "Inventory Addition Group=" + BUCKLER_GROUP + CR),
    (T + "Origonal Item=Inventory Items/ShieldSmall" + CR,
     T + "Origonal Item=Inventory Items/ShieldBuckler" + CR),
]
for old, new in swaps:
    assert old in out, "ShieldSmall does not contain: " + repr(old[:60])
    out = out.replace(old, new, 1)

# the ground sprite stays the small shield's: no buckler pickup art exists
assert "On the ground=Items/PickUps/Armor/Shield_Small_PU" in out
assert "Shield Small" not in out and "ShieldSmall" not in out, "a small-shield reference survived"
write(DEST, out)
print("item: ShieldBuckler  (+1 AC, +4 Unarmed, +2 crit, enc 1, value 6)")

# ---------------------------------------------------------------- the pool
group_text = ("CInventoryAdditionGroup" + CR + "{" + CR +
              T + "Other Group that are part of this group=Array" + CR + T + "{" + CR +
              T * 2 + "Item Count=0" + CR + T + "}" + CR + "}" + CR)
write("Resources/" + BUCKLER_GROUP + ".AdditionGroup.txt", group_text)

# snapshot the small shield's pool before writing anything that read() would shadow
pool = {}
for n in sorted(zf.namelist()):
    if not n.lower().endswith(".inventoryaddition"):
        continue
    at = read(n)
    g = re.search(r"Inventory Addition Group=(.*)" + CR, at)
    if not g or g.group(1).strip() != SMALL_GROUP:
        continue
    rel = n[len("Resources/"):-len(".InventoryAddition")]
    pool[rel] = (re.search(r"Item Grade=(.*)" + CR, at).group(1).strip(), at)
assert len(pool) == 12, "the small shield pool has %d additions" % len(pool)

# the copy each original maps to, so exclusions can be repointed inside the copied set
copy_of = {rel: COPY_DIR + rel.split("/")[-1] for rel in pool}
MESH = {"Basic": None, "Better": "Buckler", "Special": "BucklerSpecial"}
counts = {"Basic": 0, "Better": 0, "Special": 0}

for rel, (grade, at) in sorted(pool.items()):
    dest = copy_of[rel]
    c = at
    # a copy must carry its own path: the named-expression references point at their own addition
    c = c.replace("InventoryAddition=" + rel + CR, "InventoryAddition=" + dest + CR)
    assert "InventoryAddition=" + rel + CR not in c
    # exclusions must point at the copied sibling, or they silently stop firing
    for other, other_copy in copy_of.items():
        c = c.replace("Addition Cannot Be Combined With=" + other + CR,
                      "Addition Cannot Be Combined With=" + other_copy + CR)
    c = re.sub(r"Inventory Addition Group=.*" + CR,
               "Inventory Addition Group=" + BUCKLER_GROUP + CR, c)
    # no buckler ground art exists, so never override the item's own sprite
    c = re.sub(r"On the ground=.*" + CR, "On the ground=!Unknown Model" + CR, c)
    mesh = MESH[grade]
    if mesh:
        # `Character Slot Types/Arm=` occurs TWICE: once in Override Models, which the
        # engine ignores, and once in Override Names, which is what renders. Pin the
        # second by splitting on the block header -- taking the first match edits the
        # inert one and leaves the mesh pointing wherever it already pointed.
        head, _, tail = c.partition("Override Names")
        assert tail, rel + " has no Override Names block"
        m = re.search(re.escape(ARM) + r"(.*)" + CR, tail)
        assert m, "%s (%s) has no Arm name to repoint" % (rel, grade)
        tail = tail[:m.start()] + ARM + mesh + CR + tail[m.end():]
        c = head + "Override Names" + tail
        # and the Models line must still be vanilla's, untouched
        before = head.count(ARM)
        assert before == 1, "%s has %d Arm lines before Override Names" % (rel, before)
    else:
        assert "GrannyModelOverride" not in c, rel + " unexpectedly carries an override"
    write("Resources/" + dest + ".InventoryAddition", c)
    counts[grade] += 1

print("pool: Shield BUCKLER Additions  (%d Basic keep the base mesh, %d Better -> Buckler, "
      "%d Special -> BucklerSpecial)" % (counts["Basic"], counts["Better"], counts["Special"]))

# ---------------------------------------------------------------- placement
new_can = ("CCannedObject" + CR + "{" + CR +
           T + "Object=CInventoryItemGeneratorMixedList" + CR + T + "{" + CR +
           T * 2 + "Items=Array" + CR + T * 2 + "{" + CR +
           T * 3 + "Array Count=2" + CR +
           T * 3 + "Array Item=CInventoryItemGeneratorMixedListItem" + CR + T * 3 + "{" + CR +
           T * 4 + "Weighting=30" + CR +
           T * 4 + "Item=CInventoryItemGeneratorCannedList" + CR + T * 4 + "{" + CR +
           T * 5 + "Canned Item List=" + MAGIC + "All Shields" + CR + T * 4 + "}" + CR +
           T * 3 + "}" + CR +
           T * 3 + "Array Item=CInventoryItemGeneratorMixedListItem" + CR + T * 3 + "{" + CR +
           T * 4 + "Weighting=10" + CR +
           T * 4 + "Item=CInventoryItemGeneratorBasic" + CR + T * 4 + "{" + CR +
           T * 5 + "Items=Array" + CR + T * 5 + "{" + CR +
           T * 6 + "Array Count=1" + CR +
           T * 6 + "Array Item=CInventoryItemGeneratorBasicItem" + CR + T * 6 + "{" + CR +
           T * 7 + "Weighting=10" + CR +
           T * 7 + "Item=Inventory Items/ShieldBuckler" + CR + T * 6 + "}" + CR +
           T * 5 + "}" + CR + T * 4 + "}" + CR + T * 3 + "}" + CR +
           T * 2 + "}" + CR + T + "}" + CR +
           T + "Use=Shared Global Instance" + CR + "}" + CR)
write("Resources/" + NEW_CAN + ".can", new_can)

rel = "Resources/" + MAGIC + "All Armor and Shields.can"
t = read(rel)
old_ref = T * 5 + "Canned Item List=" + MAGIC + "All Shields" + CR
new_ref = T * 5 + "Canned Item List=" + NEW_CAN + CR
assert t.count(old_ref) + t.count(new_ref) == 1, "cannot pin the shields reference"
if old_ref in t:
    write(rel, t.replace(old_ref, new_ref, 1))
print("placement: All Armor and Shields -> All Shields and Buckler  "
      "(merchants only; the 69-site All Shields path is untouched)")
