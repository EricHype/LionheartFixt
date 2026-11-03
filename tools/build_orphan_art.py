"""Give five items the art that was made for them and never wired up.

`docs/unused-content.md` surveys this under "Orphaned art". Each of these is one field: an
item exists, uses generic or borrowed art, and art named for it sits in the game referenced
by nothing. The asset's own name is the evidence it belongs.

  * **Nightshade Root** is ours, not vanilla's -- Fixt authored it for the hangover-cure
    chain and gave it Darkwood's icon, so the two herbs are indistinguishable in the
    inventory while `Quest Items/Rare Herb` sits unused. Only the icon changes: both herbs
    correctly share `RareHerb_PU` on the ground, which is generic herb art Darkwood uses too.
  * **The four Wielder quest rods** drop as the generic `Wand_PU` while `RodOfBone` and
    `RodOfSpirits` go unused. Their *icons* are already distinct, so this is ground art only,
    and `Scepter of the INQ Chambers` already uses a per-rod sprite from the same folder --
    the convention is established and these four are the ones that miss it.
  * **Amulet of Dour Tidings** wears `AmuletGreenOpal`, shared with eight other amulets,
    while art named for the item sits unused.
  * **Gauntlets of La Mancha** wears the generic gauntlet icon. This one is an **inference,
    not a match**: nothing names `Gauntlets Spike` for it. The case is that it is the only
    unused gauntlet icon and La Mancha the only unique gauntlet without its own, plus a
    dating argument -- the Gauntlets of Hellfire's icon sits in the late `Images for RED
    file/` folder while Spike sits in ordinary `Armor/` beside the wired
    `Bracers Stealthy Cunning`.

Every edit is guarded both ways: the target art must exist in the build, and the field must
currently hold either the value being replaced or the value being written, so a rerun is a
no-op and a later hand edit is never clobbered.

Usage: python tools/build_orphan_art.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import CR, FX, zf, read
import resource_format

Q = "Inventory/Specific Item Cans/Quest Items/"
U = "Inventory/Specific Item Cans/Unique Magic Items/"

# (item, field, art it should use, art it currently uses)
ICON = [
    (Q + "Nightshade Root", "Items/Inventory Images/Quest Items/Rare Herb",
     "Items/Inventory Images/Quest Items/Darkwood"),
    (Q + "Special Objects for RED file/Amulet of Dour Tidings",
     "Items/Inventory Images/Misc Items/Images for RED file/Amulet Dour Tidings",
     "Items/Inventory Images/Misc Items/AmuletGreenOpal"),
    (U + "Gauntlets of La Mancha", "Items/Inventory Images/Armor/Gauntlets Spike",
     "Items/Inventory Images/Armor/Gauntlets"),
]
GROUND = [
    (Q + "Wielder DARK Quest Rod Bone NO Spirit", "Items/PickUps/Misc Items/Wands/RodOfBone"),
    (Q + "Wielder DARK Quest Rod Bone WITH Spirit", "Items/PickUps/Misc Items/Wands/RodOfBone"),
    (Q + "Wielder Quest Rod Spirits NO Spirit", "Items/PickUps/Misc Items/Wands/RodOfSpirits"),
    (Q + "Wielder Quest Rod Spirits WITH Spirit", "Items/PickUps/Misc Items/Wands/RodOfSpirits"),
]
GENERIC_GROUND = "Items/PickUps/Misc Items/Wand_PU"


def art_exists(ref):
    """Art is a Cache model, built from the Resources tree. Accept either source."""
    cache = "Cache/Models/" + ref + ".mdl16"
    return cache in zf.namelist() or (FX / cache).exists()


def write(rel, text):
    assert text.count("\n") == text.count(CR), rel + " is not all-CRLF"
    p = FX / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(resource_format.parse_resource_text(text).to_text().encode("latin-1"))


n_icon = n_ground = 0
for item, new, old in ICON:
    assert art_exists(new), "the art does not exist: " + new
    rel = "Resources/" + item + ".InventoryItem"
    t = read(rel)
    # the three grade tiers all point at one icon on these items; keep that shape
    tiers = re.findall(r"\t(Basic|Better|Special)=(.*)" + CR, t)
    assert len(tiers) == 3, "%s has %d icon tiers" % (item, len(tiers))
    have = {v.strip() for _, v in tiers}
    assert have in ({old}, {new}), "%s points at %s, expected %s or %s" % (item, have, old, new)
    if have == {new}:
        print("   ok    %-44s already %s" % (item.split("/")[-1], new.split("/")[-1]))
        continue
    out = t
    for grade, _ in tiers:
        out = out.replace("	%s=%s%s" % (grade, old, CR),
                          "	%s=%s%s" % (grade, new, CR), 1)
    # Re-parse rather than asserting `old not in out`: one of these old values is a
    # prefix of its replacement (Armor/Gauntlets inside Armor/Gauntlets Spike), so a
    # containment check can never pass. Compare the parsed tier values instead.
    after = {v.strip() for _, v in re.findall(r"	(Basic|Better|Special)=(.*)" + CR, out)}
    assert after == {new}, "%s came out as %s" % (item, after)
    write(rel, out)
    n_icon += 1
    print("   icon  %-44s %s -> %s" % (item.split("/")[-1], old.split("/")[-1], new.split("/")[-1]))

for item, new in GROUND:
    assert art_exists(new), "the art does not exist: " + new
    rel = "Resources/" + item + ".InventoryItem"
    t = read(rel)
    cur = re.search(r"On the ground=(.*)" + CR, t)
    assert cur, item + " has no On the ground field"
    have = cur.group(1).strip()
    assert have in (GENERIC_GROUND, new), "%s drops as %s, expected %s or %s" % (
        item, have, GENERIC_GROUND, new)
    if have == new:
        print("   ok    %-44s already %s" % (item.split("/")[-1], new.split("/")[-1]))
        continue
    out = t.replace("On the ground=" + GENERIC_GROUND + CR, "On the ground=" + new + CR, 1)
    assert out != t and out.count("On the ground=") == 1
    write(rel, out)
    n_ground += 1
    print("   ground %-43s %s -> %s" % (item.split("/")[-1], "Wand_PU", new.split("/")[-1]))

print()
print("%d icon(s), %d ground sprite(s) wired" % (n_icon, n_ground))
