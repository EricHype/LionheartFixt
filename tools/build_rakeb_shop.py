"""Rakeb's shop opens again, and sells what a shaman's favour is worth. Reported from play after 0.99.28: "When rakeb opens
his shop for us, we can't get him to open it again... Also the shop's contents were really bad."

**It never reopened.** The Barter turn-in of the woodcutter's eyes (`135 other reward`) activates the map's `store open`
checker and opens the shop. The reply that reopens it, *"I would like to buy some items."*, gated on that checker, is in
`3 Return Dialogue`. But once the eyes quest is complete the Goblin Warrens greeting opens `136 Vision` on every visit,
ahead of everything else, and 136 offers only goodbye. 136 now carries the same reply. A tree, so every save.

**The stock was a placeholder.** `Inventory for Shaman` (Goblin Warrens, with a twin in the unused `ShamanInterior`) held
one plain Battle Axe and four rolls of `ALL WEAPONS Mojo Standard`, all with a blank `Level`: five mundane weapons, the
thinnest shop in the game bar Raylark's, sold as *"the greatest of boons"*. 136's own design note says the shaman *"might
now sell magical items or potions"*. Every comparable shop rolls `Creating Random Magic Items` at
`Shopkeeper Generation 1 to Mojo` and `Very High Mojo`. Now he does, and leans to magic: potions, scrolls, misc items
(rings, amulets, wands), and fewer weapons and armour. Lists and level cans are all vanilla's.

The merchant lives in the map, so the new stock goes on from the tree, as vanilla's `Swap Special Merchant AI` does for
Weng Choi: the first open removes the `CMerchantAI`, adds the new one after half a second, and opens the window after one.
`Fixt Rakeb Stock` on the player keeps that to once, so the stock restocks on the vanilla 900-second timer and cannot be
rerolled by reopening. This reaches every save, including one that already bought from him.

A rerun is a no-op.

    python tools/build_rakeb_shop.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register
from build_troll_choices import act, modifier, node_span, reply, reply_start, VARS

RAKEB = "Resources/Levels/Wilderness/Dialog/Rakeb.dialogtree"
SHOP = "Inventory for Shaman"
STOCK = "Fixt Rakeb Stock"
STOCK_DCA = "Resources/" + VARS + STOCK + ".DerivedCharacterAttribute"
BUY = "I would like to buy some items."
OPEN = B("CDisplayMerchantWindowAction", [("Merchant", SHOP), ("After Closed Action", "")])
RANDOM = "Inventory/Creating Random Magic Items/"
LOW = "Common Objects and Scripts/Generate Magic Item Level Cans/Shopkeeper Generation 1 to Mojo"
HIGH = "Common Objects and Scripts/Generate Magic Item Level Cans/Shopkeeper Generation Very High Mojo"
# (quantity, list, level can)
ITEMS = [
    (6, RANDOM + "All Potions", LOW),
    (2, RANDOM + "Implementation Folder DO NOT PICK FROM/All Scrolls", LOW),
    (1, RANDOM + "Implementation Folder DO NOT PICK FROM/All Scrolls", HIGH),
    (4, RANDOM + "Implementation Folder DO NOT PICK FROM/All Misc Items except Potions", LOW),
    (2, RANDOM + "Implementation Folder DO NOT PICK FROM/All Misc Items except Potions", HIGH),
    (3, RANDOM + "All Weapons", LOW),
    (1, RANDOM + "All Weapons", HIGH),
    (2, RANDOM + "All Armor and Shields", LOW),
    (1, RANDOM + "All Armor and Shields", HIGH),
]


def merchant_ai():
    rows = ""
    for q, lst, lvl in ITEMS:
        assert ("Resources/" + lst + ".can") in lhbuild.zf.namelist(), lst
        assert ("Resources/" + lvl + ".can") in lhbuild.zf.namelist(), lvl
        rows += "Array Item=" + B("CMerchantListItem", [
            ("Quantity", str(q)),
            ("Item", ("CInventoryItemGeneratorCannedList", [("Canned Item List", lst)])),
            ("Level", ("CUseCannedExpressionExpression", [("Canned Expression", lvl)]))])
    items = "Array" + CR + "{" + CR + "Array Count=" + str(len(ITEMS)) + CR + rows + "}" + CR
    return ("CMerchantAI" + CR + "{" + CR + "Marked For Deletion=0" + CR + "Publisher=" + CR + "Display Name=Goblin Shaman" + CR +
            "Price Multiplier=1" + CR + "Time Between Restock=900" + CR + "Time Of Last Restocking=0" + CR +
            "Items=" + items + "}" + CR)


def shop():
    """Open the shop; the first time, swap in the new stock first."""
    stocked = ("CIsGreaterThan", [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", VARS + STOCK)])),
                                  ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "0")]))])
    add = ("CAddAIAction" + CR + "{" + CR + "Target Name=" + SHOP + CR + "AI=" + merchant_ai() + "Delay Between Adds=0" + CR + "}" + CR)
    first = lhbuild.multi([
        ("CRemoveAIAction", [("Target Name", SHOP), ("AI", "CMerchantAI"), ("Delay Between Removes", "0")]),
        modifier("Player1", "Game Scripting Variables/" + STOCK, "1", "0"),
        ("CDelayAction", [("Next Action", "RAW_ADD"), ("Delay", "0.5"), ("Plus or Minus", "0"), ("Forget Trigger", "0")]),
        ("CDelayAction", [("Next Action", "RAW_OPEN"), ("Delay", "1"), ("Plus or Minus", "0"), ("Forget Trigger", "0")]),
    ])
    out = B("CIfExpressionAction", [("If Expression", stocked), ("Character to get attributes from", "Player1"),
                                     ("Then", "RAW_OPEN"), ("Else", first)])
    out = out.replace("Next Action=RAW_ADD" + CR, "Next Action=" + add, 1)
    out = out.replace("Next Action=RAW_OPEN" + CR, "Next Action=" + OPEN, 1)
    out = out.replace("Then=RAW_OPEN" + CR, "Then=" + OPEN, 1)
    assert "RAW_" not in out
    return out


def build_dca():
    if (lhbuild.FX / STOCK_DCA).exists():
        return 0
    t = lhbuild.read("Resources/" + VARS + "Fixt Fernand Stride.DerivedCharacterAttribute")
    t = t.replace("Fixt Fernand Stride", STOCK)
    t = re.sub(r"Description=[^\r\n]*", "Description=1 once Rakeb's shop has been given its stock (tools/build_rakeb_shop.py).", t)
    (lhbuild.FX / STOCK_DCA).write_bytes(t.encode("latin-1"))
    register([STOCK_DCA])
    return 1


def build_tree():
    t = lhbuild.read(RAKEB)
    if STOCK in t:
        return 0
    assert t.count(OPEN) == 2, t.count(OPEN)
    t = t.replace(OPEN, shop())
    # node 3's reopen reply, copied into 136
    k = reply_start(t, "3 Return Dialogue", BUY)
    e = t.index("Go to node ID=" + CR, k)
    gate = t[k:t.index("Reply Text=" + BUY + CR, k)]
    assert gate.startswith("Requirement=!None" + CR + "Custom Requirement=CActionExpression") and "store open" in gate
    i, j = node_span(t, "136 Vision")
    blk = t[i:j]
    assert BUY not in blk and blk.count("Reply Text=") == 1
    r = reply_start(t, "136 Vision", "Thank you, and good day, goblin.")
    t = t[:r] + gate + "Reply Text=" + BUY + CR + "Go to node ID=" + CR + "Custom Action=" + shop() + CR + t[r:]
    (lhbuild.FX / RAKEB).write_bytes(t.encode("latin-1"))
    register([RAKEB])
    return 1


def main():
    print("dca:", build_dca(), "| tree:", build_tree())


if __name__ == "__main__":
    main()
