"""Two helmet additions that do not cost sight: of the Watch, and of Farsight.

The fog of war around the player is pushed back by `Resurrect player.can`'s `CAIPushFogOfWar`, whose radius is
`380 - 25 x Wearing a Helmet + a Perception bonus` (0 up to Perception 4, then 10 a point to 12, then 80). Creatures in the
fog fade out, so this radius is how far the player can see. The game has one helmet item, and it sets `Wearing a Helmet`
to 1 ("+3 AC, slightly reduces sight distance"), so every helmet costs 25 units of sight. The flag has no minimum, so an
addition can push it below zero and give sight back:

- **of the Watch** (Uncommon) takes it back to 0: a helmet that costs no sight.
- **of Farsight** (Rare) takes it to -2: 50 units more sight than going bare-headed, 75 more than a plain helmet.

They join the helmet's own addition group, so they roll on random magic helmets like the vanilla additions. Both are built
from `the Eagle`'s shape, fixed value and all, with the Watch on the plainer Helmet2 look that the Uncommon additions use.

A rerun is a no-op.

    python tools/build_sight_helmets.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced
from build_shrine_repairs import register

DIR = "Resources/Inventory/Inventory Additions/Miscellaneous/Helmets/"
TEMPLATE = DIR + "Eagle.InventoryAddition"
FLAG = "Derived Character Attributes/Wearing a Helmet"
HELMETS = {
    "Watch": dict(name="the Watch", amount="-1", value="600", rarity="Inventory Item Rarity/2 Uncommon", look="Helmet2",
                  icon="Items/Inventory Images/Armor/Helmet2 Mod",
                  text="A helmet that does not reduce the wearer's sight, as other helmets do."),
    "Farsight": dict(name="Farsight", amount="-3", value="2400", rarity="Inventory Item Rarity/3 Rare", look="Helmet3",
                     icon="Items/Inventory Images/Armor/Helmet3",
                     text="Instead of reducing the wearer's sight, as other helmets do, it lets them see farther than with no helmet at all."),
}


def set_field(t, key, value):
    t, n = re.subn(r"(?m)^(\t" + re.escape(key) + r"=)[^\r\n]*", lambda m: m.group(1) + value, t, count=1)
    assert n == 1, key
    return t


def build(file, h):
    rel = DIR + file + ".InventoryAddition"
    if (FX / rel).exists():
        return 0
    t = lhbuild.read(TEMPLATE)
    # the Eagle's three skill modifiers become one, on the helmet flag, in the base helmet's own form
    k = t.index("Modifiers=Array")
    mod = ("CCharacterModifierDerivedAttribute", [("Modification Amount", ("CConstant", [("Constant Value", h["amount"])])),
                                                  ("Modification amount is a percent", "0"), ("Allow Accumulation", "1"),
                                                  ("Derived character attribute to modify", FLAG)])
    t = t[:k] + "Modifiers=" + B("Array", [("Item Count", "1"), ("Modifier", mod)]).rstrip() + t[balanced(t, k):]
    t = t.replace("Character Slot Types/Head=Helmet3", "Character Slot Types/Head=" + h["look"])
    t = set_field(t, "On the ground", "Items/PickUps/Misc Items/" + h["look"] + "_PU")
    t = set_field(t, "Inventory Window", h["icon"])
    t = set_field(t, "Display Name", h["name"])
    t = set_field(t, "Description", h["text"])
    t = set_field(t, "Addition Rarity", h["rarity"])
    for key in ("Minimum Value", "Inbetween Value", "Maximum Value"):
        t = set_field(t, key, h["value"])
    t = re.sub(r"(Value=CConstant\r\n\t\{\r\n\t\tConstant Value=)\d+", lambda m: m.group(1) + h["value"], t, count=1)
    assert "Skills/" not in t and FLAG in t
    lhbuild.write_map(rel, t)
    register([rel])
    return 1


def main():
    print("helmet additions written:", sum(build(f, h) for f, h in HELMETS.items()))


if __name__ == "__main__":
    main()
